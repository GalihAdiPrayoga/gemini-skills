# UI/UX Pro Max — Automatic Design Intelligence & Motion Rule

## Mandatory UI/UX Protocol

Whenever you are asked to design, build, style, refactor, or review any user interface (pages, components, design systems, landing pages, dashboards, forms, mobile/desktop screens, or frontend code in React, Next.js, Vue, Svelte, Tailwind, CSS, Framer Motion, GSAP, etc.):

### 1. Automatic Activation
You MUST automatically consult the **UI/UX Pro Max** design intelligence system BEFORE writing or updating UI code.

### 2. Execution Commands
Run the local search tool via Python to extract verified design tokens, style rules, animation blueprints, and anti-patterns:
- **Full Page / Project Design System:**
  ```powershell
  python "C:\Users\teknos\.gemini\config\skills\ui-ux-pro-max\scripts\search.py" "<product_type> <industry> <keywords>" --design-system
  ```
- **Targeted Domain Queries (style, color, typography, ux, icons, chart, gsap, framer, framer-motion, react):**
  ```powershell
  python "C:\Users\teknos\.gemini\config\skills\ui-ux-pro-max\scripts\search.py" "<keyword>" --domain <domain>
  ```
- **Technology Stack Best Practices (e.g. framer-motion, react, nextjs, astro, html-tailwind, shadcn):**
  ```powershell
  python "C:\Users\teknos\.gemini\config\skills\ui-ux-pro-max\scripts\search.py" "<topic>" --stack <stack_name>
  ```

---

### 3. Context-Aware Motion & Animation Architecture ("Gunakan Sesuai Kebutuhan")

Pilih teknologi animasi yang paling tepat berdasarkan use-case tanpa over-engineering:

| Kategori Use-Case | Pilihan Utama | Alasan & Kapan Digunakan |
| :--- | :--- | :--- |
| **Micro-Interactions Sederhana** | **Tailwind CSS / Pure CSS** | Transisi hover tombol, perubahan warna, border, shadow, dan active state sederhana. Zero runtime overhead. |
| **Komponen Interaktif & State UI** | **Framer Motion** (`motion/react`) | Komponen React / Next.js / Astro Islands: exit animations (`<AnimatePresence>`), layout morphing (`layoutId`, `layout`), spring gestures (`whileHover`, `whileTap`), modal/drawer, dan staggered cards. |
| **Landing Hero, Timeline & Scrollytelling** | **GSAP + ScrollTrigger** | Animasi berurutan yang kompleks (multi-step timelines), canvas/WebGL sync, pinned sections, text split character reveals, dan scrubbing scroll yang presisi. |
| **Parallax & Visual Depth** | **GSAP / Framer Motion** (Contextual) | Efek kedalaman multi-layer pada background hero & decorative cards. Selalu terapkan batas translasi halus (5–15%) dan **wajib** nonaktifkan pada body copy / form. |

#### A. Pedoman Framer Motion (`framer-motion` / `motion/react`)
- **Exit Transitions:** Selalu bungkus elemen kondisional dalam `<AnimatePresence mode="wait">` dengan `key` unik.
- **Variants & Staggering:** Definisikan `variants` di luar fungsi render dengan `staggerChildren` dan `delayChildren`.
- **Shared Element Morphing:** Gunakan `layoutId` untuk active tab indicators, expanding cards, dan modal triggers.
- **Layout Reflow:** Tambahkan prop `layout` dengan transisi spring (`stiffness: 350, damping: 25`) agar tata letak tidak melompat kaku saat item dihapus/ditambah.
- **Micro-Interactions:** Gunakan `whileHover={{ scale: 1.02, y: -2 }}` dan `whileTap={{ scale: 0.98 }}` + `cursor-pointer`.
- **Scroll Triggers:** Gunakan `whileInView={{ opacity: 1, y: 0 }}` dengan `viewport={{ once: true }}` atau `useScroll` + `useTransform`.

#### B. Pedoman GSAP & ScrollTrigger
- **Timeline Orchestration:** Gunakan `gsap.timeline()` untuk merangkai animasi masuk multi-elemen yang berurutan.
- **ScrollTrigger Scoping:** Selalu scope trigger ke kontainer section (`trigger: containerRef.current`), dan lakukan cleanup pada `useEffect` / unmount (`tl.kill()` atau `ScrollTrigger.getAll().forEach(t => t.kill())`).
- **Performance:** Animasikan hanya `x`, `y`, `scale`, `rotation`, dan `opacity` (menghindari layout thrashing `width`/`height`/`top`/`left`).

#### C. Pedoman Desain Parallax & Kedalaman Visual
- **Layering:** Pisahkan background dekoratif (kecepatan lambat: 0.05–0.1x), midground visual (kecepatan sedang: 0.2–0.3x), dan foreground konten (kecepatan normal: 1x).
- **Golden Rule:** Jangan pernah membuat teks bacaan utama (body text) atau elemen interaktif bergerak parallax secara terpisah karena menyebabkan disorientasi visual.
- **Containment:** Gunakan `overflow: hidden` pada kontainer parallax untuk mencegah horizontal scrollbar atau clipping anomali.

---

### 4. General Implementation & Accessibility Guardrails
- **Color & Typography:** Selalu terapkan token warna semantic (`--color-primary`, `--color-background`, dll.) dan pasangan Google Fonts dari hasil intelligence.
- **Modern Aesthetics:** Hindari tampilan MVP dasar/polos. Gunakan gradasi halus, soft shadows, glassmorphism/card berkelas, dan transisi mikro yang mulus.
- **Icons:** Gunakan SVG icons (Lucide, Heroicons, Phosphor), JANGAN PERNAH gunakan emoji sebagai ikon UI.
- **Accessibility & Contrast:** Rasio kontras teks minimal 4.5:1, ring `:focus-visible` jelas untuk navigasi keyboard, dan ARIA labels lengkap pada tombol icon-only.
- **Respect Reduced Motion:** Wajib menyediakan fallback instan atau subtle fade jika pengguna mengaktifkan `prefers-reduced-motion: reduce` (`useReducedMotion()` di Framer Motion atau `gsap.matchMedia`).
- **Responsive Fluidity:** Pastikan tata letak responsif dan rapi pada breakpoint 375px (mobile), 768px (tablet), 1024px (laptop), dan 1440px (desktop).
