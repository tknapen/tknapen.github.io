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
| Animations | `_data/clips.yml`, `assets/clips/` | `/animations/` and wherever a page includes one |
| News | `_posts/YYYY-MM-DD-<name>.markdown` | `/YYYY/MM/DD/<name>.html` |
| Lab handbook pages | `_resources/` | `/resources/<file>/` |
| Lab-wide facts (affiliations, links, funders, dataset info) | `_data/lab.yml` | used on many pages |
| Menu | `_data/navigation.yml` | |
| Layouts, styles, scripts | `_layouts/`, `_includes/`, `assets/` | |

Do not rename existing files in `_publications/`, `_people/` or `_posts/`: the filename is the URL, and other sites link to them. Images for papers go in `img/publications/`, portraits in `img/people/` (about 800 px on the long side is plenty). Leave `img/wiki/` alone: the lab wiki links to those files.

Colors are tokens (CSS custom properties) at the top of `assets/css/site.css`. The site follows the visitor's light or dark system setting, and the switch in the header lets them choose light, dark or automatic (stored in their browser). The light palette is the `:root` block; the dark palette is written twice, once for the system setting and once for `data-theme="dark"`, and the two blocks must stay identical. Use a token for any new color rather than a literal value. In dark mode, figures sit on a light panel (`--figure-bg`, `--image-bg`) so transparent images keep readable labels. The page background colors also appear in the two `theme-color` tags in `_includes/head.html` and in `SCHEME_BG` in `assets/js/site.js`; change them together with `--bg`.

Each research theme has a colour, `--hue-<theme slug>` (light and dark values in the token blocks), used only for small marks next to the theme's name: the strip on theme cards and theme pages, and dots on publication filters, paper chips and theme labels. Elements get the colour through `data-hue="<theme slug>"` and the `[data-hue=…]` rules in the "Flourishes" section of `site.css`. A new theme needs a `--hue-…` token in all three token blocks and a `[data-hue=…]` rule; without them its marks fall back to grey.

The line ornaments (eccentricity rings, pRF isolines, contour lines) are inline SVG in `_includes/ornament.html`, drawn in `--ornament` at `--ornament-opacity`. They are decorative (`aria-hidden`) and hidden in print and in forced-colours mode. The logomark in the header is CSS (`.logomark`, using `--polar-wheel`): the polar-angle colour ring around a fixation dot. The tab icon is the same mark. `tools/make_favicon.py` writes `assets/img/favicon.svg`, whose dot is graphite or white depending on the browser's colour scheme; `favicon-48.png` and `apple-touch-icon.png` in the same folder are renders of it for browsers that do not take SVG icons.

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
type: article                           # article | review | perspective | preprint | chapter
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

Lab members' names are printed in bold automatically when they match an entry in `lab_authors` in `_data/lab.yml`. When a preprint is published, update its file (journal, DOI, `type: article`) rather than adding a second one; move the preprint DOI to `links.preprint`.

eLife Reviewed Preprints are entered as `journal: eLife`, `citation: "Reviewed Preprint"`, `type: preprint`, with the eLife DOI without a version suffix. When the Version of Record appears, set `type: article`, replace the citation and add the PMID. Book chapters use `type: chapter`, with the book title as `journal`.

## Check for new publications

`tools/pubwatch.py` lists papers and preprints by Tomas Knapen that have no file in `_publications/` yet. It queries PubMed and Crossref, which also registers bioRxiv, OSF and eLife preprints. Google Scholar is not used because it has no API and blocks automated access. The script matches records to existing files by DOI, PMID, linked versions and title. It prints three lists: new candidates (with the evidence that the Knapen author is Tomas Knapen), updates to existing files (a preprint that has been published, an eLife Reviewed Preprint that became a Version of Record, a missing PMID), and records that look like versions of existing entries. It changes no files.

```bash
python3 tools/pubwatch.py
```

`--json` gives the same lists with abstracts, and `--since YYYY-MM-DD` widens the Crossref window (default: the last two years; PubMed is always searched in full). The exit status is 0 when the check ran, 1 when a source failed and the check is partial, and 2 when nothing could be checked.

A weekly scheduled Claude Code task runs the script, adds what it finds and opens a pull request; nothing goes live until that pull request is merged. Records that should not be reported again (another T Knapen, a preprint of a paper listed under a different title) go in `tools/pubwatch-ignore.txt`, one DOI or PMID per line followed by `# reason`. Corrections, peer-review records and conference abstracts (Journal of Vision/VSS, ISMRM, CCN) are skipped automatically.

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

A person with an empty body gets a card on /people/ without a link. Add `sitemap: false` to their front matter until a bio exists, and remove it once it does.

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

## Change the home-page figures

The figures that rotate at the top of the home page are listed under `hero_slides` in the front matter of `index.html`, in display order:

```yaml
hero_slides:
  - img: /assets/img/hero/my-figure-1600.webp      # about 1600 px wide
    img_small: /assets/img/hero/my-figure-800.webp # about 800 px wide, for phones
    width: 1600                                    # pixel size of img
    height: 1200
    bg: dark                                       # light (white frame) or dark (black frame)
    alt: "What the figure shows, in one sentence."
    caption: "Short caption, may link to a paper ([Author et al., 2026](/publications/2026-03-01-JoN/))"
```

The frame is 3:2 and the whole figure is always shown. Slides change every 7 seconds; visitors can pause them, and they stay still for people who have turned on reduced motion. With one slide, the controls disappear.

## Add an animation

Animations are short silent clips, listed in `_data/clips.yml` and stored in `assets/clips/`. To add one:

```bash
tools/add_clip.sh my-render.mp4 my-clip
```

This writes `assets/clips/my-clip.mp4` (H.264, at most 1280 px wide) and `my-clip.webp` (the last frame, shown before the clip plays; `--poster-at 4.5` picks another moment), and prints an entry to paste into `_data/clips.yml`. Fill in its `title` and `caption`. The caption is also the text alternative, so it should say what the animation shows.

Place the clip on any page, in Markdown or HTML, with:

```liquid
{% include clip.html id="my-clip" %}
```

Every clip in `_data/clips.yml` is also shown on `/animations/`; `page` and `page_title` give the link to where it is explained, and `home: true` puts one clip on the home page.

For dark mode, render the same clip on a dark background and add it under the same id:

```bash
tools/add_clip.sh my-render-dark.mp4 my-clip --dark
```

It goes to `assets/clips/dark/` and is used automatically for visitors in dark mode. Until a dark render exists, the light one is shown on a light panel, like the figures.

Clips made for the site itself are manim8 projects in [site-animations](https://github.com/tknapen/site-animations). Its `tools/render.py <project> --profile final --site <path to this checkout>` renders a clip in the light and the dark site style and copies both, with their stills, into `assets/clips/`; only the entry in `_data/clips.yml` and the include remain to be written.

A clip plays once when it scrolls into view and then holds its last frame; the button under it pauses and replays. It does not start by itself for visitors who prefer reduced motion, and without JavaScript the browser's own video controls are shown.

## Checks

A GitHub Actions workflow (`.github/workflows/check.yml`) builds the site with the GitHub Pages gem set and checks internal links and images on every pull request.

## Lab wiki

How-tos for data handling and analysis live in the [lab wiki](https://github.com/tknapen/tknapen.github.io/wiki).

## Credits

Fonts: Space Grotesk (headings) and Public Sans (text), self-hosted, SIL Open Font License (see `assets/fonts/`).
