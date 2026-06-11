# =============================================================================
# 深圳市汇川技术股份有限公司 2025年度财报竞争情报看板
# 公司名称：深圳市汇川技术股份有限公司
# 股票代码：300124（深交所创业板）
# 报告期：2025年度（2025-01-01 至 2025-12-31）
# 数据来源：汇川技术2025年年度报告（公开披露）
# 生成时间：2026-06-11
# 使用方：西门子数字化工业（DI）竞争情报团队 · 仅供内部研究使用
# =============================================================================

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np

st.set_page_config(
    page_title="汇川技术 FY2025 竞争情报看板",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =============================================================================
# 配色方案（固定字典）
# =============================================================================
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
PRODUCT_COLORS = ["#1B3A8C", "#2BBFBF", "#5B8DEF", "#27AE60", "#8FA8C8"]
PLOTLY_TEMPLATE = "plotly_white"


# =============================================================================
# A. 数据层
# =============================================================================
def load_financial_data() -> dict:
    """
    数据层：所有DataFrame和dict集中定义。
    所有数值来源于汇川技术2025年年度报告，单位：万元（人民币）。
    派生指标在此计算。
    """

    # ── 一、盈利指标（近3年）──
    profit_df = pd.DataFrame({
        "年份": ["2023年", "2024年", "2025年"],
        "营业收入": [3_041_993, 3_704_095, 4_510_484],
        "归母净利润": [474_186, 428_549, 505_000],
        "扣非归母净利润": [407_118, 403_583, 495_051],
        "研发费用": [262_415, 314_708, 425_577],
        "销售费用": [None, 148_088, 153_557],
        "管理费用": [None, 154_135, 182_508],
    })
    profit_df["净利率"] = profit_df["归母净利润"] / profit_df["营业收入"] * 100
    profit_df["研发费用率"] = profit_df["研发费用"] / profit_df["营业收入"] * 100
    profit_df["销售费用率"] = profit_df["销售费用"] / profit_df["营业收入"] * 100
    profit_df["营收增速"] = profit_df["营业收入"].pct_change() * 100
    profit_df["净利增速"] = profit_df["归母净利润"].pct_change() * 100

    # ── 二、现金流指标 ──
    cashflow_df = pd.DataFrame({
        "年份": ["2023年", "2024年", "2025年"],
        "经营活动现金净流量": [336_992, 720_044, 668_103],
        "归母净利润": [474_186, 428_549, 505_000],
    })
    cashflow_df["现金保障倍数"] = cashflow_df["经营活动现金净流量"] / cashflow_df["归母净利润"] * 100

    # ── 三、资产负债指标 ──
    balance_df = pd.DataFrame({
        "年份": ["2023年末", "2024年末", "2025年末"],
        "总资产": [4_895_756, 5_717_882, 7_131_439],
        "归母净资产": [2_448_189, 2_799_438, 3_535_299],
        "应收账款": [None, 1_071_382, 1_151_881],
        "存货": [None, 695_551, 807_900],
        "ROE": [21.66, 16.52, 16.34],
    })
    balance_df["负债合计"] = balance_df["总资产"] - balance_df["归母净资产"]
    balance_df["资产负债率"] = balance_df["负债合计"] / balance_df["总资产"] * 100

    # ── 四、营运效率（2025年） ──
    ops_data = {
        "存货周转天数": 85.7,
        "应收账款周转天数": 90.0,
        "存货_期初": 695_551,
        "存货_期末": 807_900,
        "应收_期初": 1_071_382,
        "应收_期末": 1_151_881,
    }

    # ── 五、成长指标 ──
    growth_df = pd.DataFrame({
        "年份": ["2024年", "2025年"],
        "营收增速": [21.77, 21.77],
        "净利增速": [-9.60, 17.84],
        "扣非增速": [-0.87, 22.66],
    })
    growth_df["利润弹性系数"] = growth_df["净利增速"] / growth_df["营收增速"]

    # ── 六、分季度数据 ──
    quarterly_df = pd.DataFrame({
        "季度": ["Q1", "Q2", "Q3", "Q4"],
        "营业收入": [897_791, 1_153_145, 1_115_325, 1_344_224],
        "归母净利润": [132_283, 164_556, 128_574, 79_587],
        "扣非净利润": [123_379, 143_765, 121_666, 106_240],
        "经营现金流": [26_255, 275_752, 91_059, 275_037],
    })
    quarterly_df["净利率"] = quarterly_df["归母净利润"] / quarterly_df["营业收入"] * 100

    # ── 七、产品线数据（行业口径） ──
    product_industry_df = pd.DataFrame({
        "产品线": ["智能制造", "新能源汽车", "其他"],
        "2025年收入": [2_404_042, 2_032_258, 74_184],
        "2024年收入": [2_027_731, 1_607_976, 68_388],
        "2025年毛利率": [39.42, 16.10, None],
        "2024年毛利率": [38.12, 16.38, None],
        "2025年占比": [53.30, 45.06, 1.64],
    })
    product_industry_df["同比增速"] = (
        (product_industry_df["2025年收入"] - product_industry_df["2024年收入"])
        / product_industry_df["2024年收入"] * 100
    )

    # ── 八、产品线数据（产品口径） ──
    product_df = pd.DataFrame({
        "产品": ["工业自动化
与数字化", "新能源汽车
动力系统", "新兴产业
(机器人等)", "其他"],
        "2025年收入": [2_224_540, 2_032_258, 179_502, 74_184],
        "2024年收入": [1_872_722, 1_607_976, 155_009, 68_388],
        "2025年毛利率": [40.27, 16.10, None, None],
        "2024年毛利率": [38.62, 16.38, None, None],
        "2025年占比": [49.32, 45.06, 3.98, 1.64],
    })
    product_df["同比增速"] = (
        (product_df["2025年收入"] - product_df["2024年收入"])
        / product_df["2024年收入"] * 100
    )

    # ── 九、地区数据 ──
    region_df = pd.DataFrame({
        "地区": ["中国内地", "境外"],
        "2025年收入": [4_245_595, 264_889],
        "2024年收入": [3_500_162, 203_933],
        "2025年毛利率": [28.55, 29.89],
        "2024年毛利率": [28.54, 31.46],
        "2025年占比": [94.13, 5.87],
    })
    region_df["同比增速"] = (
        (region_df["2025年收入"] - region_df["2024年收入"])
        / region_df["2024年收入"] * 100
    )

    # ── 十、渠道数据（直销/经销合并披露，无拆分） ──
    channel_df = pd.DataFrame({
        "渠道": ["直销/分销（合并）"],
        "2025年收入": [4_510_484],
        "2024年收入": [3_704_095],
        "2025年毛利率": [21.77],
        "占比": [100.0],
    })

    # ── 十一、境内外对比 ──
    geo_df = pd.DataFrame({
        "市场": ["境内", "境外"],
        "收入": [4_245_595, 264_889],
        "占比": [94.13, 5.87],
        "毛利率": [28.55, 29.89],
    })

    # ── 十二、产销量 ──
    volume_df = pd.DataFrame({
        "板块": ["智能制造", "新能源汽车", "其他"],
        "2025年销售量(PCS)": [25_971_863, 5_933_895, 4_490],
        "2025年生产量(PCS)": [25_499_533, 6_108_223, 4_333],
        "2025年库存量(PCS)": [1_361_822, 724_156, 1_303],
        "2024年销售量(PCS)": [19_785_481, 4_619_378, 3_361],
        "2024年生产量(PCS)": [20_084_736, 4_845_348, 3_868],
        "2024年库存量(PCS)": [1_834_152, 549_828, 1_460],
    })

    # ── 十三、费用数据 ──
    expense_df = pd.DataFrame({
        "费用项目": ["销售费用", "管理费用", "研发费用"],
        "2025年（万元）": [153_557, 182_508, 425_577],
        "2024年（万元）": [148_088, 154_135, 314_708],
    })
    expense_df["同比增速"] = (
        (expense_df["2025年（万元）"] - expense_df["2024年（万元）"])
        / expense_df["2024年（万元）"] * 100
    )

    # ── 十四、研发数据 ──
    rd_df = pd.DataFrame({
        "年份": ["2023年", "2024年", "2025年"],
        "研发费用（万元）": [262_415, 314_708, 425_577],
        "研发费用率（%）": [8.63, 8.50, 9.44],
    })

    # ── 十五、研发人员学历结构 ──
    rd_edu_df = pd.DataFrame({
        "学历": ["博士", "硕士", "本科", "大专及以下"],
        "2025年人数": [94, 3_461, 3_290, 777],
        "2024年人数": [58, 2_591, 2_184, 685],
    })

    # ── 十六、分红数据 ──
    dividend_data = {
        "每股分红（元，含税）": 0.50,
        "分红总额（万元）": 135_332,
        "分红比例（%）": 26.8,
        "总股本（股）": 2_706_636_087,
        "基本EPS_2025": 1.87,
        "基本EPS_2024": 1.60,
        "稀释EPS_2025": 1.85,
    }

    # ── 十七、雷达图数据 ──
    radar_df = pd.DataFrame({
        "维度": ["毛利率", "净利率", "研发费用率", "销售费用率", "ROE"],
        "2023年": [None, 15.59, 8.63, None, 21.66],
        "2024年": [28.70, 11.57, 8.50, 4.00, 16.52],
        "2025年": [28.95, 11.20, 9.44, 3.40, 16.34],
    })

    # ── 十八、瀑布图数据（2025年，万元） ──
    waterfall_data = {
        "x": ["营业收入", "营业成本", "毛利润", "销售费用", "管理费用", "研发费用", "财务收益", "其他收益", "归母净利润"],
        "y": [4_510_484, -3_202_000, 1_308_484, -153_557, -182_508, -425_577, 6_572, 714_375, 505_000],
        "measure": ["absolute", "relative", "total", "relative", "relative", "relative", "relative", "relative", "total"],
    }
    # 注：营业成本 = 营业收入 × (1 - 综合毛利率28.95%) ≈ 3,202,000万元（估算）

    return {
        "profit": profit_df,
        "cashflow": cashflow_df,
        "balance": balance_df,
        "ops": ops_data,
        "growth": growth_df,
        "quarterly": quarterly_df,
        "product_industry": product_industry_df,
        "product": product_df,
        "region": region_df,
        "channel": channel_df,
        "geo": geo_df,
        "volume": volume_df,
        "expense": expense_df,
        "rd": rd_df,
        "rd_edu": rd_edu_df,
        "dividend": dividend_data,
        "radar": radar_df,
        "waterfall": waterfall_data,
    }


# =============================================================================
# B. 样式层
# =============================================================================
def inject_css() -> None:
    """注入全局CSS样式，统一看板视觉风格。"""
    st.markdown("""
    <style>
    /* ① 全局背景 */
    .stApp {
        background-color: #F5F7FA;
        color: #1A2B4A;
        font-family: 'Segoe UI','PingFang SC','Microsoft YaHei',sans-serif;
    }

    /* ② 主标题横幅 */
    .main-header {
        background: linear-gradient(135deg, #1B3A8C 0%, #2B5299 60%, #1B3A8C 100%);
        border-left: 6px solid #2BBFBF;
        border-radius: 14px;
        box-shadow: 0 4px 20px rgba(27,58,140,0.18);
        padding: 22px 30px 18px 30px;
        margin-bottom: 20px;
    }
    .main-header h1 {
        color: #FFFFFF;
        font-size: 1.9rem;
        font-weight: 700;
        margin: 0 0 6px 0;
    }
    .main-header p {
        color: #A8C4E8;
        font-size: 0.88rem;
        margin: 0;
    }

    /* ③ KPI卡片 */
    [data-testid="metric-container"] {
        background: #FFFFFF;
        border: 1px solid #E0E8F5;
        border-radius: 12px;
        border-top: 4px solid #1B3A8C;
        box-shadow: 0 2px 12px rgba(27,58,140,0.08);
        padding: 12px 16px;
        transition: box-shadow 0.2s;
    }
    [data-testid="metric-container"]:hover {
        box-shadow: 0 6px 24px rgba(27,58,140,0.15);
    }
    [data-testid="stMetricLabel"] {
        color: #6B7A99 !important;
        font-size: 0.82rem !important;
        font-weight: 600 !important;
    }
    [data-testid="stMetricValue"] {
        color: #1B3A8C !important;
        font-size: 1.5rem !important;
        font-weight: 700 !important;
    }

    /* ④ 隐藏delta箭头图标 */
    [data-testid="stMetricDelta"] svg { display: none; }
    [data-testid="stMetricDelta"] { font-size: 0.8rem; font-weight: 600; }

    /* ⑤ Tab导航 */
    [data-testid="stTabs"] > div:first-child {
        background: #FFFFFF;
        border-radius: 10px;
        border: 1px solid #E0E8F5;
        padding: 4px;
    }
    button[data-baseweb="tab"] {
        color: #6B7A99;
        font-weight: 600;
        font-size: 0.88rem;
        border-radius: 8px;
    }
    button[data-baseweb="tab"][aria-selected="true"] {
        background: #1B3A8C !important;
        color: #FFFFFF !important;
        border-radius: 8px;
    }

    /* ⑥ 侧边栏 */
    [data-testid="stSidebar"] {
        background: #FFFFFF;
        border-right: 2px solid #E0E8F5;
    }

    /* ⑦ h3标题装饰 */
    h3 {
        color: #1B3A8C !important;
        border-bottom: 2px solid #2BBFBF;
        padding-bottom: 6px;
        margin-bottom: 16px !important;
    }

    /* ⑧ Insight洞察框 - 4个变体 */
    .insight-box {
        background: #EEF3FC;
        border-left: 5px solid #1B3A8C;
        border-radius: 10px;
        padding: 13px 18px;
        font-size: 0.87rem;
        margin: 8px 0;
        line-height: 1.6;
    }
    .insight-box.green {
        background: #EAF7F0;
        border-left-color: #27AE60;
    }
    .insight-box.red {
        background: #FEF0EE;
        border-left-color: #E74C3C;
    }
    .insight-box.teal {
        background: #E8F8F8;
        border-left-color: #2BBFBF;
    }

    /* ⑨ 下载按钮 */
    .stDownloadButton > button {
        background: #1B3A8C;
        color: white;
        border: none;
        border-radius: 8px;
        font-weight: 600;
        transition: background 0.2s;
    }
    .stDownloadButton > button:hover {
        background: #2BBFBF;
        color: white;
    }

    /* ⑩ dataframe */
    [data-testid="stDataFrame"] {
        border-radius: 10px;
        border: 1px solid #E0E8F5;
    }

    /* 侧边栏logo区 */
    .sidebar-logo {
        background: linear-gradient(135deg, #1B3A8C, #2B5299);
        border-radius: 12px;
        padding: 16px;
        text-align: center;
        margin-bottom: 16px;
        color: white;
    }
    .sidebar-logo .company-name {
        font-size: 1.1rem;
        font-weight: 700;
        color: #FFFFFF;
    }
    .sidebar-logo .ticker {
        font-size: 0.8rem;
        color: #A8C4E8;
    }
    .sidebar-logo .dashboard-title {
        font-size: 0.75rem;
        color: #2BBFBF;
        margin-top: 4px;
    }
    </style>
    """, unsafe_allow_html=True)


# =============================================================================
# C. 图表统一布局
# =============================================================================
def base_layout(**kwargs) -> dict:
    """图表统一布局配置，所有plotly图表调用此函数获取基础layout参数。"""
    layout = dict(
        template=PLOTLY_TEMPLATE,
        paper_bgcolor=COLORS["card_bg"],
        plot_bgcolor=COLORS["plot_bg"],
        font=dict(
            family="Segoe UI, PingFang SC, Microsoft YaHei",
            color=COLORS["text_dark"],
            size=12
        ),
        title_font=dict(
            color=COLORS["primary"],
            size=14,
            family="Segoe UI, PingFang SC"
        ),
        xaxis=dict(
            gridcolor=COLORS["grid_color"],
            linecolor="#D0DAF0",
            tickcolor="#D0DAF0"
        ),
        yaxis=dict(
            gridcolor=COLORS["grid_color"],
            linecolor="#D0DAF0",
            tickcolor="#D0DAF0"
        ),
        margin=dict(t=55, b=40, l=40, r=30),
    )
    layout.update(kwargs)
    return layout


# =============================================================================
# D. KPI卡片组件
# =============================================================================
def kpi_card(col, label: str, value: str, delta: str = None,
             delta_val: str = None, note: str = None) -> None:
    """
    KPI卡片组件。
    col: st.column对象
    label: 指标名称
    value: 主要数值（字符串）
    delta: delta颜色方向（'normal'/'inverse'）
    delta_val: delta显示文字
    note: 卡片底部备注
    """
    with col:
        st.metric(label=label, value=value, delta=delta_val)
        if note:
            st.caption(note)


# =============================================================================
# Tab1：CEO概览圈
# =============================================================================
def render_tab_ceo(data: dict) -> None:
    """Tab1：CEO概览圈 - 核心财务KPI、三年趋势、雷达图、季度节奏。"""

    profit = data["profit"]
    quarterly = data["quarterly"]
    radar = data["radar"]
    balance = data["balance"]
    cashflow = data["cashflow"]

    # ── 第一行：6个KPI卡片 ──
    st.markdown("### 📊 核心经营指标（FY2025）")
    c1, c2, c3, c4, c5, c6 = st.columns(6)
    kpi_card(c1, "营业总收入", "451.05亿元", note="同比 +21.77%")
    kpi_card(c2, "归母净利润", "50.50亿元", note="同比 +17.84%")
    kpi_card(c3, "扣非归母净利润", "49.51亿元", note="同比 +22.66%")
    kpi_card(c4, "研发投入", "42.56亿元", note="研发费用率 9.44%")
    kpi_card(c5, "基本EPS", "1.87 元/股", note="同比 +16.88%")
    kpi_card(c6, "现金分红比例", "26.8%", note="每股0.50元（含税）")

    st.markdown("<br>", unsafe_allow_html=True)

    # ── 第二行：4个资产健康度卡片 ──
    st.markdown("### 🏦 资产健康度（FY2025末）")
    a1, a2, a3, a4 = st.columns(4)
    kpi_card(a1, "总资产", "713.14亿元", note="同比 +24.72%")
    kpi_card(a2, "归母净资产", "353.53亿元", note="同比 +26.29%")
    kpi_card(a3, "加权平均ROE", "16.34%", note="较2024年 -0.18pct")
    kpi_card(a4, "境外业务增速", "+29.89%", note="境外收入占比5.87%")

    st.markdown("<br>", unsafe_allow_html=True)

    # ── 第三行：三年趋势双轴图 + 雷达图 ──
    st.markdown("### 📈 三年财务趋势 & 盈利质量雷达")
    col_left, col_right = st.columns([3, 2])

    with col_left:
        fig_trend = make_subplots(specs=[[{"secondary_y": True}]])

        # 柱状：营业收入
        fig_trend.add_trace(
            go.Bar(
                x=profit["年份"],
                y=profit["营业收入"],
                name="营业收入（万元）",
                marker_color=COLORS["primary"],
                opacity=0.82,
                hovertemplate="<b>%{x}</b><br>营业收入：%{y:,.0f} 万元<extra></extra>",
                text=[f"{v/10000:.1f}亿" for v in profit["营业收入"]],
                textposition="outside",
                textfont=dict(size=11, color=COLORS["primary"]),
            ),
            secondary_y=False,
        )

        # 折线：归母净利润
        fig_trend.add_trace(
            go.Scatter(
                x=profit["年份"],
                y=profit["归母净利润"],
                name="归母净利润（万元）",
                mode="lines+markers+text",
                line=dict(color=COLORS["secondary"], width=2.5),
                marker=dict(symbol="diamond", size=10, color=COLORS["secondary"]),
                text=[f"{v/10000:.1f}亿" for v in profit["归母净利润"]],
                textposition="top center",
                textfont=dict(size=10),
                hovertemplate="<b>%{x}</b><br>归母净利润：%{y:,.0f} 万元<extra></extra>",
            ),
            secondary_y=False,
        )

        # 右轴折线：净利率
        fig_trend.add_trace(
            go.Scatter(
                x=profit["年份"],
                y=profit["净利率"],
                name="净利率（%）",
                mode="lines+markers",
                line=dict(color=COLORS["success"], width=2, dash="dot"),
                marker=dict(size=7, color=COLORS["success"]),
                hovertemplate="<b>%{x}</b><br>净利率：%{y:.2f}%<extra></extra>",
            ),
            secondary_y=True,
        )

        fig_trend.update_layout(
            **base_layout(
                title="营业收入 / 归母净利润 / 净利率（三年趋势）",
                height=420,
                legend=dict(
                    orientation="h", y=-0.18, x=0.5, xanchor="center",
                    bgcolor="rgba(255,255,255,0.8)",
                    bordercolor="#E0E8F5", borderwidth=1
                )
            )
        )
        fig_trend.update_yaxes(
            title_text="金额（万元）",
            gridcolor=COLORS["grid_color"],
            linecolor="#D0DAF0",
            secondary_y=False
        )
        fig_trend.update_yaxes(
            title_text="净利率（%）",
            gridcolor=COLORS["grid_color"],
            linecolor="#D0DAF0",
            secondary_y=True
        )
        st.plotly_chart(fig_trend, use_container_width=True)

    with col_right:
        radar_dims = radar["维度"].tolist()
        radar_dims_closed = radar_dims + [radar_dims[0]]

        def safe_vals(col_name):
            vals = radar[col_name].tolist()
            vals_closed = vals + [vals[0]]
            return [v if v is not None else 0 for v in vals_closed]

        fig_radar = go.Figure()
        configs = [
            ("2023年", COLORS["neutral"], "dot"),
            ("2024年", COLORS["secondary"], "dash"),
            ("2025年", COLORS["primary"], "solid"),
        ]
        for year, color, dash in configs:
            fig_radar.add_trace(go.Scatterpolar(
                r=safe_vals(year),
                theta=radar_dims_closed,
                fill="toself",
                name=year,
                line=dict(color=color, dash=dash, width=2),
                fillcolor=color.replace("#", "rgba(").replace(")", ",0.12)") if "#" in color else color,
                opacity=0.85,
                hovertemplate="<b>%{theta}</b><br>数值：%{r:.2f}%<extra></extra>",
            ))

        fig_radar.update_layout(
            **base_layout(
                title="盈利质量雷达图（三年对比）",
                height=420,
                polar=dict(
                    radialaxis=dict(
                        visible=True,
                        range=[0, 45],
                        gridcolor=COLORS["grid_color"],
                    ),
                    angularaxis=dict(gridcolor=COLORS["grid_color"])
                ),
                legend=dict(
                    orientation="h", y=-0.15, x=0.5, xanchor="center",
                    bgcolor="rgba(255,255,255,0.8)",
                    bordercolor="#E0E8F5", borderwidth=1
                )
            )
        )
        st.plotly_chart(fig_radar, use_container_width=True)

    # ── 第四行：季度营收节奏 ──
    st.markdown("### 🗓️ 分季度营收节奏（FY2025）")
    fig_q = make_subplots(
        rows=1, cols=2,
        subplot_titles=("季度营业收入（万元）", "季度净利率（%）"),
        horizontal_spacing=0.1
    )

    q_colors = [COLORS["neutral"], COLORS["primary"], COLORS["primary"], COLORS["secondary"]]
    fig_q.add_trace(
        go.Bar(
            x=quarterly["季度"],
            y=quarterly["营业收入"],
            marker_color=q_colors,
            name="季度营收",
            hovertemplate="<b>%{x}</b><br>营业收入：%{y:,.0f} 万元<extra></extra>",
            text=[f"{v/10000:.1f}亿" for v in quarterly["营业收入"]],
            textposition="outside",
        ),
        row=1, col=1
    )
    fig_q.add_trace(
        go.Scatter(
            x=quarterly["季度"],
            y=quarterly["净利率"],
            mode="lines+markers+text",
            line=dict(color=COLORS["secondary"], width=2.5),
            marker=dict(size=9, color=COLORS["secondary"]),
            name="季度净利率",
            text=[f"{v:.1f}%" for v in quarterly["净利率"]],
            textposition="top center",
            hovertemplate="<b>%{x}</b><br>净利率：%{y:.2f}%<extra></extra>",
        ),
        row=1, col=2
    )
    fig_q.update_layout(
        **base_layout(height=400, showlegend=False,
                      title="分季度营收与盈利节奏（FY2025）")
    )
    fig_q.update_yaxes(gridcolor=COLORS["grid_color"], linecolor="#D0DAF0")
    fig_q.update_xaxes(gridcolor=COLORS["grid_color"], linecolor="#D0DAF0")
    st.plotly_chart(fig_q, use_container_width=True)

    # ── Insight洞察框 ──
    st.markdown("### 💡 竞争情报洞察")
    st.markdown("""
    <div class="insight-box green">
    ⚡ <b>营收规模突破451亿元，同比+21.77%</b>，连续两年保持20%以上高增速，
    说明汇川技术在工控+新能源双赛道已形成规模化增长飞轮。
    <b>西门子DI视角：</b>汇川在中国市场的营收体量已接近西门子DI中国区业务量级，
    需高度警惕其在中低端工控市场的价格渗透和客户锁定速度。
    </div>
    <br>
    <div class="insight-box red">
    ⚠️ <b>净利率从2023年15.59%降至2025年11.20%</b>，ROE从21.66%降至16.34%，
    说明新能源汽车业务（毛利率仅16.10%）的高速扩张正在稀释整体盈利质量。
    <b>西门子DI视角：</b>这是汇川的结构性隐患——若新能源汽车竞争进一步加剧，
    其利润空间将持续承压，工业自动化业务需承担更多利润补偿责任。
    </div>
    <br>
    <div class="insight-box teal">
    🔍 <b>Q4净利润仅7.96亿元，净利率5.92%</b>，远低于Q1-Q3均值，
    说明Q4存在明显的费用集中确认（研发/管理费用冲刺）或计提压力。
    <b>西门子DI视角：</b>Q4是汇川客户决策和预算执行的关键窗口期，
    西门子DI可在Q3末加强客户拜访和方案锁定，抢占预算份额。
    </div>
    """, unsafe_allow_html=True)


# =============================================================================
# Tab2：产品线分析
# =============================================================================
def render_tab_product(data: dict) -> None:
    """Tab2：产品线分析 - 收入占比、毛利率、增速、产销量。"""

    product = data["product"]
    product_ind = data["product_industry"]
    volume = data["volume"]

    st.markdown("### 🏭 产品线收入结构（FY2025）")

    col1, col2 = st.columns([1, 1])

    with col1:
        # 环形饼图：产品线收入占比
        labels = ["工业自动化
与数字化", "新能源汽车
动力系统", "新兴产业
(机器人等)", "其他"]
        values = [2_224_540, 2_032_258, 179_502, 74_184]
        pie_colors = PRODUCT_COLORS[:4]

        fig_pie = go.Figure(go.Pie(
            labels=labels,
            values=values,
            hole=0.52,
            marker=dict(colors=pie_colors, line=dict(color="#FFFFFF", width=2)),
            textinfo="label+percent",
            textfont=dict(size=11),
            hovertemplate="<b>%{label}</b><br>收入：%{value:,.0f} 万元<br>占比：%{percent}<extra></extra>",
        ))
        fig_pie.add_annotation(
            text="<b>总收入</b><br>451.05亿元",
            x=0.5, y=0.5,
            font=dict(size=13, color=COLORS["primary"]),
            showarrow=False
        )
        fig_pie.update_layout(
            **base_layout(title="产品线收入占比（FY2025）", height=340, showlegend=False)
        )
        st.plotly_chart(fig_pie, use_container_width=True)

    with col2:
        # 产品线增速水平柱状图
        prod_names = ["工业自动化
与数字化", "新能源汽车
动力系统", "新兴产业
(机器人等)", "其他"]
        growth_vals = [18.79, 26.39, 15.80, 8.47]
        overall_growth = 21.77
        bar_colors = [COLORS["success"] if v >= 0 else COLORS["danger"] for v in growth_vals]

        fig_growth = go.Figure(go.Bar(
            y=prod_names,
            x=growth_vals,
            orientation="h",
            marker_color=bar_colors,
            text=[f"{v:+.2f}%" for v in growth_vals],
            textposition="outside",
            hovertemplate="<b>%{y}</b><br>同比增速：%{x:.2f}%<extra></extra>",
        ))
        fig_growth.add_vline(x=0, line_dash="dash", line_color=COLORS["text_muted"], line_width=1)
        fig_growth.add_vline(
            x=overall_growth, line_dash="dot",
            line_color=COLORS["primary"], line_width=2,
            annotation_text=f"整体增速 {overall_growth:.1f}%",
            annotation_position="top right",
            annotation_font=dict(color=COLORS["primary"], size=11)
        )
        fig_growth.update_layout(
            **base_layout(title="产品线同比增速（FY2025）", height=340, showlegend=False)
        )
        st.plotly_chart(fig_growth, use_container_width=True)

    # 双轴图：产品线收入柱状 + 毛利率折线
    st.markdown("### 💰 产品线收入 vs 毛利率")
    fig_dual = make_subplots(specs=[[{"secondary_y": True}]])

    prod_labels_short = ["工业自动化
与数字化", "新能源汽车
动力系统"]
    revenues_25 = [2_224_540, 2_032_258]
    revenues_24 = [1_872_722, 1_607_976]
    margins_25 = [40.27, 16.10]
    margins_24 = [38.62, 16.38]

    fig_dual.add_trace(
        go.Bar(x=prod_labels_short, y=revenues_24, name="2024年收入",
               marker_color=COLORS["neutral"], opacity=0.75,
               hovertemplate="<b>%{x}</b><br>2024年收入：%{y:,.0f} 万元<extra></extra>"),
        secondary_y=False
    )
    fig_dual.add_trace(
        go.Bar(x=prod_labels_short, y=revenues_25, name="2025年收入",
               marker_color=COLORS["primary"], opacity=0.85,
               hovertemplate="<b>%{x}</b><br>2025年收入：%{y:,.0f} 万元<extra></extra>"),
        secondary_y=False
    )
    fig_dual.add_trace(
        go.Scatter(x=prod_labels_short, y=margins_25, name="2025年毛利率",
                   mode="markers+lines+text",
                   marker=dict(symbol="star", size=13, color=COLORS["secondary"]),
                   line=dict(color=COLORS["secondary"], width=2),
                   text=[f"{v:.1f}%" for v in margins_25],
                   textposition="top center",
                   hovertemplate="<b>%{x}</b><br>2025年毛利率：%{y:.2f}%<extra></extra>"),
        secondary_y=True
    )
    fig_dual.add_trace(
        go.Scatter(x=prod_labels_short, y=margins_24, name="2024年毛利率",
                   mode="markers+lines",
                   marker=dict(symbol="star", size=10, color=COLORS["neutral"]),
                   line=dict(color=COLORS["neutral"], width=1.5, dash="dot"),
                   hovertemplate="<b>%{x}</b><br>2024年毛利率：%{y:.2f}%<extra></extra>"),
        secondary_y=True
    )
    fig_dual.update_layout(
        **base_layout(title="主要产品线收入 & 毛利率对比（FY2024 vs FY2025）",
                      height=400, barmode="group",
                      legend=dict(orientation="h", y=-0.18, x=0.5, xanchor="center",
                                  bgcolor="rgba(255,255,255,0.8)",
                                  bordercolor="#E0E8F5", borderwidth=1))
    )
    fig_dual.update_yaxes(title_text="收入（万元）", secondary_y=False,
                          gridcolor=COLORS["grid_color"])
    fig_dual.update_yaxes(title_text="毛利率（%）", secondary_y=True,
                          gridcolor=COLORS["grid_color"])
    st.plotly_chart(fig_dual, use_container_width=True)

    # 产销量分组柱状图
    st.markdown("### 📦 主要产品产销量对比（FY2025 vs FY2024）")
    vol_labels = ["智能制造", "新能源汽车"]
    sales_25 = [25_971_863, 5_933_895]
    prod_25 = [25_499_533, 6_108_223]
    inv_25 = [1_361_822, 724_156]
    sales_24 = [19_785_481, 4_619_378]

    fig_vol = go.Figure()
    fig_vol.add_trace(go.Bar(
        name="2025年销售量", x=vol_labels, y=sales_25,
        marker_color=COLORS["primary"],
        text=[f"{v:,.0f}" for v in sales_25], textposition="outside",
        hovertemplate="<b>%{x}</b><br>2025年销售量：%{y:,.0f} PCS<extra></extra>"
    ))
    fig_vol.add_trace(go.Bar(
        name="2025年生产量", x=vol_labels, y=prod_25,
        marker_color=COLORS["secondary"],
        hovertemplate="<b>%{x}</b><br>2025年生产量：%{y:,.0f} PCS<extra></extra>"
    ))
    fig_vol.add_trace(go.Bar(
        name="2024年销售量", x=vol_labels, y=sales_24,
        marker_color=COLORS["neutral"],
        hovertemplate="<b>%{x}</b><br>2024年销售量：%{y:,.0f} PCS<extra></extra>"
    ))
    fig_vol.update_layout(
        **base_layout(title="主要产品产销量对比（PCS）", height=400, barmode="group",
                      legend=dict(orientation="h", y=-0.18, x=0.5, xanchor="center",
                                  bgcolor="rgba(255,255,255,0.8)",
                                  bordercolor="#E0E8F5", borderwidth=1))
    )
    st.plotly_chart(fig_vol, use_container_width=True)

    # Insight
    st.markdown("### 💡 竞争情报洞察")
    st.markdown("""
    <div class="insight-box green">
    ⚡ <b>工业自动化与数字化产品毛利率40.27%，同比提升1.65pct</b>，
    说明汇川在工控核心产品上的定价能力持续增强，已具备与日系品牌正面竞争的毛利水平。
    <b>西门子DI视角：</b>汇川工控产品的毛利率已接近西门子DI中端产品线水平，
    需在高端应用场景（精密运动控制、功能安全、工业软件集成）构建差异化壁垒。
    </div>
    <br>
    <div class="insight-box red">
    ⚠️ <b>新能源汽车业务收入占比已达45.06%，毛利率仅16.10%</b>，
    说明汇川正面临"增收不增利"的结构性压力，主机厂降本压力持续向供应链传导。
    <b>西门子DI视角：</b>这是汇川的战略软肋——若新能源汽车市场竞争加剧，
    其整体盈利能力将受到严重拖累，西门子DI可借此强调工业软件和高端自动化的高价值定位。
    </div>
    <br>
    <div class="insight-box teal">
    🔍 <b>智能制造板块销售量同比+31.27%，远超收入增速18.79%</b>，
    说明单价在下降，量增价降趋势明显，可能反映汇川在中低端市场的以量换市策略。
    <b>西门子DI视角：</b>这一趋势在PLC、变频器等标准化产品上尤为突出，
    西门子DI应加速在高端定制化、行业解决方案等高附加值领域的布局。
    </div>
    """, unsafe_allow_html=True)


# =============================================================================
# Tab3：市场与渠道
# =============================================================================
def render_tab_market(data: dict) -> None:
    """Tab3：市场与渠道 - 地区分布、增速、境内外对比。"""

    region = data["region"]
    geo = data["geo"]

    st.markdown("### 🌏 地区收入分布（FY2025）")

    col1, col2 = st.columns([3, 2])

    with col1:
        # 水平柱状图 + 毛利率散点（双X轴）
        fig_region = make_subplots(specs=[[{"secondary_y": False}]])

        fig_region.add_trace(go.Bar(
            y=region["地区"],
            x=region["2025年收入"],
            orientation="h",
            name="2025年收入（万元）",
            marker_color=[COLORS["primary"], COLORS["secondary"]],
            text=[f"{v/10000:.1f}亿" for v in region["2025年收入"]],
            textposition="outside",
            hovertemplate="<b>%{y}</b><br>收入：%{x:,.0f} 万元<extra></extra>",
        ))

        fig_region.update_layout(
            **base_layout(title="地区收入分布（FY2025）", height=340, showlegend=False)
        )
        st.plotly_chart(fig_region, use_container_width=True)

        # 毛利率对比
        fig_margin = go.Figure()
        fig_margin.add_trace(go.Bar(
            x=region["地区"],
            y=region["2024年毛利率"],
            name="2024年毛利率",
            marker_color=COLORS["neutral"],
            hovertemplate="<b>%{x}</b><br>2024年毛利率：%{y:.2f}%<extra></extra>",
        ))
        fig_margin.add_trace(go.Bar(
            x=region["地区"],
            y=region["2025年毛利率"],
            name="2025年毛利率",
            marker_color=COLORS["primary"],
            text=[f"{v:.2f}%" for v in region["2025年毛利率"]],
            textposition="outside",
            hovertemplate="<b>%{x}</b><br>2025年毛利率：%{y:.2f}%<extra></extra>",
        ))
        fig_margin.update_layout(
            **base_layout(title="地区毛利率对比（FY2024 vs FY2025）", height=340,
                          barmode="group",
                          legend=dict(orientation="h", y=-0.18, x=0.5, xanchor="center",
                                      bgcolor="rgba(255,255,255,0.8)",
                                      bordercolor="#E0E8F5", borderwidth=1))
        )
        st.plotly_chart(fig_margin, use_container_width=True)

    with col2:
        # 地区增速
        overall_growth = 21.77
        growth_colors = [
            COLORS["success"] if v >= overall_growth else COLORS["primary"]
            for v in region["同比增速"]
        ]
        fig_rgrowth = go.Figure(go.Bar(
            y=region["地区"],
            x=region["同比增速"],
            orientation="h",
            marker_color=growth_colors,
            text=[f"{v:+.2f}%" for v in region["同比增速"]],
            textposition="outside",
            hovertemplate="<b>%{y}</b><br>同比增速：%{x:.2f}%<extra></extra>",
        ))
        fig_rgrowth.add_vline(
            x=overall_growth, line_dash="dot",
            line_color=COLORS["primary"], line_width=2,
            annotation_text=f"整体增速 {overall_growth:.1f}%",
            annotation_position="top right",
            annotation_font=dict(color=COLORS["primary"], size=11)
        )
        fig_rgrowth.update_layout(
            **base_layout(title="地区增速（FY2025）", height=340, showlegend=False)
        )
        st.plotly_chart(fig_rgrowth, use_container_width=True)

        # 境内外环形饼图
        fig_geo = go.Figure(go.Pie(
            labels=geo["市场"],
            values=geo["收入"],
            hole=0.52,
            marker=dict(
                colors=[COLORS["primary"], COLORS["secondary"]],
                line=dict(color="#FFFFFF", width=2)
            ),
            textinfo="label+percent",
            hovertemplate="<b>%{label}</b><br>收入：%{value:,.0f} 万元<br>占比：%{percent}<extra></extra>",
        ))
        fig_geo.add_annotation(
            text="<b>境内/境外</b><br>收入占比",
            x=0.5, y=0.5,
            font=dict(size=11, color=COLORS["primary"]),
            showarrow=False
        )
        fig_geo.update_layout(
            **base_layout(title="境内 vs 境外收入占比", height=340, showlegend=False)
        )
        st.plotly_chart(fig_geo, use_container_width=True)

    # 渠道说明
    st.markdown("### 📢 销售渠道说明")
    st.info("""
    📌 **渠道披露说明**：汇川技术2025年年度报告中，销售模式按"直销/分销"合并披露，
    未单独拆分直销与经销的收入及毛利率数据。全部营业收入4,510,484万元均归入"直销/分销"口径。
    如需渠道细分数据，请参考公司投资者关系公告或电话会议纪要。
    """)

    # Insight
    st.markdown("### 💡 竞争情报洞察")
    st.markdown("""
    <div class="insight-box red">
    ⚠️ <b>境外收入占比仅5.87%（约26.5亿元），同比增速+29.89%</b>，
    说明汇川的国际化进程仍处于早期阶段，海外市场尚未形成规模。
    <b>西门子DI视角：</b>在全球市场，汇川尚不构成直接威胁；
    但其海外增速接近30%，若持续3-5年，将在东南亚、中东等新兴市场形成竞争压力，
    西门子DI需提前布局这些区域的服务网络和本地化能力。
    </div>
    <br>
    <div class="insight-box green">
    ⚡ <b>中国内地收入4,245,595万元，同比+21.30%，毛利率28.55%</b>，
    说明汇川在本土市场的规模优势和渠道深度持续强化。
    <b>西门子DI视角：</b>汇川在中国内地的渠道覆盖密度和响应速度是其核心竞争力，
    西门子DI需在关键行业（锂电、光伏、汽车）加强本地化服务能力和快速响应机制。
    </div>
    <br>
    <div class="insight-box teal">
    🔍 <b>境外毛利率29.89%略高于境内28.55%</b>，
    说明汇川在海外市场尚未陷入价格战，仍保持相对合理的定价。
    <b>西门子DI视角：</b>这意味着汇川在海外市场的竞争策略仍以品牌建设为主，
    西门子DI在海外市场的价格优势窗口期有限，需加速在技术壁垒和行业认证上的差异化。
    </div>
    """, unsafe_allow_html=True)


# =============================================================================
# Tab4：费用与研发
# =============================================================================
def render_tab_rd(data: dict) -> None:
    """Tab4：费用与研发 - 三大费用、研发趋势、人员结构、利润瀑布图。"""

    expense = data["expense"]
    rd = data["rd"]
    rd_edu = data["rd_edu"]
    waterfall = data["waterfall"]

    st.markdown("### 💸 三大费用对比（FY2024 vs FY2025）")
    col1, col2 = st.columns(2)

    with col1:
        # 分组柱状图：三大费用两年对比
        fig_exp = go.Figure()
        fig_exp.add_trace(go.Bar(
            x=expense["费用项目"],
            y=expense["2024年（万元）"],
            name="2024年",
            marker_color=COLORS["neutral"],
            hovertemplate="<b>%{x}</b><br>2024年：%{y:,.0f} 万元<extra></extra>",
        ))
        fig_exp.add_trace(go.Bar(
            x=expense["费用项目"],
            y=expense["2025年（万元）"],
            name="2025年",
            marker_color=COLORS["primary"],
            text=[f"{v/10000:.1f}亿" for v in expense["2025年（万元）"]],
            textposition="outside",
            hovertemplate="<b>%{x}</b><br>2025年：%{y:,.0f} 万元<extra></extra>",
        ))
        fig_exp.update_layout(
            **base_layout(title="三大费用对比（FY2024 vs FY2025）", height=400,
                          barmode="group",
                          legend=dict(orientation="h", y=-0.18, x=0.5, xanchor="center",
                                      bgcolor="rgba(255,255,255,0.8)",
                                      bordercolor="#E0E8F5", borderwidth=1))
        )
        st.plotly_chart(fig_exp, use_container_width=True)

    with col2:
        # 费用增速柱状图
        revenue_growth = 21.77
        exp_growth_colors = [
            COLORS["danger"] if v > revenue_growth else COLORS["success"]
            for v in expense["同比增速"]
        ]
        fig_exp_g = go.Figure(go.Bar(
            x=expense["费用项目"],
            y=expense["同比增速"],
            marker_color=exp_growth_colors,
            text=[f"{v:+.2f}%" for v in expense["同比增速"]],
            textposition="outside",
            hovertemplate="<b>%{x}</b><br>同比增速：%{y:.2f}%<extra></extra>",
        ))
        fig_exp_g.add_hline(
            y=revenue_growth, line_dash="dot",
            line_color=COLORS["primary"], line_width=2,
            annotation_text=f"营收增速 {revenue_growth:.1f}%",
            annotation_position="top right",
            annotation_font=dict(color=COLORS["primary"], size=11)
        )
        fig_exp_g.update_layout(
            **base_layout(title="费用增速 vs 营收增速（FY2025）", height=400, showlegend=False)
        )
        st.plotly_chart(fig_exp_g, use_container_width=True)

    # 研发费用趋势双轴图
    st.markdown("### 🔬 研发费用趋势（近3年）")
    col3, col4 = st.columns(2)

    with col3:
        fig_rd = make_subplots(specs=[[{"secondary_y": True}]])
        fig_rd.add_trace(
            go.Bar(x=rd["年份"], y=rd["研发费用（万元）"],
                   name="研发费用（万元）",
                   marker_color=COLORS["primary"], opacity=0.82,
                   text=[f"{v/10000:.1f}亿" for v in rd["研发费用（万元）"]],
                   textposition="outside",
                   hovertemplate="<b>%{x}</b><br>研发费用：%{y:,.0f} 万元<extra></extra>"),
            secondary_y=False
        )
        fig_rd.add_trace(
            go.Scatter(x=rd["年份"], y=rd["研发费用率（%）"],
                       name="研发费用率（%）",
                       mode="lines+markers+text",
                       line=dict(color=COLORS["secondary"], width=2.5),
                       marker=dict(symbol="diamond", size=10, color=COLORS["secondary"]),
                       text=[f"{v:.2f}%" for v in rd["研发费用率（%）"]],
                       textposition="top center",
                       hovertemplate="<b>%{x}</b><br>研发费用率：%{y:.2f}%<extra></extra>"),
            secondary_y=True
        )
        fig_rd.update_layout(
            **base_layout(title="研发费用 & 研发费用率趋势", height=400,
                          legend=dict(orientation="h", y=-0.18, x=0.5, xanchor="center",
                                      bgcolor="rgba(255,255,255,0.8)",
                                      bordercolor="#E0E8F5", borderwidth=1))
        )
        fig_rd.update_yaxes(title_text="研发费用（万元）", secondary_y=False,
                            gridcolor=COLORS["grid_color"])
        fig_rd.update_yaxes(title_text="研发费用率（%）", secondary_y=True,
                            gridcolor=COLORS["grid_color"])
        st.plotly_chart(fig_rd, use_container_width=True)

    with col4:
        # 研发人员学历结构环形饼图
        edu_labels = rd_edu["学历"].tolist()
        edu_vals_25 = rd_edu["2025年人数"].tolist()
        fig_edu = go.Figure(go.Pie(
            labels=edu_labels,
            values=edu_vals_25,
            hole=0.42,
            marker=dict(
                colors=PRODUCT_COLORS[:4],
                line=dict(color="#FFFFFF", width=2)
            ),
            textinfo="label+percent+value",
            textfont=dict(size=11),
            hovertemplate="<b>%{label}</b><br>人数：%{value} 人<br>占比：%{percent}<extra></extra>",
        ))
        fig_edu.add_annotation(
            text=f"<b>研发人员</b><br>7,670人",
            x=0.5, y=0.5,
            font=dict(size=12, color=COLORS["primary"]),
            showarrow=False
        )
        fig_edu.update_layout(
            **base_layout(title="研发人员学历结构（FY2025）", height=400, showlegend=False)
        )
        st.plotly_chart(fig_edu, use_container_width=True)

    # 利润瀑布图
    st.markdown("### 🌊 利润瀑布图（FY2025，万元）")
    wf = waterfall

    increasing_color = COLORS["success"]
    decreasing_color = COLORS["danger"]
    total_color = COLORS["primary"]

    fig_wf = go.Figure(go.Waterfall(
        name="利润瀑布",
        orientation="v",
        measure=wf["measure"],
        x=wf["x"],
        y=wf["y"],
        text=[f"{v:+,.0f}" if m == "relative" else f"{abs(v):,.0f}"
              for v, m in zip(wf["y"], wf["measure"])],
        textposition="outside",
        textfont=dict(size=10),
        increasing=dict(marker=dict(color=increasing_color)),
        decreasing=dict(marker=dict(color=decreasing_color)),
        totals=dict(marker=dict(color=total_color)),
        connector=dict(line=dict(color=COLORS["grid_color"], width=1.5, dash="dot")),
        hovertemplate="<b>%{x}</b><br>金额：%{y:,.0f} 万元<extra></extra>",
    ))
    fig_wf.update_layout(
        **base_layout(
            title="FY2025 利润瀑布图（营业收入 → 归母净利润，万元）",
            height=470,
            showlegend=False,
        )
    )
    st.plotly_chart(fig_wf, use_container_width=True)
    st.caption("⚠️ 注：营业成本为估算值（营业收入×(1-综合毛利率28.95%)≈3,202,000万元）；其他收益含政府补助等非经常性项目。")

    # Insight
    st.markdown("### 💡 竞争情报洞察")
    st.markdown("""
    <div class="insight-box red">
    ⚠️ <b>研发费用同比+35.23%（42.56亿元），远超营收增速21.77%</b>，
    研发费用率从8.50%提升至9.44%，说明汇川正在加速研发投入以缩小与国际品牌的技术差距。
    <b>西门子DI视角：</b>汇川在工业软件、控制层核心技术上的研发提速是最值得关注的信号，
    西门子DI需持续强化在数字孪生、工业AI、功能安全等高端技术领域的领先优势。
    </div>
    <br>
    <div class="insight-box green">
    ⚡ <b>研发人员从5,538人增至7,670人（+38.5%），硕士占比高达45.1%</b>，
    说明汇川正在系统性地提升研发团队质量，而非单纯扩充人数。
    <b>西门子DI视角：</b>汇川的高学历研发团队将在2-3年内形成技术成果，
    西门子DI需在专利布局、技术标准制定和行业认证上保持领先，构建更高的技术壁垒。
    </div>
    <br>
    <div class="insight-box teal">
    🔍 <b>销售费用增速仅3.69%，远低于营收增速21.77%</b>，
    说明汇川的销售效率在持续提升，渠道杠杆效应显著。
    <b>西门子DI视角：</b>汇川依托经销商网络和存量客户复购实现低成本增长，
    西门子DI需在关键客户深度绑定和解决方案粘性上加大投入，提高客户切换成本。
    </div>
    """, unsafe_allow_html=True)


# =============================================================================
# Tab5：数据导出
# =============================================================================
def render_tab_export(data: dict) -> None:
    """Tab5：数据导出 - 数据表查看、搜索过滤、CSV下载、分红计算。"""

    st.markdown("### 📥 数据导出中心")

    # 构建可选数据表
    tables = {
        "盈利指标（近3年）": data["profit"],
        "现金流指标（近3年）": data["cashflow"],
        "资产负债指标（近3年末）": data["balance"],
        "分季度数据（FY2025）": data["quarterly"],
        "产品线数据-行业口径（FY2025）": data["product_industry"],
        "产品线数据-产品口径（FY2025）": data["product"],
        "地区数据（FY2025）": data["region"],
        "费用数据（FY2025）": data["expense"],
        "研发费用趋势（近3年）": data["rd"],
        "研发人员学历结构（FY2025）": data["rd_edu"],
        "产销量数据（FY2025）": data["volume"],
    }

    col_sel, col_search = st.columns([2, 2])
    with col_sel:
        selected_table = st.selectbox("📋 选择数据表", list(tables.keys()))
    with col_search:
        search_kw = st.text_input("🔍 关键词过滤（支持列名/数值搜索）", placeholder="输入关键词...")

    df_show = tables[selected_table].copy()

    # 关键词过滤
    if search_kw:
        mask = df_show.astype(str).apply(
            lambda col: col.str.contains(search_kw, case=False, na=False)
        ).any(axis=1)
        df_show = df_show[mask]

    st.dataframe(df_show, use_container_width=True, height=400)

    col_dl1, col_dl2 = st.columns(2)
    with col_dl1:
        csv_single = df_show.to_csv(index=False, encoding="utf-8-sig")
        st.download_button(
            label=f"⬇️ 下载当前表（{selected_table}）",
            data=csv_single,
            file_name=f"汇川FY2025_{selected_table}.csv",
            mime="text/csv"
        )
    with col_dl2:
        all_dfs = []
        for name, df in tables.items():
            tmp = df.copy()
            tmp.insert(0, "数据表", name)
            all_dfs.append(tmp)
        df_all = pd.concat(all_dfs, ignore_index=True)
        csv_all = df_all.to_csv(index=False, encoding="utf-8-sig")
        st.download_button(
            label="⬇️ 下载全量数据包（所有表）",
            data=csv_all,
            file_name="汇川FY2025_全量数据.csv",
            mime="text/csv"
        )

    st.info("""
    📌 **数据说明**
    - **数据来源**：深圳市汇川技术股份有限公司 2025年年度报告（公开披露）
    - **财务口径**：合并报表，人民币计价
    - **数据单位**：金额类指标单位为万元（人民币）；产销量单位为PCS；比率类为%
    - **数据截止**：2025年12月31日（资产负债数据）/ 2025年全年（损益及现金流数据）
    - **免责声明**：本看板数据仅供西门子数字化工业（DI）内部竞争研究使用，不构成投资建议。
      部分指标（如综合毛利率、营业成本）为根据财报数据估算，可能与实际值存在微小偏差。
    """)

    # 利润分配方案
    st.markdown("### 💰 利润分配方案（FY2025）")
    div = data["dividend"]
    d1, d2, d3 = st.columns(3)
    with d1:
        st.metric("每股现金分红（含税）", f"{div['每股分红（元，含税）']:.2f} 元/股")
        st.caption("每10股派发现金5元（含税）")
    with d2:
        st.metric("现金分红总额", f"{div['分红总额（万元）']:,.0f} 万元")
        st.caption(f"分红比例：{div['分红比例（%）']:.1f}%")
    with d3:
        st.metric("基本EPS（FY2025）", f"{div['基本EPS_2025']:.2f} 元/股")
        st.caption(f"稀释EPS：{div['稀释EPS_2025']:.2f} 元/股")

    # 股息率动态计算
    st.markdown("#### 📐 股息率动态计算")
    price_input = st.number_input(
        "请输入当前股价（元）",
        min_value=0.01, max_value=9999.0,
        value=50.0, step=0.5,
        help="输入汇川技术（300124）当前市场股价，自动计算股息率"
    )
    dividend_yield = div["每股分红（元，含税）"] / price_input * 100
    pe_ratio = price_input / div["基本EPS_2025"]

    col_y1, col_y2, col_y3 = st.columns(3)
    with col_y1:
        st.metric("股息率（含税）", f"{dividend_yield:.2f}%",
                  delta=f"基于股价 {price_input:.2f} 元")
    with col_y2:
        st.metric("市盈率（PE）", f"{pe_ratio:.1f}x",
                  delta=f"EPS {div['基本EPS_2025']:.2f} 元")
    with col_y3:
        market_cap = price_input * div["总股本（股）"] / 10000
        st.metric("市值估算", f"{market_cap/10000:.0f} 亿元",
                  delta=f"总股本 {div['总股本（股）']/1e8:.2f} 亿股")


# =============================================================================
# E. 侧边栏
# =============================================================================
def render_sidebar() -> str:
    """渲染侧边栏，返回分析视角选项。"""
    with st.sidebar:
        # Logo区
        st.markdown("""
        <div class="sidebar-logo">
            <div style="font-size:2rem;">🏭</div>
            <div class="company-name">汇川技术</div>
            <div class="ticker">300124 · 深交所创业板</div>
            <div class="dashboard-title">FY2025 竞争情报看板</div>
        </div>
        """, unsafe_allow_html=True)

        # 公司概况
        st.markdown("#### 🏢 公司概况")
        st.markdown("""
        | 项目 | 内容 |
        |------|------|
        | **全称** | 深圳市汇川技术股份有限公司 |
        | **主营** | 工业自动化、新能源汽车 |
        | **核心产品** | 变频器、伺服、PLC、机器人 |
        | **总部** | 深圳市龙华区 |
        | **上市时间** | 2010年9月 |
        """)

        # 核心数据速览
        st.markdown("#### 📊 核心数据速览")
        st.markdown("""
        | 指标 | FY2025 |
        |------|--------|
        | 营业收入 | **451.05亿元** |
        | 归母净利润 | **50.50亿元** |
        | 综合毛利率 | **~28.95%** |
        | 净利率 | **11.20%** |
        | ROE | **16.34%** |
        | 研发费用率 | **9.44%** |
        | 研发人员 | **7,670人** |
        """)

        # 竞争重叠度
        st.markdown("#### ⚔️ 与西门子DI竞争重叠度")
        st.error("🔴 高度重叠")
        st.markdown("""
        - 变频器 / 伺服系统
        - PLC / HMI
        - 工业机器人
        - 工业软件（数字化）
        """)

        # 分析视角
        st.markdown("#### 🎯 分析视角")
        view_mode = st.radio(
            "选择分析视角",
            ["全面分析", "增长聚焦", "盈利聚焦"],
            index=0
        )

        # 底部说明
        st.markdown("---")
        st.caption("📅 数据截止：2025年12月31日")
        st.caption("📄 数据来源：汇川技术2025年年度报告")
        st.caption("🔒 仅供西门子DI内部竞争研究使用")

    return view_mode


# =============================================================================
# F. 主函数
# =============================================================================
def main():
    """主函数：注入样式、加载数据、渲染看板。"""
    inject_css()

    # 加载数据
    data = load_financial_data()

    # 主标题横幅
    st.markdown("""
    <div class="main-header">
        <h1>🏭 汇川技术（300124）· FY2025 竞争情报看板</h1>
        <p>
        深圳市汇川技术股份有限公司 · 2025年度财务报告深度分析 ·
        西门子数字化工业（DI）竞争情报团队专用 ·
        数据来源：汇川技术2025年年度报告（公开披露）
        </p>
    </div>
    """, unsafe_allow_html=True)

    # 渲染侧边栏
    view_mode = render_sidebar()

    # Tab导航
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 CEO概览圈",
        "🏭 产品线分析",
        "🌏 市场与渠道",
        "🔬 费用与研发",
        "📥 数据导出"
    ])

    with tab1:
        render_tab_ceo(data)
    with tab2:
        render_tab_product(data)
    with tab3:
        render_tab_market(data)
    with tab4:
        render_tab_rd(data)
    with tab5:
        render_tab_export(data)

    # 全局免责声明
    st.markdown("---")
    st.caption("""
    ⚠️ **免责声明**：本看板由西门子数字化工业（DI）竞争情报团队生成，
    所有数据来源于汇川技术2025年年度报告公开披露内容，仅供西门子内部竞争研究使用，
    不构成任何投资建议。部分估算指标已在相应位置注明，请以原始财报数据为准。
    未经授权，禁止对外传播或商业使用。
    """)


if __name__ == "__main__":
    main()

# =============================================================================
# 运行说明：
# pip install streamlit plotly pandas numpy
# streamlit run dashboard.py
# =============================================================================
