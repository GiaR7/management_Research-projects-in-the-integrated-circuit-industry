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
C_LINK = "#D8D8D8"

nodes = [
    "半导体设备", "半导体材料", "零部件与耗材",
    "IC设计", "晶圆制造", "封装测试",
    "消费电子", "通信设备", "汽车电子", "人工智能", "工业电子",
]

node_colors = [
    CLR[1], CLR[2], CLR[3],
    CLR[4], CLR[5], CLR[6],
    CLR[7], CLR[0], CLR[1], CLR[2],
]

node_details = [
    "光刻/刻蚀/薄膜沉积/量测/离子注入设备<br>代表：新凯来、中微半导体、迈为技术<br>区域：深圳、珠海",
    "硅片/光刻胶/电子特气/溅射靶材/CMP材料<br>代表：重投天科(SiC)、鼎泰芯源、广纳芯<br>区域：深圳、广州、珠海",
    "石英件/密封件/射频电源/真空件/陶瓷件<br>代表：深圳、东莞零散分布<br>区域：深圳、东莞",
    "产值 2,109亿（58.6%）增速~25%<br>手机SoC/AI芯片/IoT芯片/FPGA/模拟芯片<br>代表：海思、中兴微、全志、汇顶、高云<br>区域：深圳南山(全国重镇)、珠海",
    "产值 92亿（2.6%）增速102%<br>12英寸逻辑晶圆/SiC/GaN三代半<br>代表：粤芯、中芯深圳、增芯、芯粤能、鹏新旭<br>区域：广州黄埔、深圳坪山",
    "产值 795亿（22.1%）增速~18%<br>先进封装(SiP/FC/WLCSP)/传统封装<br>代表：气派科技、华天科技(深圳)、佛山华芯<br>区域：佛山、中山、深圳",
    "智能手机/无人机/智能家居/可穿戴<br>代表：华为终端、OPPO、vivo、大疆<br>区域：珠三角全域",
    "5G基站/光通信设备/AI服务器/路由器<br>代表：华为、中兴通讯<br>区域：深圳、东莞",
    "车规MCU/IGBT/SiC功率器件/智能驾驶芯片<br>代表：比亚迪半导体、英诺赛科<br>区域：深圳、广州",
    "AI加速卡/NPU/GPU/数据中心芯片<br>代表：华为昇腾、海思<br>区域：深圳、广州",
    "工业控制/电力电子/医疗器械/IoT<br>代表：汇顶科技(IoT)、全志科技(工控)<br>区域：深圳、广州、东莞",
]

links_up = [
    (0, 3, 50), (0, 4, 200), (0, 5, 50),
    (1, 3, 30), (1, 4, 200), (1, 5, 20),
    (2, 4, 48),  (2, 5, 10),
]

links_down = [
    (3, 6, 700),  (3, 7, 600),  (3, 8, 400),  (3, 9, 300),  (3, 10, 109),
    (4, 6, 20),   (4, 7, 25),   (4, 8, 30),   (4, 9, 12),   (4, 10, 5),
    (5, 6, 260),  (5, 7, 230),  (5, 8, 180),  (5, 9, 80),   (5, 10, 45),
]

all_links = links_up + links_down
sources = [l[0] for l in all_links]
targets = [l[1] for l in all_links]
values  = [l[2] for l in all_links]


def rgba(hex_color, alpha=0.22):
    r, g, b = int(hex_color[1:3], 16), int(hex_color[3:5], 16), int(hex_color[5:7], 16)
    return f"rgba({r},{g},{b},{alpha})"


link_colors = [rgba(node_colors[s]) for s in sources]

fig = go.Figure(data=[go.Sankey(
    arrangement="snap",
    node=dict(
        pad=25,
        thickness=25,
        line=dict(color=C_BG, width=1.5),
        label=[f"<b>{n}</b>" for n in nodes],
        color=node_colors,
        customdata=node_details,
        hovertemplate="%{customdata}<extra></extra>",
    ),
    link=dict(
        source=sources,
        target=targets,
        value=values,
        color=link_colors,
        hovertemplate="%{source.label} → %{target.label}<br>关联权重: %{value}<extra></extra>",
    ),
)])

fig.update_layout(
    title=dict(
        text="<b>广东省集成电路产业链桑基图</b><br>"
             "<sub>上游(蓝调) → 中游(过渡) → 下游(橙调) | 节点宽度∝产值规模 | "
             "数据来源：深芯盟/深圳市半导体行业协会(2025.10)、中商产业研究院(2025.02)</sub>",
        font=dict(size=17, color=C_TEXT),
        x=0.5,
    ),
    annotations=[
        dict(x=-0.08, y=1.07, xref="paper", yref="paper",
             text="<b>上游</b><br>设备与材料<br>608亿 (16.9%)",
             showarrow=False, font=dict(size=11, color=CLR[1]), align="center"),
        dict(x=0.42, y=1.07, xref="paper", yref="paper",
             text="<b>中游</b><br>设计·制造·封测<br>~2,996亿 (83.1%)",
             showarrow=False, font=dict(size=11, color=CLR[5]), align="center"),
        dict(x=0.84, y=1.07, xref="paper", yref="paper",
             text="<b>下游</b><br>终端应用<br>广东占全国芯片消费60%",
             showarrow=False, font=dict(size=11, color=CLR[7]), align="center"),
    ],
    font=dict(size=11, color=C_TEXT),
    paper_bgcolor=C_BG,
    plot_bgcolor=C_BG,
    height=750,
    width=1300,
    margin=dict(l=20, r=20, t=130, b=20),
)

html_path = IMG_DIR / "产业链桑基图.html"
png_path  = IMG_DIR / "产业链桑基图.png"
fig.write_html(str(html_path))
pio.write_image(fig, str(png_path), scale=2, width=1300, height=750)
print(f"Sankey OK: {png_path}")
