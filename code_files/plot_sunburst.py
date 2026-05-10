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


add("root", "广东省<br>集成电路产业链", "", 6604, 0)

add("up",   "上游：设备与材料<br>(608亿 / 16.9%)",     "root", 608,  1)
add("mid",  "中游：设计·制造·封测<br>(2,996亿 / 83.1%)", "root", 2996, 1)
add("down", "下游：终端应用<br>(占全国消费 60%)",       "root", 3000, 1)

add("up_eq", "半导体设备<br>(300亿)", "up", 300, 2)
add("up_ma", "半导体材料<br>(250亿)", "up", 250, 2)
add("up_pa", "零部件与耗材<br>(58亿)", "up",  58, 2)

add("mid_de", "IC设计<br>(2,109亿)", "mid", 2109, 2)
add("mid_fa", "晶圆制造<br>(92亿)",   "mid",   92, 2)
add("mid_pk", "封装测试<br>(795亿)",  "mid",  795, 2)

add("dn_co", "消费电子<br>(900亿)", "down", 900, 2)
add("dn_te", "通信设备<br>(800亿)", "down", 800, 2)
add("dn_au", "汽车电子<br>(600亿)", "down", 600, 2)
add("dn_ai", "人工智能<br>(400亿)", "down", 400, 2)
add("dn_in", "工业电子<br>(300亿)", "down", 300, 2)

companies = [
    ("eq_xkl", "新凯来",       "up_eq", 100),
    ("eq_zhw", "中微半导体",   "up_eq", 100),
    ("eq_mw",  "迈为技术",     "up_eq", 100),
    ("ma_tk",  "重投天科(SiC)","up_ma",  90),
    ("ma_dx",  "鼎泰芯源",     "up_ma",  80),
    ("ma_gn",  "广纳芯",       "up_ma",  80),
    ("pa_sz",  "深圳供应商",   "up_pa",  30),
    ("pa_dg",  "东莞供应商",   "up_pa",  28),
    ("de_hs",  "海思半导体",    "mid_de", 422),
    ("de_zx",  "中兴微电子",    "mid_de", 422),
    ("de_qz",  "全志科技",      "mid_de", 422),
    ("de_hd",  "汇顶科技",      "mid_de", 422),
    ("de_gy",  "高云半导体",    "mid_de", 421),
    ("fa_yx",  "粤芯半导体",    "mid_fa", 25),
    ("fa_sm",  "中芯国际(深圳)","mid_fa", 25),
    ("fa_zx",  "增芯科技",      "mid_fa", 22),
    ("fa_qt",  "芯粤能/鹏新旭等","mid_fa", 20),
    ("pk_qp",  "气派科技",      "mid_pk", 300),
    ("pk_ht",  "华天科技(深圳)","mid_pk", 300),
    ("pk_fs",  "佛山华芯",      "mid_pk", 195),
    ("co_hw",  "华为终端",      "dn_co", 250),
    ("co_op",  "OPPO",          "dn_co", 220),
    ("co_vi",  "vivo",          "dn_co", 215),
    ("co_dj",  "大疆",          "dn_co", 215),
    ("te_hw",  "华为(5G/服务器)","dn_te", 450),
    ("te_zt",  "中兴通讯",      "dn_te", 350),
    ("au_by",  "比亚迪半导体",  "dn_au", 350),
    ("au_is",  "英诺赛科(GaN)", "dn_au", 250),
    ("ai_st",  "华为昇腾",      "dn_ai", 220),
    ("ai_hs",  "海思(AI芯片)",  "dn_ai", 180),
    ("in_hd",  "汇顶科技(IoT)", "dn_in", 150),
    ("in_qz",  "全志科技(工控)","dn_in", 150),
]
for id_, label, parent, value in companies:
    add(id_, label, parent, value, 3)

depth_color_idx = {
    0: 1,
    1: 2,
    2: 5,
    3: 7,
}


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
        "产值/权重: %{value:.0f} 亿元<br>"
        "占父级: %{percentParent:.1%}<br>"
        "占全局: %{percentRoot:.1%}<br>"
        "<extra></extra>"
    ),
    maxdepth=3,
))

fig.update_layout(
    title=dict(
        text="<b>广东省集成电路产业链层级结构图</b><br>"
             "<sub>内圈=产业层级  |  中圈=核心环节  |  外圈=代表企业  |  扇区面积∝产值  |  "
             "蓝调→上游  橙调→下游</sub>",
        font=dict(size=17, color=C_TEXT),
    ),
    paper_bgcolor=C_BG,
    height=950,
    width=1300,
    margin=dict(l=10, r=10, t=80, b=10),
)

html_path = IMG_DIR / "产业链旭日图.html"
png_path  = IMG_DIR / "产业链旭日图.png"
fig.write_html(str(html_path))
pio.write_image(fig, str(png_path), scale=2, width=1300, height=950)
print(f"Sunburst OK: {len(ids)} nodes -> {png_path}")
