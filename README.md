# Hesyra Labs — Brand Guidelines Website

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/hesyralabs/Hesyra-Brand-Guidelines-Website)

Comprehensive brand guidelines and interactive design system for **Hesyra Labs** — precision-crafted digital dental prosthetics (Nagpur, India).

---

## 📂 Project Structure

```
├── deploy/                  # Production-ready static site bundle
│   ├── index.html           # Brand guidelines portal
│   ├── support.js           # Runtime & interactive controls
│   ├── README.md            # Static site deployment notes
│   ├── assets/              # High-resolution logos, product visuals & assets
│   └── _ds/                 # Hesyra Design System tokens, CSS & JS
├── index.html               # Root redirect to deploy/
├── .gitignore               # Ignored system & cache files
└── README.md                # Project documentation
```

---

## 🚀 Live Deployment Options

### 1. Render (Static Site)
1. Go to **[Render Dashboard](https://dashboard.render.com)** -> **New +** -> **Static Site**.
2. Connect the `Hesyra-Brand-Guidelines-Website` repository.
3. Configure settings:
   - **Build Command**: *(leave empty)*
   - **Publish Directory**: `deploy` (or `.` using root redirect)
4. Click **Create Static Site**.

### 2. GitHub Pages
1. Go to **Settings** -> **Pages** in this GitHub repository.
2. Under **Build and deployment** > **Source**, choose **Deploy from a branch**.
3. Select branch: `main`, folder: `/ (root)` and click **Save**.
4. The site will be available directly via the root redirect.

### 3. Vercel / Netlify / Cloudflare Pages
- Zero build configuration needed. Set root or output directory to `deploy`.

---

## 💻 Local Testing

You can serve the project locally using any static HTTP server:

```bash
# Serve directly from the root
npx serve .

# Or serve the deploy directory directly
npx serve deploy
```

Then visit [http://localhost:3000](http://localhost:3000).

---

## 🎨 Brand Assets Included
- Vector & high-res PNG/WebP logos (dark/light variants)
- Design tokens: Typography (`Inter`, `Montserrat`), Color palettes (`#001A33`, `#7A9C96`, etc.)
- Product 3D renders & clinical case references
