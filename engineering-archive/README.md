# Engineering Archive

Static GitHub Pages site organized around **Study Note** and **Practice Project**.

## Publish (GitHub Pages)

1. Extract `engineering-archive.zip` on your computer.
2. In repository `Isp99/Isp99.github.io`, select **Add file → Upload files**.
3. Drag **all the contents inside** the extracted `engineering-archive` folder into the upload area: `index.html`, `assets/`, `study/`, `practice/`, and this `README.md`.
4. Commit the changes. GitHub Pages should be configured to deploy the `main` branch root (`/`).
5. Open `https://isp99.github.io/` after deployment.

**Important:** Do not upload the ZIP itself; GitHub Pages does not unpack ZIP files. Do not upload an extra enclosing directory. GitHub Pages must find `index.html` at repository root.

## Folder outline

- `index.html` — original Home design, preserved
- `assets/site.css` — shared font / colors / design rules
- `assets/hero.webp` — original Home artwork extracted from embedded image
- `study/aerodynamics.html` — Aerodynamics subject cards
- `study/aerodynamics/fundamentals.html` — original 9-chapter, 24-article TOC
- `study/aerodynamics/fundamentals/*.html` — 24 article pages; **placeholders, not full lecture text**
- `study/aerodynamics/` — future course pages
- `study/artificial-intelligence.html`, `study/heat-transfer.html` — landing pages
- `practice/` — practice landing pages

The 404 errors resulted from broken/missing links between Home, Aerodynamics, Fundamentals and the article paths. The files now exist at the expected locations. For non-provided notes, the pages intentionally indicate that content will be added later.
