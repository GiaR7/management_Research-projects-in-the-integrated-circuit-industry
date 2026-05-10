import plotly.graph_objects as go
import plotly.io as pio
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
IMG_DIR = PROJECT_ROOT / "img"
IMG_DIR.mkdir(exist_ok=True)

CLR = [
    "#BFDFD2",
    "#51999F",
    "#4198AC",
    "#7BC0CD",
    "#DBCB92",
    "#ECB66C",
    "#EA9E58",
    "#ED8D6A",
]

C_WHITE      = "#FFFFFF"
C_TEXT_DARK  = "#1A1A1A"
C_TEXT_WHITE = "#FFFFFF"
C_ARROW      = "#555555"
C_ARROW_LIGHT = "#999999"
C_TIER_UP    = "rgba(81,153,159,0.07)"
C_TIER_MID   = "rgba(219,203,146,0.07)"
C_TIER_DOWN  = "rgba(237,141,106,0.07)"
C_BORDER_UP  = "rgba(81,153,159,0.45)"
C_BORDER_MID = "rgba(219,203,146,0.55)"
C_BORDER_DN  = "rgba(237,141,106,0.45)"

fig = go.Figure()

x_range = [0, 13]
y_range = [0, 8.5]

# ============================================================
# Tier backgrounds (dashed rectangles)
# ============================================================
fig.add_shape(type="rect", x0=0.15, x1=3.70, y0=0.60, y1=7.90,
              line=dict(color=C_BORDER_UP, width=2.2, dash="dash"),
              fillcolor=C_TIER_UP, layer="below")

fig.add_shape(type="rect", x0=4.35, x1=7.85, y0=0.60, y1=7.90,
              line=dict(color=C_BORDER_MID, width=2.2, dash="dash"),
              fillcolor=C_TIER_MID, layer="below")

fig.add_shape(type="rect", x0=8.60, x1=12.45, y0=0.60, y1=7.85,
              line=dict(color=C_BORDER_DN, width=2.2, dash="dash"),
              fillcolor=C_TIER_DOWN, layer="below")

# ============================================================
# Tier title labels (above each tier)
# ============================================================
fig.add_annotation(x=1.925, y=8.25, text="<b>Upstream: Equipment & Materials</b>",
                   showarrow=False, font=dict(size=16, color=CLR[1]), xanchor="center")
fig.add_annotation(x=1.925, y=7.98, text="60.8B (16.9%)",
                   showarrow=False, font=dict(size=11, color="#888888"), xanchor="center")

fig.add_annotation(x=6.10, y=8.25, text="<b>Midstream: Design · Fab · Packaging & Test</b>",
                   showarrow=False, font=dict(size=16, color=CLR[4]), xanchor="center")
fig.add_annotation(x=6.10, y=7.98, text="~299.6B (83.1%)",
                   showarrow=False, font=dict(size=11, color="#888888"), xanchor="center")

fig.add_annotation(x=10.525, y=8.25, text="<b>Downstream: End Applications</b>",
                   showarrow=False, font=dict(size=16, color=CLR[7]), xanchor="center")
fig.add_annotation(x=10.525, y=7.98, text="60% of China's chip consumption",
                   showarrow=False, font=dict(size=11, color="#888888"), xanchor="center")

# ============================================================
# Sub-box definitions
# (x0, x1, y0, y1, fill_color, text_color, title, subtitle, detail_lines)
# ============================================================
upstream_boxes = [
    (0.70, 3.00, 5.60, 7.20, CLR[1], C_TEXT_WHITE,
     "Semiconductor Equipment", "Output 30B",
     ["Lithography / Etch / Thin-film / Metrology",
      "Repr: SiCarrier, AMEC, Maxwell Tech"]),
    (0.70, 3.00, 3.45, 5.05, CLR[2], C_TEXT_WHITE,
     "Semiconductor Materials", "Output 25B",
     ["Wafers / Photoresist / Spec. gases / CMP",
      "Repr: CT-Tanke (SiC), DingTai, GuangNaXin"]),
    (0.70, 3.00, 1.30, 2.90, CLR[3], C_TEXT_DARK,
     "Components & Consumables", "Output 5.8B",
     ["Quartz / Seals / RF power / Vacuum parts",
      "Repr: Shenzhen, Dongguan suppliers"]),
]

midstream_boxes = [
    (4.85, 7.15, 5.60, 7.20, CLR[0], C_TEXT_DARK,
     "IC Design", "Output 210.9B (58.6%)  ▲25%",
     ["Mobile SoC / AI chips / IoT / FPGA",
      "Repr: HiSilicon, ZTE Micro, Allwinner, Goodix"]),
    (4.85, 7.15, 3.45, 5.05, CLR[4], C_TEXT_DARK,
     "Wafer Fabrication", "Output 9.2B (2.6%)  ▲102%",
     ["12-inch logic / SiC / GaN / DRAM",
      "Repr: CanSemi, SMIC (SZ), ZengXin, PXX"]),
    (4.85, 7.15, 1.30, 2.90, CLR[5], C_TEXT_DARK,
     "Packaging & Testing", "Output 79.5B (22.1%)  ▲18%",
     ["Advanced pkg: SiP / FC / WLCSP",
      "Repr: Chippacking, Huatian (SZ), Foshan HuaXin"]),
]

downstream_boxes = [
    (9.20, 11.50, 6.50, 7.70, CLR[5], C_TEXT_DARK,
     "Consumer Electronics", "~90B",
     ["Smartphones / Drones / Smart home",
      "Repr: Huawei Consumer, OPPO, vivo, DJI"]),
    (9.20, 11.50, 5.15, 6.35, CLR[6], C_TEXT_DARK,
     "Telecom Equipment", "~80B",
     ["5G base stations / Optical / AI servers",
      "Repr: Huawei, ZTE"]),
    (9.20, 11.50, 3.80, 5.00, CLR[7], C_TEXT_WHITE,
     "Automotive Electronics", "~60B",
     ["Automotive MCU / IGBT / SiC power",
      "Repr: BYD Semiconductor, Innoscience (GaN)"]),
    (9.20, 11.50, 2.45, 3.65, CLR[5], C_TEXT_DARK,
     "AI & Computing", "~40B",
     ["AI accelerators / NPU / GPU",
      "Repr: Huawei Ascend, HiSilicon"]),
    (9.20, 11.50, 1.10, 2.30, CLR[6], C_TEXT_DARK,
     "Industrial Electronics", "~30B",
     ["Industrial control / Power / Medical / IoT",
      "Repr: Goodix (IoT), Allwinner (Industrial)"]),
]

all_boxes = [
    ("up", upstream_boxes),
    ("mid", midstream_boxes),
    ("down", downstream_boxes),
]

for tier_name, boxes in all_boxes:
    for (x0, x1, y0, y1, fill, text_c, title, subtitle, details) in boxes:
        fig.add_shape(type="rect", x0=x0, x1=x1, y0=y0, y1=y1,
                      line=dict(color=fill, width=2.2),
                      fillcolor=fill, opacity=0.92,
                      layer="above")
        mid_x = (x0 + x1) / 2
        inner_h = y1 - y0

        title_y = y0 + inner_h * 0.78
        fig.add_annotation(x=mid_x, y=title_y,
                           text=f"<b>{title}</b>",
                           showarrow=False,
                           font=dict(size=15, color=text_c, family="Arial, sans-serif"),
                           xanchor="center", yanchor="middle")

        sub_y = y0 + inner_h * 0.55
        fig.add_annotation(x=mid_x, y=sub_y,
                           text=subtitle,
                           showarrow=False,
                           font=dict(size=10, color=text_c, family="Arial, sans-serif"),
                           xanchor="center", yanchor="middle")

        line1_y = y0 + inner_h * 0.32
        fig.add_annotation(x=mid_x, y=line1_y,
                           text=details[0],
                           showarrow=False,
                           font=dict(size=9.5, color=text_c, family="Arial, sans-serif"),
                           xanchor="center", yanchor="middle")

        line2_y = y0 + inner_h * 0.14
        fig.add_annotation(x=mid_x, y=line2_y,
                           text=details[1],
                           showarrow=False,
                           font=dict(size=9, color=text_c, family="Arial, sans-serif"),
                           xanchor="center", yanchor="middle")

# ============================================================
# Inter-tier arrows
# ============================================================

def add_arrow(x0, y0, x1, y1, color=C_ARROW, width=1.5):
    fig.add_annotation(
        x=x1, y=y1,
        ax=x0, ay=y0,
        xref="x", yref="y",
        axref="x", ayref="y",
        showarrow=True,
        arrowhead=2,
        arrowsize=1.3,
        arrowwidth=width,
        arrowcolor=color,
        text="",
    )

up_centers = [(1.85, 7.20), (1.85, 5.05), (1.85, 2.90)]
mid_left   = [(4.85, 7.20), (4.85, 5.05), (4.85, 2.90)]

up_mid_pairs = [
    (up_centers[0], mid_left[1]),
    (up_centers[0], mid_left[2]),
    (up_centers[1], mid_left[1]),
    (up_centers[1], mid_left[2]),
    (up_centers[2], mid_left[1]),
    (up_centers[2], mid_left[2]),
]

for i, ((sx, sy), (tx, ty)) in enumerate(up_mid_pairs):
    margin = 2.95
    add_arrow(margin, sy, 4.85, ty, C_ARROW_LIGHT, 1.0)

mid_right  = [(7.15, 7.20), (7.15, 5.05), (7.15, 2.90)]

mid_down_pairs = [
    (mid_right[0], (9.20, 7.70)),
    (mid_right[0], (9.20, 6.35)),
    (mid_right[0], (9.20, 5.00)),
    (mid_right[0], (9.20, 3.65)),
    (mid_right[0], (9.20, 2.30)),
    (mid_right[1], (9.20, 7.70)),
    (mid_right[1], (9.20, 5.00)),
    (mid_right[1], (9.20, 3.65)),
    (mid_right[2], (9.20, 7.70)),
    (mid_right[2], (9.20, 6.35)),
    (mid_right[2], (9.20, 5.00)),
    (mid_right[2], (9.20, 3.65)),
    (mid_right[2], (9.20, 2.30)),
]

for (sx, sy), (tx, ty) in mid_down_pairs:
    add_arrow(7.15, sy, 9.20, ty, C_ARROW_LIGHT, 1.0)

# ============================================================
# Flow arrow labels between tiers
# ============================================================
fig.add_annotation(x=4.10, y=7.55,
                   text="<b>Supply →</b>",
                   showarrow=False,
                   font=dict(size=12, color=CLR[1], family="Arial, sans-serif"), xanchor="center")

fig.add_annotation(x=8.30, y=7.55,
                   text="<b>Supply →</b>",
                   showarrow=False,
                   font=dict(size=12, color=CLR[5], family="Arial, sans-serif"), xanchor="center")

# ============================================================
# Data source footer
# ============================================================
fig.add_annotation(x=6.5, y=-0.20,
                   text="Sources: SICA / SZSIA (2025.10), China Commerical Industry Research Inst. (2025.02)  |  Box size ∝ output value",
                   showarrow=False,
                   font=dict(size=9, color="#AAAAAA", family="Arial, sans-serif"), xanchor="center")

# ============================================================
# Layout
# ============================================================
fig.update_xaxes(range=[0, 13], showgrid=False, zeroline=False,
                 showticklabels=False, fixedrange=True)
fig.update_yaxes(range=[-0.5, 8.8], showgrid=False, zeroline=False,
                 showticklabels=False, fixedrange=True)

fig.update_layout(
    title=dict(
        text="<b>Guangdong Province Integrated Circuit Industry Chain Panorama</b>",
        font=dict(size=22, color=C_TEXT_DARK, family="Arial, sans-serif"),
        x=0.5,
        y=0.97,
    ),
    paper_bgcolor=C_WHITE,
    plot_bgcolor=C_WHITE,
    width=1200,
    height=700,
    margin=dict(l=20, r=20, t=60, b=40),
)

out_html = IMG_DIR / "产业链全景图_EN.html"
out_png  = IMG_DIR / "产业链全景图_EN.png"
fig.write_html(str(out_html))
pio.write_image(fig, str(out_png), scale=2, width=1200, height=700)
print(f"Panorama EN OK: {out_png}")
