#!/usr/bin/env python3
"""Build the one-page academic profile from src/content.json into dist/."""

from html import escape
from pathlib import Path
import json
import shutil

ROOT = Path(__file__).resolve().parent
DIST = ROOT / "dist"
CONTENT = json.loads((ROOT / "src" / "content.json").read_text(encoding="utf-8"))


def e(value):
    return escape(str(value), quote=True)


def profile_links():
    items = []
    if CONTENT["email"]:
        items.append(f'<a href="mailto:{e(CONTENT["email"])}">{e(CONTENT["email"])}</a>')
    for key, label in (("github", "GitHub"), ("linkedin", "LinkedIn"), ("scholar", "Google Scholar")):
        if CONTENT[key]:
            items.append(f'<a href="{e(CONTENT[key])}" target="_blank" rel="noopener noreferrer">{label}</a>')
    return '<span class="contact-links">' + '<span aria-hidden="true">·</span>'.join(items) + '</span>'


def render_entries(entries):
    articles = []
    for entry in entries:
        date = f'<span class="entry-date">{e(entry["dates"])}</span>' if entry.get("dates") else ""
        role = f'<p class="entry-subtitle">{e(entry["role"])}</p>' if entry.get("role") else ""
        summary = f'<p class="entry-summary">{e(entry["summary"])}</p>' if entry.get("summary") else ""
        award = f'<p class="entry-award">Award: {e(entry["award"])}</p>' if entry.get("award") else ""
        bullets = "".join(f'<li>{e(item)}</li>' for item in entry.get("bullets", []))
        articles.append(f'''<article class="entry">
        <div class="entry-heading"><h3>{e(entry["title"])}</h3>{date}</div>
        {role}{summary}{award}
        <ul>{bullets}</ul>
      </article>''')
    return "\n      ".join(articles)


def render_education():
    articles = []
    for entry in CONTENT["education"]:
        dates = entry.get("dates", "")
        if entry.get("expected_graduation"):
            dates = f'{entry["start"]}–{CONTENT["expected_graduation"]} (expected)'
        details = f'<p class="entry-details">{e(entry["details"])}</p>' if entry.get("details") else ""
        articles.append(f'''<article class="entry">
        <div class="entry-heading"><h3>{e(entry["title"])}</h3><span class="entry-date">{e(dates)}</span></div>
        <p class="entry-subtitle">{e(entry["degree"])}</p>
        <p class="entry-location">{e(entry["location"])}</p>
        {details}
      </article>''')
    return "\n      ".join(articles)


def render():
    name = e(CONTENT["name"])
    cv = f'<a class="cv-link" href="{e(CONTENT["cv_file"])}" download>Download CV <span aria-hidden="true">↓</span></a>' if CONTENT["cv_file"] else ""
    portrait = f'<img class="portrait" src="{e(CONTENT["portrait_file"])}" alt="Portrait of {name}" width="112" height="112" decoding="async">' if CONTENT["portrait_file"] else ""
    interests = "".join(f'<li>{e(interest)}</li>' for interest in CONTENT["research_interests"])
    skills = "".join(f'<div><dt>{e(skill["category"])}</dt><dd>{e(skill["items"])}</dd></div>' for skill in CONTENT["skills"])
    return f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="{e(CONTENT["bio"])}">
  <meta name="theme-color" content="#ffffff">
  <title>{name} — Robotics &amp; Control</title>
  <link rel="icon" type="image/svg+xml" href="assets/favicon.svg">
  <link rel="stylesheet" href="assets/styles.css">
</head>
<body>
  <a class="skip-link" href="#content">Skip to content</a>
  <main class="resume" id="content">
    <header class="profile-header">
      {portrait}
      <div class="profile-main">
        <h1>{name}</h1>
        <p class="position">M.S. Mechanical Engineering · Robotics &amp; Control<br>Columbia University SEAS · Expected {e(CONTENT["expected_graduation"])}</p>
        {profile_links()}
      </div>
      <div class="header-cv">{cv}</div>
    </header>
    <p class="profile-bio">{e(CONTENT["bio"])}</p>
    <nav class="section-nav" aria-label="Page sections">
      <a href="#research">Interests</a><a href="#experience">Research</a><a href="#projects">Projects</a><a href="#education">Education</a><a href="#teaching">Teaching</a><a href="#skills">Skills</a>
    </nav>
    <section class="resume-section" id="research">
      <h2>Research interests</h2>
      <ul class="interest-list">{interests}</ul>
    </section>
    <section class="resume-section" id="experience">
      <h2>Research experience</h2>
      {render_entries(CONTENT["research_experience"])}
    </section>
    <section class="resume-section" id="projects">
      <h2>Selected robotics projects</h2>
      {render_entries(CONTENT["projects"])}
    </section>
    <section class="resume-section" id="education">
      <h2>Education</h2>
      {render_education()}
    </section>
    <section class="resume-section" id="teaching">
      <h2>Teaching experience</h2>
      {render_entries(CONTENT["teaching"])}
    </section>
    <section class="resume-section" id="skills">
      <h2>Technical skills</h2>
      <dl class="skills-list">{skills}</dl>
    </section>
    <footer class="page-footer"><span>{name} · Columbia University</span><a href="#content">Back to top ↑</a></footer>
  </main>
</body>
</html>
'''


def main():
    assets = DIST / "assets"
    assets.mkdir(parents=True, exist_ok=True)
    for filename in ("styles.css", "favicon.svg"):
        shutil.copy2(ROOT / "src" / filename, assets / filename)
    source_assets = ROOT / "src" / "assets"
    if source_assets.exists():
        for source in source_assets.iterdir():
            if source.is_file() and not source.name.startswith("."):
                shutil.copy2(source, assets / source.name)
    for key in ("cv_file", "portrait_file"):
        if CONTENT[key] and not (DIST / CONTENT[key]).is_file():
            raise FileNotFoundError(f"{key} points to a missing file: {CONTENT[key]}")
    (DIST / "index.html").write_text(render(), encoding="utf-8")
    print(f"Built one-page academic website in {DIST}")


if __name__ == "__main__":
    main()
