# PainCave Guide

An independent UK guide to indoor cycling: smart bikes vs turbo trainers, the best indoor bikes, rocker plates, cycling apps and accessories. Amazon links use the tag `paincavetips-21`.

Live site: https://mbnnkmp.github.io/paincave/

## How it works

- `docs/` is the published site. GitHub Pages serves it from the `main` branch.
- `build.py` generates every page in `docs/`, plus `sitemap.xml` and `robots.txt`. All content, prices and links live in this one file.
- `source-images/rocker.py` draws the rocker plate diagram.

## Making changes

1. Edit `build.py` (for example, a price, a product or the `UPDATED` date).
2. Run `python3 build.py`.
3. Commit and push. The site updates within a minute or two.

## Images

Photos come from Unsplash and Pexels under their free licences, and each one is credited on the page and on `disclosure.html`. The rocker plate diagram is original.
