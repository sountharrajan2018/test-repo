# Design System

A small, dependency-free design system for this repo. Tokens live in
[`design-tokens.json`](design-tokens.json) and are exposed as CSS custom
properties in [`tokens.css`](tokens.css). Open
[`design-preview.html`](design-preview.html) to see every token in both themes.

## Theming

Three modes: **Light**, **Dark**, and **System** (default, follows the OS).

- `theme.js` is loaded synchronously in `<head>` and sets
  `<html data-theme="light|dark">` before first paint, so there is no flash.
  "System" removes the attribute and lets `prefers-color-scheme` decide.
- The choice is saved in `localStorage` under `theme`. Storage failures
  (private mode, blocked site data) fall back to System silently.
- Components use only semantic tokens (`--color-surface`, `--color-text`, …),
  never raw hex values, so a new component gets dark mode for free.
- Any `<fieldset class="theme-toggle">` of radio inputs named `theme` is wired
  up automatically.

## Color

Warm neutrals with a single deep-teal accent. The warm grey avoids the cold,
blue-tinted default and gives the page a paper-like feel; one accent keeps the
hierarchy obvious (the accent means "act here").

| Token | Light | Dark | Use |
|---|---|---|---|
| `bg` | `#f6f5f1` | `#121311` | Page background |
| `surface` | `#ffffff` | `#1b1c1a` | Cards |
| `surface-sunken` | `#efede7` | `#252622` | Wells, toggle track, hover fills |
| `text` | `#1c1b18` | `#ecebe6` | Primary text |
| `text-muted` | `#5f5b52` | `#a3a198` | Secondary text |
| `border` | `#e2dfd6` | `#2d2e2a` | Hairlines |
| `accent` | `#0f6e5c` | `#4fd1b5` | Primary action, eyebrow text |
| `on-accent` | `#ffffff` | `#0b1f1a` | Text on accent |

Dark mode is not an inversion: the accent is lightened to stay vivid on a dark
surface, and text on the accent flips to near-black to keep contrast.

**Contrast (WCAG 2.2):** every text pair passes AA (≥ 4.5:1).
Lowest: muted text on sunken surface, 5.78:1 light and 5.88:1 dark.
Body text is 17.2:1 light and 14.3:1 dark.

## Typography

- **Display:** a system old-style serif (Iowan / Palatino / Georgia) for
  headings. It gives the page some character with no web-font download.
- **Body:** the platform UI sans-serif for readability.
- **Mono:** for numbers that change (the counter), with tabular figures so the
  layout doesn't shift.
- Scale: `sm 14` · `base 16` · `lg 18` · `xl 24` · `2xl 36` (px).

## Spacing & shape

- 4px base grid: `4 8 12 16 24 32 48`. Nothing uses an off-scale value.
- Radius: `6` small controls, `10` buttons, `16` cards, `full` pills.
- Only cards get a shadow, a soft two-layer one; it is stronger in dark mode
  because shadows are harder to see on dark backgrounds.

## Motion

`120ms` for hover/press, `200ms` for theme changes, with one standard easing.
All durations drop to `0` under `prefers-reduced-motion`.

## Accessibility

- Buttons are ≥ 44px tall; toggle options are ≥ 32px with pill padding.
- Visible `:focus-visible` rings use the `focus` token in both themes.
- The theme switch is a real radio group (`fieldset` + `legend`), so it works
  with the keyboard (arrow keys) and screen readers.
- The counter sits in an `aria-live="polite"` region.
