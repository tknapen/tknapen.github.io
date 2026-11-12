#!/usr/bin/env python3
"""List publications by Tomas Knapen that are not yet on the website.

Queries PubMed (NCBI E-utilities) and Crossref, compares what they return with
the files in _publications/ (by DOI, PMID and title), and prints:

  * new candidates: papers and preprints that have no file yet;
  * updates: site entries of type "preprint" whose DOI is now a journal article
    (for example an eLife Reviewed Preprint that became a Version of Record),
    and preprints on the site that now have a PMID;
  * possible duplicates: candidates whose title closely resembles a site entry.

It never edits files. Google Scholar has no API and does not allow automated
access, so it is not queried; PubMed and Crossref (which also registers bioRxiv,
OSF and eLife preprints) cover the same papers.

Known false positives (another T Knapen, corrections, preprint versions of papers
already listed) go in tools/pubwatch-ignore.txt, one DOI or PMID per line.

Standard library only. Usage:
  python3 tools/pubwatch.py                 # Crossref records from the last 2 years
  python3 tools/pubwatch.py --since 2025-01-01
  python3 tools/pubwatch.py --json          # machine-readable output
Exit status: 0 on success (with or without candidates), 2 if every source failed.
"""

import argparse
import datetime as dt
import difflib
import html
import json
import re
import sys
import time
import unicodedata
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

ORCID = "0000-0001-5863-8689"
PUBMED_TERM = "Knapen T[au]"
FAMILY = "knapen"
GIVEN_PREFIX = "t"  # Tomas

ROOT = Path(__file__).resolve().parent.parent
PUB_DIR = ROOT / "_publications"
IGNORE_FILE = Path(__file__).resolve().parent / "pubwatch-ignore.txt"

EUTILS = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
CROSSREF = "https://api.crossref.org/works"
USER_AGENT = "pubwatch/1.0 (python-urllib)"

# Crossref types that are not publications in their own right.
SKIP_TYPES = {"peer-review", "component", "journal-issue", "journal-volume", "dataset", "grant"}
# Vision Sciences Society meeting abstracts are published in Journal of Vision with
# article numbers in the hundreds or thousands (e.g. 10.1167/jov.24.10.574).
CONFERENCE_DOI = re.compile(r"^10\.1167/jov\.\d+\.\d+\.\d{3,}$")
SKIP_TITLE = re.compile(r"^\s*(correction|erratum|corrigendum|retraction|author response|reply to|decision letter)\b", re.I)


# --------------------------------------------------------------------- helpers

def get_json(url, params=None, tries=4):
    if params:
        url = url + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept": "application/json"})
    last = None
    for attempt in range(tries):
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                body = r.read()
            if not body.strip():
                raise ValueError("empty response")
            return json.loads(body)
        except urllib.error.HTTPError as e:
            last = e
            if e.code == 404:
                return None
            if e.code not in (429, 500, 502, 503, 504):
                raise
        except (urllib.error.URLError, TimeoutError, ValueError) as e:
            last = e
        time.sleep(2 ** attempt + 1)
    raise RuntimeError(f"{url}: {last}")


def norm_doi(doi):
    if not doi:
        return ""
    doi = doi.strip().strip('"').strip("'").lower()
    doi = re.sub(r"^(https?://)?(dx\.)?doi\.org/", "", doi)
    doi = re.sub(r"^doi:\s*", "", doi)
    # eLife version DOIs (10.7554/elife.110134.2) and review DOIs (.sa1) -> concept DOI
    m = re.match(r"^(10\.7554/elife\.\d+)(\.\d+)?(\.sa\d+)?$", doi)
    if m:
        return m.group(1)
    return doi


def is_review_doi(doi):
    return bool(re.search(r"\.sa\d+$", (doi or "").lower()))


def norm_title(t):
    t = html.unescape(re.sub(r"<[^>]+>", "", t or ""))
    t = unicodedata.normalize("NFKD", t)
    t = "".join(c for c in t if not unicodedata.combining(c)).lower()
    return " ".join(re.sub(r"[^a-z0-9]+", " ", t).split())


def clean_text(t):
    return " ".join(html.unescape(re.sub(r"<[^>]+>", " ", t or "")).split())


def initials(given):
    parts = re.split(r"[\s\-.]+", given or "")
    return "".join(p[0].upper() for p in parts if p)


def pubmed_style(author):
    family = author.get("family") or author.get("name") or ""
    ini = initials(author.get("given", ""))
    return f"{family} {ini}".strip()


def crossref_date(item):
    for key in ("published-print", "published-online", "issued", "posted", "created"):
        parts = (item.get(key) or {}).get("date-parts") or [[]]
        if parts and parts[0] and parts[0][0]:
            p = list(parts[0]) + [1, 1]
            return f"{p[0]:04d}-{p[1]:02d}-{p[2]:02d}"
    return ""


def is_tomas(author):
    fam = norm_title(author.get("family", ""))
    giv = norm_title(author.get("given", ""))
    orcid = (author.get("ORCID") or "").rstrip("/").split("/")[-1]
    return orcid == ORCID or (fam == FAMILY and giv.startswith(GIVEN_PREFIX))


# ------------------------------------------------------------------- site data

def front_matter(text):
    m = re.match(r"^---\s*\n(.*?)\n---", text, re.S)
    return m.group(1) if m else ""


def field(fm, key):
    m = re.search(rf"^{key}:\s*(.*?)\s*$", fm, re.M)
    if not m:
        return ""
    return m.group(1).strip().strip('"').strip("'")


def load_site():
    entries = []
    for f in sorted(PUB_DIR.glob("*.markdown")) + sorted(PUB_DIR.glob("*.md")):
        fm = front_matter(f.read_text(encoding="utf-8"))
        dois = {norm_doi(field(fm, "doi"))}
        for m in re.finditer(r"^\s+preprint:\s*(\S+)", fm, re.M):
            if "10." in m.group(1):
                dois.add(norm_doi(m.group(1)))
        entries.append({
            "file": str(f.relative_to(ROOT)),
            "title": field(fm, "title"),
            "ntitle": norm_title(field(fm, "title")),
            "doi": norm_doi(field(fm, "doi")),
            "dois": {d for d in dois if d},
            "pmid": field(fm, "pmid"),
            "type": field(fm, "type") or "article",
            "journal": field(fm, "journal"),
        })
    return entries


def site_author_forms(site_files):
    """Map (normalized last word of family name, first initial) -> author strings used on the site."""
    forms = {}
    for f in site_files:
        fm = front_matter(f.read_text(encoding="utf-8"))
        m = re.search(r"^authors:\s*\[(.*)\]\s*$", fm, re.M)
        if not m:
            continue
        for a in m.group(1).split(","):
            a = a.strip().strip('"')
            parts = a.rsplit(" ", 1)
            if len(parts) != 2 or not parts[1].isupper():
                continue
            key = (norm_title(parts[0]).split(" ")[-1], parts[1][0])
            forms.setdefault(key, set()).add(a)
    return forms


def suggest_forms(authors, forms):
    """For authors written differently on the site, return 'Crossref form -> site form' hints."""
    hints = []
    for a in authors:
        parts = a.rsplit(" ", 1)
        if len(parts) != 2 or not parts[1]:
            continue
        fam = norm_title(parts[0]).split(" ")
        keys = [(fam[-1], parts[1][0])]
        if len(fam) == 1 and len(parts[1]) > 1:  # "Abdirashid SS" may be "Sheikh Abdirashid S" on the site
            keys.append((fam[0], parts[1][-1]))
        for key in keys:
            known = forms.get(key, set())
            if known and a not in known:
                hints.append(f"{a} -> {' / '.join(sorted(known))}")
                break
    return hints


def load_ignore():
    ids = set()
    if IGNORE_FILE.exists():
        for line in IGNORE_FILE.read_text(encoding="utf-8").splitlines():
            line = line.split("#", 1)[0].strip()
            if line:
                ids.add(line if line.isdigit() else norm_doi(line))
    return ids


# --------------------------------------------------------------------- sources

def pubmed_records(log):
    found = get_json(EUTILS + "esearch.fcgi", {"db": "pubmed", "term": PUBMED_TERM, "retmode": "json", "retmax": 2000})
    ids = found["esearchresult"]["idlist"]
    log.append(f"PubMed: {len(ids)} records for {PUBMED_TERM}")
    return ids


def pubmed_summaries(pmids):
    out = {}
    for i in range(0, len(pmids), 100):
        chunk = pmids[i:i + 100]
        res = get_json(EUTILS + "esummary.fcgi", {"db": "pubmed", "id": ",".join(chunk), "retmode": "json"})["result"]
        for uid in res.get("uids", []):
            r = res[uid]
            doi = next((a["value"] for a in r.get("articleids", []) if a.get("idtype") == "doi"), "")
            out[uid] = {
                "source": "pubmed",
                "title": clean_text(r.get("title", "")).rstrip("."),
                "authors": [a.get("name", "") for a in r.get("authors", []) if a.get("authtype", "Author") == "Author"],
                "venue": r.get("fulljournalname") or r.get("source", ""),
                "date": r.get("sortpubdate", "")[:10].replace("/", "-"),
                "doi": doi,
                "pmid": uid,
                "kind": "journal-article",
                "pubtypes": r.get("pubtype", []),
            }
        time.sleep(0.4)
    return out


def crossref_items(since, log):
    select = "DOI,title,type,issued,posted,created,published-print,published-online,container-title,publisher,relation,author,abstract"
    queries = [
        ("crossref-orcid", {"filter": f"orcid:{ORCID},from-created-date:{since}", "rows": 200, "select": select}),
        ("crossref-author", {"query.author": "Tomas Knapen", "filter": f"from-created-date:{since}", "rows": 200, "select": select}),
    ]
    items, ok = {}, 0
    for name, params in queries:
        try:
            msg = get_json(CROSSREF, params)["message"]
        except Exception as e:  # keep going with the other sources
            log.append(f"Crossref ({name}) failed: {e}")
            continue
        ok += 1
        kept, last = 0, -1
        for idx, it in enumerate(msg.get("items", [])):
            if not any(is_tomas(a) for a in it.get("author", [])):
                continue
            kept, last = kept + 1, idx
            key = norm_doi(it["DOI"])
            entry = items.setdefault(key, {"item": it, "found_by": set()})
            entry["found_by"].add(name)
            # prefer the concept record (shortest DOI) for eLife versions
            if len(it["DOI"]) < len(entry["item"]["DOI"]):
                entry["item"] = it
        log.append(f"Crossref ({name}): {msg.get('total-results', 0)} hits, {kept} with T. Knapen as author")
        if last >= 0.75 * params["rows"]:
            log.append(f"Warning: Crossref ({name}) matches reach result {last + 1} of {params['rows']}; some may be cut off, so raise rows")
        time.sleep(1)
    return items, ok


def crossref_work(doi):
    res = get_json(f"{CROSSREF}/{urllib.parse.quote(doi)}")
    return res["message"] if res else None


# ------------------------------------------------------------------- comparing

def match_site(site, doi="", pmid="", title="", related=()):
    ndoi = norm_doi(doi)
    rel = {norm_doi(r) for r in related}
    for e in site:
        if ndoi and ndoi in e["dois"]:
            return e, "doi"
        if pmid and pmid == e["pmid"]:
            return e, "pmid"
        if rel & e["dois"]:
            return e, "related doi"
    nt = norm_title(title)
    for e in site:
        if nt and nt == e["ntitle"]:
            return e, "title"
    return None, ""


def similar_site(site, title, cutoff=0.82):
    nt = norm_title(title)
    best, score = None, 0.0
    for e in site:
        s = difflib.SequenceMatcher(None, nt, e["ntitle"]).ratio()
        if s > score:
            best, score = e, s
    return (best, round(score, 2)) if score >= cutoff else (None, 0.0)


def relations(item):
    rel = []
    for k, v in (item.get("relation") or {}).items():
        if k in ("is-version-of", "has-version", "is-preprint-of", "has-preprint", "is-same-as", "is-identical-to"):
            rel += [x.get("id", "") for x in v if x.get("id-type") == "doi"]
    return rel


def run(since):
    log, failures = [], 0
    site = load_site()
    ignore = load_ignore()
    log.append(f"Site: {len(site)} publication files")

    candidates = {}  # keyed by normalized doi or pmid

    def add(c, found_by):
        key = norm_doi(c.get("doi")) or f"pmid:{c.get('pmid')}"
        if key in candidates:
            candidates[key]["found_by"] |= set(found_by)
            for k in ("pmid", "abstract"):
                if c.get(k) and not candidates[key].get(k):
                    candidates[key][k] = c[k]
            return
        c["found_by"] = set(found_by)
        candidates[key] = c

    # PubMed
    try:
        pmids = pubmed_records(log)
        site_pmids = {e["pmid"] for e in site if e["pmid"]}
        unknown = [p for p in pmids if p not in site_pmids and p not in ignore]
        for pmid, r in pubmed_summaries(unknown).items():
            if norm_doi(r["doi"]) in ignore or SKIP_TITLE.match(r["title"]):
                continue
            if any(t in ("Published Erratum", "Retraction of Publication", "Comment") for t in r["pubtypes"]):
                continue
            e, how = match_site(site, r["doi"], pmid, r["title"])
            if e:
                if not e["pmid"]:
                    r["update"] = f"{e['file']}: add pmid \"{pmid}\" (matched by {how})"
                    add(r, ["pubmed"])
                continue
            add(r, ["pubmed"])
    except Exception as ex:
        failures += 1
        log.append(f"PubMed failed: {ex}")

    # Crossref
    skipped_abstracts = []
    cr, ok = crossref_items(since, log)
    if not ok:
        failures += 1
    for key, entry in cr.items():
        it = entry["item"]
        doi = it["DOI"]
        title = clean_text((it.get("title") or [""])[0])
        if it.get("type") in SKIP_TYPES or is_review_doi(doi) or SKIP_TITLE.match(title):
            continue
        if key in ignore:
            continue
        if CONFERENCE_DOI.match(key):
            skipped_abstracts.append(key)
            continue
        e, how = match_site(site, doi, "", title, relations(it))
        if e:
            continue
        kind = it.get("type", "")
        if kind == "posted-content":
            kind = "reviewed-preprint" if norm_doi(doi).startswith("10.7554/elife.") else "preprint"
        add({
            "source": "crossref",
            "title": title,
            "authors": [pubmed_style(a) for a in it.get("author", [])],
            "venue": clean_text((it.get("container-title") or [""])[0]) or it.get("publisher", ""),
            "date": crossref_date(it),
            "doi": norm_doi(doi) if norm_doi(doi).startswith("10.7554/elife.") else doi.lower(),
            "pmid": "",
            "kind": kind,
            "related": relations(it),
            "abstract": clean_text(it.get("abstract", "")),
        }, entry["found_by"])

    if skipped_abstracts:
        log.append(f"Skipped {len(skipped_abstracts)} conference abstracts (Journal of Vision / VSS): " + ", ".join(sorted(skipped_abstracts)))

    # Preprints on the site that may have been published since
    for e in site:
        if e["type"] != "preprint" or not e["doi"]:
            continue
        try:
            w = crossref_work(e["doi"])
        except Exception as ex:
            log.append(f"Crossref lookup of {e['doi']} failed: {ex}")
            continue
        time.sleep(1)
        if not w:
            continue
        if w.get("type") == "journal-article":
            add({"source": "crossref", "title": clean_text((w.get("title") or [""])[0]), "authors": [], "venue": clean_text((w.get("container-title") or [""])[0]),
                 "date": crossref_date(w), "doi": e["doi"], "pmid": "", "kind": "journal-article",
                 "update": f"{e['file']}: {e['doi']} is now a journal article ({clean_text((w.get('container-title') or [''])[0])}); set type: article, update journal, citation and date"},
                ["crossref-site-preprint"])
        for r in (w.get("relation") or {}).get("is-preprint-of", []):
            if r.get("id-type") == "doi":
                add({"source": "crossref", "title": e["title"], "authors": [], "venue": "", "date": "", "doi": r["id"].lower(), "pmid": "", "kind": "journal-article",
                     "update": f"{e['file']}: preprint published as {r['id']}; update this file rather than adding a new one"},
                    ["crossref-site-preprint"])

    forms = site_author_forms(sorted(PUB_DIR.glob("*.markdown")) + sorted(PUB_DIR.glob("*.md")))
    out = {"new": [], "updates": [], "possible_duplicates": []}
    for c in candidates.values():
        c["found_by"] = sorted(c["found_by"])
        c["name_hints"] = suggest_forms(c.get("authors", []), forms)
        if c.get("update"):
            out["updates"].append(c)
            continue
        sim, score = similar_site(site, c["title"])
        if sim:
            c["similar_to"] = {"file": sim["file"], "title": sim["title"], "type": sim["type"], "score": score}
            out["possible_duplicates"].append(c)
        else:
            out["new"].append(c)
    for k in out:
        out[k].sort(key=lambda c: c.get("date", ""), reverse=True)
    out["log"] = log
    out["failed"] = failures >= 2
    return out


def print_report(res, since):
    today = dt.date.today().isoformat()
    print(f"Publication check {today} (Crossref records created since {since}; all PubMed records for {PUBMED_TERM})")
    for line in res["log"]:
        print("  " + line)

    def show(c, i):
        print(f"\n{i}. {c['title']}")
        if c.get("authors"):
            print("   " + ", ".join(c["authors"]))
        print(f"   {c.get('venue', '')} | {c.get('kind', '')} | {c.get('date', '')}")
        ids = [f"DOI {c['doi']}" if c.get("doi") else "", f"PMID {c['pmid']}" if c.get("pmid") else ""]
        print("   " + "  ".join(x for x in ids if x) + f"  (found by {', '.join(c['found_by'])})")
        if c.get("name_hints"):
            print("   names as written elsewhere on the site: " + "; ".join(c["name_hints"]))
        if c.get("related"):
            print("   related DOIs: " + ", ".join(c["related"]))
        if c.get("similar_to"):
            s = c["similar_to"]
            print(f"   similar to {s['file']} ({s['type']}, similarity {s['score']}): {s['title']}")
        if c.get("update"):
            print("   update: " + c["update"])

    for key, heading in (("new", "New candidates"), ("updates", "Updates to existing entries"), ("possible_duplicates", "Possible versions of existing entries (check by hand)")):
        print(f"\n{heading}: {len(res[key])}")
        for i, c in enumerate(res[key], 1):
            show(c, i)
    if res["failed"]:
        print("\nBoth PubMed and Crossref failed; nothing was checked.")


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--since", help="only Crossref records created on or after this date (YYYY-MM-DD); default two years ago")
    ap.add_argument("--json", action="store_true", help="print JSON instead of a text report")
    args = ap.parse_args()
    since = args.since or (dt.date.today() - dt.timedelta(days=730)).isoformat()
    res = run(since)
    if args.json:
        print(json.dumps(res, indent=2, ensure_ascii=False))
    else:
        print_report(res, since)
    sys.exit(2 if res["failed"] else 0)


if __name__ == "__main__":
    main()
