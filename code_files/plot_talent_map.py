"""
全国集成电路人才分布图 (中英文版)
使用 City/city.shp 对城市区块填色，不同颜色表示人才多少

数据来源：
- 《中国集成电路产业人才白皮书》
- 集微咨询《集成电路行业人才发展洞察报告（2024）》
- 芯思想研究院城市IC竞争力排行榜
- 各地政府官网公开数据
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.patheffects as pe
import matplotlib.font_manager as fm
import geopandas as gpd
from pathlib import Path
import numpy as np

# CJK font
CJK_FONT = "Arial Unicode MS"
plt.rcParams["font.family"] = CJK_FONT
from matplotlib.font_manager import findfont
print(f"Using font: {findfont(CJK_FONT)}")

PROJECT_ROOT = Path(__file__).resolve().parent.parent
IMG_DIR = PROJECT_ROOT / "img"
IMG_DIR.mkdir(exist_ok=True)

# ============================================================
# Color palette from img/color.JPG
# ============================================================
CLR = [
    "#51999F",  # dark teal
    "#4198AC",  # medium teal
    "#7BC0CD",  # light teal
    "#BFDFD2",  # pale sage
    "#DBCB92",  # warm gold
    "#ECB66C",  # warm amber
    "#EA9E58",  # warm orange
    "#ED8D6A",  # warm coral
]

C_BG       = "#FAFBFC"
C_NO_DATA  = "#E8E8E2"
C_BORDER   = "#FFFFFF"
C_TEXT     = "#2D2D2D"
C_WATER    = "#EAF2F7"

# ============================================================
# IC Talent data: shapefile city name -> talent (万人)
# ============================================================
city_talent = {
    "上海城区": 20.0,  "北京城区": 13.0,  "深圳市":   15.0,
    "无锡市":    7.0,  "成都市":    5.0,  "西安市":    4.5,
    "南京市":    4.0,  "武汉市":    3.5,  "杭州市":    3.0,
    "广州市":    3.0,  "合肥市":    2.5,  "苏州市":    2.5,
    "珠海市":    1.5,  "厦门市":    1.2,  "天津城区":  1.0,
    "重庆城区":  1.0,  "大连市":    1.0,  "济南市":    0.8,
    "青岛市":    0.6,  "长沙市":    0.6,  "福州市":    0.5,
    "沈阳市":    0.4,  "郑州市":    0.3,  "宁波市":    0.3,
    "石家庄市":  0.3,  "东莞市":    0.3,  "绍兴市":    0.2,
    "嘉兴市":    0.2,  "南通市":    0.2,  "惠州市":    0.2,
    "佛山市":    0.2,
}

# ============================================================
# Bins, labels, colors
# ============================================================
bins = [0, 0.01, 0.5, 1.5, 3, 7, 12, 22]
bin_colors = [C_NO_DATA, CLR[3], CLR[2], CLR[1], CLR[0], CLR[5], CLR[6], CLR[7]]

labels_cn = [
    "无数据",
    "萌芽 (<0.5万人)",
    "起步 (0.5~1.5万人)",
    "成长 (1.5~3万人)",
    "区域中心 (3~7万人)",
    "全国重镇 (7~12万人)",
    "产业龙头 (>12万人)",
]
labels_en = [
    "No data",
    "Emerging (<5K)",
    "Early (5K~15K)",
    "Growing (15K~30K)",
    "Regional Hub (30K~70K)",
    "National Base (70K~120K)",
    "Industry Leader (>120K)",
]

region_anns_cn = [
    ("长三角\nIC人才集群",  123.8, 33.5, 10),  # east of Shanghai, over sea
    ("珠三角\nIC人才集群",  111.8, 21.8, 10),  # west of PRD, over sea
    ("京津冀\nIC人才集群",  119.8, 41.5, 10),  # north of Bohai
    ("中西部\n新兴力量",    100.5, 32.5, 10),  # west side, clear area
]
region_anns_en = [
    ("Yangtze River Delta\nIC Talent Cluster",   123.8, 33.5, 10),
    ("Pearl River Delta\nIC Talent Cluster",     111.8, 21.8, 10),
    ("Beijing-Tianjin-Hebei\nIC Talent Cluster", 119.8, 41.5, 10),
    ("Central & Western\nEmerging Hubs",          100.5, 32.5, 10),
]

TITLE_CN = "全国集成电路产业人才分布图"
TITLE_EN = "National IC Industry Talent Distribution Map"

FOOTNOTE_CN = (
    "数据来源：《中国集成电路产业人才白皮书》、集微咨询（2024）、芯思想研究院、各地政府官网  |  "
    "从业人员数据含估算，非官方精确统计  |  "
    "制图时间：2026年5月  |  "
    "底图：City/city.shp"
)
FOOTNOTE_EN = (
    "Sources: China IC Industry Talent White Paper, JW Insights (2024), IC Insights Research, "
    "official government data  |  "
    "Talent figures include estimates  |  "
    "Generated: May 2026  |  "
    "Basemap: City/city.shp"
)

LEGEND_TITLE_CN = "IC产业人才规模"
LEGEND_TITLE_EN = "IC Talent Scale"

# ============================================================
# Load shapefile
# ============================================================
gdf = gpd.read_file(PROJECT_ROOT / "City" / "city.shp")
print(f"Loaded {len(gdf)} city polygons, CRS={gdf.crs}")

gdf["talent"] = gdf["ct_name"].map(city_talent).fillna(0)

talent_arr = gdf["talent"].values
bin_idx = np.digitize(talent_arr, bins[1:], right=True)
gdf["color"] = [bin_colors[i] for i in bin_idx]

# ============================================================
# City name mappings for labels
# ============================================================
city_name_cn = {
    "上海城区": "上海", "北京城区": "北京", "深圳市": "深圳",
    "无锡市": "无锡", "成都市": "成都", "西安市": "西安",
    "南京市": "南京", "武汉市": "武汉", "杭州市": "杭州",
    "广州市": "广州", "合肥市": "合肥", "苏州市": "苏州",
    "珠海市": "珠海", "厦门市": "厦门", "天津城区": "天津",
    "重庆城区": "重庆", "大连市": "大连", "济南市": "济南",
    "青岛市": "青岛", "长沙市": "长沙", "福州市": "福州",
    "沈阳市": "沈阳", "郑州市": "郑州",
}
city_name_en = {
    "上海城区": "Shanghai", "北京城区": "Beijing", "深圳市": "Shenzhen",
    "无锡市": "Wuxi", "成都市": "Chengdu", "西安市": "Xi'an",
    "南京市": "Nanjing", "武汉市": "Wuhan", "杭州市": "Hangzhou",
    "广州市": "Guangzhou", "合肥市": "Hefei", "苏州市": "Suzhou",
    "珠海市": "Zhuhai", "厦门市": "Xiamen", "天津城区": "Tianjin",
    "重庆城区": "Chongqing", "大连市": "Dalian", "济南市": "Jinan",
    "青岛市": "Qingdao", "长沙市": "Changsha", "福州市": "Fuzhou",
    "沈阳市": "Shenyang", "郑州市": "Zhengzhou",
}


def make_map(lang="cn"):
    """Generate a single map. lang='cn' for Chinese, 'en' for English."""
    labels = labels_cn if lang == "cn" else labels_en
    region_anns = region_anns_cn if lang == "cn" else region_anns_en
    title = TITLE_CN if lang == "cn" else TITLE_EN
    footnote = FOOTNOTE_CN if lang == "cn" else FOOTNOTE_EN
    legend_title = LEGEND_TITLE_CN if lang == "cn" else LEGEND_TITLE_EN
    city_name_map = city_name_cn if lang == "cn" else city_name_en

    fig, ax = plt.subplots(1, 1, figsize=(22, 18), facecolor=C_BG)
    ax.set_facecolor(C_WATER)

    # --- Draw all city polygons ---
    gdf.plot(ax=ax, color=gdf["color"], edgecolor=C_BORDER,
             linewidth=0.12, antialiased=True)

    # --- Highlight IC cities with thicker borders ---
    ic_cities = gdf[gdf["talent"] >= 0.3]
    ic_cities.plot(ax=ax, facecolor="none", edgecolor="#666666",
                   linewidth=0.5, antialiased=True)

    top_cities = gdf[gdf["talent"] >= 3]
    top_cities.plot(ax=ax, facecolor="none", edgecolor="#333333",
                    linewidth=0.9, antialiased=True)

    # --- City labels ---
    label_cities = gdf[gdf["talent"] >= 0.5].copy()
    label_cities["rep_point"] = label_cities.geometry.representative_point()

    for _, row in label_cities.iterrows():
        pt = row["rep_point"]
        t = row["talent"]
        ct_name = row["ct_name"]
        name = city_name_map.get(ct_name, ct_name)

        if t >= 10:
            fs, fw, fc = 12 if lang == "en" else 11.5, "bold", "#1A1A1A"
        elif t >= 3:
            fs, fw, fc = 10 if lang == "en" else 9.5, "bold", "#2D2D2D"
        else:
            fs, fw, fc = 7.5, "normal", "#444444"

        ax.annotate(
            name, (pt.x, pt.y),
            fontsize=fs, fontweight=fw, color=fc,
            ha="center", va="center",
            path_effects=[pe.withStroke(linewidth=2.5, foreground="white", alpha=0.7)],
        )

    # --- Region cluster labels (placed to avoid city name overlap) ---
    for text, x, y, fs in region_anns:
        ax.annotate(
            text, (x, y),
            fontsize=fs, color="#777777",
            ha="center", va="center",
            fontstyle="italic", alpha=0.65,
        )

    # --- Legend ---
    legend_patches = []
    for i, label in enumerate(labels):
        legend_patches.append(mpatches.Patch(
            facecolor=bin_colors[i],
            edgecolor="#BBBBBB" if i == 0 else "#999999",
            linewidth=0.3, label=label,
        ))
    legend = ax.legend(
        handles=legend_patches, title=legend_title,
        title_fontsize=12, fontsize=10,
        loc="lower left", bbox_to_anchor=(0.012, 0.012),
        framealpha=0.92, edgecolor="#CCCCCC", facecolor="white",
        ncol=2 if lang == "cn" else 4,
    )
    legend.get_title().set_fontweight("bold")

    # --- Title ---
    ax.set_title(title, fontsize=26, fontweight="bold",
                 color=C_TEXT, pad=18)

    # --- Footnote ---
    fig.text(0.5, 0.015, footnote, ha="center", va="center",
             fontsize=7.5, color="#AAAAAA")

    # --- Bounds ---
    ax.set_xlim(73, 135.5)
    ax.set_ylim(17, 54)
    ax.set_aspect("equal")
    ax.axis("off")

    plt.tight_layout(pad=1.5)

    # --- Save ---
    suffix = "cn" if lang == "cn" else "en"
    out_png = IMG_DIR / f"全国IC人才分布图_{suffix}.png"
    out_pdf = IMG_DIR / f"全国IC人才分布图_{suffix}.pdf"

    fig.savefig(str(out_png), dpi=200, bbox_inches="tight",
                facecolor=C_BG, edgecolor="none")
    print(f"PNG saved: {out_png}")
    fig.savefig(str(out_pdf), bbox_inches="tight",
                facecolor=C_BG, edgecolor="none")
    print(f"PDF saved: {out_pdf}")
    plt.close(fig)


# ============================================================
# Generate both versions
# ============================================================
make_map("cn")
make_map("en")
print("Done!")
