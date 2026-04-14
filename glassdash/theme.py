"""Theme system for GlassDash."""

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class GlassTheme:
    colors: dict = field(
        default_factory=lambda: {
            "primary": "#e94560",
            "accent": "#4facfe",
            "success": "#10b981",
            "warning": "#f59e0b",
            "dark_yellow": "#d4a017",
            "purple": "#8b5cf6",
            "cyan": "#06b6d4",
            "bg_start": "#1a1a2e",
            "bg_end": "#0f3460",
            "glass_bg": "rgba(255,255,255,0.15)",
            "glass_border": "rgba(255,255,255,0.2)",
            "text": "#ffffff",
            "text_muted": "rgba(255,255,255,0.6)",
        }
    )
    fonts: dict = field(
        default_factory=lambda: {
            "family": "Inter, -apple-system, BlinkMacSystemFont, sans-serif",
            "kpi_value": 28,
            "kpi_label": 11,
            "chart_title": 14,
            "axis_label": 10,
        }
    )
    effects: dict = field(
        default_factory=lambda: {
            "blur": 12,
            "glow": True,
            "animation": True,
        }
    )

    def get_css(self) -> str:
        return f"""
        body {{
            font-family: {self.fonts["family"]};
            background: linear-gradient(135deg, {self.colors["bg_start"]}, {self.colors["bg_end"]});
            margin: 0;
            padding: 20px;
        }}
        .glass-card {{
            background: {self.colors["glass_bg"]};
            backdrop-filter: blur({self.effects["blur"]}px);
            -webkit-backdrop-filter: blur({self.effects["blur"]}px);
            border: 1px solid {self.colors["glass_border"]};
            border-radius: 16px;
            padding: 20px;
        }}
        .glass-kpi {{
            text-align: center;
        }}
        .glass-kpi-label {{
            font-size: {self.fonts["kpi_label"]}px;
            text-transform: uppercase;
            color: {self.colors["text_muted"]};
            margin-bottom: 8px;
        }}
        .glass-kpi-value {{
            font-size: {self.fonts["kpi_value"]}px;
            font-weight: 700;
            color: {self.colors["text"]};
        }}
        .glass-kpi-trend-up {{ color: {self.colors["success"]}; }}
        .glass-kpi-trend-down {{ color: {self.colors["primary"]}; }}
        .glass-chart-title {{
            font-size: {self.fonts["chart_title"]}px;
            font-weight: 500;
            color: {self.colors["text"]};
            margin-bottom: 16px;
        }}
        .glass-axis-label {{
            font-size: {self.fonts["axis_label"]}px;
            color: {self.colors["text_muted"]};
        }}
        """
