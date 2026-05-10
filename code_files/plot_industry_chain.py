"""
广东省集成电路产业链可视化图谱生成脚本
=============================================
使用 Plotly 生成两种图谱：
  1. 产业链桑基图 (Sankey) —— 展示上下游流动关系与产值占比
  2. 产业链旭日图 (Sunburst) —— 展示层级结构

输出文件：
  - img/产业链桑基图.html  （交互式 HTML）
  - img/产业链桑基图.png   （静态图片）
  - img/产业链旭日图.html
  - img/产业链旭日图.png

使用方法：
  cd /Users/langran/LocalFiles/课堂笔记/管理学/project_research_report
  source .venv/bin/activate
  python code_files/plot_industry_chain.py
"""

import plotly.graph_objects as go
import plotly.express as px
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
IMG_DIR = PROJECT_ROOT / "img"
IMG_DIR.mkdir(exist_ok=True)

# ============================================================
# 全局配色方案
# ============================================================
COLOR_UPSTREAM = "#FF6B6B"    # 上游 - 红色暖调
COLOR_UPSTREAM_2 = "#FF8E8E"
COLOR_UPSTREAM_3 = "#FFB3B3"
COLOR_MID_DESIGN = "#4ECDC4"   # 中游-设计 - 青绿
COLOR_MID_FAB = "#45B7D1"      # 中游-制造 - 蓝色
COLOR_MID_PACK = "#96CEB4"     # 中游-封测 - 绿色
COLOR_DOWN_1 = "#FFEAA7"       # 下游 - 暖黄
COLOR_DOWN_2 = "#FDCB6E"
COLOR_DOWN_3 = "#F39C12"
COLOR_DOWN_4 = "#E67E22"

# 深色版本（用于标签）
COLOR_LABEL = "#2C3E50"
COLOR_NODE_BG = "#F8F9FA"


def make_sankey():
    """
    产业链桑基图 (Sankey Diagram)
    展示从上游到下游的产值流动关系。
    每个环节的节点宽度代表其产值占比。
    """
    # ---- 节点定义 ----
    # 按从上到下、从左到右的顺序定义节点
    labels = [
        # 列0：上游（3个节点）
        "半导体设备",
        "半导体材料",
        "零部件与耗材",
        # 列1：中游-核心制造（3个节点）
        "IC设计",
        "晶圆制造",
        "封装测试",
        # 列2：下游-终端应用（4个节点）
        "消费电子",
        "通信设备",
        "汽车电子",
        "人工智能/AI",
    ]

    # ---- 流向定义 ----
    # (source_index, target_index, flow_value)
    # 值是相对权重，桑基图会自动归一化
    source = [
        # 上游 → 中游
        0, 0,  # 设备 → 设计, 制造
        1, 1,  # 材料 → 设计, 制造
        2, 2,  # 零部件 → 设计, 制造
        # 中游 → 下游
        3, 3, 3, 3,  # 设计 → 4个下游
        4, 4, 4, 4,  # 制造 → 4个下游
        5, 5, 5, 5,  # 封测 → 4个下游
    ]
    target = [
        # 上游 → 中游
        3, 4,  # 设备 → 设计(多), 制造(少)
        3, 4,  # 材料 → 设计, 制造
        3, 4,  # 零部件 → 设计, 制造
        # 中游 → 下游
        6, 7, 8, 9,  # 设计 → 消费电子, 通信, 汽车, AI
        6, 7, 8, 9,  # 制造 → 4个下游
        6, 7, 8, 9,  # 封测 → 4个下游
    ]
    value = [
        # 上游 → 中游（产值权重）
        300, 200,   # 设备
        200, 300,   # 材料
        60,  48,    # 零部件
        # 中游 → 下游（IC设计2109亿 → 各下游）
        800,  600,  400,  309,
        # 中游 → 下游（制造92亿 → 各下游，主要在汽车和AI）
        15,   20,   35,   22,
        # 中游 → 下游（封测795亿 → 各下游）
        280,  200,  200,  115,
    ]

    # ---- 节点颜色 ----
    node_colors = [
        COLOR_UPSTREAM, COLOR_UPSTREAM_2, COLOR_UPSTREAM_3,    # 上游
        COLOR_MID_DESIGN, COLOR_MID_FAB, COLOR_MID_PACK,        # 中游
        COLOR_DOWN_1, COLOR_DOWN_2, COLOR_DOWN_3, COLOR_DOWN_4, # 下游
    ]

    # ---- 链路颜色（从源节点取色，加透明度） ----
    link_colors = []
    for s in source:
        base = node_colors[s]
        # 转为 rgba 并降低透明度
        link_colors.append(base.replace("#", "rgba(") + "0.3)" if False else
                          f"rgba({int(base[1:3],16)},{int(base[3:5],16)},{int(base[5:7],16)},0.25)")

    # 重新计算链路颜色为 rgba 格式
    link_colors_rgba = []
    for s in source:
        r, g, b = int(node_colors[s][1:3], 16), int(node_colors[s][3:5], 16), int(node_colors[s][5:7], 16)
        link_colors_rgba.append(f"rgba({r},{g},{b},0.25)")

    # ---- 构建桑葚图 ----
    fig = go.Figure(data=[go.Sankey(
        arrangement="snap",
        node=dict(
            pad=20,
            thickness=30,
            line=dict(color="white", width=1),
            label=labels,
            color=node_colors,
            customdata=[
                "光刻/刻蚀/薄膜沉积/量测设备<br>新凯来、中微、迈为技术",
                "硅片/光刻胶/特气/靶材/CMP<br>重投天科、鼎泰芯源、广纳芯",
                "石英件/密封件/射频电源<br>深圳、东莞",
                "产值 2,109亿 (58.6%)<br>手机/AI/IoT/FPGA芯片<br>海思、中兴微、全志、汇顶",
                "产值 92亿 (2.6%) 增速102%<br>12英寸/SiC/GaN晶圆<br>粤芯、中芯深圳、增芯、鹏新旭",
                "产值 795亿 (22.1%)<br>先进封装SiP/FC<br>气派科技、华天、佛山华芯",
                "智能手机/无人机/智能家居<br>华为、OPPO、vivo、大疆",
                "5G基站/光通信/AI服务器<br>华为、中兴通讯",
                "车规MCU/IGBT/SiC功率器件<br>比亚迪半导体、英诺赛科",
                "AI加速卡/NPU/GPU<br>华为昇腾、海思",
            ],
            hovertemplate=(
                "<b>%{label}</b><br>"
                "%{customdata}<br>"
                "<extra></extra>"
            ),
        ),
        link=dict(
            source=source,
            target=target,
            value=value,
            color=link_colors_rgba,
            hovertemplate=(
                "%{source.label} → %{target.label}<br>"
                "产值关联权重: %{value}<br>"
                "<extra></extra>"
            ),
        ),
    )])

    # ---- 添加分组标注（用 annotation 模拟） ----
    annotations = [
        dict(x=-0.08, y=1.05, xref="paper", yref="paper",
             text="<b>🔺 上游：设备与材料</b><br>608亿 (16.9%)",
             showarrow=False, font=dict(size=13, color=COLOR_UPSTREAM)),
        dict(x=0.40, y=1.05, xref="paper", yref="paper",
             text="<b>🔵 中游：设计·制造·封测</b><br>~2,996亿 (83.1%)",
             showarrow=False, font=dict(size=13, color=COLOR_MID_DESIGN)),
        dict(x=0.82, y=1.05, xref="paper", yref="paper",
             text="<b>🔽 下游：终端应用</b><br>广东占全国芯片消费市场60%",
             showarrow=False, font=dict(size=13, color=COLOR_DOWN_3)),
    ]

    fig.update_layout(
        title=dict(
            text="<b>广东省集成电路产业链桑基图</b><br>"
                 "<sub>数据来源：深芯盟/深圳市半导体行业协会（2025.10）、中商产业研究院（2025.02）</sub>",
            font=dict(size=18),
            x=0.5,
        ),
        annotations=annotations,
        font=dict(size=12, color=COLOR_LABEL),
        paper_bgcolor="white",
        plot_bgcolor="white",
        height=700,
        width=1200,
        margin=dict(l=20, r=20, t=120, b=20),
    )

    return fig


def make_sunburst():
    """
    产业链旭日图 (Sunburst Chart)
    展示产业链的层级树形结构，从内到外逐层展开。
    """
    # 层级结构数据
    data = dict(
        ids=[
            # 根
            "root",
            # 一级：上中下游
            "upstream", "midstream", "downstream",
            # 二级：上游环节
            "up_equipment", "up_material", "up_parts",
            # 二级：中游环节
            "mid_design", "mid_fab", "mid_pack",
            # 二级：下游环节
            "down_consumer", "down_telecom", "down_auto", "down_ai",
            # 三级：代表企业（选部分）
            "eq_xklai", "eq_zwei",
            "mat_tianke", "mat_dingxin",
            "ds_haisi", "ds_zxwei", "ds_qzhi",
            "fab_yuexin", "fab_smic", "fab_zengxin",
            "pk_qipai", "pk_huatian",
            "con_huawei", "con_dji",
            "com_huawei", "com_zte",
            "auto_byd", "auto_innoscience",
            "ai_shengteng", "ai_haisi",
        ],
        labels=[
            # 根
            "广东省集成电路产业链",
            # 一级
            "上游：设备与材料\n(608亿 / 16.9%)",
            "中游：设计·制造·封测\n(~2,996亿 / 83.1%)",
            "下游：终端应用\n(占全国芯片消费60%)",
            # 二级：上游
            "半导体设备", "半导体材料", "零部件与耗材",
            # 二级：中游
            "IC设计\n(2,109亿)", "晶圆制造\n(92亿)", "封装测试\n(795亿)",
            # 二级：下游
            "消费电子", "通信设备", "汽车电子", "人工智能",
            # 三级：企业
            "新凯来", "中微半导体",
            "重投天科", "鼎泰芯源",
            "海思半导体", "中兴微电子", "全志科技",
            "粤芯半导体", "中芯国际(深圳)", "增芯科技",
            "气派科技", "华天科技(深圳)",
            "华为终端", "大疆",
            "华为(5G/AI服务器)", "中兴通讯",
            "比亚迪半导体", "英诺赛科",
            "华为昇腾", "海思(AI芯片)",
        ],
        parents=[
            # 根
            "",
            # 一级
            "root", "root", "root",
            # 二级：上游
            "upstream", "upstream", "upstream",
            # 二级：中游
            "midstream", "midstream", "midstream",
            # 二级：下游
            "downstream", "downstream", "downstream", "downstream",
            # 三级：上游企业
            "up_equipment", "up_equipment",
            "up_material", "up_material",
            # 三级：中游企业
            "mid_design", "mid_design", "mid_design",
            "mid_fab", "mid_fab", "mid_fab",
            "mid_pack", "mid_pack",
            # 三级：下游企业
            "down_consumer", "down_consumer",
            "down_telecom", "down_telecom",
            "down_auto", "down_auto",
            "down_ai", "down_ai",
        ],
        values=[
            # 根及一级（按产值比例缩放）
            3600,
            608, 2996, 3600,  # 上/中/下游
            # 上游
            300, 250, 58,
            # 中游
            2109, 92, 795,
            # 下游
            900, 800, 600, 300,
            # 企业（均分）
            150, 150,
            125, 125,
            700, 700, 700,
            35, 35, 22,
            400, 400,
            450, 450,
            400, 400,
            300, 300,
            150, 150,
        ],
    )

    # 颜色映射
    color_map = {
        "upstream": COLOR_UPSTREAM,
        "midstream": COLOR_MID_DESIGN,
        "downstream": COLOR_DOWN_1,
        "up_equipment": "#FF8A80",
        "up_material": "#FF5252",
        "up_parts": "#FF1744",
        "mid_design": "#1ABC9C",
        "mid_fab": "#3498DB",
        "mid_pack": "#2ECC71",
        "down_consumer": "#F9E79F",
        "down_telecom": "#F8C471",
        "down_auto": "#F0B27A",
        "down_ai": "#E59866",
    }

    def get_color(label_id):
        if label_id in color_map:
            return color_map[label_id]
        # 继承父节点颜色
        parent = data["parents"][data["ids"].index(label_id)] if label_id in data["ids"] else "root"
        while parent and parent not in color_map:
            if parent in data["ids"]:
                idx = data["ids"].index(parent)
                parent = data["parents"][idx] if idx < len(data["parents"]) else ""
            else:
                parent = ""
        return color_map.get(parent, "#BDC3C7")

    marker_colors = [get_color(id_) for id_ in data["ids"]]

    fig = go.Figure(go.Sunburst(
        ids=data["ids"],
        labels=data["labels"],
        parents=data["parents"],
        values=data["values"],
        branchvalues="total",
        marker=dict(
            colors=marker_colors,
            line=dict(color="white", width=1.5),
        ),
        textinfo="label",
        textfont=dict(size=11),
        insidetextorientation="radial",
        hovertemplate=(
            "<b>%{label}</b><br>"
            "产值/权重: %{value:.0f} 亿元<br>"
            "占父级比例: %{percentParent:.1%}<br>"
            "<extra></extra>"
        ),
        maxdepth=3,
    ))

    fig.update_layout(
        title=dict(
            text="<b>广东省集成电路产业链层级结构图</b><br>"
                 "<sub>内圈=产业层级 | 中圈=核心环节 | 外圈=代表企业</sub>",
            font=dict(size=18),
        ),
        paper_bgcolor="white",
        height=900,
        width=1100,
        margin=dict(l=10, r=10, t=80, b=10),
    )

    return fig


def main():
    print("=" * 56)
    print("  广东省集成电路产业链可视化图谱生成")
    print("=" * 56)

    # ---- 桑基图 ----
    print("\n[1/2] 生成桑基图 (Sankey)...")
    sankey_fig = make_sankey()

    html_path = IMG_DIR / "产业链桑基图.html"
    sankey_fig.write_html(html_path)
    print(f"  ✓ HTML 已保存: {html_path}")

    try:
        png_path = IMG_DIR / "产业链桑基图.png"
        sankey_fig.write_image(png_path, scale=2, width=1200, height=700)
        print(f"  ✓ PNG  已保存: {png_path}")
    except Exception as e:
        print(f"  [提示] PNG 导出需要 kaleido 库，跳过: {e}")
        print(f"         可运行: pip install kaleido")

    # ---- 旭日图 ----
    print("\n[2/2] 生成旭日图 (Sunburst)...")
    sunburst_fig = make_sunburst()

    html_path = IMG_DIR / "产业链旭日图.html"
    sunburst_fig.write_html(html_path)
    print(f"  ✓ HTML 已保存: {html_path}")

    try:
        png_path = IMG_DIR / "产业链旭日图.png"
        sunburst_fig.write_image(png_path, scale=2, width=1100, height=900)
        print(f"  ✓ PNG  已保存: {png_path}")
    except Exception as e:
        print(f"  [提示] PNG 导出需要 kaleido 库，跳过: {e}")
        print(f"         可运行: pip install kaleido")

    print(f"\n{'='*56}")
    print(f"  完成！生成的文件在: {IMG_DIR}")
    print(f"  用浏览器打开 .html 文件即可交互查看")
    print(f"{'='*56}")


if __name__ == "__main__":
    main()
