#!/usr/bin/env python3
"""List publications by Tomas Knapen that are not yet on the website.

Queries PubMed (NCBI E-utilities) and Crossref, compares what they return with
the files in _publications/ (by DOI, PMID, related DOIs and title), and prints:

  * new candidates: papers and preprints that have no file yet, with the
    abstract and the evidence that the Knapen author is Tomas Knapen;
  * updates to existing files: a site preprint that has been published (as a
    journal article or an eLife Reviewed Preprint), an eLife Reviewed Preprint
    that became a Version of Record, or a PMID that a file lacks;
  * possible versions of existing entries: candidates whose title closely
    resembles a site entry, to be checked by hand.

It never edits files. Google Scholar has no API and does not allow automated
access, so it is not queried; PubMed and Crossref (which also registers bioRxiv,
OSF and eLife preprints) cover the same papers.

Records that should not be reported again (another T Knapen, a preprint of a
paper already listed under a different title) go in tools/pubwatch-ignore.txt,
one DOI or PMID per line followed by "# reason". Corrections, peer-review
records and conference abstracts (Journal of Vision/VSS, ISMRM, CCN) are skipped
automatically and listed in the log.

Standard library only. Usage:
  python3 tools/pubwatch.py                 # Crossref records from the last 2 years
  python3 tools/pubwatch.py --since 2025-01-01
  python3 tools/pubwatch.py --json          # machine-readable output
Exit status: 0 when the check ran (with or without findings), 1 when it ran only
partly (a source failed; see the log), 2 when every source failed.
"""

import argparse
import datetime as dt
import difflib
import html
import http.client
import json
import re
import sys
import time
import unicodedata
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

ORCID = "0000-0001-5863-8689"
PUBMED_TERM = "Knapen T[au]"
FAMILY = "knapen"
GIVEN_PREFIX = "t"  # Tomas
# Words in his affiliations, used only as evidence of authorship in the report.
AFFILIATION_HINTS = ("vrije universiteit", "vu amsterdam", "vu university", "spinoza", "netherlands institute for neuroscience", "knaw", "amsterdam")

ROOT = Path(__file__).resolve().parent.parent
PUB_DIR = ROOT / "_publications"
IGNORE_FILE = Path(__file__).resolve().parent / "pubwatch-ignore.txt"

EUTILS = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
CROSSREF = "https://api.crossref.org/works"
USER_AGENT = "pubwatch/1.1 (python-urllib)"
CROSSREF_SELECT = ("DOI,title,type,issued,posted,created,published-print,published-online,container-title,"
                   "publisher,relation,author,abstract,update-to,page,volume,issue,article-number")

# Crossref types that are not publications in their own right.
SKIP_TYPES = {"peer-review", "component", "journal-issue", "journal-volume", "dataset", "grant", "report-component"}
# Meeting abstracts: Vision Sciences Society abstracts in Journal of Vision (article numbers
# in the hundreds or thousands, or with a letter suffix, e.g. 10.1167/jov.24.10.574,
# 10.1167/16.12.1306, 10.1167/19.10.64b), ISMRM (10.58530) and CCN (10.32470) abstracts.
CONFERENCE_DOI = re.compile(r"^(10\.1167/(jov\.)?\d+\.\d+\.(\d{3,}|\d+[a-z])|10\.58530/.*|10\.32470/.*)$")
CORRECTION_TITLE = re.compile(r"^\s*((author|publisher)('s)?\s+)?(correction|erratum|corrigendum|retraction(\s+note)?|expression of concern)\b\s*(to|of|for)?\s*[:\-–]", re.I)
REVIEW_TITLE = re.compile(r"^\s*(author response|decision letter|reviewer #?\d|editor's evaluation|elife assessment)\b", re.I)
CORRECTION_UPDATES = {"correction", "erratum", "corrigendum", "retraction", "removal", "withdrawal", "expression_of_concern", "expression-of-concern"}
VERSION_RELATIONS = ("is-version-of", "has-version", "is-same-as", "is-identical-to")
PREPRINT_RELATIONS = ("is-preprint-of", "has-preprint")


# --------------------------------------------------------------------- helpers

def http_get(url, params=None, tries=4, accept="application/json"):
    if params:
        url = url + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept": accept})
    last = None
    for attempt in range(tries):
        wait = 2 ** attempt + 1
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                body = r.read()
            if not body.strip():
                raise ValueError("empty response")
            return body
        except urllib.error.HTTPError as e:
            last = e
            if e.code == 404:
                return None
            if e.code not in (429, 500, 502, 503, 504):
                raise RuntimeError(f"{url}: {e}") from e
            retry_after = e.headers.get("Retry-After", "") if e.headers else ""
            if retry_after.isdigit():
                wait = min(int(retry_after), 120)
        except (OSError, http.client.HTTPException, ValueError) as e:  # URLError, resets, timeouts, short reads
            last = e
        if attempt < tries - 1:
            time.sleep(wait)
    raise RuntimeError(f"{url}: {last}")


def get_json(url, params=None):
    body = http_get(url, params)
    return json.loads(body) if body is not None else None


def norm_doi(doi):
    """Lowercase, strip URL prefixes, and collapse version DOIs to one key per work."""
    if not doi:
        return ""
    doi = doi.strip().strip('"').strip("'").lower()
    doi = re.sub(r"^(https?://)?(dx\.)?doi\.org/", "", doi)
    doi = re.sub(r"^doi:\s*", "", doi)
    m = re.match(r"^(10\.7554/elife\.\d+)(\.\d+)?(\.sa\d+)?$", doi)  # eLife versions and reviews
    if m:
        return m.group(1)
    doi = re.sub(r"^(10\.31\d{3}/osf\.io/[a-z0-9]+)_v\d+$", r"\1", doi)  # OSF and PsyArXiv versions
    doi = re.sub(r"^(10\.21203/rs\.3\.rs-\d+)/v\d+$", r"\1", doi)     # Research Square versions
    return doi


def display_doi(doi):
    """The DOI as the site writes it (DOIs are case-insensitive; eLife keeps its capital L)."""
    n = norm_doi(doi)
    m = re.match(r"^10\.7554/elife\.(\d+)$", n)
    if m:
        return f"10.7554/eLife.{m.group(1)}"
    return re.sub(r"^(https?://)?(dx\.)?doi\.org/", "", (doi or "").strip(), flags=re.I)


def is_review_doi(doi):
    return bool(re.search(r"\.sa\d+$", (doi or "").lower()))


def norm_title(t):
    t = html.unescape(re.sub(r"<[^>]+>", "", t or ""))
    t = unicodedata.normalize("NFKD", t)
    t = "".join(c for c in t if not unicodedata.combining(c)).lower()
    return " ".join(re.sub(r"[^a-z0-9]+", " ", t).split())


def clean_text(t):
    return " ".join(html.unescape(re.sub(r"<[^>]+>", " ", t or "")).split())


def jats_abstract(jats):
    """Crossref JATS abstract -> plain text, one paragraph per <jats:p>, headings dropped."""
    if not jats:
        return ""
    jats = re.sub(r"<jats:title>.*?</jats:title>", "", jats, flags=re.S)
    paras = re.findall(r"<jats:p[^>]*>(.*?)</jats:p>", jats, flags=re.S) or [jats]
    return "\n\n".join(p for p in (clean_text(x) for x in paras) if p)


def no_email(text):
    return " ".join(re.sub(r"\S+@\S+", "", text or "").split()).strip(" .;,")


def initials(given):
    parts = re.split(r"[\s\-.]+", given or "")
    return "".join(p[0].upper() for p in parts if p)


def pubmed_style(author):
    family = author.get("family") or author.get("name") or ""
    ini = initials(author.get("given", ""))
    return f"{family} {ini}".strip()


def date_parts(item, key):
    parts = (item.get(key) or {}).get("date-parts") or [[]]
    if parts and parts[0] and parts[0][0]:
        p = [int(x) for x in parts[0]] + [1, 1]
        return f"{p[0]:04d}-{p[1]:02d}-{p[2]:02d}"
    return ""


def crossref_date(item):
    """First public appearance: posted date for preprints, online date before print date otherwise."""
    order = ("posted", "published-online", "published-print", "issued", "created") if item.get("type") == "posted-content" \
        else ("published-online", "published-print", "issued", "posted", "created")
    for key in order:
        d = date_parts(item, key)
        if d:
            return d
    return ""


def is_tomas(author):
    fam = norm_title(author.get("family", ""))
    giv = norm_title(author.get("given", ""))
    orcid = (author.get("ORCID") or "").rstrip("/").split("/")[-1]
    return orcid == ORCID or (fam == FAMILY and giv.startswith(GIVEN_PREFIX))


def venue_name(doi, container, publisher):
    n = norm_doi(doi)
    for prefix, name in (("10.1101/", "bioRxiv"), ("10.7554/elife.", "eLife"), ("10.31219/osf.io", "OSF Preprints"),
                         ("10.31234/osf.io", "PsyArXiv"), ("10.48550/arxiv", "arXiv"), ("10.21203/rs.", "Research Square")):
        if n.startswith(prefix) and not container:
            return name
    return container or publisher or ""


def crossref_kind(item):
    t = item.get("type", "")
    if t == "posted-content":
        return "reviewed-preprint" if norm_doi(item.get("DOI")).startswith("10.7554/elife.") else "preprint"
    return t


def related_dois(item, kinds=VERSION_RELATIONS + PREPRINT_RELATIONS):
    out = []
    for k, v in (item.get("relation") or {}).items():
        if k in kinds:
            out += [x.get("id", "") for x in v if x.get("id-type") == "doi" and x.get("id")]
    return out


# ------------------------------------------------------------------- site data

def front_matter(text):
    m = re.match(r"^---\s*\n(.*?)\n---", text, re.S)
    return m.group(1) if m else ""


def field(fm, key):
    m = re.search(rf"^{key}:\s*(.*?)\s*$", fm, re.M)
    if not m:
        return ""
    return m.group(1).strip().strip('"').strip("'")


def site_files():
    return sorted(PUB_DIR.glob("*.markdown")) + sorted(PUB_DIR.glob("*.md"))


def load_site():
    entries = []
    for f in site_files():
        fm = front_matter(f.read_text(encoding="utf-8"))
        doi = norm_doi(field(fm, "doi"))
        dois = {doi}
        for m in re.finditer(r"^\s+preprint:\s*(\S+)", fm, re.M):
            if "10." in m.group(1):
                dois.add(norm_doi(m.group(1)))
        entries.append({
            "file": str(f.relative_to(ROOT)),
            "title": field(fm, "title"),
            "ntitle": norm_title(field(fm, "title")),
            "doi": doi,
            "dois": {d for d in dois if d},
            "pmid": field(fm, "pmid"),
            "type": field(fm, "type") or "article",
            "journal": field(fm, "journal"),
        })
    return entries


def site_author_forms():
    """Map (normalized last word of family name, first initial) -> author strings used on the site."""
    forms = {}
    for f in site_files():
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
    """For authors written differently on the site, return 'source form -> site form' hints."""
    hints = []
    for a in authors:
        parts = a.rsplit(" ", 1)
        if len(parts) != 2 or not parts[1]:
            continue
        fam = norm_title(parts[0]).split(" ")
        if not fam or not fam[-1]:
            continue
        keys = [(fam[-1], parts[1][0])]
        if len(fam) == 1 and len(parts[1]) > 1:  # "Abdirashid SS" is "Sheikh Abdirashid S" on the site
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


# --------------------------------------------------------------------- PubMed

def pubmed_search(term, retmax=2000):
    res = get_json(EUTILS + "esearch.fcgi", {"db": "pubmed", "term": term, "retmode": "json", "retmax": retmax})
    return res["esearchresult"]["idlist"] if res else []


def pubmed_fetch(pmids):
    """efetch XML -> records with title, authors, journal, date, DOI, abstract, publication types, Knapen affiliation."""
    out = {}
    for i in range(0, len(pmids), 100):
        chunk = pmids[i:i + 100]
        body = http_get(EUTILS + "efetch.fcgi", {"db": "pubmed", "id": ",".join(chunk), "retmode": "xml"}, accept="application/xml")
        time.sleep(0.4)
        if not body:
            continue
        root = ET.fromstring(body)
        for art in root.iter("PubmedArticle"):
            pmid = art.findtext(".//MedlineCitation/PMID", "")
            a = art.find(".//Article")
            if a is None:
                continue
            title = "".join(a.find("ArticleTitle").itertext()) if a.find("ArticleTitle") is not None else ""
            authors, affil = [], []
            for au in a.findall(".//AuthorList/Author"):
                last, ini = au.findtext("LastName", ""), au.findtext("Initials", "")
                if last:
                    authors.append(f"{last} {ini}".strip())
                    if norm_title(last) == FAMILY and ini.upper().startswith("T"):
                        affil += [no_email(clean_text("".join(x.itertext()))) for x in au.findall(".//AffiliationInfo/Affiliation")]
                elif au.findtext("CollectiveName"):
                    authors.append(au.findtext("CollectiveName"))
            paras = []
            for t in a.findall(".//Abstract/AbstractText"):
                text = clean_text("".join(t.itertext()))
                label = t.get("Label")
                paras.append(f"{label}: {text}" if label and label.upper() != "UNLABELLED" else text)
            doi = ""
            for aid in art.findall(".//PubmedData/ArticleIdList/ArticleId"):
                if aid.get("IdType") == "doi":
                    doi = (aid.text or "").strip()
            if not doi:
                for eid in a.findall("ELocationID"):
                    if eid.get("EIdType") == "doi":
                        doi = (eid.text or "").strip()
            date = ""
            ad = a.find("ArticleDate")
            if ad is not None and ad.findtext("Year"):
                date = f"{ad.findtext('Year')}-{int(ad.findtext('Month', '1')):02d}-{int(ad.findtext('Day', '1')):02d}"
            else:
                pd = a.find(".//Journal/JournalIssue/PubDate")
                if pd is not None and pd.findtext("Year"):
                    months = {m: i for i, m in enumerate(["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"], 1)}
                    mo = pd.findtext("Month", "1")
                    mo = months.get(mo[:3].lower(), int(mo) if mo.isdigit() else 1)
                    date = f"{pd.findtext('Year')}-{mo:02d}-{int(pd.findtext('Day', '1')):02d}"
            ji = a.find(".//Journal/JournalIssue")
            vol = ji.findtext("Volume", "") if ji is not None else ""
            iss = ji.findtext("Issue", "") if ji is not None else ""
            pages = a.findtext(".//Pagination/MedlinePgn", "")
            out[pmid] = {
                "source": "pubmed",
                "title": clean_text(title).rstrip("."),
                "authors": authors,
                "venue": a.findtext(".//Journal/Title", ""),
                "date": date,
                "doi": doi,
                "pmid": pmid,
                "kind": "preprint" if any((pt.text or "") == "Preprint" for pt in a.findall(".//PublicationTypeList/PublicationType")) else "journal-article",
                "pubtypes": [pt.text or "" for pt in a.findall(".//PublicationTypeList/PublicationType")],
                "citation_hint": f"{vol}({iss}), {pages}".replace("(), ", ", ").strip(", ") if vol else pages,
                "abstract": "\n\n".join(p for p in paras if p),
                "authorship": [f"PubMed affiliation: {x}" for x in affil if x] or ["PubMed gives no affiliation for the Knapen author"],
                "related": [],
            }
    return out


# --------------------------------------------------------------------- Crossref

def crossref_query(params, log, name, cap=5000):
    """All items of a Crossref works query, read with a cursor."""
    items, cursor, total = [], "*", None
    while True:
        p = dict(params, rows=1000, cursor=cursor, select=CROSSREF_SELECT)
        msg = get_json(CROSSREF, p)["message"]
        total = msg.get("total-results", 0)
        batch = msg.get("items", [])
        items += batch
        cursor = msg.get("next-cursor")
        time.sleep(1)
        if not batch or not cursor or len(items) >= total or len(items) >= cap:
            break
    if len(items) < total:
        log.append(f"Warning: Crossref ({name}) read {len(items)} of {total} results; the rest were not checked")
    return items, total


def crossref_work(doi):
    res = get_json(f"{CROSSREF}/{urllib.parse.quote(doi)}")
    return res["message"] if res else None


def crossref_record(it, found_by):
    authors = it.get("author", [])
    evidence = []
    if any((a.get("ORCID") or "").rstrip("/").endswith(ORCID) for a in authors):
        evidence.append(f"Crossref lists ORCID {ORCID} for the Knapen author")
    for a in authors:
        if is_tomas(a):
            names = [no_email(x.get("name", "")) for x in a.get("affiliation", []) if no_email(x.get("name", ""))]
            evidence += [f"Crossref affiliation: {n}" for n in names]
    if not evidence:
        evidence.append("Crossref gives no ORCID or affiliation for the Knapen author")
    vol, iss = it.get("volume", ""), it.get("issue", "")
    num = it.get("page") or it.get("article-number", "")
    cit = (f"{vol}({iss}), {num}" if iss else f"{vol}, {num}") if vol else num
    return {
        "source": "crossref",
        "title": clean_text((it.get("title") or [""])[0]),
        "authors": [pubmed_style(a) for a in authors],
        "venue": venue_name(it.get("DOI"), clean_text((it.get("container-title") or [""])[0]), it.get("publisher", "")),
        "date": crossref_date(it),
        "doi": display_doi(it["DOI"]),
        "pmid": "",
        "kind": crossref_kind(it),
        "related": related_dois(it),
        "citation_hint": (cit or "").strip(", "),
        "abstract": jats_abstract(it.get("abstract", "")),
        "authorship": evidence,
        "found_by": set(found_by),
    }


def crossref_items(since, log):
    """Crossref works with T. Knapen as author created since `since`, keyed by normalized DOI."""
    queries = [
        ("crossref-orcid", {"filter": f"orcid:{ORCID},from-created-date:{since}"}),
        # Family name only: "Tomas Knapen" ranks by relevance over thousands of other Tomases and
        # buries papers with long author lists; "Knapen" returns a few hundred records in total.
        ("crossref-author", {"query.author": "Knapen", "filter": f"from-created-date:{since}"}),
    ]
    items, ok = {}, 0
    for name, params in queries:
        try:
            raw, total = crossref_query(params, log, name)
        except Exception as e:  # keep going with the other sources
            log.append(f"Crossref ({name}) failed: {e}")
            continue
        ok += 1
        kept = 0
        for it in raw:
            if not any(is_tomas(a) for a in it.get("author", [])):
                continue
            kept += 1
            key = norm_doi(it["DOI"])
            entry = items.setdefault(key, {"item": it, "found_by": set()})
            entry["found_by"].add(name)
            if len(it["DOI"]) < len(entry["item"]["DOI"]):  # prefer the eLife concept record over versions
                entry["item"] = it
        log.append(f"Crossref ({name}): {total} records, {kept} with T. Knapen as author")
    return items, ok, len(queries)


# ------------------------------------------------------------------- comparing

def match_site(site, doi="", pmid="", title="", related=()):
    ndoi = norm_doi(doi)
    rel = {norm_doi(r) for r in related if r}
    for e in site:
        if ndoi and ndoi in e["dois"]:
            return e, "doi"
        if pmid and pmid == e["pmid"]:
            return e, "pmid"
    for e in site:
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


def upd(entry, action, text):
    return {"file": entry["file"], "action": action, "text": text}


def supersedes(rec, entry):
    """True if rec is a later, more final version of the site preprint `entry`."""
    if entry["type"] != "preprint" or norm_doi(rec.get("doi")) == entry["doi"]:
        return False
    if rec.get("kind") in ("journal-article", "book-chapter", "proceedings-article"):
        return True
    return rec.get("kind") == "reviewed-preprint" and not entry["doi"].startswith("10.7554/elife.")


def run(since):
    log, failed_sources, total_sources = [], [], 0
    site = load_site()
    ignore = load_ignore()
    log.append(f"Site: {len(site)} publication files; ignore list: {len(ignore)} identifiers")
    skipped = {"conference abstracts": [], "corrections": [], "peer-review records": [], "ignored": []}

    candidates = {}

    def add(c):
        key = norm_doi(c.get("doi")) or f"pmid:{c.get('pmid')}"
        c.setdefault("found_by", set())
        c.setdefault("updates", [])
        if key not in candidates:
            candidates[key] = c
            return
        old = candidates[key]
        old["found_by"] |= set(c["found_by"])
        seen = {(u["file"], u["action"]) for u in old["updates"]}
        for u in c["updates"]:
            if (u["file"], u["action"]) not in seen:
                old["updates"].append(u)
        for k in ("pmid", "abstract", "citation_hint", "related"):
            if c.get(k) and not old.get(k):
                old[k] = c[k]
        if c.get("source") == "pubmed":  # PubMed author lists, dates and DOI casing are closer to the site's format
            for k in ("authors", "date", "doi"):
                if c.get(k):
                    old[k] = c[k]
        old["authorship"] = list(dict.fromkeys(old.get("authorship", []) + c.get("authorship", [])))

    def consider(rec):
        """Classify one record from any source against the site."""
        e, how = match_site(site, rec.get("doi"), rec.get("pmid"), rec.get("title"), rec.get("related", ()))
        if not e:
            add(rec)
            return
        if supersedes(rec, e):
            rec["updates"] = [upd(e, "published", f"preprint {e['doi']} has been published as {rec['doi'] or 'PMID ' + rec['pmid']} "
                                  f"in {rec.get('venue') or '?'} (matched by {how}); update this file rather than adding a new one")]
            add(rec)
        elif rec.get("pmid") and not e["pmid"] and how in ("doi", "related doi") and rec.get("kind") != "preprint":
            rec["updates"] = [upd(e, "pmid", f"add pmid \"{rec['pmid']}\"")]
            add(rec)

    # PubMed
    total_sources += 1
    try:
        pmids = pubmed_search(PUBMED_TERM)
        log.append(f"PubMed: {len(pmids)} records for {PUBMED_TERM}")
        site_pmids = {e["pmid"] for e in site if e["pmid"]}
        unknown = [p for p in pmids if p not in site_pmids and p not in ignore]
        for pmid, r in pubmed_fetch(unknown).items():
            if norm_doi(r["doi"]) in ignore:
                skipped["ignored"].append(pmid)
                continue
            if CORRECTION_TITLE.match(r["title"]) or any(t in ("Published Erratum", "Retraction of Publication", "Retraction Notice", "Expression of Concern") for t in r["pubtypes"]):
                skipped["corrections"].append(f"PMID {pmid}")
                continue
            r["found_by"] = {"pubmed"}
            consider(r)
    except Exception as ex:
        failed_sources.append("PubMed")
        log.append(f"PubMed failed: {ex}")

    # Crossref
    cr, ok, n = crossref_items(since, log)
    total_sources += n
    failed_sources += ["Crossref"] * (n - ok)
    for key, entry in cr.items():
        it = entry["item"]
        title = clean_text((it.get("title") or [""])[0])
        updates_to = {(u.get("type") or "").lower() for u in it.get("update-to", []) or []}
        if it.get("type") in SKIP_TYPES or is_review_doi(it["DOI"]) or REVIEW_TITLE.match(title):
            skipped["peer-review records"].append(key)
            continue
        if CONFERENCE_DOI.match(key):
            skipped["conference abstracts"].append(key)
            continue
        if updates_to & CORRECTION_UPDATES or CORRECTION_TITLE.match(title):
            skipped["corrections"].append(key)
            continue
        version_rel = {norm_doi(d) for d in related_dois(it, VERSION_RELATIONS)}
        if key in ignore or (it.get("type") == "posted-content" and version_rel & ignore):
            skipped["ignored"].append(key)
            continue
        consider(crossref_record(it, entry["found_by"]))

    # Preprints on the site: look for a published version directly, whatever its creation date.
    for e in site:
        if e["type"] != "preprint" or not e["doi"]:
            continue
        try:
            w = crossref_work(e["doi"])
            time.sleep(1)
            if w and w.get("type") == "journal-article":  # an eLife Reviewed Preprint became a Version of Record
                rec = crossref_record(w, ["crossref-site-preprint"])
                rec["updates"] = [upd(e, "version-of-record", f"{e['doi']} is now a journal article (Version of Record) in {rec['venue']}; "
                                      f"set type: article, date, citation (volume) and pmid, and check the title, authors and abstract")]
                add(rec)
            linked = set(related_dois(w, VERSION_RELATIONS + PREPRINT_RELATIONS)) if w else set()
            back, _ = crossref_query({"filter": f"relation.object:{e['doi']}"}, log, f"relations of {e['doi']}")
            for b in back:
                if norm_doi(b["DOI"]) != e["doi"]:
                    linked.add(b["DOI"])
            for d in linked:
                nd = norm_doi(d)
                if nd == e["doi"] or nd in ignore or is_review_doi(d):
                    continue
                other, _ = match_site(site, d)
                w2 = crossref_work(d)
                time.sleep(1)
                if not w2:
                    continue
                rec = crossref_record(w2, ["crossref-site-preprint"])
                if not supersedes(rec, e):
                    continue
                if other and other["file"] != e["file"]:
                    rec["updates"] = [upd(e, "merge", f"this preprint and {other['file']} look like two versions of one paper; consider merging them")]
                elif not other:
                    rec["updates"] = [upd(e, "published", f"preprint {e['doi']} has been published as {rec['doi']} in {rec['venue']}; update this file rather than adding a new one")]
                else:
                    continue
                add(rec)
            # PubMed may index the journal version under the same title before Crossref links them.
            if not e["pmid"]:
                for pmid in pubmed_search(f"\"{e['title']}\"[ti]", retmax=5):
                    if pmid in ignore:
                        continue
                    for r in pubmed_fetch([pmid]).values():
                        if r["kind"] != "preprint" and norm_title(r["title"]) == e["ntitle"]:
                            r["found_by"] = {"pubmed-site-preprint"}
                            consider(r)
        except Exception as ex:
            log.append(f"Check of site preprint {e['doi']} failed: {ex}")
            failed_sources.append(f"preprint check {e['file']}")

    for k, v in skipped.items():
        if v:
            log.append(f"Skipped {len(v)} {k}: " + ", ".join(sorted(set(v))))

    forms = site_author_forms()
    out = {"new": [], "updates": [], "possible_duplicates": []}
    for c in candidates.values():
        c["found_by"] = sorted(c["found_by"])
        c["name_hints"] = suggest_forms(c.get("authors", []), forms)
        if c.get("updates"):
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
    out["failed_sources"] = sorted(set(failed_sources))
    out["status"] = "failed" if failed_sources.count("PubMed") + failed_sources.count("Crossref") >= total_sources else ("partial" if failed_sources else "ok")
    return out


def print_report(res, since):
    today = dt.date.today().isoformat()
    print(f"Publication check {today}: Crossref records created since {since}, and all PubMed records for {PUBMED_TERM}")
    print(f"Status: {res['status']}" + (f" (failed: {', '.join(res['failed_sources'])})" if res["failed_sources"] else ""))
    for line in res["log"]:
        print("  " + line)

    def show(c, i):
        print(f"\n{i}. {c['title']}")
        if c.get("authors"):
            print("   " + ", ".join(c["authors"]))
        print(f"   {c.get('venue', '')} | {c.get('kind', '')} | {c.get('date', '')}" + (f" | {c['citation_hint']}" if c.get("citation_hint") else ""))
        ids = [f"DOI {c['doi']}" if c.get("doi") else "", f"PMID {c['pmid']}" if c.get("pmid") else ""]
        print("   " + "  ".join(x for x in ids if x) + f"  (found by {', '.join(c['found_by'])})")
        for u in c.get("updates", []):
            print(f"   update {u['file']}: {u['text']}")
        if c.get("similar_to"):
            s = c["similar_to"]
            print(f"   similar to {s['file']} ({s['type']}, similarity {s['score']}): {s['title']}")
        if c.get("name_hints"):
            print("   names as written elsewhere on the site: " + "; ".join(c["name_hints"]))
        for a in c.get("authorship", []):
            print("   authorship: " + a)
        if c.get("related"):
            print("   related DOIs: " + ", ".join(c["related"]))
        print("   abstract: " + ("available in --json output" if c.get("abstract") else "none in PubMed or Crossref"))

    for key, heading in (("new", "New candidates"), ("updates", "Updates to existing files"), ("possible_duplicates", "Possible versions of existing entries (check by hand)")):
        print(f"\n{heading}: {len(res[key])}")
        for i, c in enumerate(res[key], 1):
            show(c, i)


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--since", help="only Crossref records created on or after this date (YYYY-MM-DD); default two years ago")
    ap.add_argument("--json", action="store_true", help="print JSON (with abstracts) instead of a text report")
    args = ap.parse_args()
    since = args.since or (dt.date.today() - dt.timedelta(days=730)).isoformat()
    res = run(since)
    if args.json:
        print(json.dumps(res, indent=2, ensure_ascii=False))
    else:
        print_report(res, since)
    sys.exit({"ok": 0, "partial": 1, "failed": 2}[res["status"]])


if __name__ == "__main__":
    main()
