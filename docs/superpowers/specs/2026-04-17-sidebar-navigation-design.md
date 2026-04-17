# GlassDash Multi-Page Navigation Spec

## Overview

Add a collapsible left sidebar to GlassDash demo that supports multiple dashboard pages (Workforce, Finance, Sales) with the glassmorphism theme.

## Architecture

- **Sidebar**: Fixed-position left panel with glassmorphic styling (blur, transparency, border)
- **Collapsed state**: 60px wide, icons only with tooltips
- **Expanded state**: 220px wide, icons + text labels
- **Toggle button**: Bottom of sidebar to collapse/expand
- **Page routing**: Dash `dcc.Location` + `html.Div` content swapping
- **Multi-page app**: Single Dash app with page state managed via callbacks

## Pages

1. **Workforce Statistics Dashboard** (current demo, rename "Workforce")
2. **Finance Statistics Dashboard** (new - placeholder charts)
3. **Sales Statistics Dashboard** (new - placeholder charts)

## Sidebar Design

```
Expanded (220px):          Collapsed (60px):
┌──────────────────┐      ┌────┐
│ 🏠 Workforce      │      │ 🏠│
│ 💰 Finance        │      │ 💰│
│ 📊 Sales          │      │ 📊│
│                   │      │   │
│                   │      │   │
│                   │      │   │
│              [─]  │      │[─]│
└──────────────────┘      └────┘
```

- Glass background: `rgba(255,255,255,0.15)` with blur
- Border: `1px solid rgba(255,255,255,0.2)`
- Active item: accent color highlight (`#4facfe`)
- Hover: slightly brighter background
- Icons: emoji or Dash-compatible icons
- Font: Inter, 14px labels
- Toggle button: centered at bottom, glass style

## CSS Classes

```css
.glass-sidebar { ... }
.glass-sidebar.collapsed { width: 60px; }
.glass-sidebar.expanded { width: 220px; }
.glass-sidebar-item { ... }
.glass-sidebar-item.active { ... }
.glass-sidebar-item:hover { ... }
.glass-sidebar-toggle { ... }
```

## Data Flow

```
User clicks sidebar item
    → Dash callback fires
    → Updates content container's children
    → Page component (WorkforcePage, FinancePage, SalesPage) is rendered
    → URL updates via dcc.Location
```

## Implementation Files

- `glassdash/demo/app.py` - Main demo app with multi-page structure
- `glassdash/assets/glass.css` - Add sidebar styles
- `glassdash/components/__init__.py` - (no change)
- `glassdash/demo/pages/` - New directory for page content

## No Placeholders

- Finance and Sales pages use placeholder data (realistic fake numbers)
- Each page self-contained with its own data and sections
- Follow same Section/chart pattern as Workforce page
