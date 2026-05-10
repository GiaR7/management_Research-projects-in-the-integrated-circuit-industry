"""
广东省集成电路产业数据抓取脚本
==============================================
功能：
  1. 抓取深圳市半导体行业协会会员名单
  2. 抓取广东省集成电路行业协会会员名单
  3. 整理产业链数据并输出为 CSV/Excel
  4. 生成产业链信息 Markdown 表格

使用方法：
  cd /Users/langran/LocalFiles/课堂笔记/管理学/project_research_report
  source .venv/bin/activate
  python code_files/scrape_ic_data.py

注意：
  - 部分网站可能有反爬机制，若抓取失败会自动降级为本地静态数据
  - 抓取间隔已设为 1-2 秒，避免对服务器造成压力
"""

import csv
import json
import os
import re
import sys
import time
from datetime import datetime
from pathlib import Path

import pandas as pd
import requests
from bs4 import BeautifulSoup

# ============================================================
# 配置区
# ============================================================

# 项目根目录（脚本位于 code_files/ 下，项目根为其父目录）
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
DATA_DIR.mkdir(exist_ok=True)

# 请求头，模拟正常浏览器访问
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/125.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
}

# 请求超时（秒）
TIMEOUT = 15
# 请求间隔（秒），避免对服务器造成压力
REQUEST_DELAY = 1.5


def safe_request(url: str, max_retries: int = 2) -> requests.Response | None:
    """带重试机制的 HTTP GET 请求"""
    for attempt in range(max_retries):
        try:
            resp = requests.get(url, headers=HEADERS, timeout=TIMEOUT)
            resp.raise_for_status()
            resp.encoding = resp.apparent_encoding  # 自动检测编码
            return resp
        except requests.RequestException as e:
            print(f"  [警告] 请求失败 (第{attempt+1}次): {url[:80]}... — {e}")
            if attempt < max_retries - 1:
                time.sleep(REQUEST_DELAY * 2)
    return None


# ============================================================
# 数据源 1：深圳市半导体行业协会会员列表
# 网站: https://www.szsia.com/?page_id=117
# ============================================================

def scrape_szsia_members() -> list[dict]:
    """
    抓取深圳市半导体行业协会会员名单。
    该页面会员数据由 JS 动态加载，BeautifulSoup 无法直接获取，
    因此直接使用本地整理的静态数据（来源：深芯盟报告/协会公开信息）。
    """
    url = "https://www.szsia.com/?page_id=117"
    print(f"\n[1/4] 正在获取深圳市半导体行业协会会员列表...")
    print(f"      URL: {url}")

    resp = safe_request(url)
    if resp is None:
        print("      [降级] 无法访问网站，使用本地静态数据")
        return get_static_shenzhen_members()

    soup = BeautifulSoup(resp.text, "html.parser")

    # 导航词黑名单：这些不是企业名，而是页面导航/菜单项
    nav_blacklist = {
        "首页", "关于", "联系", "新闻", "会员", "协会", "首页", "信息公开",
        "业务范围", "协会章程", "组织架构", "联系我们", "会员中心", "入会申请",
        "会员资讯", "会员名单", "会长单位", "副会长单位", "监理事单位",
        "专家智库咨询委员会", "专家委员会", "RISC-V生态专委会",
        "人工智能专委会", "专家入库", "咨询委员会", "更多", "详情", "查看",
        "下一页", "上一页", "返回", "搜索", "登录", "注册",
    }

    members = []

    # 方式1：查找表格
    tables = soup.find_all("table")
    for table in tables:
        rows = table.find_all("tr")
        for row in rows:
            cells = row.find_all(["td", "th"])
            if len(cells) >= 2:
                name = cells[0].get_text(strip=True)
                if name and len(name) > 1 and name not in nav_blacklist:
                    members.append({
                        "企业名称": name,
                        "来源": "深圳市半导体行业协会",
                        "抓取时间": datetime.now().strftime("%Y-%m-%d"),
                    })

    # 方式2：在文章内容区域内查找 <a> 或 <li> 标签
    if not members:
        # 优先在文章内容区域查找
        content_area = (
            soup.find("div", class_="entry-content")
            or soup.find("article")
            or soup.find("main")
            or soup.find("div", class_="content")
        )
        search_root = content_area if content_area else soup

        # 收集候选企业名
        candidates = []
        for tag in search_root.find_all(["a", "li", "p", "span", "div"]):
            text = tag.get_text(strip=True)
            if not text or len(text) < 4 or len(text) > 80:
                continue
            if text in nav_blacklist:
                continue
            # 排除导航词的一部分
            if any(nav in text for nav in [
                "委员会", "专委会", "入会", "申请", "中心",
                "首页", "关于", "联系", "新闻",
            ]):
                continue
            candidates.append(text)

        # 去重
        seen = set()
        for text in candidates:
            if text not in seen:
                seen.add(text)
                members.append({
                    "企业名称": text,
                    "来源": "深圳市半导体行业协会",
                    "抓取时间": datetime.now().strftime("%Y-%m-%d"),
                })

    # 质量检查：真实中国企业名几乎都包含"有限公司"或"股份"
    # 如果抓到的条目中不到 15% 是真实企业名，则判定为 JS 渲染页面
    company_pattern = re.compile(r'有限公司|股份有限公司|有限责任公司|集团')
    if members:
        company_like = sum(
            1 for m in members
            if company_pattern.search(m["企业名称"])
        )
        ratio = company_like / len(members)
        if ratio < 0.15:
            print(f"      [降级] 仅 {ratio:.0%} 条目包含公司注册名后缀（页面为 JS 动态渲染），使用本地静态数据")
            return get_static_shenzhen_members()

    if not members:
        print("      [降级] 未抓取到有效数据，使用本地静态数据")
        return get_static_shenzhen_members()

    print(f"      ✓ 抓取到 {len(members)} 条记录")
    return members


def get_static_shenzhen_members() -> list[dict]:
    """
    深圳市半导体行业已知代表企业静态数据。
    来源：深芯盟《深圳集成电路及国产半导体产业调研报告》(2025年10月)、
          深圳市半导体行业协会公开信息。
    当网页抓取失败时使用此兜底数据。
    """
    companies = [
        # IC 设计（深圳是中国 IC 设计重镇）
        ("海思半导体有限公司", "IC设计", "深圳", "民企/华为系"),
        ("中兴微电子技术有限公司", "IC设计", "深圳", "民企"),
        ("深圳市汇顶科技股份有限公司", "IC设计", "深圳", "民企"),
        ("深圳市必易微电子股份有限公司", "IC设计", "深圳", "民企"),
        ("深圳中科飞测科技股份有限公司", "半导体设备", "深圳", "民企"),
        ("峰岹科技（深圳）股份有限公司", "IC设计", "深圳", "民企"),
        ("深圳市江波龙电子股份有限公司", "存储/模组", "深圳", "民企"),
        ("深圳佰维存储科技股份有限公司", "存储/模组", "深圳", "民企"),
        ("深圳市德明利技术股份有限公司", "存储/模组", "深圳", "民企"),
        # 晶圆制造
        ("中芯国际集成电路制造（深圳）有限公司", "晶圆制造", "深圳", "外企/中芯国际"),
        ("润鹏半导体（深圳）有限公司", "晶圆制造", "深圳", "国企/华润微"),
        ("方正微电子有限公司", "晶圆制造/三代半", "深圳", "民企"),
        ("鹏新旭技术有限公司", "晶圆制造", "深圳", "民企"),
        ("鹏芯微集成电路制造有限公司", "晶圆制造", "深圳", "民企"),
        ("昇维旭技术有限公司", "DRAM制造", "深圳", "民企"),
        # 封测
        ("深圳气派科技股份有限公司", "封装测试", "深圳", "民企"),
        ("深圳市华天集成电路有限公司", "封装测试", "深圳", "民企/华天科技"),
        # 设备与材料
        ("深圳市新凯来技术有限公司", "半导体设备", "深圳", "民企"),
        ("深圳中微半导体设备有限公司", "半导体设备", "深圳", "民企"),
        ("重投天科半导体有限公司", "SiC衬底/外延", "深圳", "民企"),
        # 终端/IDM
        ("比亚迪半导体股份有限公司", "功率半导体/IDM", "深圳", "民企"),
    ]

    return [
        {
            "企业名称": name,
            "产业链环节": segment,
            "所在城市": city,
            "企业类型": etype,
            "来源": "静态数据-深芯盟报告/行业协会公开信息",
            "抓取时间": datetime.now().strftime("%Y-%m-%d"),
        }
        for name, segment, city, etype in companies
    ]


# ============================================================
# 数据源 2：广东省集成电路行业协会会员列表
# 网站: https://www.gdica.net.cn/
# ============================================================

def scrape_gdica_members() -> list[dict]:
    """
    抓取广东省集成电路行业协会会员名单。
    该页面同样可能由 JS 动态加载内容，BS4 解析可能失败。
    """
    url = "https://www.gdica.net.cn/"
    print(f"\n[2/4] 正在获取广东省集成电路行业协会会员列表...")
    print(f"      URL: {url}")

    resp = safe_request(url)
    if resp is None:
        print("      [降级] 无法访问网站，使用本地静态数据")
        return get_static_guangdong_members()

    soup = BeautifulSoup(resp.text, "html.parser")
    members = []

    # 在页面主体内容中查找企业名称
    main_content = (
        soup.find("div", class_="entry-content")
        or soup.find("article")
        or soup.find("main")
        or soup.find("div", class_="content")
        or soup
    )

    # 查找所有链接文字（企业名通常可点击）
    nav_pattern = re.compile(
        r'^(首页|关于|新闻|联系|更多|详情|查看|下一页|上一页|返回|'
        r'登录|注册|搜索|下载|版权所有|ICP|备案|首页|'
        r'\d+|\s*|©|网站|地图|友情|链接)$'
    )
    for a_tag in main_content.find_all("a"):
        text = a_tag.get_text(strip=True)
        if text and 4 <= len(text) <= 80 and not nav_pattern.match(text):
            if not any(kw in text for kw in ["委员会", "专委会", "申请"]):
                members.append({
                    "企业名称": text,
                    "来源": "广东省集成电路行业协会",
                    "抓取时间": datetime.now().strftime("%Y-%m-%d"),
                })

    # 质量检查：真实中国企业名几乎都包含"有限公司"或"股份"
    company_pattern = re.compile(r'有限公司|股份有限公司|有限责任公司|集团')
    if members:
        company_like = sum(
            1 for m in members
            if company_pattern.search(m["企业名称"])
        )
        if company_like / len(members) < 0.15:
            print(f"      [降级] 抓取质量不足（页面应为 JS 渲染），使用本地静态数据")
            return get_static_guangdong_members()

    if not members:
        print("      [降级] 未抓取到有效数据，使用本地静态数据")
        return get_static_guangdong_members()

    print(f"      ✓ 抓取到 {len(members)} 条记录")
    return members


# ============================================================
# Selenium 备用方案：适用于 JS 动态加载的页面
# 使用方法：python code_files/scrape_ic_data.py --selenium
# ============================================================

def scrape_szsia_with_selenium() -> list[dict]:
    """
    使用 Selenium + ChromeDriver 抓取深圳市半导体行业协会会员页面。
    该页面会员列表由 JavaScript 动态渲染，requests+BS4 无法直接获取。

    使用方法：
      python code_files/scrape_ic_data.py --selenium

    前提条件：
      - Chrome 浏览器已安装
      - webdriver-manager 会自动下载匹配的 ChromeDriver
    """
    print("\n[1/4-Selenium] 正在使用 Selenium 抓取深圳市半导体行业协会会员列表...")

    try:
        from selenium import webdriver
        from selenium.webdriver.chrome.service import Service
        from selenium.webdriver.chrome.options import Options
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        from webdriver_manager.chrome import ChromeDriverManager
    except ImportError as e:
        print(f"      [错误] 缺少依赖: {e}")
        print("      请运行: pip install selenium webdriver-manager")
        return get_static_shenzhen_members()

    options = Options()
    options.add_argument("--headless")  # 无头模式，不弹出浏览器窗口
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument(f"user-agent={HEADERS['User-Agent']}")

    driver = None
    try:
        print("      正在启动 ChromeDriver...")
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)

        url = "https://www.szsia.com/?page_id=117"
        print(f"      正在加载页面: {url}")
        driver.get(url)

        # 等待页面 JS 渲染完成
        wait = WebDriverWait(driver, 10)
        time.sleep(3)  # 额外等待确保 JS 执行完毕

        members = []

        # 尝试多种选择器定位会员列表
        selectors = [
            "table tr",                    # 表格行
            ".member-list li",             # 会员列表
            ".entry-content li",           # 文章内容列表
            ".entry-content a",            # 文章内容链接
            "article a",                   # article 内链接
        ]

        for selector in selectors:
            try:
                elements = driver.find_elements(By.CSS_SELECTOR, selector)
                for el in elements:
                    text = el.text.strip()
                    if text and 4 <= len(text) <= 80:
                        # 过滤导航词
                        nav_kw = ["首页", "关于", "联系", "新闻", "会员中心",
                                   "申请", "委员会", "专委会"]
                        if not any(kw in text for kw in nav_kw):
                            members.append({
                                "企业名称": text,
                                "来源": "深圳市半导体行业协会(Selenium)",
                                "抓取时间": datetime.now().strftime("%Y-%m-%d"),
                            })
                if members:
                    break
            except Exception:
                continue

        if not members:
            print("      [降级] Selenium 未找到会员列表，使用本地静态数据")
            return get_static_shenzhen_members()

        print(f"      ✓ Selenium 抓取到 {len(members)} 条记录")
        return members

    except Exception as e:
        print(f"      [降级] Selenium 抓取失败: {e}")
        print(f"      使用本地静态数据作为兜底")
        return get_static_shenzhen_members()

    finally:
        if driver:
            driver.quit()


def get_static_guangdong_members() -> list[dict]:
    """
    广东省（非深圳）集成电路行业已知代表企业静态数据。
    来源：中商产业研究院、公开新闻报道、行业协会公开信息。
    """
    companies = [
        # 广州
        ("粤芯半导体技术股份有限公司", "晶圆制造", "广州", "民企"),
        ("增芯科技有限公司", "晶圆制造", "广州", "民企"),
        ("芯粤能半导体有限公司", "SiC制造", "广州", "民企"),
        ("芯聚能半导体有限公司", "功率模块", "广州", "民企"),
        ("广纳芯科技有限公司", "5G滤波器/材料", "广州", "民企"),
        ("泰斗微电子科技有限公司", "IC设计/导航", "广州", "民企"),
        ("安凯微电子股份有限公司", "IC设计", "广州", "民企"),
        ("高云半导体科技股份有限公司", "FPGA/IC设计", "广州", "民企"),
        # 珠海
        ("全志科技股份有限公司", "IC设计", "珠海", "民企"),
        ("英诺赛科（珠海）科技有限公司", "GaN/IDM", "珠海", "民企"),
        ("炬芯科技股份有限公司", "IC设计", "珠海", "民企"),
        ("珠海艾派克微电子有限公司", "IC设计", "珠海", "民企"),
        ("鼎泰芯源晶体有限公司", "半导体材料", "珠海", "民企"),
        ("迈为技术（珠海）有限公司", "半导体设备", "珠海", "民企"),
        # 东莞
        ("天域半导体股份有限公司", "SiC外延", "东莞", "民企"),
        ("广东先导稀材股份有限公司", "半导体材料", "东莞", "民企"),
        # 佛山/中山/惠州
        ("佛山市国星光电股份有限公司", "LED/光电器件", "佛山", "国企/广晟"),
        ("佛山华芯微电子有限公司", "IC设计", "佛山", "民企"),
        ("中山市汉仁电子有限公司", "IC设计", "中山", "民企"),
        ("惠州市芯片科技发展有限公司", "IC设计", "惠州", "民企"),
    ]

    return [
        {
            "企业名称": name,
            "产业链环节": segment,
            "所在城市": city,
            "企业类型": etype,
            "来源": "静态数据-中商产业研究院/新闻报道/行业协会公开信息",
            "抓取时间": datetime.now().strftime("%Y-%m-%d"),
        }
        for name, segment, city, etype in companies
    ]


# ============================================================
# 数据源 3：广东省统计局 - 工业运行数据
# 网站: https://stats.gd.gov.cn/tjkx185/
# ============================================================

def scrape_gd_stats() -> dict:
    """
    尝试从广东省统计局获取集成电路相关月度/季度运行数据。
    统计局官网主要发布经济运行的简况新闻，而非结构化数据表格，
    因此本函数提取网页中的关键数字并整理为结构化字典。
    """
    url = "http://stats.gd.gov.cn/tjkx185/content/post_4887387.html"
    print(f"\n[3/4] 正在获取广东省统计局最新数据...")
    print(f"      URL: {url}")

    resp = safe_request(url)
    stats = {
        "数据来源": "广东省统计局",
        "更新时间": datetime.now().strftime("%Y-%m-%d"),
        "备注": "若抓取失败则为手动整理的静态数据",
    }

    if resp is None:
        print("      [降级] 使用本地静态统计数据")
        stats.update({
            "2024年集成电路产量(亿块)": "804",
            "2024年产量同比增长": "21.0%",
            "2024年半导体与集成电路产业营收(亿元)": "超3200",
            "2024年产业增加值增速": "17.9%",
            "2024年集成电路出口额(亿元)": "2785",
            "2024年集成电路出口增速": "15.2%",
            "2026年一季度产量增速": "43.1%",
        })
        return stats

    soup = BeautifulSoup(resp.text, "html.parser")
    text = soup.get_text()

    # 用正则提取"集成电路"相关的数字
    ic_matches = re.findall(
        r'集成电路[^。，；\d]*?(\d+\.?\d*%?)',
        text
    )
    if ic_matches:
        stats["提取到的集成电路相关数据"] = ic_matches

    print(f"      ✓ 获取到页面文本 {len(text)} 字符")
    return stats


# ============================================================
# 数据源 4：全国及各省市集成电路产量
# 网站: 国家统计局 / 各省统计局月度数据
# 说明: 此类数据通常以 PDF/Excel 形式发布，直接抓取门槛较高
# ============================================================

def get_ic_production_data() -> pd.DataFrame:
    """
    整理广东省及全国集成电路产量公开数据。
    来源：国家统计局月度数据、广东省统计局、行业报告。

    替代方案说明：
      若需要最新月度/季度产量数据，建议：
      1. 访问国家统计局官网 (stats.gov.cn) → 月度数据 → 工业产品产量
      2. 访问广东省统计局 (stats.gd.gov.cn) → 统计数据库
      3. 下载 CNKI/万方的统计年鉴
    """
    print(f"\n[4/4] 整理集成电路产量数据...")

    data = {
        "年份": [2019, 2020, 2021, 2022, 2023, 2024, 2025],
        "广东省集成电路产量(亿块)": [
            362.5, 427.3, 561.2, 516.8, 664.5, 804.0, None
        ],
        "广东省产量增速(%)": [
            None, 17.9, 31.3, -7.9, 28.6, 21.0, None
        ],
        "全国集成电路产量(亿块)": [
            2018.2, 2612.6, 3594.3, 3241.9, 3514.0, 4514.0, None
        ],
        "广东占全国比重(%)": [
            18.0, 16.4, 15.6, 15.9, 18.9, 17.8, None
        ],
        "广东产业营收(亿元)": [
            1200, 1700, 2100, 2300, 2700, 3200, 4000  # 2025 为目标值
        ],
        "数据来源": [
            "中商产业研究院",
            "中商产业研究院",
            "中商产业研究院",
            "广东省统计局",
            "广东省统计局/行业报告",
            "广东省统计局/深芯盟报告",
            "省政府行动计划目标",
        ],
    }

    df = pd.DataFrame(data)
    print(f"      ✓ 整理完毕，共 {len(df)} 行")
    return df


# ============================================================
# 产业链信息整理：基于搜索结果的静态 Markdown 表格
# ============================================================

def generate_industry_chain_report():
    """
    基于网络搜索结果和公开数据，生成产业链信息 Markdown 报告。
    此报告可直接嵌入《广东省集成电路产业研究报告》。
    所有数据均附带完整来源链接。
    """
    print(f"\n{'='*60}")
    print("生成产业链信息 Markdown 报告...")
    print(f"{'='*60}")

    # 集中定义所有来源链接，方便维护
    SRC = {
        "askci": "https://m.askci.com/news/chanye/20250211/104829273924210960325264.shtml",
        "seccw": "https://www.seccw.com/Document/detail/id/34188.html",
        "szsia": "https://www.szsia.com",
        "yicai": "https://www.21jingji.com/article/20251218/herald/9e946b753d39f6f0a8d6049254f740f7.html",
        "stats_q1": "http://stats.gd.gov.cn/tjkx185/content/post_4887387.html",
        "stats_industry": "http://stats.gd.gov.cn/fhygy/",
        "gdii": "http://gdii.gd.gov.cn/",
        "dfz": "http://dfz.gd.gov.cn/sqyl/gmjj/content/post_4886274.html",
        "southcn": "https://news.southcn.com/node_d75048eff3/5f6ba8926e.shtml",
        "chinanews": "https://www.chinanews.com/cj/2024/06-03/10227829.shtml",
        "ycwb": "https://money.ycwb.com/2024-06/03/content_52725623.htm",
        "zhuhai": "https://www.zhuhai-hitech.gov.cn/gxxw/gxdt/content/post_3832668.html",
        "ifeng": "https://gd.ifeng.com/c/8mSJ8ZwUP8s",
        "dayoo": "https://news.dayoo.com/guangzhou/202502/20/139995_54789207.htm",
        "szsica": "https://www.szsica.com/zcyd/87",
        "gzsia": "http://www.gzsia.net.cn/cybg",
        "gztjj": "https://tjj.gz.gov.cn/datav/admin/home/ndsj/",
        "gippc": "https://www.gippc.com.cn/ippc/zscqxxts/202208/",
        "gdica": "https://www.gdica.net.cn/",
        "stockstar": "https://wap.stockstar.com/detail/IG2022090600002689",
        "gdii_spe1": "https://gdii.gd.gov.cn/zwgk/tzgg1011/content/post_4856034.html",
        "gdii_spe2": "https://gdii.gd.gov.cn/zwgk/tzgg1011/content/post_4851686.html",
    }

    report = f"""## 广东省集成电路产业链信息整理

> **数据来源：**
> - 中商产业研究院《2025年广东半导体与集成电路产业链全景图谱》（2025-02-11）
>   [{SRC['askci']}]({SRC['askci']})
> - 深芯盟/深圳市半导体行业协会《深圳集成电路及国产半导体产业调研报告》（2025-10月发布）
>   [{SRC['seccw']}]({SRC['seccw']}) | 协会官网: [{SRC['szsia']}]({SRC['szsia']})
> - 南方财经全媒体集团/21世纪经济报道《从买家到卖家，广东"芯"跳加速何以实现？》（2025-12-18）
>   [{SRC['yicai']}]({SRC['yicai']})
> - 广东省统计局工业运行简况（2026年一季度）
>   [{SRC['stats_q1']}]({SRC['stats_q1']})
> - 《广东省培育半导体及集成电路战略性新兴产业集群行动计划（2023-2025年）》（广东省工信厅）
>   [{SRC['gdii']}]({SRC['gdii']})
> - 广东省情网《战略性新兴产业》
>   [{SRC['dfz']}]({SRC['dfz']})
>
> ⚠ 部分 2026年数据为预测值，具体标注以"预计/估算/目标"字样标出。

---

### 一、产业链上下游分布

#### 1.1 产业链全景

| 产业链层级 | 主要环节 | 代表产品/技术 | 区域布局 | 代表企业 |
|-----------|---------|-------------|---------|---------|
| **上游：设备与材料** | 半导体设备 | 光刻机、刻蚀机、薄膜沉积、量测设备 | 深圳、珠海 | 新凯来、中微半导体、迈为技术 |
| | 半导体材料 | 硅片、光刻胶、电子特气、靶材、CMP材料 | 深圳、广州、珠海 | 重投天科(SiC衬底)、鼎泰芯源、广纳芯 |
| | 零部件与耗材 | 石英件、密封件、射频电源 | 深圳、东莞 | — |
| **中游：设计·制造·封测** | IC设计 | 手机芯片、AI芯片、IoT芯片、FPGA | 深圳南山(全国重镇)、珠海 | 海思半导体、中兴微电子、全志科技、汇顶科技、高云半导体 |
| | 晶圆制造 | 12英寸晶圆、SiC/GaN三代半 | 广州黄埔、深圳坪山 | 粤芯半导体、中芯深圳、增芯科技、芯粤能、鹏新旭、方正微电子 |
| | 封装测试 | 先进封装(SiP/FC)、传统封装 | 佛山、中山、深圳 | 气派科技、华天科技(深圳)、佛山华芯 |
| **下游：终端应用** | 消费电子 | 智能手机、无人机、智能家居 | 珠三角全域 | 华为、OPPO、vivo、大疆 |
| | 通信设备 | 5G基站、光通信、AI服务器 | 深圳、东莞 | 华为、中兴通讯 |
| | 汽车电子 | 车规MCU、IGBT、SiC功率器件 | 深圳、广州 | 比亚迪半导体、英诺赛科 |
| | 人工智能 | AI加速卡、NPU、GPU | 深圳、广州 | 华为昇腾、海思 |

> **来源：** 中商产业研究院《2025年广东半导体与集成电路产业链全景图谱》
> [{SRC['askci']}]({SRC['askci']})

#### 1.2 中国60%芯片应用市场在珠三角

广东省是全球最大的电子信息产品制造基地，集成电路进口额常年占全国约**40%**，
同时60%的芯片应用市场集中在珠三角地区。"从买家到卖家"的转型是广东省"强芯工程"的核心目标。

> **来源：** 南方财经/21世纪经济报道（2025-12-18）
> [{SRC['yicai']}]({SRC['yicai']})

---

### 二、核心环节产值与企业数量占比

#### 2.1 产业链各环节产值分布（2024年，总营收约3,600亿元）

| 产业链环节 | 产值（亿元） | 占比（%） | 同比增速 | 特征说明 |
|-----------|-------------|----------|---------|---------|
| **IC设计业** | 2,109 | 58.6% | ~25% | 传统优势环节，全国领先，深圳南山为全国IC设计重镇 |
| **封测业** | 795 | 22.1% | ~18% | 佛山、中山建有封测产业集群 |
| **装备与材料业** | 608 | 16.9% | ~15% | 设备国产化替代加速 |
| **晶圆制造业** | 92 | 2.6% | **102%** | 近年增长最快环节，多个12英寸线在建/量产 |
| **合计** | **~3,600** | **100%** | **~22%** | 产业链结构正从"偏科设计"转向"设计-制造-封测"铁三角 |

> **来源：** 深芯盟/深圳市半导体行业协会《深圳集成电路产业发展报告》（2025年10月发布，于2025中国（深圳）集成电路峰会公开）
> [{SRC['seccw']}]({SRC['seccw']})
>
> 注：深芯盟报告口径为3,600亿元；中商产业研究院口径为"超3,200亿元"。差异可能来自统计范围不同。

#### 2.2 核心环节企业数量分布（深圳市数据，2024年，共727家）

| 产业链环节 | 企业数量（家） | 占比（%） | 较上年变化 |
|-----------|-------------|----------|----------|
| IC设计 | 456 | 62.7% | 数量最多，占比略降 |
| 设备及零部件 | 133 | 18.3% | 快速增长 |
| 封装测试 | 82 | 11.3% | 稳步增长 |
| 材料 | 48 | 6.6% | 稳步增长 |
| 晶圆制造 | 8 | 1.1% | 数量少但单个投资规模大 |
| **合计** | **727** | **100%** | — |

> **来源：** 深芯盟/深圳市半导体行业协会《深圳集成电路产业发展报告》（2025年10月发布）
> [{SRC['seccw']}]({SRC['seccw']})
>
> 注：深圳占广东省IC产业总营收约79%，按此推算全省IC企业总数约为**900-1,000家**（含广州、珠海、东莞、佛山、中山等地）。

#### 2.3 研发/生产/销售 环节结构

| 功能环节 | 涉及产业链位置 | 产值占比估算 | 企业集中领域 |
|---------|-------------|------------|------------|
| **研发（设计）** | IC设计 + 材料研发 + 设备研发 | ~65% | 深圳（IC设计）、广州（材料研发）、珠海（IC设计） |
| **生产（制造+封测）** | 晶圆制造 + 封装测试 + 材料生产 | ~25% | 广州（晶圆制造）、佛山/中山（封测）、深圳（三代半） |
| **销售** | 全链条 | ~10% | 深圳（总部经济）、广州（商贸中心） |

> 注：研发/生产/销售占比为基于上述产业链环节数据推算的估算值。

---

### 三、企业类型分布（国企/民企/外企）

#### 3.1 关键说明

**⚠ 目前公开的统计年鉴和行业报告中，未披露广东省集成电路产业按所有制（国企/民企/外企）划分的精确企业数量与产值占比数据。** 下表是基于公开代表企业信息整理的结构化估算，标注为"估算"的项目请在使用时注明数据局限性。

**建议精确数据获取途径：**
1. 《广东统计年鉴2025》"高技术制造业"章节，查阅按登记注册类型分组的细分数据 — [{SRC['stats_q1'].rsplit('/', 1)[0]}](http://stats.gd.gov.cn)
2. 中国半导体行业协会（CSIA）年度产业报告
3. 深芯盟/深圳市半导体行业协会完整版年度报告（当前仅公开摘要） — [{SRC['szsia']}]({SRC['szsia']})

#### 3.2 企业类型分布估算

| 企业类型 | 估算企业数量占比 | 估算产值占比 | 主要分布领域 | 代表企业 |
|---------|---------------|-----------|------------|---------|
| **民营企业** | ~75-80% | ~55-60% | IC设计、设备、材料、封测 | 海思半导体、中兴微电子、粤芯半导体、比亚迪半导体、全志科技、汇顶科技、天域半导体、增芯科技、鹏新旭、高云半导体 |
| **国有企业/国有控股** | ~10-15% | ~20-25% | 晶圆制造、关键材料 | 华润微(润鹏半导体)、广晟集团(国星光电)、中国电子(部分子公司)、方正微电子 |
| **外资/合资企业** | ~5-10% | ~15-20% | 晶圆制造、高端封测、设备 | 中芯国际(深圳)、英诺赛科(珠海)、部分封测代工厂 |
| **合计** | **~100%** | **~100%** | — | — |

> **推算逻辑说明：**
> - **民营企业占比高**：广东省尤其是深圳的IC设计产业全国领先，而IC设计行业以民营企业为主体（海思、中兴微、汇顶等），IC设计产值占全省IC总产值的58.6%；
> - **国企在制造端占比较高**：晶圆制造单个项目投资大（百亿级），国有资本参与度高（华润微、粤芯亦有国资背景）；
> - **外企占比相对低**：受限于贸易管制和技术封锁，外资在华/在粤集成电路制造布局有限。
>
> 本估算交叉参考了证券之星《2022年广东省集成电路企业大数据全景分析》的企业竞争格局数据：
> [{SRC['stockstar']}]({SRC['stockstar']})

#### 3.3 代表企业按类型细分

| 企业名称 | 企业类型 | 产业链环节 | 所在城市 | 2024年营收或估值参考 |
|---------|---------|-----------|---------|-------------------|
| 海思半导体 | 民企 | IC设计 | 深圳 | 未公开(华为体系内) |
| 中兴微电子 | 民企 | IC设计 | 深圳 | 未公开(中兴体系内) |
| 粤芯半导体 | 民企(含国资背景) | 晶圆制造 | 广州 | 估值约160亿元，拟A股上市 |
| 比亚迪半导体 | 民企 | 功率半导体/IDM | 深圳 | 百亿级(比亚迪体系) |
| 中芯国际(深圳) | 外资/合资 | 晶圆制造 | 深圳 | 中芯国际体系内 |
| 润鹏半导体 | 国企/华润微 | 晶圆制造 | 深圳 | 十二英寸线在建 |
| 全志科技 | 民企 | IC设计 | 珠海 | 上市公司 |
| 汇顶科技 | 民企 | IC设计 | 深圳 | 上市公司 |
| 天域半导体 | 民企 | SiC外延 | 东莞 | 拟港股上市 |
| 英诺赛科 | 民企/外资 | GaN/IDM | 珠海 | 港股上市公司 |
| 国星光电 | 国企/广晟集团 | LED/光电器件 | 佛山 | 上市公司 |
| 气派科技 | 民企 | 封装测试 | 深圳 | 上市公司 |

> **来源：** 各企业上市公司公告/招股书、中商产业研究院《2025年广东半导体与集成电路产业链全景图谱》
> [{SRC['askci']}]({SRC['askci']})

---

### 四、产业区域布局（"3+N"格局）

| 城市 | 定位 | 产业规模参考 | 重点产业园区 | 核心特征 |
|------|------|-----------|------------|---------|
| **深圳** | 绝对核心 | 营收2,839.6亿元(占全省79%)，企业727家 | 坪山集成电路产业园、南山科技园 | 全产业链优势，IC设计全国前三，发力晶圆制造 |
| **广州** | 核心城市 | 黄埔区集聚企业超150家 | 广州开发区(黄埔)、增城开发区、南沙新区 | 粤芯半导体所在地，"一核两极多点"布局 |
| **珠海** | 核心城市 | IC设计珠三角第二，高新区规上232亿元 | 珠海高新区半导体与集成电路产业园(省级特色产业园) | 化合物半导体"五料俱全"(GaN/SiC/InP/GaAs/GaSb) |
| **东莞** | 协同发展 | — | 松山湖高新区 | 封装测试、第三代半导体(SiC外延) |
| **佛山** | 协同发展 | — | 佛山高新区 | 封测产业集群、LED光电器件 |
| **中山** | 协同发展 | — | 火炬开发区(省级特色产业园) | 集成电路及电子元器件 |
| **惠州** | 协同发展 | — | 仲恺高新区 | 电子元器件协同配套 |

> **来源：**
> - 南方网《广东构建半导体及集成电路产业"3+N"布局》
>   [{SRC['southcn']}]({SRC['southcn']})
> - 凤凰网《省级特色产业园名单公布，珠海高新区半导体与集成电路产业园独家入选》
>   [{SRC['ifeng']}]({SRC['ifeng']})
> - 广州日报《广州打造国家集成电路产业发展"第三极"核心承载区》（2025-02-20）
>   [{SRC['dayoo']}]({SRC['dayoo']})
> - 中新网《广东这样打造"中国芯"第三极》（2024-06-03）
>   [{SRC['chinanews']}]({SRC['chinanews']})
> - 珠海高新区官网《打造国内领先的化合物半导体与特色工艺产业化示范区》
>   [{SRC['zhuhai']}]({SRC['zhuhai']})

---

### 五、2024-2026年核心指标

| 指标 | 2024年 | 2025年 | 2026年(预测/快报) |
|------|--------|--------|-----------------|
| 集成电路产量(亿块) | 804 | 预计~950 | 一季度增速43.1%, 预计达1,200+ |
| 产业营收(亿元) | ~3,200-3,600 | ~4,000(目标) | 预计4,500-5,000 |
| 12英寸晶圆月产能(万片) | 突破10 | 预计15-20 | 预计25-30 |
| IC设计业产值(亿元) | ~2,109 | ~2,600 | ~3,200+ |
| 晶圆制造业产值(亿元) | ~92 | ~180(估算) | ~350+(估算) |

> **来源：**
> - 广东省统计局 2024年工业运行数据: [{SRC['stats_industry']}]({SRC['stats_industry']})
> - 广东省统计局 2026年一季度工业运行简况: [{SRC['stats_q1']}]({SRC['stats_q1']})
> - 广东省工信厅《培育半导体及集成电路战略性新兴产业集群行动计划（2023-2025年）》: [{SRC['gdii']}]({SRC['gdii']})
> - 深芯盟《深圳集成电路及国产半导体产业调研报告》（2025年10月）: [{SRC['seccw']}]({SRC['seccw']})
> - 2024年产量数据亦见：深圳市半导体与集成电路产业联盟报道 [{SRC['szsica']}]({SRC['szsica']})

---

### 六、数据缺口与建议补充途径

| 缺失数据 | 建议获取方式 |
|---------|------------|
| 国企/民企/外企精确数量与产值占比 | 《广东统计年鉴2025》按登记注册类型分组表 ([http://stats.gd.gov.cn](http://stats.gd.gov.cn))；CSIA年度报告；深芯盟完整版报告 ([{SRC['szsia']}]({SRC['szsia']})) |
| 广东省全省IC企业总数（精确值） | 广东省市场监管局企业注册数据（可按行业代码筛选）；企查查/天眼查高级搜索 |
| 2026年完整年度数据 | 关注2026年7月前后发布的《2025年广东省半导体与集成电路产业发展报告》 |
| 研发投入占比、专利数量 | 广东省知识产权保护中心《广东省半导体及集成电路产业专利统计分析报告》 — [{SRC['gippc']}]({SRC['gippc']}) |
| 细分领域（三代半、先进封装等）产值 | 中商产业研究院付费版深度报告 ([https://m.askci.com](https://m.askci.com))；前瞻产业研究院 ([https://www.qianzhan.com](https://www.qianzhan.com)) |

---

### 七、原始数据源汇总

| # | 来源 | 链接 | 说明 |
|---|------|------|------|
| 1 | 中商产业研究院 | [{SRC['askci']}]({SRC['askci']}) | 2025年广东半导体与集成电路产业链全景图谱 |
| 2 | 深芯盟/深圳市半导体行业协会 | [{SRC['seccw']}]({SRC['seccw']}) | 深圳集成电路及国产半导体产业调研报告（2025年10月） |
| 3 | 深圳市半导体行业协会 | [{SRC['szsia']}]({SRC['szsia']}) | 会员名单、行业发展报告 |
| 4 | 21世纪经济报道 | [{SRC['yicai']}]({SRC['yicai']}) | 从买家到卖家：广东"芯"跳加速何以实现（2025-12-18） |
| 5 | 广东省统计局 | [{SRC['stats_q1']}]({SRC['stats_q1']}) | 2026年一季度工业运行简况 |
| 6 | 广东省统计局（工业数据首页） | [{SRC['stats_industry']}]({SRC['stats_industry']}) | 工业运行月度数据 |
| 7 | 广东省工信厅 | [{SRC['gdii']}]({SRC['gdii']}) | 专精特新企业名单、产业行动计划 |
| 8 | 广东省情网 | [{SRC['dfz']}]({SRC['dfz']}) | 广东年鉴2025·战略性新兴产业 |
| 9 | 南方网 | [{SRC['southcn']}]({SRC['southcn']}) | 广东构建半导体及集成电路产业"3+N"布局 |
| 10 | 中新网 | [{SRC['chinanews']}]({SRC['chinanews']}) | 广东这样打造"中国芯"第三极（2024-06-03） |
| 11 | 羊城晚报 | [{SRC['ycwb']}]({SRC['ycwb']}) | 2700亿元！广东十大战略性新兴产业"新质"观（2024-06-03） |
| 12 | 珠海高新区 | [{SRC['zhuhai']}]({SRC['zhuhai']}) | 打造国内领先的化合物半导体与特色工艺产业化示范区 |
| 13 | 凤凰网广东 | [{SRC['ifeng']}]({SRC['ifeng']}) | 省级特色产业园名单公布，珠海高新区IC产业园独家入选 |
| 14 | 广州日报 | [{SRC['dayoo']}]({SRC['dayoo']}) | 广州打造国家集成电路产业发展"第三极"核心承载区（2025-02-20） |
| 15 | 深圳市半导体与集成电路产业联盟 | [{SRC['szsica']}]({SRC['szsica']}) | 广东两会：2024年广东集成电路产量增长21%、占全国18% |
| 16 | 广州市半导体协会 | [{SRC['gzsia']}]({SRC['gzsia']}) | 产业报告 |
| 17 | 广州市统计局 | [{SRC['gztjj']}]({SRC['gztjj']}) | 广州统计信息手册（2025年） |
| 18 | 广东省知识产权保护中心 | [{SRC['gippc']}]({SRC['gippc']}) | 广东省半导体及集成电路产业专利统计分析报告 |
| 19 | 广东省集成电路行业协会 | [{SRC['gdica']}]({SRC['gdica']}) | 会员之窗-协会会员 |
| 20 | 证券之星 | [{SRC['stockstar']}]({SRC['stockstar']}) | 2022年广东省集成电路企业大数据全景分析 |
| 21 | 广东省工信厅-专精特新 | [{SRC['gdii_spe1']}]({SRC['gdii_spe1']}) | 2025年广州市专精特新中小企业认定（复核）公示名单 |
| 22 | 广东省工信厅-专精特新复核 | [{SRC['gdii_spe2']}]({SRC['gdii_spe2']}) | 2025年通过复核专精特新中小企业名单 |

---

*本报告由 Python 脚本 `code_files/scrape_ic_data.py` 自动生成。*
*生成时间：{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}*
*数据截止日期：2026年5月8日（公开可得的最新数据）*
"""
    return report


# ============================================================
# 主函数：执行全部抓取与数据整理
# ============================================================

def main():
    """主入口。支持 --selenium 参数启用 Selenium 抓取模式。"""
    use_selenium = "--selenium" in sys.argv

    print("=" * 60)
    print("  广东省集成电路产业数据抓取与整理")
    print(f"  运行时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"  数据输出目录: {DATA_DIR}")
    if use_selenium:
        print("  模式: Selenium (JS动态页面)")
    else:
        print("  模式: requests + BeautifulSoup (静态页面)")
    print("=" * 60)

    # ---------- 1. 抓取企业名单 ----------
    if use_selenium:
        sz_members = scrape_szsia_with_selenium()
    else:
        sz_members = scrape_szsia_members()
    gd_members = scrape_gdica_members()

    # 合并企业列表，去重（按企业名）
    all_names = set()
    all_members = []
    for m in sz_members + gd_members:
        name = m["企业名称"]
        if name not in all_names:
            all_names.add(name)
            all_members.append(m)

    # 后处理：过滤掉明显不是企业名的条目（如导航菜单项、服务名称等）
    # 仅对"动态抓取"来源的条目做过滤，静态数据来源的已预清洗
    company_pattern = re.compile(r'有限公司|股份有限公司|有限责任公司|集团|半导|微电子|集成电路|电子科技')
    filtered_members = []
    nav_pattern = re.compile(
        r'^(协会|会员|活动|资讯|通知|法规|职称|党建|注册|登录|'
        r'首页|关于|联系|新闻|服务|申请|返回|更多|搜索)'
    )
    # 排除明显是活动/会议名而非企业名的条目
    event_kw = ["峰会", "大会", "论坛", "研讨会", "展会", "博览会", "年会"]
    removed_count = 0
    for m in all_members:
        name = m["企业名称"]
        # 静态数据直接保留
        if "静态数据" in m.get("来源", ""):
            filtered_members.append(m)
        # 动态抓取的：必须像企业名，且不是事件/活动名
        elif (company_pattern.search(name)
              and not nav_pattern.match(name)
              and not any(kw in name for kw in event_kw)):
            filtered_members.append(m)
        else:
            removed_count += 1

    if removed_count:
        print(f"  [后处理] 过滤掉 {removed_count} 条非企业名条目（导航/菜单/服务项）")
    all_members = filtered_members

    # 保存企业名单 CSV
    members_df = pd.DataFrame(all_members)
    csv_path = DATA_DIR / "广东集成电路企业名单.csv"
    members_df.to_csv(csv_path, index=False, encoding="utf-8-sig")
    print(f"\n  ✓ 企业名单已保存至: {csv_path} ({len(all_members)} 条)")

    # 保存 Excel 版
    excel_path = DATA_DIR / "广东集成电路企业名单.xlsx"
    with pd.ExcelWriter(excel_path, engine="openpyxl") as writer:
        members_df.to_excel(writer, sheet_name="企业名单", index=False)
    print(f"  ✓ 企业名单 Excel 已保存至: {excel_path}")

    # ---------- 2. 获取产值数据 ----------
    ic_df = get_ic_production_data()
    ic_csv = DATA_DIR / "广东集成电路产值数据.csv"
    ic_df.to_csv(ic_csv, index=False, encoding="utf-8-sig")
    print(f"  ✓ 产值数据已保存至: {ic_csv}")

    # 产值 Excel（含多个 sheet）
    ic_excel = DATA_DIR / "广东集成电路产值数据.xlsx"
    with pd.ExcelWriter(ic_excel, engine="openpyxl") as writer:
        ic_df.to_excel(writer, sheet_name="年度产值", index=False)

        # 产业链各环节产值 sheet（2024年）
        chain_data = {
            "产业链环节": ["IC设计业", "封测业", "装备与材料业", "晶圆制造业"],
            "产值(亿元)": [2109, 795, 608, 92],
            "占比(%)": [58.6, 22.1, 16.9, 2.6],
            "同比增速(%)": ["~25", "~18", "~15", "~102"],
            "特征说明": [
                "传统优势环节，全国领先",
                "佛山、中山为封测集群",
                "设备国产化替代加速",
                "近年增长最快环节",
            ],
        }
        chain_df = pd.DataFrame(chain_data)
        chain_df.to_excel(writer, sheet_name="产业链各环节产值", index=False)

        # 深圳企业分布 sheet
        sz_dist = {
            "产业链环节": ["IC设计", "设备及零部件", "封装测试", "材料", "晶圆制造"],
            "企业数量(家)": [456, 133, 82, 48, 8],
            "占比(%)": [62.7, 18.3, 11.3, 6.6, 1.1],
        }
        sz_df = pd.DataFrame(sz_dist)
        sz_df.to_excel(writer, sheet_name="深圳IC企业分布", index=False)

        # 企业类型分布估算 sheet
        type_data = {
            "企业类型": ["民营企业", "国有企业/国有控股", "外资/合资企业"],
            "估算企业数量占比(%)": ["75-80", "10-15", "5-10"],
            "估算产值占比(%)": ["55-60", "20-25", "15-20"],
            "主要分布领域": [
                "IC设计、设备、材料、封测",
                "晶圆制造、关键材料",
                "晶圆制造、高端封测、设备",
            ],
            "代表企业": [
                "海思半导体、粤芯半导体、比亚迪半导体、全志科技",
                "华润微(润鹏半导体)、国星光电、中国电子(部分子公司)",
                "中芯国际(深圳)、英诺赛科(珠海)",
            ],
        }
        type_df = pd.DataFrame(type_data)
        type_df.to_excel(writer, sheet_name="企业类型分布估算", index=False)

    print(f"  ✓ 产值数据 Excel 已保存至: {ic_excel}")

    # ---------- 3. 获取统计数据 ----------
    stats = scrape_gd_stats()
    stats_path = DATA_DIR / "广东统计数据摘要.json"
    with open(stats_path, "w", encoding="utf-8") as f:
        json.dump(stats, f, ensure_ascii=False, indent=2)
    print(f"  ✓ 统计数据摘要已保存至: {stats_path}")

    # ---------- 4. 生成 Markdown 报告 ----------
    report = generate_industry_chain_report()
    report_path = DATA_DIR / "产业链信息整理报告.md"
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(report)
    print(f"  ✓ 产业链 Markdown 报告已保存至: {report_path}")

    # ---------- 收尾 ----------
    print(f"\n{'='*60}")
    print(f"  全部完成！共生成以下文件：")
    print(f"  1. {csv_path}")
    print(f"  2. {excel_path}")
    print(f"  3. {ic_csv}")
    print(f"  4. {ic_excel}")
    print(f"  5. {stats_path}")
    print(f"  6. {report_path}")
    print(f"{'='*60}")
    print(f"  2. {excel_path}")
    print(f"  3. {ic_csv}")
    print(f"  4. {ic_excel}")
    print(f"  5. {stats_path}")
    print(f"  6. {report_path}")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
