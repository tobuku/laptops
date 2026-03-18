# FindLaptopDeals.com — Project Notes
Last updated: 2026-03-17

## Overview
- **Goal:** Monetize findlaptopdeals.com to $1,000/month via Amazon affiliate commissions
- **Strategy:** Pinterest pins + Telegram posts → findlaptopdeals.com (bridge site) → Amazon affiliate links
- **Domain:** findlaptopdeals.com (bought on Namecheap, DNS pointed to GitHub Pages)
- **Hosting:** GitHub Pages — repo: tobuku/laptops
- **Local path:** C:/Users/HDNG_HelpDesk/Documents/GitHub/laptops/
- **Amazon Affiliate Tag:** dwelldoc-20
- **Company Name:** Laptops Everything

## Analytics & SEO
- **Google Analytics:** GA4, Measurement ID: G-78BQT6GBBC, Stream ID: 13634517644
- **Google Search Console:** Verified via TXT record on Namecheap
- **Sitemap:** findlaptopdeals.com/sitemap.xml (submitted to Search Console)
- **robots.txt:** In place, points to sitemap

## Site Pages
1. index.html — Homepage with hero, category cards, gallery strip, trust section
2. students.html — 6 student laptop picks ($429–$1,049)
3. gaming.html — 6 gaming laptop picks ($699–$2,799)
4. budget.html — 6 budget laptops under $500
5. gaming-under-500.html — 5 gaming laptops under $500
6. gaming-under-1000.html — 5 gaming laptops under $1000
7. under-1000.html — 5 laptops under $1000
8. touchscreen.html — 5 touchscreen/2-in-1 laptops
9. deals.html — 5 current deals with sale pricing
10. black-friday.html — 4 Black Friday 2026 predictions
11. privacy.html — Privacy policy (required for Pinterest API app)
12. laptop-backpacks.html — Best laptop backpacks guide (11 products, linked from homepage)
13. portable-power-banks.html — Best portable power banks guide (8 products, linked from homepage)

## Design & Tech Stack
- **Font:** Inter (Google Fonts)
- **Animations:** GSAP ScrollTrigger (fade-ups, counters, staggered reveals)
- **Style:** Dark theme, glassmorphism nav, CSS custom properties
- **Logo:** img/logo.jpeg (black circular design)
- **Favicon:** favicon.svg ("FLD" text)
- **Images:** img/1.jpg through img/38.jpg + logo.jpeg

## Social Media Automation — FULLY OPERATIONAL ✅
Both Pinterest and Telegram schedulers are live and running automatically every day via GitHub Actions.
- **Repo:** github.com/tobuku/social-automation-system
- **Local path:** C:/Users/HDNG_HelpDesk/Documents/GitHub/social-automation-system
- **Progress file:** C:/Users/HDNG_HelpDesk/Desktop/Content Creation/Social Media/Pinterest/Claude Pinterest Plan/PINTEREST-API-PROGRESS.md
- **To-do file:** C:/Users/HDNG_HelpDesk/Desktop/Content Creation/Social Media/Pinterest/Claude Pinterest Plan/TODO-AND-RESTART.md

### Pinterest
- **App:** FindLaptopDeals — App ID: 1551695 — **STANDARD ACCESS APPROVED 2026-03-15** ✅
- **Scopes:** pins:read, pins:write, boards:read, boards:write
- **Schedule:** 5 pins/day at 8am Hawaii via GitHub Actions
- **Queue:** ~51 pins across 10 boards (runs out ~2026-03-26)
- **Token expires:** 2026-04-14 — run `npm run pinterest:demo` to refresh

### Telegram
- **Bot:** @findlaptopdealsbot
- **Channel ID:** -1003540921578
- **Schedule:** 1 post/day at 8am Hawaii via GitHub Actions
- **Queue:** ~37 posts (runs out ~2026-04-22)

## GSC Issues (all resolved as of 2/27/26)
- [x] Duplicate without user-selected canonical — canonical tags added to all pages
- [x] Nav logo links normalized to `/` to prevent `/index.html` duplicate
- [x] Crawled/not indexed pages — guide content added to all pages (~400 words each)
- [ ] Request re-indexing in GSC for all updated pages (still pending)

## Upcoming Maintenance
| Date | Action |
|---|---|
| **~2026-03-26** | Pinterest queue runs out — add second wave to `adapters/pinterest/pin-content.ts` |
| **2026-04-14** | Pinterest access token expires — run `npm run pinterest:demo` to refresh |
| **~2026-04-22** | Telegram queue runs out — add second wave to `adapters/telegram/post-content.ts` |
