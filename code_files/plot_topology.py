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

C_BG    = "#FFFFFF"
C_TEXT  = "#1A1A1A"
C_EDGE  = "#C8CED4"
C_LABEL = "#1A1A1A"

nodes = [
    ("up_equip",  "半导体设备<br>300亿",            -1.0,  1.2,  300, CLR[1],
     "产品：光刻/刻蚀/薄膜沉积/量测/离子注入<br>代表：新凯来、中微半导体、迈为技术<br>区域：深圳、珠海"),
    ("up_mater",  "半导体材料<br>250亿",            -1.0,  0.0,  250, CLR[2],
     "产品：硅片/光刻胶/特气/靶材/CMP/湿电子化学品<br>代表：重投天科(SiC)、鼎泰芯源、广纳芯<br>区域：深圳、广州、珠海"),
    ("up_parts",  "零部件与耗材<br>58亿",           -1.0, -1.2,   58, CLR[3],
     "产品：石英件/密封件/射频电源/真空件<br>代表：深圳、东莞零散分布<br>区域：深圳、东莞"),

    ("mid_design", "IC设计<br>2,109亿 (58.6%)",      0.0,  1.2, 2109, CLR[4],
     "产品：手机SoC/AI芯片/IoT/FPGA/模拟<br>代表：海思、中兴微、全志、汇顶、高云<br>区域：深圳南山(全国重镇)、珠海<br>企业数：456家(深圳)"),
    ("mid_fab",    "晶圆制造<br>92亿 (2.6% ▲102%)",  0.0,  0.0,   92, CLR[5],
     "产品：12英寸逻辑/SiC/GaN/DRAM<br>代表：粤芯、中芯深圳、增芯、芯粤能、鹏新旭<br>区域：广州黄埔、深圳坪山<br>企业数：8家(深圳)"),
    ("mid_pack",   "封装测试<br>795亿 (22.1%)",       0.0, -1.2,  795, CLR[6],
     "产品：先进封装(SiP/FC/WLCSP)/传统封装<br>代表：气派科技、华天科技(深圳)、佛山华芯<br>区域：佛山、中山、深圳<br>企业数：82家(深圳)"),

    ("down_cons", "消费电子<br>900亿",    1.0,  1.6, 900, CLR[7],
     "产品：智能手机/无人机/智能家居/可穿戴<br>代表：华为终端、OPPO、vivo、大疆<br>区域：珠三角全域"),
    ("down_tele", "通信设备<br>800亿",    1.0,  0.8, 800, CLR[0],
     "产品：5G基站/光通信/AI服务器<br>代表：华为、中兴通讯<br>区域：深圳、东莞"),
    ("down_auto", "汽车电子<br>600亿",    1.0,  0.0, 600, CLR[1],
     "产品：车规MCU/IGBT/SiC功率器件<br>代表：比亚迪半导体、英诺赛科<br>区域：深圳、广州"),
    ("down_ai",   "人工智能<br>400亿",    1.0, -0.8, 400, CLR[6],
     "产品：AI加速卡/NPU/GPU/数据中心芯片<br>代表：华为昇腾、海思<br>区域：深圳、广州"),
    ("down_indu", "工业电子<br>300亿",    1.0, -1.6, 300, CLR[7],
     "产品：工控/电力电子/医疗器械/IoT<br>代表：汇顶科技(IoT)、全志科技(工控)<br>区域：深圳、广州、东莞"),
]

node_map = {n[0]: n for n in nodes}

edges = [
    ("up_equip", "mid_design"), ("up_equip", "mid_fab"), ("up_equip", "mid_pack"),
    ("up_mater", "mid_design"), ("up_mater", "mid_fab"), ("up_mater", "mid_pack"),
    ("up_parts", "mid_fab"),    ("up_parts", "mid_pack"),
    ("mid_design", "down_cons"), ("mid_design", "down_tele"),
    ("mid_design", "down_auto"), ("mid_design", "down_ai"), ("mid_design", "down_indu"),
    ("mid_fab",    "down_cons"), ("mid_fab",    "down_tele"),
    ("mid_fab",    "down_auto"), ("mid_fab",    "down_ai"), ("mid_fab",    "down_indu"),
    ("mid_pack",   "down_cons"), ("mid_pack",   "down_tele"),
    ("mid_pack",   "down_auto"), ("mid_pack",   "down_ai"), ("mid_pack",   "down_indu"),
]

traces = []

for src_id, tgt_id in edges:
    src, tgt = node_map[src_id], node_map[tgt_id]
    traces.append(go.Scatter(
        x=[src[2], tgt[2]],
        y=[src[3], tgt[3]],
        mode="lines",
        line=dict(color=C_EDGE, width=1.5),
        hoverinfo="none",
        showlegend=False,
    ))

min_val = min(n[4] for n in nodes)
max_val = max(n[4] for n in nodes)


def node_size(val):
    return 22 + (val - min_val) / (max_val - min_val) * 52


col_groups = [
    ("上游：设备与材料 (608亿 / 16.9%)",
     -1.0, ["up_equip", "up_mater", "up_parts"], CLR[1]),
    ("中游：设计·制造·封测 (~2,996亿 / 83.1%)",
     0.0, ["mid_design", "mid_fab", "mid_pack"], CLR[5]),
    ("下游：终端应用 (广东占全国芯片消费60%)",
     1.0, ["down_cons", "down_tele", "down_auto", "down_ai", "down_indu"], CLR[7]),
]

for label, col_x, col_ids, legend_color in col_groups:
    col_nodes = [node_map[nid] for nid in col_ids]
    xs = [n[2] for n in col_nodes]
    ys = [n[3] for n in col_nodes]
    sz = [node_size(n[4]) for n in col_nodes]
    cs = [n[5] for n in col_nodes]
    cd = [n[6] for n in col_nodes]

    traces.append(go.Scatter(
        x=xs, y=ys,
        mode="markers+text",
        marker=dict(
            size=sz,
            color=cs,
            line=dict(color=C_BG, width=2.5),
            opacity=0.94,
        ),
        text=[n[1] for n in col_nodes],
        textposition="middle center",
        textfont=dict(size=10, color=C_BG),
        customdata=cd,
        hovertemplate="<b>%{text}</b><br>%{customdata}<extra></extra>",
        name=label,
        showlegend=True,
        legendgroup=label,
    ))


def rgba(hex_color, alpha=0.05):
    r, g, b = int(hex_color[1:3], 16), int(hex_color[3:5], 16), int(hex_color[5:7], 16)
    return f"rgba({r},{g},{b},{alpha})"


shapes = [
    dict(type="rect", x0=-1.35, x1=-0.65, y0=-1.65, y1=1.65,
         fillcolor=rgba(CLR[1], 0.06),
         line=dict(color=rgba(CLR[1], 0.30), width=1, dash="dash"),
         layer="below"),
    dict(type="rect", x0=-0.35, x1=0.35, y0=-1.65, y1=1.65,
         fillcolor=rgba(CLR[5], 0.06),
         line=dict(color=rgba(CLR[5], 0.30), width=1, dash="dash"),
         layer="below"),
    dict(type="rect", x0=0.65, x1=1.35, y0=-2.05, y1=2.05,
         fillcolor=rgba(CLR[7], 0.06),
         line=dict(color=rgba(CLR[7], 0.30), width=1, dash="dash"),
         layer="below"),
]

fig = go.Figure(data=traces)
fig.update_layout(
    shapes=shapes,
    title=dict(
        text="<b>广东省集成电路产业链拓扑结构图</b><br>"
             "<sub>上游(蓝调·左) → 中游(过渡·中) → 下游(橙调·右) | "
             "圆圈大小∝产值规模 | 数据来源：深芯盟/深圳市半导体行业协会(2025.10)、中商产业研究院(2025.02)</sub>",
        font=dict(size=18, color=C_TEXT),
        x=0.5,
    ),
    xaxis=dict(range=[-1.6, 1.6], showgrid=False, zeroline=False, showticklabels=False, fixedrange=True),
    yaxis=dict(range=[-2.1, 2.1], showgrid=False, zeroline=False, showticklabels=False, fixedrange=True),
    paper_bgcolor=C_BG,
    plot_bgcolor=C_BG,
    height=850,
    width=1400,
    legend=dict(x=0.5, y=-0.10, xanchor="center", orientation="h", font=dict(size=11, color=C_TEXT)),
    margin=dict(l=40, r=40, t=110, b=90),
)

html_path = IMG_DIR / "产业链拓扑结构图.html"
png_path  = IMG_DIR / "产业链拓扑结构图.png"
fig.write_html(str(html_path))
pio.write_image(fig, str(png_path), scale=2, width=1400, height=850)
print(f"Topology OK: {png_path}")
