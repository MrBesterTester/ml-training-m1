---
id: REQ-026
title: "Step 6.1: Static comparison page + samkirk.com feature page"
status: pending
created_at: 2026-03-13T00:00:00Z
user_request: UR-010
source_step: "6.1"
source_doc: docs/TODO.md
blueprint_ref: docs/BLUEPRINT.md
---

# Step 6.1: Static Comparison Page + samkirk.com Feature Page

## What

Create three deliverables:
1. `web/index.html` — styled HTML comparison page from results/comparison.md
2. `web/feature.html` — portfolio feature page for this project, designed to live on samkirk.com
3. Suggested home page entry — a section block for samkirk.com's page.tsx

## Requirements

### Comparison page (web/index.html)
- Generate styled HTML from results/comparison.md
- Side-by-side base vs fine-tuned responses for all 12 comparisons
- Clean, readable styling consistent with Sam's other project documents

### Feature page (web/feature.html)
- Standalone portfolio page showcasing this project
- Career narrative: ties 3 years of genAI study (samkirk.com projects) with 4 decades of Silicon Valley test automation experience
- Physics-first approach as the distinctive value proposition
- Key results highlighted (boundary scan, numerical data analysis)
- Tech stack, training details, reproduction steps
- Match samkirk.com's visual style (Tailwind-inspired, dark theme with accent colors)

### Home page entry (suggested snippet)
- Follow the pattern from samkirk.com page.tsx: h2 title, description, tech notes list, link
- Position this as the career-bridging project it is

## Context

- samkirk.com is Next.js + Tailwind, hosted on Vercel (github.com/MrBesterTester/samkirk.com-v3)
- Home page sections: Dance Menu, Photo Fun, Villa Madu Bali, Song Dedication, Explorations
- This project bridges genAI (the site's theme) with hardware test automation (Sam's career)
- Career agent context at ../mycareeragent

## Verification

- web/index.html renders correctly showing 12 comparisons
- web/feature.html renders as a polished portfolio piece
- Suggested page.tsx snippet follows existing pattern
