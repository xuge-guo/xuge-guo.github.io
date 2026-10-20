# Xuge Guo — academic résumé website

A compact, one-page academic profile for PhD applications. It is plain HTML and CSS with a small Python build script and no JavaScript dependencies.

Website: https://xuge-guo.github.io/

## Preview locally

From this folder, run:

```bash
python3 build.py
python3 -m http.server 8000 --directory dist
```

Then open `http://localhost:8000`. Python 3 is the only build requirement.

## Update the site

- Edit `src/content.json` to update your profile, research interests, education, research experience, projects, teaching, and skills. The expected graduation date is stored once in `expected_graduation` and used in both the header and education section.
- Edit `build.py` only when changing the page structure or adding new kinds of sections.
- Edit `src/styles.css` to adjust the layout or typography.
- Rebuild with `python3 build.py`.

The supplied CV is included at `src/assets/xuge-guo-cv.pdf` and linked from the page header. Replace that file when your CV changes, then rebuild. Your portrait is included at `src/assets/xuge-guo.jpg` and displayed in the header; replace it there to update the photo. The build checks that configured files exist.

Google Scholar is omitted until you have a profile URL. No publications are claimed or displayed. Content is based on the supplied CV, with expected graduation in May 2027; research dates and outcomes absent from the CV have not been added.

## Deploy

### GitHub Pages

For a personal account homepage, create a public repository named `<username>.github.io` in the account that will own the site, and put this folder's contents at its root. In **Settings → Pages**, choose **GitHub Actions** under **Build and deployment**. The included workflow builds and publishes `dist/` when changes are pushed to `main`.

After the deployment succeeds, GitHub reports the live URL in the workflow's `github-pages` environment and under **Settings → Pages**. Confirm that the homepage, portrait, and CV download are accessible before sharing the URL.

## Files

```text
src/content.json       Profile, dates, experience, projects, and asset paths
src/styles.css         Compact responsive résumé layout
src/favicon.svg        Site icon
src/assets/            Included CV and portrait files
build.py               Generates dist/index.html
dist/                  Ready-to-publish site
```
