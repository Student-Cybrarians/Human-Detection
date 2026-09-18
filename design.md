# Design System — JARVIS

## Visual direction
Cinematic technical command center: dark surfaces, restrained cyan/green signal accents, thin instrument lines, glass-like panels, high information density, and motion that communicates sensing state.

## Design DNA
1. Color & typography — near-black navy background; cyan primary signal; green healthy state; amber warning; red alert; monospace telemetry paired with a clean sans-serif.
2. Spacing & layout — 8px base rhythm; wide central core; compact telemetry rails.
3. Shape & elevation — 1px luminous borders, 12–18px radii, layered translucent panels.
4. Visual effects — SVG rings, scan arcs, waveform bars, grid texture and CSS glow. No heavy WebGL dependency for the MVP.
5. Motion — state-driven pulse/rotation. Respect prefers-reduced-motion.

## Semantic colors
- signal: #59F3FF
- success: #5DFF9A
- warning: #FFC857
- danger: #FF5C7A
- background: #050914
- surface: #0B1220
- text: #E8F7FF
- muted: #7690A4

## UX principles
- Every animation maps to a sensing state.
- Connection state is always visible.
- Confidence is shown numerically and visually.
- Alerts require explicit acknowledgement.
- No decorative motion when the system is offline.
