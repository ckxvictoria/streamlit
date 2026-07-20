# ============================================================
# 汇川技术 (300124.SZ) 竞争情报看板
# 报告期：2025年年度报告（FY2025）
# 数据来源：深圳市汇川技术股份有限公司 2025年年度报告全文
# 生成时间：2026年6月
# 使用方：西门子数字化工业（DI）竞争情报团队
# 免责声明：本看板数据均来源于汇川技术公开披露的年度报告，
#           仅供西门子内部竞争研究使用，不构成投资建议。
# ============================================================

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ─────────────────────────────────────────
# 全局配色方案
# ─────────────────────────────────────────
COLORS = {
    "primary":    "#1B3A8C",
    "secondary":  "#2BBFBF",
    "success":    "#27AE60",
    "danger":     "#E74C3C",
    "neutral":    "#8FA8C8",
    "bg_light":   "#F5F7FA",
    "card_bg":    "#FFFFFF",
    "text_dark":  "#1A2B4A",
    "text_muted": "#6B7A99",
    "plot_bg":    "#FFFFFF",
    "grid_color": "#E8EDF5",
}

PLOTLY_TEMPLATE = "plotly_white"
PRODUCT_COLORS  = ["#1B3A8C", "#2BBFBF", "#5B8DEF", "#27AE60", "#8FA8C8"]

# ─────────────────────────────────────────
# 兼容性封装：统一处理 use_container_width
# ─────────────────────────────────────────
def _st_version_tuple():
    """返回当前streamlit版本元组，用于兼容判断。"""
    try:
        parts = st.__version__.split(".")
        return tuple(int(x) for x in parts[:2])
    except Exception:
        return (1, 35)

_VER = _st_version_tuple()

def plotly_chart(fig, stretch=True):
    """兼容新旧版本的plotly_chart封装。"""
    if _VER >= (1, 42):
        st.plotly_chart(fig, width="stretch" if stretch else "content")
    else:
        st.plotly_chart(fig, use_container_width=stretch)

def dataframe(df, **kwargs):
    """兼容新旧版本的dataframe封装。"""
    if _VER >= (1, 42):
        kwargs.pop("use_container_width", None)
        st.dataframe(df, width="stretch", **kwargs)
    else:
        st.dataframe(df, use_container_width=True, **kwargs)

# ─────────────────────────────────────────
# 数据层
# ─────────────────────────────────────────
def load_financial_data() -> dict:
    """
    加载汇川技术FY2025财务数据。
    所有数据均来源于公司2025年年度报告，单位：万元（人民币）。
    未披露项标注为None，不估算填充。
    """

    # ── 一、盈利指标（近3年）──
    profit = pd.DataFrame({
        "年份":           ["2023",     "2024",     "2025"],
        "营业收入":       [304199.25,  370409.52,  451048.44],
        "归母净利润":     [47418.63,   42854.93,   50500.02],
        "扣非归母净利润": [40711.77,   40358.32,   49505.05],
        "营业成本":       [215659.49,  264094.04,  320449.39],
        "研发费用":       [26241.48,   31470.81,   42557.74],
        "销售费用":       [None,       14808.78,   15355.69],
        "管理费用":       [None,       15413.53,   18250.83],
    })
    profit["毛利率"]     = (profit["营业收入"] - profit["营业成本"]) / profit["营业收入"] * 100
    profit["净利率"]     = profit["归母净利润"] / profit["营业收入"] * 100
    profit["研发费用率"] = profit["研发费用"]   / profit["营业收入"] * 100
    profit["销售费用率"] = profit["销售费用"]   / profit["营业收入"] * 100

    # ── 二、现金流指标 ──
    cashflow = pd.DataFrame({
        "年份":               ["2023",   "2024",   "2025"],
        "经营活动现金净流量": [33699.16, 72004.40, 66810.25],
        "归母净利润":         [47418.63, 42854.93, 50500.02],
    })
    cashflow["现金保障倍数(%)"] = cashflow["经营活动现金净流量"] / cashflow["归母净利润"] * 100

    # ── 三、资产负债指标 ──
    balance = pd.DataFrame({
        "年份":       ["2023",     "2024",     "2025"],
        "总资产":     [489575.64,  571788.24,  713143.94],
        "归母净资产": [244818.94,  279943.78,  353529.91],
        "负债合计":   [None,       287496.93,  341795.83],
        "流动资产":   [None,       304506.86,  430087.38],
        "流动负债":   [None,       233739.63,  298940.57],
    })
    balance["资产负债率(%)"] = balance["负债合计"] / balance["总资产"] * 100
    balance["流动比率"]      = balance["流动资产"] / balance["流动负债"]

    # ── 四、ROE ──
    roe = pd.DataFrame({
        "年份": ["2023", "2024", "2025"],
        "ROE":  [21.66,  16.52,  16.34],
    })

    # ── 五、成长指标 ──
    growth = pd.DataFrame({
        "年份":     ["2024", "2025"],
        "营收增速": [round((370409.52 - 304199.25) / 304199.25 * 100, 2), 21.77],
        "净利增速": [round((42854.93  - 47418.63)  / 47418.63  * 100, 2), 17.84],
    })
    growth["利润弹性系数"] = growth["净利增速"] / growth["营收增速"]

    # ── 六、股东回报 ──
    shareholder = pd.DataFrame({
        "年份":     ["2023", "2024", "2025"],
        "基本EPS":  [1.78,   1.60,   1.87],
        "稀释EPS":  [1.78,   1.60,   1.85],
        "每股分红": [None,   None,   0.50],
        "分红总额": [None,   None,   13533.18],
        "分红比例": [None,   None,   round(13533.18 / 50500.02 * 100, 2)],
    })

    # ── 七、产品线 ──
    product = pd.DataFrame({
        "产品线":   ["工业自动化与数字化", "新能源汽车动力系统", "新兴产业", "其他"],
        "营业收入": [222454.02, 203225.82, 17950.19, 7418.41],
        "营业成本": [132865.04, 170504.18, 12760.01, 4320.15],
        "2024收入": [187272.21, 160797.56, 15500.92, 6838.83],
    })
    product["毛利率(%)"]   = (product["营业收入"] - product["营业成本"]) / product["营业收入"] * 100
    product["收入占比(%)"] = product["营业收入"] / product["营业收入"].sum() * 100
    product["同比增速(%)"] = (product["营业收入"] - product["2024收入"]) / product["2024收入"] * 100

    # ── 八、分地区 ──
    region = pd.DataFrame({
        "地区":      ["中国内地", "境外"],
        "营业收入":  [424559.52,  26488.92],
        "毛利率(%)": [28.55,      None],
        "2024收入":  [350016.18,  20393.34],
    })
    region["同比增速(%)"] = (region["营业收入"] - region["2024收入"]) / region["2024收入"] * 100

    # ── 九、分季度 ──
    quarterly = pd.DataFrame({
        "季度":       ["Q1",      "Q2",       "Q3",       "Q4"],
        "营业收入":   [89779.12,  115314.46,  111532.49,  134422.38],
        "归母净利润": [13228.25,  16455.63,   12857.43,   7958.71],
    })
    quarterly["净利率(%)"] = quarterly["归母净利润"] / quarterly["营业收入"] * 100

    # ── 十、产销量 ──
    volume = pd.DataFrame({
        "行业":         ["智能制造",  "新能源汽车"],
        "销售量(PCS)":  [25971863,    5933895],
        "生产量(PCS)":  [25499533,    6108223],
        "库存量(PCS)":  [1361822,     724156],
        "2024销售量":   [19785481,    4619378],
        "2024生产量":   [20084736,    4845348],
        "2024库存量":   [1834152,     549828],
    })
    volume["销售量增速(%)"] = (volume["销售量(PCS)"] - volume["2024销售量"]) / volume["2024销售量"] * 100

    # ── 十一、费用对比 ──
    expenses = pd.DataFrame({
        "费用类型": ["销售费用", "管理费用", "研发费用"],
        "2024年":   [14808.78,   15413.53,   31470.81],
        "2025年":   [15355.69,   18250.83,   42557.74],
    })
    expenses["增速(%)"] = (expenses["2025年"] - expenses["2024年"]) / expenses["2024年"] * 100

    # ── 十二、市场份额 ──
    market_share = pd.DataFrame({
        "产品":        ["通用伺服系统", "低压变频器", "中高压变频器", "PLC（不含I/O）", "工业机器人（出货量）", "SCARA机器人"],
        "市场份额(%)": [31.0,           20.0,          14.0,            5.7,              8.8,                    28.0],
        "排名":        ["第1名",         "第1名",        "第1名",         "第4名",          "第4名（本土第2）",     "第1名"],
        "数据来源":    ["弗若斯特沙利文"] * 6,
    })

    # ── 十三、利润瀑布图数据 ──
    waterfall = {
        "节点":    ["营业收入", "营业成本", "毛利润", "销售费用", "管理费用",
                    "研发费用", "财务收益", "其他净收益", "归母净利润"],
        "金额":    [451048.44, -320449.39, 130599.05, -15355.69, -18250.83,
                    -42557.74, 657.19, 3407.03, 50500.02],
        "measure": ["absolute", "relative", "total", "relative", "relative",
                    "relative", "relative", "relative", "total"],
    }

    # ── 十四、研发数据 ──
    rd_staff = {
        "研发人员总数":    7670,
        "累计专利及软著":  3375,
        "研发费用_2023":   26241.48,
        "研发费用_2024":   31470.81,
        "研发费用_2025":   42557.74,
        "研发费用率_2023": 8.63,
        "研发费用率_2024": 8.50,
        "研发费用率_2025": 9.44,
    }

    return {
        "profit": profit, "cashflow": cashflow, "balance": balance,
        "roe": roe, "growth": growth, "shareholder": shareholder,
        "product": product, "region": region, "quarterly": quarterly,
        "volume": volume, "expenses": expenses, "market_share": market_share,
        "waterfall": waterfall, "rd_staff": rd_staff,
    }

# ─────────────────────────────────────────
# 样式层
# ─────────────────────────────────────────
def inject_css() -> None:
    """注入全局CSS样式。Tab交互样式已修复，不覆盖Streamlit原生事件区域。"""
    st.markdown("""
    <style>
    .stApp {
        background-color: #F5F7FA;
        color: #1A2B4A;
        font-family: 'Segoe UI', 'PingFang SC', 'Microsoft YaHei', sans-serif;
    }
    .main-header {
        background: linear-gradient(135deg, #1B3A8C 0%, #2B5299 60%, #1B3A8C 100%);
        border-left: 6px solid #2BBFBF;
        border-radius: 14px;
        box-shadow: 0 4px 20px rgba(27,58,140,0.18);
        padding: 22px 28px 18px 28px;
        margin-bottom: 20px;
    }
    .main-header h1 { color:#FFFFFF; font-size:1.9rem; font-weight:700; margin:0 0 6px 0; }
    .main-header p  { color:#A8C4E8; font-size:0.88rem; margin:0; }

    [data-testid="metric-container"] {
        background:#FFFFFF; border:1px solid #E0E8F5;
        border-radius:12px; border-top:4px solid #1B3A8C;
        box-shadow:0 2px 12px rgba(27,58,140,0.08);
        padding:14px 16px; transition:box-shadow 0.2s;
    }
    [data-testid="metric-container"]:hover { box-shadow:0 6px 24px rgba(27,58,140,0.15); }
    [data-testid="stMetricLabel"] { color:#6B7A99 !important; font-size:0.82rem !important; font-weight:600 !important; }
    [data-testid="stMetricValue"] { color:#1B3A8C !important; font-size:1.5rem !important; font-weight:700 !important; }
    [data-testid="stMetricDelta"] svg { display:none; }
    [data-testid="stMetricDelta"] { font-size:0.8rem; font-weight:600; }

    /* ══ Tab修复核心：只改颜色，绝不动padding/margin/pointer-events ══ */
    [data-testid="stTabs"] [role="tablist"] {
        background:#FFFFFF;
        border-radius:10px;
        border:1px solid #E0E8F5;
    }
    [data-testid="stTabs"] button[role="tab"] {
        color:#6B7A99 !important;
        font-weight:600;
        font-size:0.88rem;
        border-radius:8px;
        background:transparent;
        border:none;
        transition:background 0.18s, color 0.18s;
    }
    [data-testid="stTabs"] button[role="tab"]:hover {
        background:#EEF3FC !important;
        color:#1B3A8C !important;
    }
    [data-testid="stTabs"] button[role="tab"][aria-selected="true"] {
        background:#1B3A8C !important;
        color:#FFFFFF !important;
    }

    [data-testid="stSidebar"] { background:#FFFFFF; border-right:2px solid #E0E8F5; }

    h3 { color:#1B3A8C !important; border-bottom:2px solid #2BBFBF;
         padding-bottom:6px; margin-bottom:16px !important; }

    .insight-box {
        background:#EEF3FC; border-left:5px solid #1B3A8C;
        border-radius:10px; padding:13px 18px;
        font-size:0.87rem; margin-bottom:10px; line-height:1.6;
    }
    .insight-box.green { background:#EAF7F0; border-left-color:#27AE60; }
    .insight-box.red   { background:#FEF0EE; border-left-color:#E74C3C; }
    .insight-box.teal  { background:#E8F8F8; border-left-color:#2BBFBF; }

    [data-testid="stDownloadButton"] button {
        background:#1B3A8C; color:white; border-radius:8px; border:none; font-weight:600;
    }
    [data-testid="stDownloadButton"] button:hover { background:#2BBFBF; }
    [data-testid="stDataFrame"] { border-radius:10px; border:1px solid #E0E8F5; }

    .sidebar-logo {
        background:linear-gradient(135deg,#1B3A8C,#2B5299);
        border-radius:12px; padding:16px; text-align:center; margin-bottom:16px;
    }
    .sidebar-logo h2 { color:#FFFFFF; font-size:1.1rem; margin:0 0 4px 0; }
    .sidebar-logo p  { color:#A8C4E8; font-size:0.78rem; margin:0; }
    </style>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────
# 图表统一布局
# ─────────────────────────────────────────
def base_layout(**kwargs) -> dict:
    """返回Plotly图表统一布局配置。"""
    layout = dict(
        template      = PLOTLY_TEMPLATE,
        paper_bgcolor = COLORS["card_bg"],
        plot_bgcolor  = COLORS["plot_bg"],
        font          = dict(family="Segoe UI, PingFang SC, Microsoft YaHei",
                             color=COLORS["text_dark"], size=12),
        title_font    = dict(color=COLORS["primary"], size=14,
                             family="Segoe UI, PingFang SC"),
        xaxis  = dict(gridcolor=COLORS["grid_color"], linecolor="#D0DAF0", tickcolor="#D0DAF0"),
        yaxis  = dict(gridcolor=COLORS["grid_color"], linecolor="#D0DAF0", tickcolor="#D0DAF0"),
        margin = dict(t=55, b=40, l=40, r=30),
    )
    layout.update(kwargs)
    return layout

# ─────────────────────────────────────────
# KPI卡片组件
# ─────────────────────────────────────────
def kpi_card(col, label: str, value: str, delta: str, delta_val: str, note: str = "") -> None:
    """渲染单个KPI卡片。"""
    with col:
        st.metric(label=label, value=value, delta=f"{delta}: {delta_val}")
        if note:
            st.caption(note)

# ─────────────────────────────────────────
# Tab1：CEO概览圈
# ─────────────────────────────────────────
def render_tab_ceo(data: dict) -> None:
    """渲染CEO概览Tab。"""
    profit    = data["profit"]
    quarterly = data["quarterly"]
    roe       = data["roe"]

    st.markdown("### 📊 核心经营指标（FY2025）")
    c1, c2, c3, c4, c5, c6 = st.columns(6)
    kpi_card(c1, "营业总收入",     "451.05亿元", "同比",   "+21.77%", "2025年")
    kpi_card(c2, "归母净利润",     "50.50亿元",  "同比",   "+17.84%", "2025年")
    kpi_card(c3, "扣非归母净利润", "49.51亿元",  "同比",   "+22.66%", "2025年")
    kpi_card(c4, "研发投入",       "42.56亿元",  "费用率", "9.44%",   "研发人员7,670人")
    kpi_card(c5, "基本EPS",        "1.87元/股",  "同比",   "+16.88%", "稀释EPS 1.85元")
    kpi_card(c6, "现金分红比例",   "26.80%",     "每股",   "0.50元",  "共派13.53亿元")

    st.markdown("<br>", unsafe_allow_html=True)
    a1, a2, a3, a4 = st.columns(4)
    kpi_card(a1, "总资产",      "713.14亿元", "同比", "+24.72%",  "2025年末")
    kpi_card(a2, "归母净资产",  "353.53亿元", "同比", "+26.29%",  "2025年末")
    kpi_card(a3, "加权平均ROE", "16.34%",     "同比", "-0.18pct", "2024年16.52%")
    kpi_card(a4, "境外收入",    "26.49亿元",  "同比", "+29.89%",  "占比5.87%")

    st.markdown("<br>", unsafe_allow_html=True)
    col_left, col_right = st.columns([3, 2])

    with col_left:
        st.markdown("### 三年核心财务趋势")
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        years = profit["年份"].tolist()
        fig.add_trace(go.Bar(
            x=years, y=profit["营业收入"], name="营业收入（万元）",
            marker_color=COLORS["primary"], opacity=0.82,
            hovertemplate="<b>%{x}</b><br>营业收入：%{y:,.0f} 万元<extra></extra>",
        ), secondary_y=False)
        fig.add_trace(go.Scatter(
            x=years, y=profit["归母净利润"], name="归母净利润（万元）",
            mode="lines+markers+text",
            line=dict(color=COLORS["secondary"], width=2.5),
            marker=dict(symbol="diamond", size=10, color=COLORS["secondary"]),
            text=[f"{v:,.0f}" for v in profit["归母净利润"]],
            textposition="top center", textfont=dict(size=11, color=COLORS["secondary"]),
            hovertemplate="<b>%{x}</b><br>归母净利润：%{y:,.0f} 万元<extra></extra>",
        ), secondary_y=False)
        fig.add_trace(go.Scatter(
            x=years, y=profit["净利率"], name="净利率（%）",
            mode="lines+markers",
            line=dict(color=COLORS["success"], width=2, dash="dot"),
            marker=dict(size=8, color=COLORS["success"]),
            hovertemplate="<b>%{x}</b><br>净利率：%{y:.2f}%<extra></extra>",
        ), secondary_y=True)
        fig.update_layout(**base_layout(
            title="营业收入 / 归母净利润 / 净利率（三年趋势）", height=420,
            legend=dict(orientation="h", y=-0.18, x=0.5, xanchor="center",
                        bgcolor="rgba(255,255,255,0.8)", bordercolor="#E0E8F5", borderwidth=1),
        ))
        fig.update_yaxes(title_text="金额（万元）", secondary_y=False, gridcolor=COLORS["grid_color"])
        fig.update_yaxes(title_text="净利率（%）",  secondary_y=True,  gridcolor=COLORS["grid_color"])
        plotly_chart(fig)

    with col_right:
        st.markdown("### 盈利质量雷达图")
        categories = ["毛利率", "净利率", "研发费用率", "销售费用率", "ROE"]

        def get_radar_vals(yr):
            p   = profit[profit["年份"] == yr]
            r   = roe[roe["年份"] == yr]
            sf_raw = p["销售费用率"].values[0]
            if sf_raw is None or (isinstance(sf_raw, float) and np.isnan(sf_raw)):
                sf = float(profit[profit["年份"] == "2024"]["销售费用率"].values[0])
            else:
                sf = float(sf_raw)
            return [float(p["毛利率"].values[0]), float(p["净利率"].values[0]),
                    float(p["研发费用率"].values[0]), sf, float(r["ROE"].values[0])]

        fig_r = go.Figure()
        for yr, color in [("2023", COLORS["neutral"]), ("2024", COLORS["secondary"]), ("2025", COLORS["primary"])]:
            vals = get_radar_vals(yr)
            fig_r.add_trace(go.Scatterpolar(
                r=vals + [vals[0]], theta=categories + [categories[0]],
                fill="toself", name=yr,
                line=dict(color=color, width=2), opacity=0.85,
            ))
        fig_r.update_layout(**base_layout(
            title="盈利质量雷达（三年对比）", height=420,
            polar=dict(radialaxis=dict(visible=True, range=[0, 35]), bgcolor=COLORS["plot_bg"]),
            legend=dict(orientation="h", y=-0.12, x=0.5, xanchor="center",
                        bgcolor="rgba(255,255,255,0.8)", bordercolor="#E0E8F5", borderwidth=1),
        ))
        plotly_chart(fig_r)

    st.markdown("### 季度营收节奏（FY2025）")
    fig_q = make_subplots(rows=1, cols=2, subplot_titles=("季度营业收入（万元）", "季度净利率（%）"))
    q_colors = [COLORS["neutral"], COLORS["primary"], COLORS["primary"], COLORS["secondary"]]
    fig_q.add_trace(go.Bar(
        x=quarterly["季度"], y=quarterly["营业收入"], marker_color=q_colors,
        text=[f"{v:,.0f}" for v in quarterly["营业收入"]],
        textposition="outside", textfont=dict(size=11),
        hovertemplate="<b>%{x}</b><br>营业收入：%{y:,.0f} 万元<extra></extra>",
        showlegend=False,
    ), row=1, col=1)
    fig_q.add_trace(go.Scatter(
        x=quarterly["季度"], y=quarterly["净利率(%)"],
        mode="lines+markers+text",
        line=dict(color=COLORS["secondary"], width=2.5),
        marker=dict(size=10, color=COLORS["secondary"]),
        text=[f"{v:.2f}%" for v in quarterly["净利率(%)"]],
        textposition="top center", textfont=dict(size=11, color=COLORS["secondary"]),
        hovertemplate="<b>%{x}</b><br>净利率：%{y:.2f}%<extra></extra>",
        showlegend=False,
    ), row=1, col=2)
    fig_q.update_layout(**base_layout(height=400, showlegend=False))
    fig_q.update_yaxes(gridcolor=COLORS["grid_color"])
    plotly_chart(fig_q)

    st.markdown("""
    <div class="insight-box red">
    ⚠️ <b>【西门子DI警示】Q4净利率骤降至5.92%（全年最低）：</b>
    汇川Q4营收134.42亿元创历史新高，但净利率仅5.92%，说明新能源汽车业务价格压力与研发投入加速在Q4集中体现。
    西门子DI需关注：汇川是否以价换量侵蚀工控市场，Q4低利润率或预示2026年价格战风险上升。
    </div>
    <div class="insight-box green">
    ✅ <b>【增长引擎确认】双轮驱动格局清晰：</b>
    工业自动化与数字化收入222亿元（+19%），新能源汽车动力系统203亿元（+26%），两大业务合计占总收入94%。
    汇川已构建"工控+新能源"双飞轮，抗周期能力显著强于纯工控厂商，西门子DI在中国工控市场面临的竞争烈度将持续加剧。
    </div>
    <div class="insight-box teal">
    🌐 <b>【国际化加速信号】境外收入增速29.89%，远超整体21.77%：</b>
    汇川正加速"借船出海"战略，同时筹划H股上市（2026年1月公告）。
    西门子DI需在东南亚、中东等新兴市场提前布局防御，避免被汇川以性价比优势蚕食中低端市场份额。
    </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────
# Tab2：产品线分析
# ─────────────────────────────────────────
def render_tab_product(data: dict) -> None:
    """渲染产品线分析Tab。"""
    product = data["product"]
    volume  = data["volume"]
    market  = data["market_share"]

    st.markdown("### 🏭 产品线收入结构（FY2025）")
    col1, col2 = st.columns(2)

    with col1:
        fig_pie = go.Figure(go.Pie(
            labels=product["产品线"], values=product["营业收入"], hole=0.52,
            marker=dict(colors=PRODUCT_COLORS[:len(product)], line=dict(color="white", width=2)),
            textinfo="label+percent", textfont=dict(size=12),
            hovertemplate="<b>%{label}</b><br>收入：%{value:,.0f} 万元<br>占比：%{percent}<extra></extra>",
        ))
        fig_pie.add_annotation(text="总收入<br><b>451.05亿</b>", x=0.5, y=0.5, showarrow=False,
                               font=dict(size=13, color=COLORS["primary"]))
        fig_pie.update_layout(**base_layout(title="产品线收入占比（FY2025）", height=340),
                              showlegend=True,
                              legend=dict(orientation="h", y=-0.12, x=0.5, xanchor="center"))
        plotly_chart(fig_pie)

    with col2:
        colors_g = [COLORS["success"] if v >= 0 else COLORS["danger"] for v in product["同比增速(%)"]]
        fig_g = go.Figure(go.Bar(
            x=product["同比增速(%)"], y=product["产品线"], orientation="h",
            marker_color=colors_g,
            text=[f"{v:+.2f}%" for v in product["同比增速(%)"]],
            textposition="outside", textfont=dict(size=12),
            hovertemplate="<b>%{y}</b><br>同比增速：%{x:.2f}%<extra></extra>",
        ))
        fig_g.add_vline(x=0, line_dash="dash", line_color=COLORS["text_muted"], line_width=1)
        fig_g.add_vline(x=21.77, line_dash="dot", line_color=COLORS["primary"], line_width=2,
                        annotation_text="整体增速 21.8%", annotation_position="top right",
                        annotation_font=dict(color=COLORS["primary"], size=11))
        fig_g.update_layout(**base_layout(title="产品线同比增速（FY2025 vs FY2024）", height=340), showlegend=False)
        fig_g.update_xaxes(title_text="同比增速（%）")
        plotly_chart(fig_g)

    st.markdown("### 产品线收入与毛利率对比")
    fig_dual = make_subplots(specs=[[{"secondary_y": True}]])
    fig_dual.add_trace(go.Bar(
        x=product["产品线"], y=product["营业收入"], name="营业收入（万元）",
        marker_color=PRODUCT_COLORS[:len(product)],
        hovertemplate="<b>%{x}</b><br>营业收入：%{y:,.0f} 万元<extra></extra>",
    ), secondary_y=False)
    fig_dual.add_trace(go.Scatter(
        x=product["产品线"], y=product["毛利率(%)"], name="毛利率（%）",
        mode="lines+markers",
        line=dict(color=COLORS["danger"], width=2.5),
        marker=dict(symbol="star", size=13, color=COLORS["danger"]),
        hovertemplate="<b>%{x}</b><br>毛利率：%{y:.2f}%<extra></extra>",
    ), secondary_y=True)
    fig_dual.update_layout(**base_layout(
        title="产品线营业收入 & 毛利率", height=400,
        legend=dict(orientation="h", y=-0.18, x=0.5, xanchor="center",
                    bgcolor="rgba(255,255,255,0.8)", bordercolor="#E0E8F5", borderwidth=1),
    ))
    fig_dual.update_yaxes(title_text="营业收入（万元）", secondary_y=False)
    fig_dual.update_yaxes(title_text="毛利率（%）", secondary_y=True, range=[0, 60])
    plotly_chart(fig_dual)

    st.markdown("### 产销量对比（FY2025）")
    fig_vol = go.Figure()
    for metric, color in [("销售量(PCS)", COLORS["primary"]),
                           ("生产量(PCS)", COLORS["secondary"]),
                           ("库存量(PCS)", COLORS["neutral"])]:
        fig_vol.add_trace(go.Bar(
            name=metric, x=volume["行业"], y=volume[metric],
            marker_color=color, opacity=0.9,
            text=[f"{v:,.0f}" for v in volume[metric]],
            textposition="outside", textfont=dict(size=10),
            hovertemplate=f"<b>%{{x}}</b><br>{metric}：%{{y:,.0f}} PCS<extra></extra>",
        ))
    fig_vol.update_layout(**base_layout(
        title="主要产品产销量（PCS）", height=400, barmode="group",
        legend=dict(orientation="h", y=-0.18, x=0.5, xanchor="center",
                    bgcolor="rgba(255,255,255,0.8)", bordercolor="#E0E8F5", borderwidth=1),
    ))
    plotly_chart(fig_vol)

    st.markdown("### 中国市场份额（弗若斯特沙利文，2025年）")
    dataframe(market, height=250)

    st.markdown("""
    <div class="insight-box red">
    🔴 <b>【西门子DI核心威胁】伺服系统市占率31%，稳居中国第一：</b>
    汇川伺服系统在中国市场份额31%，远超西门子在华伺服份额。其"工控+工艺"一体化解决方案策略
    正在锂电、光伏、包装等高景气行业快速渗透，西门子DI的SINAMICS/SIMOTICS产品线在中低端应用场景面临持续价格压力。
    </div>
    <div class="insight-box">
    🔵 <b>【PLC市场：汇川仍是弱项，西门子DI的机会窗口】</b>
    汇川PLC市场份额仅5.7%（第4名），远低于其伺服/变频器的市场地位。
    西门子DI应在PLC+SCADA+MES全栈方案上加速布局，在汇川PLC尚未成熟前巩固高端制造客户的系统粘性。
    </div>
    <div class="insight-box teal">
    🤖 <b>【新兴产业：SCARA机器人市占率28%全国第一，长期威胁不容忽视】</b>
    汇川正在构建"自动化+机器人+能源"的生态闭环，与西门子DI的数字化工厂战略形成正面竞争，
    需密切跟踪其InoCube平台的客户渗透速度。
    </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────
# Tab3：市场与渠道
# ─────────────────────────────────────────
def render_tab_market(data: dict) -> None:
    """渲染市场与渠道Tab。"""
    region = data["region"]

    st.markdown("### 🌍 地区收入分布（FY2025）")
    col1, col2 = st.columns([3, 2])

    with col1:
        fig_r = go.Figure(go.Bar(
            x=region["营业收入"], y=region["地区"], orientation="h",
            marker_color=[COLORS["primary"], COLORS["secondary"]],
            text=[f"{v:,.0f} 万元" for v in region["营业收入"]],
            textposition="outside", textfont=dict(size=12),
            hovertemplate="<b>%{y}</b><br>营业收入：%{x:,.0f} 万元<extra></extra>",
        ))
        fig_r.update_layout(**base_layout(title="分地区营业收入（FY2025）", height=340), showlegend=False)
        fig_r.update_xaxes(title_text="营业收入（万元）")
        plotly_chart(fig_r)

    with col2:
        fig_geo = go.Figure(go.Pie(
            labels=region["地区"], values=region["营业收入"], hole=0.52,
            marker=dict(colors=[COLORS["primary"], COLORS["secondary"]], line=dict(color="white", width=2)),
            textinfo="label+percent",
            hovertemplate="<b>%{label}</b><br>%{value:,.0f} 万元<extra></extra>",
        ))
        fig_geo.add_annotation(text="境内/境外<br><b>94:6</b>", x=0.5, y=0.5, showarrow=False,
                               font=dict(size=12, color=COLORS["primary"]))
        fig_geo.update_layout(**base_layout(title="境内 vs 境外收入占比", height=340), showlegend=False)
        plotly_chart(fig_geo)

    st.markdown("### 地区收入增速对比")
    growth_colors = [COLORS["success"] if v >= 21.77 else COLORS["primary"] for v in region["同比增速(%)"]]
    fig_rg = go.Figure(go.Bar(
        x=region["同比增速(%)"], y=region["地区"], orientation="h",
        marker_color=growth_colors,
        text=[f"{v:+.2f}%" for v in region["同比增速(%)"]],
        textposition="outside", textfont=dict(size=13),
        hovertemplate="<b>%{y}</b><br>同比增速：%{x:.2f}%<extra></extra>",
    ))
    fig_rg.add_vline(x=21.77, line_dash="dot", line_color=COLORS["primary"], line_width=2,
                     annotation_text="整体增速 21.8%", annotation_position="top right",
                     annotation_font=dict(color=COLORS["primary"], size=11))
    fig_rg.update_layout(**base_layout(title="分地区同比增速（FY2025 vs FY2024）", height=340), showlegend=False)
    fig_rg.update_xaxes(title_text="同比增速（%）")
    plotly_chart(fig_rg)

    st.markdown("### 📦 销售渠道结构")
    st.warning("⚠️ 财报未单独披露直销与经销拆分数据，渠道口径合并披露：FY2025营业收入 451,048.44 万元，毛利率 28.95%。")

    st.markdown("### 🗺️ 海外布局进展")
    overseas = pd.DataFrame({
        "区域":     ["欧洲（意大利/德国/西班牙/匈牙利）", "亚洲（印度/日本/韩国/泰国）",
                     "中东（土耳其/阿联酋）",              "美洲（美国/墨西哥）"],
        "布局形式": ["全资子公司+研发中心", "全资子公司+研发中心", "全资子公司", "全资子公司"],
        "战略重点": ["高端制造客户渗透", "借船出海+本地化交付", "新兴市场拓展", "北美市场布局"],
    })
    dataframe(overseas, height=200)

    st.markdown("""
    <div class="insight-box red">
    🌐 <b>【西门子DI警示】汇川境外增速29.89%，H股上市在即：</b>
    汇川境外收入26.49亿元，增速远超境内（21.30%），且正筹划港股上市以拓宽国际融资渠道。
    其在欧洲（意大利、德国、西班牙）已设立全资子公司，正向西门子DI的核心市场渗透。
    西门子DI需在欧洲本土市场加强品牌防御，防止汇川以"中国性价比+本地化服务"组合策略蚕食中小客户。
    </div>
    <div class="insight-box teal">
    🏭 <b>【"借船出海"战略：随中国制造业出海的系统性威胁】</b>
    汇川在纺织、锂电、光伏、物流等行业随中国头部客户出海，在东南亚、中东形成规模化覆盖。
    西门子DI在新兴市场的本土化策略需针对性加强，避免被汇川"跟随式出海"逐步替代。
    </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────
# Tab4：费用与研发
# ─────────────────────────────────────────
def render_tab_rd(data: dict) -> None:
    """渲染费用与研发Tab。"""
    expenses = data["expenses"]
    rd       = data["rd_staff"]

    st.markdown("### 💰 三大费用对比（FY2024 vs FY2025）")
    col1, col2 = st.columns(2)

    with col1:
        fig_exp = go.Figure()
        fig_exp.add_trace(go.Bar(
            name="2024年", x=expenses["费用类型"], y=expenses["2024年"],
            marker_color=COLORS["neutral"],
            text=[f"{v:,.0f}" for v in expenses["2024年"]],
            textposition="outside", textfont=dict(size=10),
            hovertemplate="<b>%{x}</b><br>2024年：%{y:,.0f} 万元<extra></extra>",
        ))
        fig_exp.add_trace(go.Bar(
            name="2025年", x=expenses["费用类型"], y=expenses["2025年"],
            marker_color=COLORS["primary"],
            text=[f"{v:,.0f}" for v in expenses["2025年"]],
            textposition="outside", textfont=dict(size=10),
            hovertemplate="<b>%{x}</b><br>2025年：%{y:,.0f} 万元<extra></extra>",
        ))
        fig_exp.update_layout(**base_layout(
            title="三大费用两年对比（万元）", height=400, barmode="group",
            legend=dict(orientation="h", y=-0.18, x=0.5, xanchor="center",
                        bgcolor="rgba(255,255,255,0.8)", bordercolor="#E0E8F5", borderwidth=1),
        ))
        plotly_chart(fig_exp)

    with col2:
        exp_colors = [COLORS["danger"] if v > 21.77 else COLORS["success"] for v in expenses["增速(%)"]]
        fig_eg = go.Figure(go.Bar(
            x=expenses["费用类型"], y=expenses["增速(%)"],
            marker_color=exp_colors,
            text=[f"{v:+.2f}%" for v in expenses["增速(%)"]],
            textposition="outside", textfont=dict(size=12),
            hovertemplate="<b>%{x}</b><br>增速：%{y:.2f}%<extra></extra>",
        ))
        fig_eg.add_hline(y=21.77, line_dash="dot", line_color=COLORS["primary"], line_width=2,
                         annotation_text="收入增速 21.8%", annotation_position="top right",
                         annotation_font=dict(color=COLORS["primary"], size=11))
        fig_eg.update_layout(**base_layout(title="费用增速 vs 收入增速（%）", height=400), showlegend=False)
        plotly_chart(fig_eg)

    st.markdown("### 🔬 研发投入趋势（近3年）")
    years_rd = ["2023", "2024", "2025"]
    rd_vals  = [rd["研发费用_2023"], rd["研发费用_2024"], rd["研发费用_2025"]]
    rd_rates = [rd["研发费用率_2023"], rd["研发费用率_2024"], rd["研发费用率_2025"]]

    fig_rd = make_subplots(specs=[[{"secondary_y": True}]])
    fig_rd.add_trace(go.Bar(
        x=years_rd, y=rd_vals, name="研发费用（万元）",
        marker_color=COLORS["primary"], opacity=0.85,
        text=[f"{v:,.0f}" for v in rd_vals], textposition="outside",
        hovertemplate="<b>%{x}</b><br>研发费用：%{y:,.0f} 万元<extra></extra>",
    ), secondary_y=False)
    fig_rd.add_trace(go.Scatter(
        x=years_rd, y=rd_rates, name="研发费用率（%）",
        mode="lines+markers+text",
        line=dict(color=COLORS["secondary"], width=2.5),
        marker=dict(symbol="diamond", size=10, color=COLORS["secondary"]),
        text=[f"{v:.2f}%" for v in rd_rates],
        textposition="top center", textfont=dict(size=11, color=COLORS["secondary"]),
        hovertemplate="<b>%{x}</b><br>研发费用率：%{y:.2f}%<extra></extra>",
    ), secondary_y=True)
    fig_rd.update_layout(**base_layout(
        title="研发费用 & 研发费用率（三年趋势）", height=420,
        legend=dict(orientation="h", y=-0.18, x=0.5, xanchor="center",
                    bgcolor="rgba(255,255,255,0.8)", bordercolor="#E0E8F5", borderwidth=1),
    ))
    fig_rd.update_yaxes(title_text="研发费用（万元）", secondary_y=False)
    fig_rd.update_yaxes(title_text="研发费用率（%）", secondary_y=True, range=[7, 12])
    plotly_chart(fig_rd)

    col3, col4, col5 = st.columns(3)
    with col3:
        st.metric("研发人员总数",  f"{rd['研发人员总数']:,} 人",  delta="2025年末")
    with col4:
        st.metric("累计专利及软著", f"{rd['累计专利及软著']:,} 个", delta="含发明专利、实用新型、软著")
    with col5:
        st.metric("研发资本化比例", "0%", delta="全部费用化处理")

    st.warning("⚠️ 财报未单独披露研发人员学历结构及专利分类数量。")

    st.markdown("### 📉 利润拆解瀑布图（FY2025，万元）")
    wf = data["waterfall"]
    fig_wf = go.Figure(go.Waterfall(
        name="利润拆解", orientation="v",
        measure=wf["measure"], x=wf["节点"], y=wf["金额"],
        text=[f"{v:,.0f}" for v in wf["金额"]],
        textposition="outside", textfont=dict(size=10),
        increasing=dict(marker=dict(color=COLORS["success"])),
        decreasing=dict(marker=dict(color=COLORS["danger"])),
        totals=dict(marker=dict(color=COLORS["primary"])),
        connector=dict(line=dict(color=COLORS["grid_color"], width=1.5, dash="dot")),
        hovertemplate="<b>%{x}</b><br>金额：%{y:,.0f} 万元<extra></extra>",
    ))
    fig_wf.update_layout(**base_layout(title="FY2025 利润拆解瀑布图（万元）", height=470), showlegend=False)
    plotly_chart(fig_wf)

    st.markdown("""
    <div class="insight-box red">
    🔬 <b>【研发费用增速35.23%，远超收入增速21.77%：西门子DI的长期威胁信号】</b>
    汇川2025年研发费用42.56亿元，研发费用率提升至9.44%（2024年8.50%），研发人员7,670人。
    汇川正在系统性缩小与西门子DI在技术层面的差距，尤其在运动控制算法、工业AI、数字孪生等领域的追赶速度值得高度警惕。
    </div>
    <div class="insight-box">
    💧 <b>【管理费用增速18.41%：规模扩张带来的效率挑战】</b>
    管理费用18.25亿元，增速18.41%，说明汇川在快速扩张期面临一定管理效率压力。
    西门子DI可在高端客户服务质量上保持差异化优势。
    </div>
    <div class="insight-box green">
    ✅ <b>【财务费用为负：汇川现金充裕，无财务压力】</b>
    财务费用净收益657万元，说明汇川财务状况健康，可持续支撑高强度研发投入和国际化扩张。
    </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────
# Tab5：数据导出
# ─────────────────────────────────────────
def render_tab_export(data: dict) -> None:
    """渲染数据导出Tab。"""
    st.markdown("### 📥 数据导出与查询")

    export_tables = {
        "盈利指标（近3年）":          data["profit"][["年份","营业收入","归母净利润","扣非归母净利润","毛利率","净利率","研发费用率"]],
        "现金流指标（近3年）":        data["cashflow"],
        "资产负债指标（近3年）":      data["balance"][["年份","总资产","归母净资产","负债合计","流动资产","流动负债","资产负债率(%)","流动比率"]],
        "产品线结构（FY2025）":       data["product"][["产品线","营业收入","营业成本","毛利率(%)","收入占比(%)","同比增速(%)"]],
        "分地区数据（FY2025）":       data["region"][["地区","营业收入","毛利率(%)","同比增速(%)"]],
        "分季度数据（FY2025）":       data["quarterly"],
        "产销量数据（FY2025）":       data["volume"][["行业","销售量(PCS)","生产量(PCS)","库存量(PCS)","销售量增速(%)"]],
        "费用对比（FY2024 vs 2025）": data["expenses"],
        "市场份额（弗若斯特沙利文）": data["market_share"],
        "ROE近3年":                   data["roe"],
        "股东回报（近3年）":          data["shareholder"],
    }

    selected = st.selectbox("📋 选择数据表", list(export_tables.keys()))
    df_show  = export_tables[selected].copy()

    keyword = st.text_input("🔍 关键词搜索（过滤行）", placeholder="输入关键词...")
    if keyword:
        mask    = df_show.astype(str).apply(lambda col: col.str.contains(keyword, na=False)).any(axis=1)
        df_show = df_show[mask]

    dataframe(df_show, height=400)

    csv_single = df_show.to_csv(index=False, encoding="utf-8-sig")
    st.download_button(
        label=f"⬇️ 下载当前表格（{selected}）",
        data=csv_single,
        file_name=f"汇川FY2025_{selected}.csv",
        mime="text/csv",
    )

    st.markdown("---")
    all_dfs = []
    for name, df in export_tables.items():
        df_copy = df.copy()
        df_copy.insert(0, "数据表", name)
        all_dfs.append(df_copy)
    csv_all = pd.concat(all_dfs, ignore_index=True).to_csv(index=False, encoding="utf-8-sig")
    st.download_button(
        label="📦 下载全量数据包（所有表格合并CSV）",
        data=csv_all,
        file_name="汇川FY2025_竞争情报全量数据.csv",
        mime="text/csv",
    )

    st.info("""
    📌 **数据说明**
    - **来源**：深圳市汇川技术股份有限公司 2025年年度报告（合并报表口径）
    - **单位**：金额类指标单位为人民币万元；百分比指标已换算
    - **报告期**：2025年1月1日 - 2025年12月31日
    - **审计意见**：信永中和会计师事务所出具标准无保留意见
    - **未披露项**：渠道拆分、存货总额、研发人员学历结构等财报未单独披露，相关字段标注为空
    - **免责声明**：本数据仅供西门子数字化工业内部竞争研究使用，不构成投资建议
    """)

    st.markdown("### 💰 FY2025 利润分配方案")
    d1, d2, d3 = st.columns(3)
    with d1:
        st.metric("每10股现金分红", "5.00 元（含税）", delta="每股 0.50 元")
    with d2:
        st.metric("分红总额", "13.53 亿元（含税）", delta="占归母净利润 26.80%")
    with d3:
        st.metric("分红基准股本", "27.07 亿股", delta="扣除回购股份后")

    st.markdown("### 📈 股息率动态计算")
    price = st.number_input("请输入当前股价（元）", min_value=0.01, value=60.00, step=0.5,
                            help="输入汇川技术（300124.SZ）当前市场价格")
    if price > 0:
        yield_rate = 0.50 / price * 100
        st.metric(
            label=f"股息率（基于股价 {price:.2f} 元）",
            value=f"{yield_rate:.2f}%",
            delta="每股分红 0.50 元（含税）",
        )
        if yield_rate < 1.0:
            st.warning("⚠️ 当前股息率低于1%，汇川以成长性为主要投资逻辑，分红比例相对较低。")
        elif yield_rate >= 2.0:
            st.success("✅ 当前股息率具备一定吸引力。")

# ─────────────────────────────────────────
# 侧边栏
# ─────────────────────────────────────────
def render_sidebar() -> str:
    """渲染侧边栏。"""
    with st.sidebar:
        st.markdown("""
        <div class="sidebar-logo">
            <h2>🏭 汇川技术</h2>
            <p>300124.SZ · 深交所创业板</p>
            <p>竞争情报看板 · FY2025</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("#### 📋 公司概况")
        st.markdown("""
| 项目 | 内容 |
|------|------|
| 全称 | 深圳市汇川技术股份有限公司 |
| 主营 | 工业自动化与数字化、新能源汽车动力系统 |
| 核心产品 | 变频器、伺服系统、PLC/HMI、电驱系统 |
| 总部 | 深圳市龙华区 |
| 上市时间 | 2010年 |
| 实控人 | 朱兴明 |
        """)

        st.markdown("#### 📊 核心数据速览（FY2025）")
        st.markdown("""
| 指标 | 数值 |
|------|------|
| 营业收入 | **451.05亿元** |
| 归母净利润 | **50.50亿元** |
| 毛利率 | **28.95%** |
| 净利率 | **11.20%** |
| 研发费用率 | **9.44%** |
| ROE（加权） | **16.34%** |
| 基本EPS | **1.87元** |
        """)

        st.markdown("#### ⚔️ 与西门子DI竞争重叠度")
        st.error("🔴 高度重叠")
        st.markdown("""
- 伺服系统：**直接竞争**（汇川中国第一）
- 变频器：**直接竞争**（汇川中国第一）
- PLC/HMI：**直接竞争**（汇川追赶中）
- 工业软件/MES：**间接竞争**（InoCube平台）
- 机器人：**间接竞争**（汇川快速扩张）
        """)

        st.markdown("#### 🎯 分析视角")
        view_mode = st.radio("选择分析聚焦方向", ["全面分析", "增长聚焦", "盈利聚焦"], index=0)

        st.markdown("---")
        st.caption("📅 数据截止：2025年12月31日")
        st.caption("📄 数据来源：汇川技术2025年年度报告")
        st.caption("🔒 仅供西门子DI内部使用")

    return view_mode

# ─────────────────────────────────────────
# 主函数
# ─────────────────────────────────────────
def main():
    """主函数：初始化页面、加载数据、渲染各Tab。"""
    st.set_page_config(
        page_title="汇川技术 FY2025 竞争情报看板 | 西门子DI",
        page_icon="🏭",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    inject_css()
    data = load_financial_data()
    render_sidebar()

    st.markdown("""
    <div class="main-header">
        <h1>🏭 汇川技术（300124.SZ）竞争情报看板</h1>
        <p>
        FY2025 年度报告深度分析 ｜ 西门子数字化工业（DI）竞争情报团队专用
        ｜ 数据来源：汇川技术2025年年度报告（合并报表）
        ｜ 数据截止：2025年12月31日
        </p>
    </div>
    """, unsafe_allow_html=True)

    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 CEO概览圈",
        "🏭 产品线分析",
        "🌍 市场与渠道",
        "🔬 费用与研发",
        "📥 数据导出",
    ])

    with tab1: render_tab_ceo(data)
    with tab2: render_tab_product(data)
    with tab3: render_tab_market(data)
    with tab4: render_tab_rd(data)
    with tab5: render_tab_export(data)

if __name__ == "__main__":
    main()

# ============================================================
# 运行说明：
#   pip install streamlit==1.35.0 plotly==5.22.0 pandas==2.2.2 numpy==1.26.4
#   streamlit run inovance_dashboard.py
#
# 免责声明：
#   本看板所有数据均来源于汇川技术公开披露的2025年年度报告，
#   仅供深圳市西门子数字化工业内部竞争研究使用，
#   不构成任何形式的投资建议或商业决策依据。
# ============================================================
