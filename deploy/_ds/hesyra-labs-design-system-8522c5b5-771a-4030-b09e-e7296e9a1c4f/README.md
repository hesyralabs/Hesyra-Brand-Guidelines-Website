# Hesyra Labs — Design System

## Company Overview

**Hesyra Labs Pvt Ltd** is a precision B2B dental prosthetics manufacturer and SaaS platform based in Nagpur, Maharashtra, India (Tech Park, MIDC, Vidarbha Region). They operate a high-resolution DLP 3D printing facility producing dental restorations and appliances for dentist clinics.

**Core value proposition:** Digital-first dental lab — any case fabricated and shipped within 24–72 hours, at a fraction of conventional lab costs. Target customers are dental clinics and individual dentists in India.

**Products offered:**
- Crowns & Bridges (ceramic-hybrid resin, 48hr)
- Digital Denture Systems (72hr)
- Ceramic Veneers (48hr)
- Surgical Guides (24hr)
- Retainers & Clear Aligners (48–72hr)

**Contact:** hesyralabs@gmail.com

---

## Sources Provided

| Source | Path / URL |
|---|---|
| Marketing website codebase (React/Vite) | `src/` (mounted via File System Access API) |
| Brand logo (large) | `uploads/logo.png` → `assets/logo.png` |
| Brand logo (small webp) | `uploads/logo-small.webp` → `assets/logo-small.webp` |

---

## Products / Surfaces

### 1. Marketing Website (`hesyralabs.com`)
React + Vite SPA. Sections: Navbar, Hero (video bg), Products grid, Technology bento, Portal Teaser (animated scroll demo), Workflow, Trust, ROI Calculator, CTA Banner (lead capture form), Footer. Routes: `/`, `/about`, `/blog`, `/products/:slug`, `/portal-docs`, `/privacy`, `/terms`.

### 2. Hesyra Portal (under development)
A SaaS portal (`portal.hesyralabs.com`) for dental clinics to upload intraoral scans, track case status (Kanban board), and submit Rx requests. Multi-step modal workflow. Auth tiers: Clinic / Lab / Admin. Currently "Coming Soon" — the `PortalTeaser.jsx` component contains an animated mockup of the planned UI.

---

## CONTENT FUNDAMENTALS

### Tone & Voice
- **Clinical authority.** Copy speaks directly to dentists as knowledgeable peers. Uses precise terminology: "62µm XY resolution", "bi-axial flexural strength", "CE Class IIa / FDA 510(k)".
- **Problem-first.** Pain points are named in dramatic, scenario-based language ("The Nerve Near-Miss", "The E.max Fracture"). These are vivid, specific stories with quotes.
- **Confident, not arrogant.** Direct statements: "48 hours. Done." "Zero metal. No grey gingival line. Ever." Punchy. Short sentences. Present tense.
- **Technical precision + emotional resonance.** Specs are listed as data tables. Competitor comparisons are clinical and factual, never aggressive in tone.
- **No fluff, no hype.** No superlatives like "revolutionary" or "world-class". Instead: "sub-clinical marginal gap", "mean deviation under 1mm".

### Casing
- **Section mono-labels:** ALL CAPS, monospaced — e.g. `OUTPUTS`, `INFRASTRUCTURE`, `[INITIATE_PROTOCOL]`
- **Headings:** Sentence case — "Precision-Crafted Prosthetics. Any Case. 48 Hours."
- **Navigation:** Title case — "For Dentists", "Partner With Us"
- **Spec labels:** Title Case — "XY Resolution", "UV Wavelength"
- **Footer column headers:** ALL CAPS — `PLATFORM`, `COMPANY`, `HQ`
- **Logo wordmark:** ALL CAPS, spaced — "HESYRA LABS"

### Pronouns
- Addresses dentists as "you" / "your". E.g. "Your practice", "you place", "your patient".
- Company referred to as "we" / "our". E.g. "We fabricate", "our portal".
- No first-person singular "I".

### Emoji
- **Not used in UI.** Only used in pain-point scenario content (as icon stand-ins in data files), never rendered in production components. The codebase's pain point icons (`😤`, `💔`, `😰`) are data only; the production UI would use proper icons.

### Copy Patterns
- Bracketed labels for emphasis: `[INITIATE_PROTOCOL]`, `HESYRA PORTAL 2.0`
- Arrow links: `View Portal →`
- Short factual taglines: "Enter the era of digital dentistry."
- Italicised taglines in hero: e.g. "The end of 'Where is my case?'"

---

## VISUAL FOUNDATIONS

### Colors
- **Base background:** `#001A33` (Dark Azure) — deep navy, not pure black. The entire site sits on this.
- **Surface / elevated:** `#00243f` — glass panels, cards, overlays.
- **Deep surface:** `#000d1a` — footer, code blocks, data boxes.
- **Accent:** `#7A9C96` (Bioceramic teal) — the singular brand accent. Used for glows, borders, mono-labels, hover states, and the Brand CTA button.
- **Text:** `#E8E6E5` (Substrate Gray) primary; `#9baab0` secondary; `#5e7a80` tertiary.
- **Category pills:** Teal (restorations), blue (`#7aaff0`, surgical), violet (`#c4a0e8`, orthodontics).
- **No true white.** The "white" button is `#E8E6E5` — warm off-white. Never pure `#fff`.

### Typography
- **Display:** Montserrat — all headings, buttons, nav, logo wordmark. Tight letter-spacing (`-0.02em`).
- **Body:** Inter — all paragraphs, form inputs, card descriptions.
- **Mono:** JetBrains Mono — section labels, data spec rows, code snippets, the `mono-label` component. Always uppercase when used as a label.
- **Hero H1:** 4.5rem, Montserrat Bold, line-height 1.1.
- **Section H2:** 2.5rem, Montserrat Bold.
- **Body copy:** 0.875rem, Inter Regular, line-height 1.6.

### Backgrounds & Textures
- **Dot grid:** `radial-gradient` of `rgba(122,156,150,0.06)` dots on a 32px grid — applied as a fixed overlay at z-index -2.
- **Noise overlay:** SVG fractal noise at 3% opacity, fixed full-screen — creates subtle texture like premium print materials.
- **Ambient glow blobs:** Two radial gradient circles (teal/navy) blur-filtered at 80–100px — positioned top-right and bottom-left. Provides a soft luminous depth.
- **Glass panels:** `backdrop-filter: blur(24px)` + semi-transparent navy fill. The primary card/surface component.
- **No photography as decorative background.** Hero uses a looping factory video (dimmed to 40% opacity) with a dark gradient overlay fading to the base bg at the bottom.
- **No patterns or illustrations used decoratively.** Clean, spatial aesthetic.

### Borders
- Subtle: `rgba(255,255,255,0.04)` — almost invisible separators.
- Default: `rgba(255,255,255,0.08)` — card outlines, input borders.
- Strong: `rgba(122,156,150,0.30)` — hover states, focused elements, active pills.
- Border radius: Cards use `16px`. Buttons use `8px`. Pills/tags use `30px` (fully rounded). Icon boxes use `12px`.

### Cards
- Type: `glass-panel` — frosted glass on dark bg, 16px radius, subtle border.
- On hover: border transitions to strong (teal), box-shadow deepens + teal glow added, translateY(-8px).
- Cards have a top-edge inner gradient (`linear-gradient(180deg, rgba(255,255,255,0.06), transparent)`) via `::after` pseudo-element for a lit-from-above effect.
- Bento grid used for technology section: 12-column grid, cards spanning 8 or 4 columns.

### Shadows
- Card resting: `0 4px 30px rgba(0,0,0,0.5)`
- Card hover: `0 8px 40px rgba(0,0,0,0.6)` + teal glow
- Button glow: `0 0 20px rgba(122,156,150,0.2)` resting; stronger on hover.

### Buttons
- **Primary:** Substrate gray bg (`#E8E6E5`), dark navy text. Used for main CTAs.
- **Brand:** Bioceramic teal bg (`#7A9C96`), dark navy text. Used for "Partner With Us" / form submits.
- **Outline:** Transparent bg, off-white text, subtle border. Used for secondary actions.
- Magnetic effect: buttons have a JS-powered magnetic attraction on cursor hover (subtle, ~15px max pull).
- Font: Montserrat SemiBold, 0.875rem.
- Padding: `0.75rem 1.5rem` default; `1rem 2rem` for large hero CTAs.

### Animations & Motion
- **Framer Motion** used for page transitions, scroll-triggered animations, and portal mockup animation.
- **Scroll-based cross-dissolve:** Portal teaser section uses `useScroll` + `useTransform` to fade text out and fade UI mockup in as the user scrolls. Easing is natural/smooth.
- **Entrance animations:** `fadeInUp` with `ease-out`, staggered. Subtle.
- **Hover transitions:** 0.2–0.3s ease. Product cards lift with `translateY(-8px)`, images scale to 1.05.
- **No bounces or springy animations** in the marketing site — reserved for portal UI.
- **Preloader:** Custom branded preloader component.
- **Easing:** Primarily `ease`, `ease-out`, `cubic-bezier(0.16, 1, 0.3, 1)` (snappy ease-out-expo for mobile menu).

### Hover States
- Links: color transitions from `--text-secondary` to `--text-primary`. Underline via `::after` pseudo-element (accent color, slides in width).
- Cards: lift + stronger border + glow.
- Buttons: primary dims to 90% opacity; brand transitions to `--accent-bright`; outline gains teal border + accent glow bg.
- Footer links: color to `--accent` (teal).

### Corner Radii System
| Element | Radius |
|---|---|
| Cards / glass panels | 16px |
| Buttons | 8px |
| Icon boxes | 12px |
| Pills / tags | 30px |
| Input fields | 8px |
| Data boxes (inset) | 8px |
| Spec chips | varies |

### Layout Rules
- **Container:** max-width 1400px, 2rem horizontal padding.
- **Section padding:** ~6–8rem vertical.
- **Grid:** CSS Grid throughout. Product grid: 3 columns (→2 →1). Bento: 12-col. Footer: 4 columns.
- **Navbar:** Fixed, full-width, transparent with gradient-to-transparent fade. Blur backdrop.
- **Min-width lock:** Site locks to desktop layout at min-width 1200px (mobile views exist but are secondary). Desktop-first.

### Transparency & Blur
- Heavy use of `backdrop-filter: blur(24px)` on glass panels. Used on cards, navbar, mobile menu overlay.
- Glass bg uses `rgba(0,26,51,0.55)` — semi-transparent navy.
- Noise overlay at 3% — consistent film grain effect.

### Imagery
- **Color temperature:** Cool/clinical. Images of dental prosthetics (white ceramics on dark backgrounds).
- **No grain filters or B&W treatment.**
- **Product images:** High-contrast product shots on near-black backgrounds.
- **Video:** Factory tour background, dimmed to 40%.

---

## ICONOGRAPHY

### Icon System
- **Lucide React** (`lucide-react` npm package) — the primary icon library throughout. Stroke-based icons, `strokeWidth={2}`, `strokeLinecap="round"`, `strokeLinejoin="round"`. 16–24px typical sizes.
- Icons used in portal UI: `Search`, `Monitor`, `Box`, `CreditCard`, `Settings`, `Palette`, `Bell`, `LogOut`, `FileText`, `MoreHorizontal`, `Lock`, `Mail`, `X`, `CheckCircle`, `UploadCloud`, `ChevronRight`, `Menu`.
- CDN reference for HTML-only usage: `https://unpkg.com/lucide@latest` (or `lucide-static` for individual SVG files).
- Custom SVGs are used only for the logo icon and a few simple inline arrow/arrow-right icons (hand-coded in JSX).

### Logo Mark
- Atom-like orbital ring symbol — four interlocking elliptical rings forming a symmetrical knot/atomic shape.
- Rendered as PNG (`assets/logo.png`) loaded via `<img>` with `filter: invert(1)` on dark backgrounds (making it appear white).
- Displayed alongside the wordmark "HESYRA LABS" in Montserrat SemiBold. "HESYRA" regular weight, "LABS" bold weight.
- Small variant available as `assets/logo-small.webp`.

### No emoji in UI. No unicode character icons.

---

## FILE INDEX

```
hesyra-design-system/
├── README.md                        ← This file
├── SKILL.md                         ← Agent skill descriptor
├── colors_and_type.css              ← Full CSS token sheet (colors, type, spacing, utilities)
│
├── assets/
│   ├── logo.png                     ← Brand logo mark (PNG, use with filter:invert(1) on dark)
│   └── logo-small.webp              ← Compact logo mark variant
│
├── preview/                         ← Design system card previews (registered in asset review)
│   ├── colors-base.html
│   ├── colors-semantic.html
│   ├── colors-pills.html
│   ├── type-display.html
│   ├── type-body.html
│   ├── type-mono.html
│   ├── spacing-tokens.html
│   ├── spacing-radius.html
│   ├── spacing-shadows.html
│   ├── components-buttons.html
│   ├── components-cards.html
│   ├── components-pills.html
│   ├── components-inputs.html
│   ├── components-data-rows.html
│   ├── brand-logo.html
│   └── brand-mono-label.html
│
└── ui_kits/
    ├── website/
    │   ├── README.md
    │   ├── index.html               ← Interactive marketing website prototype
    │   ├── Navbar.jsx
    │   ├── Hero.jsx
    │   ├── Products.jsx
    │   ├── Technology.jsx
    │   └── Footer.jsx
    └── portal/
        ├── README.md
        ├── index.html               ← Interactive portal prototype
        ├── Login.jsx
        ├── Dashboard.jsx
        └── RxModal.jsx
```
