# Hesyra Labs — Brand Guidelines (static site)

## Files
- `index.html` — the site
- `support.js` — runtime (required)
- `assets/` — logo + product images
- `_ds/` — Hesyra design tokens (fonts, colors)

Keep the folder structure as-is. No build step needed.

## Deploy on Render
1. Push this folder to a GitHub repo (in Antigravity: Source Control → Publish).
2. Render → New → **Static Site** → pick the repo.
3. Build Command: *(leave empty)*
4. Publish Directory: `.` (or `deploy` if this folder sits inside a larger repo)
5. Create Static Site. Use the resulting URL in Pomelli.

## Test locally
`npx serve .` then open http://localhost:3000
