    
"""
信捷电气 (603416) 2025年年度财报可视化看板
数据来源：无锡信捷电气股份有限公司 2025年年度报告
作者：SiemensGPT 财报分析助手
配色主题：明亮商务风（参考月度财务分析报告模板）
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import numpy as np
import io

# ─────────────────────────────────────────────
# 全局配置
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="信捷电气 2025 财报看板",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── 明亮商务配色方案（对标参考模板）──
COLORS = {
    # 主色：深海蓝（标题、主要柱状图、强调）
    "primary":    "#1B3A8C",
    # 辅色：青绿（折线、点缀、第二系列）
    "secondary":  "#2BBFBF",
    # 成功绿（正增长）
    "success":    "#27AE60",
    # 警示红（负增长）
    "danger":     "#E74C3C",
    # 中性灰蓝（次要数据、对比柱）
    "neutral":    "#8FA8C8",
    # 浅背景色（卡片底色）
    "bg_light":   "#F5F7FA",
    # 卡片白底
    "card_bg":    "#FFFFFF",
    # 深色文字
    "text_dark":  "#1A2B4A",
    # 次要文字
    "text_muted": "#6B7A99",
    # 产品线专属色
    "plc":        "#1B3A8C",   # 深蓝
    "drive":      "#2BBFBF",   # 青绿
    "hmi":        "#5B8DEF",   # 中蓝
    "robot":      "#27AE60",   # 绿
    # 图表背景
    "plot_bg":    "#FFFFFF",
    "grid_color": "#E8EDF5",
}

# Plotly 使用浅色模板
PLOTLY_TEMPLATE = "plotly_white"

# ─────────────────────────────────────────────
# 数据层（与原版完全相同，不改动）
# ─────────────────────────────────────────────

def load_financial_data() -> dict:
    annual_pnl = pd.DataFrame({
        "年份": [2023, 2024, 2025],
        "营业收入":      [150505.08, 170827.31, 201358.58],
        "营业成本":      [106383.31, 106383.31, 125867.03],
        "毛利润":        [44121.77,  64994.00,  75491.55],
        "销售费用":      [18563.00,  19499.50,  21189.87],
        "管理费用":      [7500.00,   8162.04,   9362.97],
        "研发费用":      [14200.00,  16751.29,  19924.71],
        "归母净利润":    [19901.67,  22855.19,  25416.63],
        "扣非归母净利润":[16125.38,  20285.74,  23612.05],
        "经营现金流净额":[19790.60,  12770.59,   9279.70],
    })
    annual_pnl["营业成本"]   = [106383.31, 106383.31, 125867.03]
    annual_pnl["毛利润"]     = annual_pnl["营业收入"] - annual_pnl["营业成本"]
    annual_pnl["毛利率"]     = annual_pnl["毛利润"]   / annual_pnl["营业收入"] * 100
    annual_pnl["净利率"]     = annual_pnl["归母净利润"] / annual_pnl["营业收入"] * 100
    annual_pnl["研发费用率"] = annual_pnl["研发费用"]  / annual_pnl["营业收入"] * 100
    annual_pnl["销售费用率"] = annual_pnl["销售费用"]  / annual_pnl["营业收入"] * 100

    quarterly = pd.DataFrame({
        "季度":      ["Q1 (1-3月)", "Q2 (4-6月)", "Q3 (7-9月)", "Q4 (10-12月)"],
        "季度序号":  [1, 2, 3, 4],
        "营业收入":  [38829.79, 48884.85, 50480.95, 63162.99],
        "归母净利润":[4600.94,  8108.08,  5306.73,  7400.89],
        "扣非净利润":[4048.91,  7644.18,  4971.61,  6947.34],
        "经营现金流":[-7166.37, 6444.06, -636.28,  10638.29],
    })
    quarterly["净利率"]     = quarterly["归母净利润"] / quarterly["营业收入"] * 100
    quarterly["环比增长率"] = quarterly["营业收入"].pct_change() * 100

    product_revenue = pd.DataFrame({
        "产品线":   ["可编程控制器(PLC)", "驱动系统(伺服)", "人机界面(HMI)", "智能装置(机器人)", "其他"],
        "营业收入": [70763.80, 101930.30, 20535.79, 6814.87, 912.11],
        "营业成本": [30391.60,  75532.94, 13805.07, 5231.92, 820.04],
        "收入占比": [35.21, 50.72, 10.22, 3.39, 0.45],
        "同比增长": [9.16, 26.39, 5.21, 64.96, -28.06],
        "颜色":     [COLORS["plc"], COLORS["drive"], COLORS["hmi"],
                     COLORS["robot"], COLORS["neutral"]],
    })
    product_revenue["毛利润"] = product_revenue["营业收入"] - product_revenue["营业成本"]
    product_revenue["毛利率"] = product_revenue["毛利润"] / product_revenue["营业收入"] * 100

    regional_revenue = pd.DataFrame({
        "地区":     ["广东省", "江苏省", "浙江省", "山东省", "其他省份"],
        "营业收入": [62964.21, 46235.51, 32684.80, 18133.17, 40939.18],
        "营业成本": [39003.16, 29242.26, 21433.76, 11461.19, 24641.20],
        "同比增长": [28.54, 12.54, 10.83, 8.75, 19.85],
    })
    regional_revenue["毛利率"] = (
        (regional_revenue["营业收入"] - regional_revenue["营业成本"])
        / regional_revenue["营业收入"] * 100
    )

    channel_data = pd.DataFrame({
        "渠道":     ["经销", "直销"],
        "营业收入": [166518.24, 34438.63],
        "营业成本": [104233.71, 21547.86],
        "同比增长": [14.82, 35.73],
    })
    channel_data["毛利率"] = (
        (channel_data["营业收入"] - channel_data["营业成本"])
        / channel_data["营业收入"] * 100
    )
    channel_data["占比"] = channel_data["营业收入"] / channel_data["营业收入"].sum() * 100

    geo_data = pd.DataFrame({
        "市场":     ["境内", "境外"],
        "营业收入": [196823.21, 4535.37],
        "营业成本": [123314.33, 2552.70],
    })
    geo_data["毛利率"] = (
        (geo_data["营业收入"] - geo_data["营业成本"])
        / geo_data["营业收入"] * 100
    )
    geo_data["占比"] = geo_data["营业收入"] / geo_data["营业收入"].sum() * 100

    key_metrics = pd.DataFrame({
        "指标":   ["基本每股收益(元)", "净资产收益率ROE(%)", "扣非ROE(%)",
                   "总资产(亿元)", "归母净资产(亿元)", "资产负债率(%)"],
        "2023年": [1.42, 9.72, 7.87, 28.80, 21.35, 25.86],
        "2024年": [1.64, 10.36, 9.20, 32.16, 22.97, 28.56],
        "2025年": [1.68, 9.88, 9.18, 37.31, 27.12, 27.24],
    })

    expense_structure = pd.DataFrame({
        "费用项目": ["销售费用", "管理费用", "研发费用"],
        "2024年":   [19499.50, 8162.04, 16751.29],
        "2025年":   [21189.87, 9362.97, 19924.71],
        "同比增长": [8.67, 14.71, 18.94],
    })

    production_sales = pd.DataFrame({
        "产品":      ["可编程控制器", "人机界面", "驱动系统"],
        "生产量(台)":[1898440, 621325, 2735971],
        "销售量(台)":[1815711, 655563, 3522463],
        "库存量(台)":[688084,  165241, 1212910],
        "生产量同比":[5.07, -9.62, 30.79],
        "销售量同比":[11.08, 4.47, 40.46],
    })

    dividend_data = {
        "归母净利润(万元)":    25416.63,
        "现金分红总额(万元)":  24157.36,
        "分红比例(%)":         95.05,
        "每股股息(元，含税)":  0.95,
        "半年度每股股息(元)":  0.59,
        "年度每股股息(元)":    0.95,
    }

    return {
        "annual_pnl":        annual_pnl,
        "quarterly":         quarterly,
        "product_revenue":   product_revenue,
        "regional_revenue":  regional_revenue,
        "channel_data":      channel_data,
        "geo_data":          geo_data,
        "key_metrics":       key_metrics,
        "expense_structure": expense_structure,
        "production_sales":  production_sales,
        "dividend_data":     dividend_data,
    }

# ─────────────────────────────────────────────
# 工具函数
# ─────────────────────────────────────────────

def fmt_wan(val: float, decimals: int = 2) -> str:
    if val >= 10000:
        return f"{val/10000:.{decimals}f} 亿元"
    return f"{val:.{decimals}f} 万元"

def kpi_card(col, label: str, value: str, delta: str = None,
             delta_val: float = None, note: str = None):
    with col:
        st.metric(label=label, value=value, delta=delta)
        if note:
            st.caption(note)

# ─────────────────────────────────────────────
# CSS 注入：明亮商务风（对标参考模板）
# ─────────────────────────────────────────────

def inject_css():
    st.markdown("""
    <style>
    /* ── 全局背景：浅灰白 ── */
    .stApp {
        background-color: #F5F7FA;
        color: #1A2B4A;
        font-family: 'Segoe UI', 'PingFang SC', 'Microsoft YaHei', sans-serif;
    }

    /* ── 主标题横幅：深蓝底+青绿左边框 ── */
    .main-header {
        background: linear-gradient(135deg, #1B3A8C 0%, #2B5299 60%, #1B3A8C 100%);
        padding: 24px 36px;
        border-radius: 14px;
        margin-bottom: 28px;
        border-left: 6px solid #2BBFBF;
        box-shadow: 0 4px 20px rgba(27,58,140,0.18);
    }
    .main-header h1 {
        color: #FFFFFF;
        margin: 0;
        font-size: 1.9rem;
        font-weight: 700;
        letter-spacing: 0.5px;
    }
    .main-header p {
        color: #A8C4E8;
        margin: 6px 0 0 0;
        font-size: 0.88rem;
    }

    /* ── KPI 卡片：白底+蓝顶边框+阴影 ── */
    [data-testid="metric-container"] {
        background: #FFFFFF;
        border: 1px solid #E0E8F5;
        border-radius: 12px;
        padding: 18px 16px;
        border-top: 4px solid #1B3A8C;
        box-shadow: 0 2px 12px rgba(27,58,140,0.08);
        transition: box-shadow 0.2s;
    }
    [data-testid="metric-container"]:hover {
        box-shadow: 0 6px 24px rgba(27,58,140,0.15);
    }

    /* KPI 标签文字 */
    [data-testid="metric-container"] label {
        color: #6B7A99 !important;
        font-size: 0.82rem !important;
        font-weight: 600 !important;
    }
    /* KPI 主数值 */
    [data-testid="metric-container"] [data-testid="stMetricValue"] {
        color: #1B3A8C !important;
        font-size: 1.5rem !important;
        font-weight: 700 !important;
    }
    /* KPI delta 正值 */
    [data-testid="stMetricDelta"] svg { display: none; }
    [data-testid="stMetricDelta"] {
        font-size: 0.8rem !important;
        font-weight: 600 !important;
    }

    /* ── Tab 导航：白底+蓝色选中态 ── */
    .stTabs [data-baseweb="tab-list"] {
        background: #FFFFFF;
        border-radius: 10px;
        padding: 4px 6px;
        border: 1px solid #E0E8F5;
        box-shadow: 0 2px 8px rgba(27,58,140,0.06);
        gap: 4px;
    }
    .stTabs [data-baseweb="tab"] {
        color: #6B7A99;
        font-weight: 600;
        font-size: 0.88rem;
        border-radius: 8px;
        padding: 8px 16px;
    }
    .stTabs [aria-selected="true"] {
        background: #1B3A8C !important;
        color: #FFFFFF !important;
        border-radius: 8px;
    }

    /* ── 侧边栏：白底+右侧分隔线 ── */
    [data-testid="stSidebar"] {
        background: #FFFFFF;
        border-right: 2px solid #E0E8F5;
    }
    [data-testid="stSidebar"] .stMarkdown {
        color: #1A2B4A;
    }

    /* ── 分隔线 ── */
    hr {
        border: none;
        border-top: 1.5px solid #E0E8F5;
        margin: 20px 0;
    }

    /* ── Insight 洞察框：浅蓝底+深蓝左边框 ── */
    .insight-box {
        background: #EEF3FC;
        border: 1px solid #C5D5F0;
        border-left: 5px solid #1B3A8C;
        border-radius: 10px;
        padding: 13px 18px;
        margin: 10px 0;
        font-size: 0.87rem;
        color: #1A2B4A;
        line-height: 1.6;
    }
    .insight-box.green {
        background: #EAF7F0;
        border-color: #B2DFC7;
        border-left-color: #27AE60;
    }
    .insight-box.red {
        background: #FEF0EE;
        border-color: #F5C6C0;
        border-left-color: #E74C3C;
    }
    .insight-box.teal {
        background: #E8F8F8;
        border-color: #A8E0E0;
        border-left-color: #2BBFBF;
    }

    /* ── 区块标题装饰 ── */
    h3 {
        color: #1B3A8C !important;
        border-bottom: 2px solid #2BBFBF;
        padding-bottom: 6px;
        margin-bottom: 16px !important;
    }

    /* ── dataframe 表格 ── */
    .stDataFrame {
        border-radius: 10px;
        overflow: hidden;
        border: 1px solid #E0E8F5;
    }

    /* ── 下载按钮 ── */
    .stDownloadButton button {
        background: #1B3A8C;
        color: white;
        border-radius: 8px;
        border: none;
        font-weight: 600;
        padding: 8px 20px;
    }
    .stDownloadButton button:hover {
        background: #2BBFBF;
        color: white;
    }

    /* ── selectbox / radio ── */
    .stSelectbox label, .stRadio label {
        color: #1A2B4A !important;
        font-weight: 600;
    }

    /* ── caption ── */
    .stCaption {
        color: #6B7A99 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
# 通用图表布局配置（浅色风格）
# ─────────────────────────────────────────────

def base_layout(**kwargs) -> dict:
    """返回统一的浅色图表布局基础配置。"""
    layout = dict(
        template=PLOTLY_TEMPLATE,
        paper_bgcolor=COLORS["card_bg"],
        plot_bgcolor=COLORS["plot_bg"],
        font=dict(family="Segoe UI, PingFang SC, Microsoft YaHei", color=COLORS["text_dark"], size=12),
        title_font=dict(color=COLORS["primary"], size=14, family="Segoe UI, PingFang SC"),
        xaxis=dict(gridcolor=COLORS["grid_color"], linecolor="#D0DAF0", tickcolor="#D0DAF0"),
        yaxis=dict(gridcolor=COLORS["grid_color"], linecolor="#D0DAF0", tickcolor="#D0DAF0"),
        margin=dict(t=55, b=40, l=40, r=30),
    )
    layout.update(kwargs)
    return layout

# ─────────────────────────────────────────────
# Tab 1：CEO 概览圈
# ─────────────────────────────────────────────

def render_tab_ceo(data: dict):
    pnl = data["annual_pnl"]
    qtr = data["quarterly"]

    st.markdown("### 📊 核心经营 KPI（2025年度）")

    c1, c2, c3, c4, c5, c6 = st.columns(6)
    kpi_card(c1, "营业总收入",    "20.14 亿元", "+17.87% YoY", 17.87, note="首次突破20亿大关")
    kpi_card(c2, "归母净利润",    "2.54 亿元",  "+11.21% YoY", 11.21, note="近十年年均复合增长10%")
    kpi_card(c3, "扣非归母净利润","2.36 亿元",  "+16.40% YoY", 16.40, note="利润质量持续改善")
    kpi_card(c4, "研发投入",      "1.99 亿元",  "+18.94% YoY", 18.94, note="占收入比9.90%")
    kpi_card(c5, "基本每股收益",  "1.68 元",    "+2.44% YoY",  2.44,  note="2024年为1.64元")
    kpi_card(c6, "现金分红比例",  "95.05%",     "分红0.95元/股", None, note="半年度+年度合计")

    st.divider()

    st.markdown("### 🏦 资产负债与健康度指标")
    c7, c8, c9, c10 = st.columns(4)
    kpi_card(c7, "总资产",       "37.31 亿元", "+16.01% YoY", 16.01)
    kpi_card(c8, "归母净资产",   "27.12 亿元", "+18.07% YoY", 18.07)
    kpi_card(c9, "加权平均ROE",  "9.88%",      "-0.48pct YoY", -0.48,
             note="⚠️ 较2024年小幅下降")
    kpi_card(c10,"海外订单增长", ">60%",       "国际化加速",   None,
             note="东南亚/中东/俄罗斯重点突破")

    st.divider()

    st.markdown("### 📈 三年核心财务趋势")
    col_left, col_right = st.columns([3, 2])

    with col_left:
        fig_trend = make_subplots(specs=[[{"secondary_y": True}]])

        # 营业收入柱状（深蓝，带透明度）
        fig_trend.add_trace(
            go.Bar(
                x=pnl["年份"].astype(str),
                y=pnl["营业收入"],
                name="营业收入(万元)",
                marker=dict(
                    color=COLORS["primary"],
                    opacity=0.82,
                    line=dict(color=COLORS["primary"], width=0),
                ),
                hovertemplate="<b>%{x}年</b><br>营业收入：%{y:,.0f} 万元<extra></extra>",
            ),
            secondary_y=False,
        )

        # 归母净利润折线（青绿）
        fig_trend.add_trace(
            go.Scatter(
                x=pnl["年份"].astype(str),
                y=pnl["归母净利润"],
                name="归母净利润(万元)",
                mode="lines+markers+text",
                line=dict(color=COLORS["secondary"], width=3),
                marker=dict(size=10, symbol="diamond",
                            color=COLORS["secondary"],
                            line=dict(color="white", width=2)),
                text=[f"{v:,.0f}" for v in pnl["归母净利润"]],
                textposition="top center",
                textfont=dict(color=COLORS["secondary"], size=11),
                hovertemplate="<b>%{x}年</b><br>归母净利润：%{y:,.0f} 万元<extra></extra>",
            ),
            secondary_y=False,
        )

        # 净利率（右轴，绿色虚线）
        fig_trend.add_trace(
            go.Scatter(
                x=pnl["年份"].astype(str),
                y=pnl["净利率"],
                name="净利率(%)",
                mode="lines+markers",
                line=dict(color=COLORS["success"], width=2, dash="dot"),
                marker=dict(size=8, color=COLORS["success"],
                            line=dict(color="white", width=1.5)),
                hovertemplate="<b>%{x}年</b><br>净利率：%{y:.2f}%<extra></extra>",
            ),
            secondary_y=True,
        )

        fig_trend.update_layout(
            **base_layout(
                title="营业收入 / 归母净利润 / 净利率（2023-2025）",
                legend=dict(orientation="h", y=-0.18,
                            bgcolor="rgba(255,255,255,0.8)",
                            bordercolor="#E0E8F5", borderwidth=1),
                height=420,
                margin=dict(t=55, b=70),
            )
        )
        fig_trend.update_yaxes(title_text="金额（万元）", secondary_y=False,
                               gridcolor=COLORS["grid_color"])
        fig_trend.update_yaxes(title_text="净利率（%）", secondary_y=True,
                               tickformat=".1f", ticksuffix="%",
                               gridcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig_trend, use_container_width=True)

    with col_right:
        categories = ["毛利率", "净利率", "研发费用率", "销售费用率", "ROE"]
        vals_2023 = [
            pnl.loc[pnl["年份"]==2023, "毛利率"].values[0],
            pnl.loc[pnl["年份"]==2023, "净利率"].values[0],
            pnl.loc[pnl["年份"]==2023, "研发费用率"].values[0],
            pnl.loc[pnl["年份"]==2023, "销售费用率"].values[0],
            9.72,
        ]
        vals_2024 = [
            pnl.loc[pnl["年份"]==2024, "毛利率"].values[0],
            pnl.loc[pnl["年份"]==2024, "净利率"].values[0],
            pnl.loc[pnl["年份"]==2024, "研发费用率"].values[0],
            pnl.loc[pnl["年份"]==2024, "销售费用率"].values[0],
            10.36,
        ]
        vals_2025 = [
            pnl.loc[pnl["年份"]==2025, "毛利率"].values[0],
            pnl.loc[pnl["年份"]==2025, "净利率"].values[0],
            pnl.loc[pnl["年份"]==2025, "研发费用率"].values[0],
            pnl.loc[pnl["年份"]==2025, "销售费用率"].values[0],
            9.88,
        ]

        fig_radar = go.Figure()
        for year, vals, color, opacity in [
            ("2023", vals_2023, COLORS["neutral"],    0.15),
            ("2024", vals_2024, COLORS["secondary"],  0.20),
            ("2025", vals_2025, COLORS["primary"],    0.25),
        ]:
            fig_radar.add_trace(go.Scatterpolar(
                r=vals + [vals[0]],
                theta=categories + [categories[0]],
                name=f"{year}年",
                line=dict(color=color, width=2.5),
                fill="toself",
                fillcolor=color,
                opacity=opacity + 0.5,
                hovertemplate="%{theta}: %{r:.2f}%<extra></extra>",
            ))

        fig_radar.update_layout(
            paper_bgcolor=COLORS["card_bg"],
            plot_bgcolor=COLORS["plot_bg"],
            font=dict(color=COLORS["text_dark"]),
            title=dict(text="盈利质量雷达图（三年对比）",
                       font=dict(color=COLORS["primary"], size=14)),
            polar=dict(
                bgcolor="#F5F7FA",
                radialaxis=dict(
                    visible=True, range=[0, 45],
                    gridcolor="#D0DAF0", linecolor="#D0DAF0",
                    tickfont=dict(color=COLORS["text_muted"], size=10),
                ),
                angularaxis=dict(
                    gridcolor="#D0DAF0", linecolor="#D0DAF0",
                    tickfont=dict(color=COLORS["text_dark"], size=11),
                ),
            ),
            legend=dict(orientation="h", y=-0.12,
                        bgcolor="rgba(255,255,255,0.8)",
                        bordercolor="#E0E8F5", borderwidth=1),
            height=420,
        )
        st.plotly_chart(fig_radar, use_container_width=True)

    # ── 季度节奏 ──
    st.markdown("### 🗓️ 2025年分季度营收节奏")
    fig_qtr = make_subplots(
        rows=1, cols=2,
        subplot_titles=["季度营业收入（万元）", "季度净利率（%）"],
        specs=[[{"type": "bar"}, {"type": "scatter"}]]
    )

    # Q1灰蓝，Q2/Q3深蓝，Q4青绿（最高季）
    bar_colors = [COLORS["neutral"], COLORS["primary"],
                  COLORS["primary"], COLORS["secondary"]]

    fig_qtr.add_trace(
        go.Bar(
            x=qtr["季度"], y=qtr["营业收入"],
            marker_color=bar_colors,
            marker_line_width=0,
            text=[f"{v:,.0f}" for v in qtr["营业收入"]],
            textposition="outside",
            textfont=dict(size=11, color=COLORS["text_dark"]),
            hovertemplate="<b>%{x}</b><br>营业收入：%{y:,.0f} 万元<extra></extra>",
            name="营业收入",
        ),
        row=1, col=1,
    )

    fig_qtr.add_trace(
        go.Scatter(
            x=qtr["季度"], y=qtr["净利率"],
            mode="lines+markers+text",
            line=dict(color=COLORS["secondary"], width=3),
            marker=dict(size=11, color=COLORS["secondary"],
                        line=dict(color="white", width=2)),
            text=[f"{v:.1f}%" for v in qtr["净利率"]],
            textposition="top center",
            textfont=dict(color=COLORS["primary"], size=11, family="Segoe UI"),
            hovertemplate="<b>%{x}</b><br>净利率：%{y:.2f}%<extra></extra>",
            name="净利率",
        ),
        row=1, col=2,
    )

    fig_qtr.update_layout(
        **base_layout(height=400, showlegend=False, margin=dict(t=55, b=30))
    )
    fig_qtr.update_xaxes(gridcolor=COLORS["grid_color"], linecolor="#D0DAF0")
    fig_qtr.update_yaxes(gridcolor=COLORS["grid_color"], linecolor="#D0DAF0")
    st.plotly_chart(fig_qtr, use_container_width=True)

    st.markdown("""
    <div class="insight-box teal">
    💡 <b>CEO 洞察：</b>Q4 营收 6.32 亿元为全年最高，呈现明显的"前低后高"季节性规律；
    Q2 净利率 16.58% 为全年峰值，Q3 净利率 10.51% 为全年谷值，显示驱动系统旺季集中在上半年。
    海外订单全年增长超 60%，国际化拓展成效显著，但境外收入占比仍仅 2.25%，国际化仍处早期阶段。
    </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
# Tab 2：产品线深度分析
# ─────────────────────────────────────────────

def render_tab_product(data: dict):
    prod = data["product_revenue"]
    ps   = data["production_sales"]

    st.markdown("### 🏭 产品线收入结构（2025年）")
    col1, col2 = st.columns([2, 3])

    with col1:
        fig_pie = go.Figure(go.Pie(
            labels=prod["产品线"],
            values=prod["营业收入"],
            hole=0.52,
            marker=dict(
                colors=[COLORS["plc"], COLORS["drive"],
                        COLORS["hmi"], COLORS["robot"], COLORS["neutral"]],
                line=dict(color="white", width=2),
            ),
            textinfo="label+percent",
            textfont=dict(size=11, color=COLORS["text_dark"]),
            hovertemplate="<b>%{label}</b><br>收入：%{value:,.2f} 万元<br>占比：%{percent}<extra></extra>",
        ))
        fig_pie.update_layout(
            **base_layout(
                title="产品线收入占比",
                height=400,
                annotations=[dict(
                    text="<b>20.14亿</b>", x=0.5, y=0.5,
                    font=dict(size=15, color=COLORS["primary"]),
                    showarrow=False,
                )],
            )
        )
        st.plotly_chart(fig_pie, use_container_width=True)

    with col2:
        fig_prod = make_subplots(specs=[[{"secondary_y": True}]])
        fig_prod.add_trace(
            go.Bar(
                x=prod["产品线"],
                y=prod["营业收入"],
                name="营业收入(万元)",
                marker=dict(
                    color=[COLORS["plc"], COLORS["drive"],
                           COLORS["hmi"], COLORS["robot"], COLORS["neutral"]],
                    line=dict(color="white", width=1),
                ),
                hovertemplate="<b>%{x}</b><br>收入：%{y:,.2f} 万元<extra></extra>",
            ),
            secondary_y=False,
        )
        fig_prod.add_trace(
            go.Scatter(
                x=prod["产品线"],
                y=prod["毛利率"],
                name="毛利率(%)",
                mode="lines+markers+text",
                line=dict(color=COLORS["secondary"], width=3),
                marker=dict(size=13, symbol="star",
                            color=COLORS["secondary"],
                            line=dict(color="white", width=1.5)),
                text=[f"{v:.1f}%" for v in prod["毛利率"]],
                textposition="top center",
                textfont=dict(color=COLORS["secondary"], size=11),
                hovertemplate="<b>%{x}</b><br>毛利率：%{y:.2f}%<extra></extra>",
            ),
            secondary_y=True,
        )
        fig_prod.update_layout(
            **base_layout(
                title="各产品线收入 vs 毛利率",
                height=400,
                legend=dict(orientation="h", y=-0.18,
                            bgcolor="rgba(255,255,255,0.8)",
                            bordercolor="#E0E8F5", borderwidth=1),
            )
        )
        fig_prod.update_yaxes(title_text="收入（万元）", secondary_y=False,
                              gridcolor=COLORS["grid_color"])
        fig_prod.update_yaxes(title_text="毛利率（%）", secondary_y=True,
                              tickformat=".1f", ticksuffix="%",
                              range=[0, 75], gridcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig_prod, use_container_width=True)

    st.divider()
    st.markdown("### 🚀 产品线同比增长动能")
    col3, col4 = st.columns([3, 2])

    with col3:
        colors_growth = [
            COLORS["success"] if v >= 0 else COLORS["danger"]
            for v in prod["同比增长"]
        ]
        fig_growth = go.Figure(go.Bar(
            x=prod["同比增长"],
            y=prod["产品线"],
            orientation="h",
            marker=dict(color=colors_growth, line=dict(color="white", width=1)),
            text=[f"{v:+.1f}%" for v in prod["同比增长"]],
            textposition="outside",
            textfont=dict(size=11, color=COLORS["text_dark"]),
            hovertemplate="<b>%{y}</b><br>同比增长：%{x:.1f}%<extra></extra>",
        ))
        fig_growth.add_vline(x=0, line_dash="dash",
                             line_color=COLORS["text_muted"], opacity=0.6)
        fig_growth.add_vline(x=17.87, line_dash="dot",
                             line_color=COLORS["secondary"], opacity=0.9,
                             annotation_text="公司整体增速 17.87%",
                             annotation_position="top right",
                             annotation_font=dict(color=COLORS["secondary"]))
        fig_growth.update_layout(
            **base_layout(
                title="各产品线同比增长率（2025 vs 2024）",
                height=370,
            )
        )
        fig_growth.update_xaxes(title_text="同比增长率（%）")
        st.plotly_chart(fig_growth, use_container_width=True)

    with col4:
        st.markdown("#### 📋 产品线毛利率明细")
        display_prod = prod[["产品线", "营业收入", "毛利率", "同比增长"]].copy()
        display_prod["营业收入"] = display_prod["营业收入"].apply(lambda x: f"{x:,.2f} 万元")
        display_prod["毛利率"]   = display_prod["毛利率"].apply(lambda x: f"{x:.2f}%")
        display_prod["同比增长"] = display_prod["同比增长"].apply(lambda x: f"{x:+.2f}%")
        st.dataframe(display_prod, use_container_width=True, hide_index=True)

        st.markdown("""
        <div class="insight-box green">
        ✅ <b>PLC 毛利率高达 57.05%</b>，是公司最核心的利润奶牛，
        小型 PLC 国产品牌市占率 8%，稳居国产第一。
        </div>
        <div class="insight-box teal">
        ⚡ <b>驱动系统</b>收入突破 10 亿，同比增长 26.39%，
        成为增长最快的主力产品线，但毛利率仅 25.90%，规模扩张伴随成本压力。
        </div>
        <div class="insight-box green">
        🤖 <b>智能装置（机器人）</b>同比增长 64.96%，
        虽然体量小（0.68亿），但增速最快，是未来战略增长极。
        </div>
        """, unsafe_allow_html=True)

    st.divider()
    st.markdown("### 📦 主要产品产销量分析（2025年）")

    fig_ps = go.Figure()
    fig_ps.add_trace(go.Bar(
        name="生产量",
        x=[f"{p} 生产" for p in ps["产品"]],
        y=ps["生产量(台)"],
        marker=dict(color=COLORS["primary"], line=dict(color="white", width=1)),
        hovertemplate="<b>%{x}</b><br>生产量：%{y:,} 台<extra></extra>",
    ))
    fig_ps.add_trace(go.Bar(
        name="销售量",
        x=[f"{p} 销售" for p in ps["产品"]],
        y=ps["销售量(台)"],
        marker=dict(color=COLORS["secondary"], line=dict(color="white", width=1)),
        hovertemplate="<b>%{x}</b><br>销售量：%{y:,} 台<extra></extra>",
    ))
    fig_ps.add_trace(go.Bar(
        name="库存量",
        x=[f"{p} 库存" for p in ps["产品"]],
        y=ps["库存量(台)"],
        marker=dict(color=COLORS["neutral"], line=dict(color="white", width=1)),
        hovertemplate="<b>%{x}</b><br>库存量：%{y:,} 台<extra></extra>",
    ))
    fig_ps.update_layout(
        **base_layout(
            title="产品产量 / 销量 / 库存量（台）",
            barmode="group",
            height=400,
            legend=dict(orientation="h", y=-0.15,
                        bgcolor="rgba(255,255,255,0.8)",
                        bordercolor="#E0E8F5", borderwidth=1),
        )
    )
    fig_ps.update_xaxes(tickangle=-15)
    st.plotly_chart(fig_ps, use_container_width=True)

# ─────────────────────────────────────────────
# Tab 3：市场与渠道分析
# ─────────────────────────────────────────────

def render_tab_market(data: dict):
    reg  = data["regional_revenue"]
    chan = data["channel_data"]
    geo  = data["geo_data"]

    st.markdown("### 🗺️ 主营业务分地区收入（2025年）")
    col1, col2 = st.columns([3, 2])

    with col1:
        fig_reg = go.Figure()
        fig_reg.add_trace(go.Bar(
            y=reg["地区"],
            x=reg["营业收入"],
            orientation="h",
            name="营业收入",
            marker=dict(color=COLORS["primary"],
                        line=dict(color="white", width=1)),
            hovertemplate="<b>%{y}</b><br>收入：%{x:,.2f} 万元<extra></extra>",
        ))
        fig_reg.add_trace(go.Scatter(
            y=reg["地区"],
            x=reg["毛利率"],
            mode="markers+text",
            name="毛利率(%)",
            marker=dict(color=COLORS["secondary"], size=15, symbol="diamond",
                        line=dict(color="white", width=2)),
            text=[f"{v:.1f}%" for v in reg["毛利率"]],
            textposition="middle right",
            textfont=dict(color=COLORS["secondary"], size=11),
            xaxis="x2",
            hovertemplate="<b>%{y}</b><br>毛利率：%{x:.2f}%<extra></extra>",
        ))
        fig_reg.update_layout(
            **base_layout(
                title="各地区营业收入 vs 毛利率",
                height=400,
                xaxis=dict(title="营业收入（万元）",
                           gridcolor=COLORS["grid_color"]),
                xaxis2=dict(title="毛利率（%）", overlaying="x",
                            side="top", range=[30, 45],
                            gridcolor="rgba(0,0,0,0)"),
                legend=dict(orientation="h", y=-0.18,
                            bgcolor="rgba(255,255,255,0.8)",
                            bordercolor="#E0E8F5", borderwidth=1),
            )
        )
        st.plotly_chart(fig_reg, use_container_width=True)

    with col2:
        reg_sorted = reg.sort_values("同比增长", ascending=True)
        colors_r = [
            COLORS["success"] if v >= 17.87 else COLORS["primary"]
            for v in reg_sorted["同比增长"]
        ]
        fig_reg_growth = go.Figure(go.Bar(
            y=reg_sorted["地区"],
            x=reg_sorted["同比增长"],
            orientation="h",
            marker=dict(color=colors_r, line=dict(color="white", width=1)),
            text=[f"{v:.1f}%" for v in reg_sorted["同比增长"]],
            textposition="outside",
            textfont=dict(size=11, color=COLORS["text_dark"]),
            hovertemplate="<b>%{y}</b><br>同比增长：%{x:.1f}%<extra></extra>",
        ))
        fig_reg_growth.add_vline(
            x=17.87, line_dash="dot",
            line_color=COLORS["secondary"], opacity=0.9,
            annotation_text="整体增速",
            annotation_font=dict(color=COLORS["secondary"]),
        )
        fig_reg_growth.update_layout(
            **base_layout(title="地区增速排名", height=400)
        )
        st.plotly_chart(fig_reg_growth, use_container_width=True)

    st.divider()
    st.markdown("### 🔀 销售渠道与境内外市场结构")
    col3, col4, col5 = st.columns(3)

    pie_layout_base = dict(
        paper_bgcolor=COLORS["card_bg"],
        plot_bgcolor=COLORS["plot_bg"],
        font=dict(color=COLORS["text_dark"]),
        title_font=dict(color=COLORS["primary"], size=14),
        height=340,
        margin=dict(t=55, b=30, l=20, r=20),
    )

    with col3:
        fig_chan = go.Figure(go.Pie(
            labels=chan["渠道"],
            values=chan["营业收入"],
            hole=0.55,
            marker=dict(
                colors=[COLORS["primary"], COLORS["secondary"]],
                line=dict(color="white", width=2),
            ),
            textinfo="label+percent",
            textfont=dict(size=12),
            hovertemplate="<b>%{label}</b><br>收入：%{value:,.2f} 万元<br>占比：%{percent}<extra></extra>",
        ))
        fig_chan.update_layout(
            **pie_layout_base,
            title="经销 vs 直销（2025年）",
            annotations=[dict(text="<b>渠道</b>", x=0.5, y=0.5,
                              font=dict(size=13, color=COLORS["primary"]),
                              showarrow=False)],
        )
        st.plotly_chart(fig_chan, use_container_width=True)

    with col4:
        fig_geo = go.Figure(go.Pie(
            labels=geo["市场"],
            values=geo["营业收入"],
            hole=0.55,
            marker=dict(
                colors=[COLORS["primary"], COLORS["secondary"]],
                line=dict(color="white", width=2),
            ),
            textinfo="label+percent",
            textfont=dict(size=12),
            hovertemplate="<b>%{label}</b><br>收入：%{value:,.2f} 万元<br>占比：%{percent}<extra></extra>",
        ))
        fig_geo.update_layout(
            **pie_layout_base,
            title="境内 vs 境外（2025年）",
            annotations=[dict(text="<b>市场</b>", x=0.5, y=0.5,
                              font=dict(size=13, color=COLORS["primary"]),
                              showarrow=False)],
        )
        st.plotly_chart(fig_geo, use_container_width=True)

    with col5:
        fig_chan_gp = go.Figure()
        fig_chan_gp.add_trace(go.Bar(
            x=chan["渠道"],
            y=chan["毛利率"],
            marker=dict(
                color=[COLORS["primary"], COLORS["secondary"]],
                line=dict(color="white", width=1),
            ),
            text=[f"{v:.2f}%" for v in chan["毛利率"]],
            textposition="outside",
            textfont=dict(size=12, color=COLORS["text_dark"]),
            hovertemplate="<b>%{x}</b><br>毛利率：%{y:.2f}%<extra></extra>",
        ))
        fig_chan_gp.update_layout(
            **base_layout(
                title="渠道毛利率对比",
                height=340,
            )
        )
        fig_chan_gp.update_yaxes(title_text="毛利率（%）", range=[0, 50])
        st.plotly_chart(fig_chan_gp, use_container_width=True)

    st.markdown("""
    <div class="insight-box teal">
    🌍 <b>国际化处于战略早期：</b>境外收入 4,535 万元，仅占总收入 2.25%，
    但 2025 年海外订单增长超 60%，重点布局东南亚、中东、俄罗斯、南美。
    未来 3-5 年国际化将是重要增量来源。
    </div>
    <div class="insight-box">
    🏪 <b>经销为主、直销提速：</b>经销占比 82.9%，直销同比增长 35.73%（远超经销的 14.82%），
    公司正积极推进大客户直销战略，直销毛利率 37.43% 与经销 37.40% 基本持平，
    但直销有助于深化客户粘性和品牌溢价。
    </div>
    <div class="insight-box green">
    📍 <b>广东省为第一大市场：</b>收入 6.30 亿元，同比增长 28.54%，
    增速远超其他省份，3C 电子、锂电、新能源汽车等新兴行业需求旺盛。
    </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
# Tab 4：费用与研发分析
# ─────────────────────────────────────────────

def render_tab_rd(data: dict):
    pnl = data["annual_pnl"]
    exp = data["expense_structure"]

    st.markdown("### 💰 费用结构分析（2025 vs 2024）")
    col1, col2 = st.columns([3, 2])

    with col1:
        fig_exp = go.Figure()
        for year, color in [("2024年", COLORS["neutral"]), ("2025年", COLORS["primary"])]:
            fig_exp.add_trace(go.Bar(
                name=year,
                x=exp["费用项目"],
                y=exp[year],
                marker=dict(color=color, line=dict(color="white", width=1)),
                text=[f"{v:,.0f}" for v in exp[year]],
                textposition="outside",
                textfont=dict(size=11, color=COLORS["text_dark"]),
                hovertemplate=f"<b>%{{x}}</b><br>{year}：%{{y:,.0f}} 万元<extra></extra>",
            ))
        fig_exp.update_layout(
            **base_layout(
                title="三大费用对比（万元）",
                barmode="group",
                height=400,
                legend=dict(orientation="h", y=-0.18,
                            bgcolor="rgba(255,255,255,0.8)",
                            bordercolor="#E0E8F5", borderwidth=1),
            )
        )
        fig_exp.update_yaxes(title_text="金额（万元）")
        st.plotly_chart(fig_exp, use_container_width=True)

    with col2:
        colors_exp = [
            COLORS["danger"] if v > 17.87 else COLORS["success"]
            for v in exp["同比增长"]
        ]
        fig_exp_g = go.Figure(go.Bar(
            x=exp["费用项目"],
            y=exp["同比增长"],
            marker=dict(color=colors_exp, line=dict(color="white", width=1)),
            text=[f"{v:+.2f}%" for v in exp["同比增长"]],
            textposition="outside",
            textfont=dict(size=11, color=COLORS["text_dark"]),
            hovertemplate="<b>%{x}</b><br>同比增长：%{y:.2f}%<extra></extra>",
        ))
        fig_exp_g.add_hline(
            y=17.87, line_dash="dot",
            line_color=COLORS["secondary"], opacity=0.9,
            annotation_text="收入增速 17.87%",
            annotation_font=dict(color=COLORS["secondary"]),
        )
        fig_exp_g.update_layout(
            **base_layout(title="费用同比增速 vs 收入增速", height=400)
        )
        fig_exp_g.update_yaxes(title_text="同比增长（%）")
        st.plotly_chart(fig_exp_g, use_container_width=True)

    st.divider()
    st.markdown("### 🔬 研发投入深度分析")
    col3, col4 = st.columns([3, 2])

    with col3:
        fig_rd = make_subplots(specs=[[{"secondary_y": True}]])
        fig_rd.add_trace(
            go.Bar(
                x=pnl["年份"].astype(str),
                y=pnl["研发费用"],
                name="研发费用(万元)",
                marker=dict(color=COLORS["primary"],
                            line=dict(color="white", width=1)),
                hovertemplate="<b>%{x}年</b><br>研发费用：%{y:,.0f} 万元<extra></extra>",
            ),
            secondary_y=False,
        )
        fig_rd.add_trace(
            go.Scatter(
                x=pnl["年份"].astype(str),
                y=pnl["研发费用率"],
                name="研发费用率(%)",
                mode="lines+markers+text",
                line=dict(color=COLORS["secondary"], width=3),
                marker=dict(size=11, color=COLORS["secondary"],
                            line=dict(color="white", width=2)),
                text=[f"{v:.2f}%" for v in pnl["研发费用率"]],
                textposition="top center",
                textfont=dict(color=COLORS["secondary"], size=11),
                hovertemplate="<b>%{x}年</b><br>研发费用率：%{y:.2f}%<extra></extra>",
            ),
            secondary_y=True,
        )
        fig_rd.update_layout(
            **base_layout(
                title="研发费用 & 研发费用率趋势（2023-2025）",
                height=400,
                legend=dict(orientation="h", y=-0.18,
                            bgcolor="rgba(255,255,255,0.8)",
                            bordercolor="#E0E8F5", borderwidth=1),
            )
        )
        fig_rd.update_yaxes(title_text="研发费用（万元）", secondary_y=False,
                            gridcolor=COLORS["grid_color"])
        fig_rd.update_yaxes(title_text="研发费用率（%）", secondary_y=True,
                            tickformat=".1f", ticksuffix="%",
                            gridcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig_rd, use_container_width=True)

    with col4:
        st.markdown("#### 🧑‍🔬 研发团队构成（2025年）")
        edu_data = pd.DataFrame({
            "学历": ["博士", "硕士", "本科", "大专及以下"],
            "人数": [1, 97, 580, 130],
        })
        fig_edu = go.Figure(go.Pie(
            labels=edu_data["学历"],
            values=edu_data["人数"],
            hole=0.42,
            marker=dict(
                colors=[COLORS["primary"], COLORS["secondary"],
                        COLORS["hmi"], COLORS["neutral"]],
                line=dict(color="white", width=2),
            ),
            textinfo="label+percent",
            textfont=dict(size=11),
            hovertemplate="<b>%{label}</b><br>人数：%{value}<br>占比：%{percent}<extra></extra>",
        ))
        fig_edu.update_layout(
            paper_bgcolor=COLORS["card_bg"],
            plot_bgcolor=COLORS["plot_bg"],
            font=dict(color=COLORS["text_dark"]),
            title=dict(text="研发人员学历结构（共808人，占比30.33%）",
                       font=dict(color=COLORS["primary"], size=13)),
            height=340,
            margin=dict(t=55, b=20, l=20, r=20),
        )
        st.plotly_chart(fig_edu, use_container_width=True)

    # ── 利润瀑布图 ──
    st.markdown("### 📉 2025年利润瀑布分析（万元）")
    revenue_2025 = 201358.58
    cost_2025    = 125867.03
    gross_profit = revenue_2025 - cost_2025
    selling_exp  = -21189.87
    admin_exp    = -9362.97
    rd_exp       = -19924.71
    fin_exp      =  428.81
    other_income =  5527.88
    net_profit   = 25416.63

    waterfall_x = ["营业收入", "营业成本", "毛利润", "销售费用",
                   "管理费用", "研发费用", "财务收益", "其他收益", "归母净利润"]
    waterfall_y = [revenue_2025, -cost_2025, gross_profit, selling_exp,
                   admin_exp, rd_exp, fin_exp, other_income, net_profit]
    measure     = ["absolute", "relative", "total", "relative",
                   "relative", "relative", "relative", "relative", "total"]

    fig_wf = go.Figure(go.Waterfall(
        name="利润瀑布",
        orientation="v",
        measure=measure,
        x=waterfall_x,
        y=waterfall_y,
        text=[f"{v:,.0f}" for v in waterfall_y],
        textposition="outside",
        textfont=dict(size=11, color=COLORS["text_dark"]),
        connector=dict(line=dict(color=COLORS["neutral"], width=1, dash="dot")),
        increasing=dict(marker=dict(color=COLORS["success"],
                                    line=dict(color="white", width=1))),
        decreasing=dict(marker=dict(color=COLORS["danger"],
                                    line=dict(color="white", width=1))),
        totals=dict(marker=dict(color=COLORS["primary"],
                                line=dict(color="white", width=1))),
        hovertemplate="<b>%{x}</b><br>金额：%{y:,.0f} 万元<extra></extra>",
    ))
    fig_wf.update_layout(
        **base_layout(
            title="2025年利润形成瀑布图（万元）",
            height=470,
            showlegend=False,
        )
    )
    fig_wf.update_yaxes(title_text="金额（万元）")
    st.plotly_chart(fig_wf, use_container_width=True)

    st.markdown("""
    <div class="insight-box teal">
    🔬 <b>研发费用增速（18.94%）高于收入增速（17.87%）</b>，
    显示公司持续加大技术投入，研发费用率维持在 9.90%，
    在国内工控行业属于高研发密度。808 名研发人员占员工总数 30.33%。
    </div>
    <div class="insight-box red">
    ⚠️ <b>销售费用增速（8.67%）低于收入增速</b>，销售效率提升；
    但管理费用增速（14.71%）接近收入增速，需关注组织规模扩张的管理效率。
    </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
# Tab 5：数据导出
# ─────────────────────────────────────────────

def render_tab_export(data: dict):
    st.markdown("### 📥 财报数据导出中心")

    selected_table = st.selectbox(
        "选择要查看/导出的数据表",
        options=[
            "年度损益数据 (annual_pnl)",
            "分季度数据 (quarterly)",
            "产品线数据 (product_revenue)",
            "地区数据 (regional_revenue)",
            "渠道数据 (channel_data)",
            "境内外数据 (geo_data)",
            "主要财务指标 (key_metrics)",
            "费用结构 (expense_structure)",
            "产销量数据 (production_sales)",
        ]
    )

    key_map = {
        "年度损益数据 (annual_pnl)":      "annual_pnl",
        "分季度数据 (quarterly)":          "quarterly",
        "产品线数据 (product_revenue)":    "product_revenue",
        "地区数据 (regional_revenue)":     "regional_revenue",
        "渠道数据 (channel_data)":         "channel_data",
        "境内外数据 (geo_data)":           "geo_data",
        "主要财务指标 (key_metrics)":      "key_metrics",
        "费用结构 (expense_structure)":    "expense_structure",
        "产销量数据 (production_sales)":   "production_sales",
    }

    df_show = data[key_map[selected_table]].copy()

    search = st.text_input("🔍 搜索过滤（输入关键词）",
                           placeholder="如：广东、PLC、Q1...")
    if search:
        mask = df_show.astype(str).apply(
            lambda col: col.str.contains(search, case=False, na=False)
        ).any(axis=1)
        df_show = df_show[mask]

    st.dataframe(df_show, use_container_width=True, height=400)
    st.caption(f"共 {len(df_show)} 行数据")

    csv_buffer = io.StringIO()
    df_show.to_csv(csv_buffer, index=False, encoding="utf-8-sig")
    st.download_button(
        label="⬇️ 下载 CSV（当前表格）",
        data=csv_buffer.getvalue().encode("utf-8-sig"),
        file_name=f"xinje_2025_{key_map[selected_table]}.csv",
        mime="text/csv",
    )

    st.divider()
    st.markdown("### 📦 全量数据打包下载")
    all_dfs = []
    for k, v in data.items():
        if isinstance(v, pd.DataFrame):
            v_copy = v.copy()
            v_copy.insert(0, "数据表", k)
            all_dfs.append(v_copy)

    if all_dfs:
        df_all  = pd.concat(all_dfs, ignore_index=True)
        csv_all = df_all.to_csv(index=False, encoding="utf-8-sig")
        st.download_button(
            label="⬇️ 下载全量财报数据 CSV",
            data=csv_all.encode("utf-8-sig"),
            file_name="xinje_2025_full_report.csv",
            mime="text/csv",
        )

    st.divider()
    st.markdown("### 📌 数据说明")
    st.info("""
    **数据来源：** 无锡信捷电气股份有限公司 2025年年度报告（合并报表口径）

    **货币单位：** 人民币万元（特别标注除外）

    **数据口径说明：**
    - 营业收入：合并报表口径，含主营业务及其他业务
    - 产品线数据：母公司口径（主营业务分产品）
    - 地区数据：母公司口径（主营业务分地区）
    - 渠道数据：母公司口径（主营业务分销售模式）

    **重要提示：** 本看板数据仅供内部分析参考，不构成投资建议。
    """)

    div_data = data["dividend_data"]
    st.markdown("### 💰 2025年利润分配方案")
    d1, d2, d3 = st.columns(3)
    with d1:
        st.metric("归母净利润",   f"{div_data['归母净利润(万元)']:,.2f} 万元")
        st.metric("现金分红总额", f"{div_data['现金分红总额(万元)']:,.2f} 万元")
    with d2:
        st.metric("分红比例",           f"{div_data['分红比例(%)']:.2f}%")
        st.metric("年度每股股息（含税）", f"{div_data['年度每股股息(元)']:.2f} 元")
    with d3:
        st.metric("半年度每股股息（含税）", f"{div_data['半年度每股股息(元)']:.2f} 元")
        st.markdown("""
        <div class="insight-box green">
        💡 2025年现金分红比例高达 <b>95.05%</b>，
        彰显公司强烈的股东回报意愿。
        </div>
        """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
# 侧边栏
# ─────────────────────────────────────────────

def render_sidebar():
    with st.sidebar:
        st.markdown("""
        <div style="text-align:center; padding:20px 0 12px 0;
                    border-bottom:2px solid #E0E8F5; margin-bottom:16px;">
            <div style="font-size:2.2rem;">⚡</div>
            <h2 style="color:#1B3A8C; margin:4px 0 2px 0;
                       font-size:1.3rem; font-weight:700;">信捷电气</h2>
            <p style="color:#6B7A99; font-size:0.82rem; margin:2px 0;">
                股票代码：603416 | 上交所
            </p>
            <p style="color:#2BBFBF; font-size:0.78rem; font-weight:600;">
                2025年年度财报分析看板
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("#### 🏢 公司概况")
        st.markdown("""
        - **全称：** 无锡信捷电气股份有限公司
        - **主营：** 工业自动化产品研发/生产/销售
        - **核心产品：** PLC、伺服系统、HMI、机器人
        - **总部：** 江苏省无锡市
        - **上市时间：** 2016年
        """)

        st.divider()

        st.markdown("#### 📊 2025年核心数据速览")
        st.markdown("""
        | 指标 | 数值 |
        |------|------|
        | 营业收入 | **20.14亿元** |
        | 同比增长 | **+17.87%** |
        | 归母净利润 | **2.54亿元** |
        | 净利润增长 | **+11.21%** |
        | 研发费用率 | **9.90%** |
        | 现金分红比 | **95.05%** |
        | 海外订单增长 | **>60%** |
        """)

        st.divider()

        st.markdown("#### ⚙️ 分析视角")
        view_mode = st.radio(
            "选择分析维度",
            ["全面分析", "增长聚焦", "盈利聚焦"],
            index=0,
        )

        st.divider()
        st.caption("📅 数据截止：2025年12月31日")
        st.caption("🔒 数据来源：公司年度报告（合并报表）")

    return view_mode

# ─────────────────────────────────────────────
# 主程序入口
# ─────────────────────────────────────────────

def main():
    inject_css()

    st.markdown("""
    <div class="main-header">
        <h1>⚡ 信捷电气 (603416) · 2025年度财报可视化看板</h1>
        <p>无锡信捷电气股份有限公司 | 工业自动化领域国产领军企业 |
           营收首破20亿 · 国产PLC市占率第一 · 海外订单增长60%+</p>
    </div>
    """, unsafe_allow_html=True)

    data      = load_financial_data()
    view_mode = render_sidebar()

    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 CEO 概览圈",
        "🏭 产品线分析",
        "🗺️ 市场与渠道",
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