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
box_w = 2.3
arrow_gap_start = 3.5
arrow_gap_mid   = 7.9
mid_x_start = 4.8
down_x_start = 9.15

# ============================================================
# Tier backgrounds (dashed rectangles)
# ============================================================
fig.add_shape(type="rect", x0=0.15, x1=3.70, y0=0.60, y1=7.90,
              line=dict(color=C_BORDER_UP, width=2.2, dash="dash"),
              fillcolor=C_TIER_UP, layer="below")

fig.add_shape(type="rect", x0=4.35, x1=7.85, y0=0.60, y1=7.90,
              line=dict(color=C_BORDER_MID, width=2.2, dash="dash"),
              fillcolor=C_TIER_MID, layer="below")

fig.add_shape(type="rect", x0=8.60, x1=12.45, y0=0.30, y1=8.20,
              line=dict(color=C_BORDER_DN, width=2.2, dash="dash"),
              fillcolor=C_TIER_DOWN, layer="below")

# ============================================================
# Tier title labels (above each tier)
# ============================================================
fig.add_annotation(x=1.925, y=8.25, text="<b>上游：设备与材料</b>",
                   showarrow=False, font=dict(size=16, color=CLR[1]), xanchor="center")
fig.add_annotation(x=1.925, y=7.98, text="608亿 (16.9%)",
                   showarrow=False, font=dict(size=11, color="#888888"), xanchor="center")

fig.add_annotation(x=6.10, y=8.25, text="<b>中游：设计·制造·封测</b>",
                   showarrow=False, font=dict(size=16, color=CLR[4]), xanchor="center")
fig.add_annotation(x=6.10, y=7.98, text="~2,996亿 (83.1%)",
                   showarrow=False, font=dict(size=11, color="#888888"), xanchor="center")

fig.add_annotation(x=10.525, y=8.25, text="<b>下游：终端应用</b>",
                   showarrow=False, font=dict(size=16, color=CLR[7]), xanchor="center")
fig.add_annotation(x=10.525, y=7.98, text="广东占全国芯片消费市场60%",
                   showarrow=False, font=dict(size=11, color="#888888"), xanchor="center")

# ============================================================
# Sub-box definitions
# (x0, x1, y0, y1, fill_color, text_color, title, subtitle, detail_lines)
# ============================================================
upstream_boxes = [
    (0.70, 3.00, 5.60, 7.20, CLR[1], C_TEXT_WHITE,
     "半导体设备", "产值 300亿",
     ["光刻 / 刻蚀 / 薄膜沉积 / 量测",
      "代表：新凯来、中微半导体、迈为技术"]),
    (0.70, 3.00, 3.45, 5.05, CLR[2], C_TEXT_WHITE,
     "半导体材料", "产值 250亿",
     ["硅片 / 光刻胶 / 特气 / 靶材 / CMP",
      "代表：重投天科(SiC)、鼎泰芯源、广纳芯"]),
    (0.70, 3.00, 1.30, 2.90, CLR[3], C_TEXT_DARK,
     "零部件与耗材", "产值 58亿",
     ["石英件 / 密封件 / 射频电源 / 真空件",
      "代表：深圳、东莞供应商"]),
]

midstream_boxes = [
    (4.85, 7.15, 5.60, 7.20, CLR[0], C_TEXT_DARK,
     "IC设计", "产值 2,109亿（58.6%）▲25%",
     ["手机SoC / AI芯片 / IoT芯片 / FPGA",
      "代表：海思、中兴微、全志、汇顶、高云"]),
    (4.85, 7.15, 3.45, 5.05, CLR[4], C_TEXT_DARK,
     "晶圆制造", "产值 92亿（2.6%）▲102%",
     ["12英寸逻辑 / SiC / GaN / DRAM",
      "代表：粤芯、中芯深圳、增芯、鹏新旭"]),
    (4.85, 7.15, 1.30, 2.90, CLR[5], C_TEXT_DARK,
     "封装测试", "产值 795亿（22.1%）▲18%",
     ["先进封装 SiP / FC / WLCSP",
      "代表：气派科技、华天科技、佛山华芯"]),
]

downstream_boxes = [
    (9.20, 11.50, 6.50, 7.70, CLR[5], C_TEXT_DARK,
     "消费电子", "900亿",
     ["智能手机 / 无人机 / 智能家居",
      "代表：华为终端、OPPO、vivo、大疆"]),
    (9.20, 11.50, 5.15, 6.35, CLR[6], C_TEXT_DARK,
     "通信设备", "800亿",
     ["5G基站 / 光通信 / AI服务器",
      "代表：华为、中兴通讯"]),
    (9.20, 11.50, 3.80, 5.00, CLR[7], C_TEXT_WHITE,
     "汽车电子", "600亿",
     ["车规MCU / IGBT / SiC功率器件",
      "代表：比亚迪半导体、英诺赛科"]),
    (9.20, 11.50, 2.45, 3.65, CLR[5], C_TEXT_DARK,
     "人工智能", "400亿",
     ["AI加速卡 / NPU / GPU",
      "代表：华为昇腾、海思"]),
    (9.20, 11.50, 1.10, 2.30, CLR[6], C_TEXT_DARK,
     "工业电子", "300亿",
     ["工控 / 电力电子 / 医疗器械 / IoT",
      "代表：汇顶科技(IoT)、全志科技(工控)"]),
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
        top_y = y1
        inner_h = y1 - y0

        title_y = y0 + inner_h * 0.78
        fig.add_annotation(x=mid_x, y=title_y,
                           text=f"<b>{title}</b>",
                           showarrow=False,
                           font=dict(size=15, color=text_c),
                           xanchor="center", yanchor="middle")

        sub_y = y0 + inner_h * 0.55
        fig.add_annotation(x=mid_x, y=sub_y,
                           text=subtitle,
                           showarrow=False,
                           font=dict(size=10, color=text_c),
                           xanchor="center", yanchor="middle")

        line1_y = y0 + inner_h * 0.32
        fig.add_annotation(x=mid_x, y=line1_y,
                           text=details[0],
                           showarrow=False,
                           font=dict(size=9.5, color=text_c),
                           xanchor="center", yanchor="middle")

        line2_y = y0 + inner_h * 0.14
        fig.add_annotation(x=mid_x, y=line2_y,
                           text=details[1],
                           showarrow=False,
                           font=dict(size=9, color=text_c),
                           xanchor="center", yanchor="middle")

# ============================================================
# Inter-tier arrows (between boxes of adjacent tiers)
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
# Big flow arrow labels between tiers
# ============================================================
fig.add_annotation(x=4.10, y=7.55,
                   text="<b>供给 →</b>",
                   showarrow=False,
                   font=dict(size=12, color=CLR[1]), xanchor="center")

fig.add_annotation(x=8.30, y=7.55,
                   text="<b>供给 →</b>",
                   showarrow=False,
                   font=dict(size=12, color=CLR[5]), xanchor="center")

# ============================================================
# Data source footer
# ============================================================
fig.add_annotation(x=6.5, y=-0.20,
                   text="数据来源：深芯盟/深圳市半导体行业协会（2025.10）、中商产业研究院（2025.02）｜节点大小∝产值规模",
                   showarrow=False,
                   font=dict(size=9, color="#AAAAAA"), xanchor="center")

# ============================================================
# Layout
# ============================================================
fig.update_xaxes(range=[0, 13], showgrid=False, zeroline=False,
                 showticklabels=False, fixedrange=True)
fig.update_yaxes(range=[-0.5, 8.8], showgrid=False, zeroline=False,
                 showticklabels=False, fixedrange=True)

fig.update_layout(
    title=dict(
        text="<b>广东省集成电路产业链全景图</b>",
        font=dict(size=22, color=C_TEXT_DARK),
        x=0.5,
        y=0.97,
    ),
    paper_bgcolor=C_WHITE,
    plot_bgcolor=C_WHITE,
    width=1200,
    height=700,
    margin=dict(l=20, r=20, t=60, b=40),
)

out_html = IMG_DIR / "产业链全景图.html"
out_png  = IMG_DIR / "产业链全景图.png"
fig.write_html(str(out_html))
pio.write_image(fig, str(out_png), scale=2, width=1200, height=700)
print(f"Panorama OK: {out_png}")
