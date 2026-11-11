# Design System

## Colors

**Light Theme (Pure White / Dark Bronze / Onyx):**
- Primary: `#D4AF37` (Dark Bronze)
- Primary Hover: `#B5952F`
- Neutrals: `#D8D4CD` (BG), `#F2EFE9` (Surface), `#E8E5DE` (Surface Alt), `#C2BDB5` (Border), `#22201D` (Text), `#5E5952` (Text Muted), `#121212` (On Primary)
- Success: `#3f7d3c`
- Error: `#9c3b2e`

**Dark Theme:**
- Primary: `#D4AF37`
- Primary Hover: `#B5952F`
- Neutrals: `#121212` (BG), `#1E1E1E` (Surface), `#2A2A2A` (Surface Alt), `#333333` (Border), `#E8E8E8` (Text), `#A0A0A0` (Text Muted), `#121212` (On Primary)

## Typography

- Font Family: `system-ui, -apple-system, "Segoe UI", Roboto, sans-serif`
- Heading: Base font size, `line-height: 1.5`, bold (`700`)
- Subheading: Base font size, `line-height: 1.5`, bold (`700`)
- Body text: `1rem` base size, `line-height: 1.5`
- Small/Labels: `0.8rem` – `0.9rem`

## Spacing

- Scale used: 4px base grid
  - `xs`: 4px
  - `sm`: 8px
  - `md`: 16px
  - `lg`: 24px
  - `xl`: 32px

## Radius

- `md`: 8px
- `lg`: 14px

## Components

- [x] Primary button (`.button-primary`)
- [x] Secondary button (`.button-secondary`)
- [x] Text field (`.field input`, `.search`)
- [x] Card (`.card`, `.steps__card`)
- [x] Navbar (`.navbar`)
- [x] Avatar (`.avatar`, `.avatar--lg`, `.avatar-profile`)
- [x] Tags (`.tag`)
- [x] Hero section (`.hero`)
- [x] Footer (`.footer`)
- [x] Validation messages (`.error-field`, `.message-success`)

## States considered

- **Hover**: Buttons change background color, footer links change opacity.
- **Focus**: `:focus-visible` applies a 2px solid outline (`#B5952F`) with a 2px offset for accessibility.
- **Active**: Navigation links use `[aria-current="page"]` to highlight the active state.
- **Responsive**: Grid and layout adapt at `375px`, `768px` and `1200px` breakpoints.
- **Theme**: Automatic Dark Mode support based on OS preferences via `@media (prefers-color-scheme: dark)`.
