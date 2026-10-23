# learn

**[learn.sankhacooray.com](https://learn.sankhacooray.com)** — the education & learning hub in the
sankhacooray.com network: Kiwrious science sensors, SPARK microlearning at NUS CHILL, Scratch GPT for
children, and the ICE design-thinking programmes.

Served by a Cloudflare Worker: static assets from `public/`, plus `src/worker.js`, whose `/api/og?url=` route
fetches a project site's current `og:image` (allowlisted hosts only, cached 1 h). Cards with an `og` page in
`projects.json` show a shared fallback, then fade to that live image.
The VS Code workspace for the hub and its projects is `../learn-sankhacooray-com.code-workspace`.

## Files

| Path | Purpose |
|------|---------|
| `projects.json` | The hub's content: research areas, projects, roles, live links |
| `footer.html` | One-line footer, placed in the last section |
| `template.html` | Page template (CSS + JS inline) |
| `build.py` | Renders `public/index.html` from the two files above, as static HTML for crawlers |
| `public/thumbs/` | Screenshots of the live sites, 800 px wide |
| `public/og.png` | 1200×630 share image, rendered from `og/og.html` |
| `public/icon*.png`, `icon.svg`, `apple-touch-icon.png`, `manifest.webmanifest` | Icons + PWA manifest |
| `src/worker.js` | Serves assets; `/api/og` live share-image proxy |
| `wrangler.toml` | Worker config + custom domain (creates the DNS record) |

Roles on each card: **Mine** (I built and run it), **Co-owned** (shared ownership),
**Contributed** (belongs to another team or org — NUS CHILL, the Augmented Human Lab or a colleague).
Only live sites are linked; several source repositories are private.

## Edit, preview, deploy

```
python3 build.py
python3 -m http.server 4796 --bind 127.0.0.1 -d public
CLOUDFLARE_ACCOUNT_ID=9a1da48a0f61e7cebcba39517856d87e npx wrangler deploy
```

Share image: edit `og/og.html`, then render it and bump `?v=N` on `og:image`/`twitter:image` in `template.html`:

```
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless=new --hide-scrollbars \
  --force-device-scale-factor=1 --window-size=1200,630 --virtual-time-budget=6000 \
  --allow-file-access-from-files --screenshot=public/og.png "file://$PWD/og/og.html"
```

After deploying, curl the page, `og.png` and the icons to confirm 200s and the right content types.
