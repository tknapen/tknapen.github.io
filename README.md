# Knapen Lab website

Source of https://tknapen.github.io. GitHub Pages builds the site from the `master` branch with Jekyll; anything merged into `master` is live within a few minutes.

Most changes are one file: add a markdown file to the right folder and open a pull request. The sections below give a template for each kind of content.

## Preview locally

```bash
bundle install
```

```bash
bundle exec jekyll serve
```

Then open http://localhost:4000. The `Gemfile` pins the same gem versions GitHub Pages uses, so what builds here builds there.

## Where things live

| What | Where | URL |
|---|---|---|
| Home page | `index.html` | `/` |
| Research themes | `_research/<slug>.md` | `/research/<slug>/` |
| Publications | `_publications/YYYY-MM-DD-<abbr>.markdown` | `/publications/<file>/` |
| People | `_people/<name>.markdown` | `/people/<file>/` |
| Software and datasets | `_data/software.yml` | `/software/` |
| News | `_posts/YYYY-MM-DD-<name>.markdown` | `/YYYY/MM/DD/<name>.html` |
| Lab handbook pages | `_resources/` | `/resources/<file>/` |
| Lab-wide facts (affiliations, links, funders, dataset info) | `_data/lab.yml` | used on many pages |
| Menu | `_data/navigation.yml` | |
| Layouts, styles, scripts | `_layouts/`, `_includes/`, `assets/` | |

Do not rename existing files in `_publications/`, `_people/` or `_posts/`: the filename is the URL, and other sites link to them. Images for papers go in `img/publications/`, portraits in `img/people/` (about 800 px on the long side is plenty). Leave `img/wiki/` alone: the lab wiki links to those files.

## Add a publication

Create `_publications/2026-03-01-JoN.markdown` (date of publication, short journal code):

```yaml
---
title: "Exact title of the paper"
date: 2026-03-01
authors: [Lastname A, Knapen T]        # PubMed style, full list, in order
journal: Journal of Neuroscience
citation: "46(9), e1234252026"          # optional
doi: 10.1523/JNEUROSCI.1234-25.2026
pmid: "40000000"                        # optional
type: article                           # article | review | perspective | preprint
themes: [topographic-maps]              # 1-2 of: topographic-maps, precision-imaging, computational-models, perception-awareness
selected: false                         # true puts it in "Selected work"
img: /img/publications/my_figure.png    # optional
description: "One sentence on what the paper shows."
links:                                  # optional
  preprint: https://www.biorxiv.org/content/...
  code: https://github.com/...
  data: https://openneuro.org/datasets/...
---
Abstract text.
```

Lab members' names are printed in bold automatically when they match an entry in `lab_authors` in `_data/lab.yml`. When a preprint is published, update its file (journal, DOI, `type: article`) rather than adding a second one.

## Add or update a person

Create `_people/firstname-lastname.markdown`:

```yaml
---
title: Firstname Lastname
role: PhD student
status: current                 # pi | current | alumni
order: 2026                     # sort key, usually the start year
start: 2026
end:                            # year of leaving, for alumni
now: ""                         # alumni: current position or institution
photo: /img/people/fl.jpg       # optional; initials are shown without it
pubname: "Lastname F"           # how PubMed writes the name; lists their papers on their page
themes: [computational-models]
description: "One line about their project."
links: { email: , website: , scholar: , orcid: , github: , x: , bluesky: , linkedin: }
---
Short bio in the third person. Leave the body empty if there is none yet.
```

When someone joins, also add their `pubname` to `lab_authors` in `_data/lab.yml`, so their name is printed in bold in publication lists. When someone leaves, change `status` to `alumni` and fill in `end` and `now`.

## Add news

Create `_posts/2026-12-15-short-name.markdown`:

```yaml
---
title: Short headline in sentence case
date: 2026-12-15 12:00:00
description: One sentence shown in lists.
img: /img/posts/optional_image.png
---
Text of the news item.
```

For a vacancy, add `closed: true` once it is filled; the post then shows a notice.

## Add software or a dataset

Add an entry to `_data/software.yml`:

```yaml
- name: toolname
  kind: software            # software | dataset
  status: maintained        # maintained | in development | upcoming | available | archived
  description: "One or two sentences."
  url: https://github.com/VU-Cog-Sci/toolname
  docs: https://toolname.readthedocs.io
  paper: /publications/2026-03-01-JoN/
  themes: [computational-models]
  featured: false           # true shows it on the home page (keep to four)
```

## Checks

A GitHub Actions workflow (`.github/workflows/check.yml`) builds the site with the GitHub Pages gem set and checks internal links and images on every pull request.

## Lab wiki

How-tos for data handling and analysis live in the [lab wiki](https://github.com/tknapen/tknapen.github.io/wiki).

## Credits

Fonts: Source Serif 4 and Inter, self-hosted, SIL Open Font License (see `assets/fonts/`).
