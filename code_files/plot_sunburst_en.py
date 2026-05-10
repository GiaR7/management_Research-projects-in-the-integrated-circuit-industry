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

C_BG   = "#FFFFFF"
C_TEXT = "#1A1A1A"


ids = []
labels = []
parents = []
values = []
depths = []


def add(id_, label, parent, value, depth):
    ids.append(id_)
    labels.append(label)
    parents.append(parent)
    values.append(value)
    depths.append(depth)


# ---- Root (depth 0) ----
add("root", "Guangdong<br>IC Industry", "", 6604, 0)

# ---- Tier 1 (depth 1) ----
add("up",   "Upstream<br>Equipment & Materials<br>60.8B (16.9%)",   "root", 608,  1)
add("mid",  "Midstream<br>Design · Fab · Packaging<br>299.6B (83.1%)", "root", 2996, 1)
add("down", "Downstream<br>End Applications<br>60% of national demand", "root", 3000, 1)

# ---- Tier 2 (depth 2) ----
add("up_eq", "Equipment<br>30B",               "up", 300, 2)
add("up_ma", "Materials<br>25B",               "up", 250, 2)
add("up_pa", "Components &<br>Consumables 5.8B", "up",  58, 2)

add("mid_de", "IC Design<br>210.9B (58.6%)",  "mid", 2109, 2)
add("mid_fa", "Wafer Fab<br>9.2B (2.6%)",      "mid",   92, 2)
add("mid_pk", "Packaging & Test<br>79.5B (22.1%)", "mid",  795, 2)

add("dn_co", "Consumer<br>Electronics 90B",  "down", 900, 2)
add("dn_te", "Telecom<br>Equipment 80B",     "down", 800, 2)
add("dn_au", "Automotive<br>Electronics 60B", "down", 600, 2)
add("dn_ai", "AI &<br>Computing 40B",         "down", 400, 2)
add("dn_in", "Industrial<br>Electronics 30B", "down", 300, 2)

# ---- Tier 3 (depth 3) — representative enterprises ----
companies = [
    ("eq_xkl", "SiCarrier",           "up_eq", 100),
    ("eq_zhw", "AMEC",                "up_eq", 100),
    ("eq_mw",  "Maxwell Tech",        "up_eq", 100),
    ("ma_tk",  "CT-Tanke (SiC)",      "up_ma",  90),
    ("ma_dx",  "DingTai XinYuan",     "up_ma",  80),
    ("ma_gn",  "GuangNaXin",          "up_ma",  80),
    ("pa_sz",  "Shenzhen Suppliers",  "up_pa",  30),
    ("pa_dg",  "Dongguan Suppliers",  "up_pa",  28),
    ("de_hs",  "HiSilicon",           "mid_de", 422),
    ("de_zx",  "ZTE Micro",           "mid_de", 422),
    ("de_qz",  "Allwinner",           "mid_de", 422),
    ("de_hd",  "Goodix",              "mid_de", 422),
    ("de_gy",  "Gowin Semi",          "mid_de", 421),
    ("fa_yx",  "CanSemi",             "mid_fa", 25),
    ("fa_sm",  "SMIC (Shenzhen)",     "mid_fa", 25),
    ("fa_zx",  "ZengXin Tech",        "mid_fa", 22),
    ("fa_qt",  "XinYueNeng / PXX",    "mid_fa", 20),
    ("pk_qp",  "China Chippacking",   "mid_pk", 300),
    ("pk_ht",  "Huatian Tech (SZ)",   "mid_pk", 300),
    ("pk_fs",  "Foshan HuaXin",       "mid_pk", 195),
    ("co_hw",  "Huawei Consumer",     "dn_co", 250),
    ("co_op",  "OPPO",                "dn_co", 220),
    ("co_vi",  "vivo",                "dn_co", 215),
    ("co_dj",  "DJI",                 "dn_co", 215),
    ("te_hw",  "Huawei (5G/Server)",  "dn_te", 450),
    ("te_zt",  "ZTE",                 "dn_te", 350),
    ("au_by",  "BYD Semiconductor",   "dn_au", 350),
    ("au_is",  "Innoscience (GaN)",   "dn_au", 250),
    ("ai_st",  "Huawei Ascend",       "dn_ai", 220),
    ("ai_hs",  "HiSilicon (AI)",      "dn_ai", 180),
    ("in_hd",  "Goodix (IoT)",        "dn_in", 150),
    ("in_qz",  "Allwinner (Ind.)",    "dn_in", 150),
]
for id_, label, parent, value in companies:
    add(id_, label, parent, value, 3)

# ---- Color mapping (unchanged logic) ----
depth_color_idx = {0: 1, 1: 2, 2: 5, 3: 7}


def _depth_color(d, i_in_depth):
    base = depth_color_idx[d]
    return CLR[(base + i_in_depth) % len(CLR)]


depth_counters = {0: 0, 1: 0, 2: 0, 3: 0}
marker_colors = []
for i, d in enumerate(depths):
    idx = depth_counters[d]
    marker_colors.append(_depth_color(d, idx))
    depth_counters[d] += 1

assert len(ids) == len(labels) == len(parents) == len(values) == len(marker_colors)
assert parents[0] == ""
assert all(v > 0 for v in values)

# ---- Build figure ----
fig = go.Figure(go.Sunburst(
    ids=ids,
    labels=labels,
    parents=parents,
    values=values,
    branchvalues="total",
    marker=dict(
        colors=marker_colors,
        line=dict(color=C_BG, width=2.2),
    ),
    textfont=dict(size=12, color=C_TEXT, family="Arial, sans-serif"),
    insidetextorientation="auto",
    hovertemplate=(
        "<b>%{label}</b><br>"
        "Value / Weight: %{value:.0f}<br>"
        "Share of parent: %{percentParent:.1%}<br>"
        "Share of total: %{percentRoot:.1%}<br>"
        "<extra></extra>"
    ),
    maxdepth=3,
))

# ---- Layout ----
fig.update_layout(
    title=dict(
        text="<b>Guangdong Province Integrated Circuit Industry Chain Panorama (Sunburst Chart)</b><br>"
             "<sub>Sector area ∝ output value  |  "
             "Inner → Outer: Tiers → Segments → Representative enterprises  |  "
             "Blue = Upstream &nbsp; Orange = Downstream</sub>",
        font=dict(size=17, color=C_TEXT),
    ),
    paper_bgcolor=C_BG,
    height=950,
    width=1300,
    margin=dict(l=10, r=10, t=80, b=10),
)

# ---- Export ----
html_path = IMG_DIR / "产业链旭日图_EN.html"
png_path  = IMG_DIR / "产业链旭日图_EN.png"
fig.write_html(str(html_path))
pio.write_image(fig, str(png_path), scale=2, width=1300, height=950)
print(f"Sunburst EN OK: {len(ids)} nodes -> {png_path}")
