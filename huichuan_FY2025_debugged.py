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
from plotly.subplots import make_subplots
import pandas as pd

st.set_page_config(
    page_title="汇川技术 FY2025 竞争情报看板",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =============================================================================
# 配色方案
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
# 数据层
# =============================================================================
def load_financial_data():
    """数据层：所有DataFrame和dict集中定义，单位：万元（人民币）。"""

    # 盈利指标（近3年）
    profit_df = pd.DataFrame({
        "年份": ["2023年", "2024年", "2025年"],
        "营业收入": [3041993, 3704095, 4510484],
        "归母净利润": [474186, 428549, 505000],
        "扣非归母净利润": [407118, 403583, 495051],
        "研发费用": [262415, 314708, 425577],
        "销售费用": [0, 148088, 153557],
        "管理费用": [0, 154135, 182508],
    })
    profit_df["净利率"] = profit_df["归母净利润"] / profit_df["营业收入"] * 100
    profit_df["研发费用率"] = profit_df["研发费用"] / profit_df["营业收入"] * 100
    profit_df["营收增速"] = profit_df["营业收入"].pct_change() * 100
    profit_df["净利增速"] = profit_df["归母净利润"].pct_change() * 100

    # 现金流指标
    cashflow_df = pd.DataFrame({
        "年份": ["2023年", "2024年", "2025年"],
        "经营活动现金净流量": [336992, 720044, 668103],
        "归母净利润": [474186, 428549, 505000],
    })
    cashflow_df["现金保障倍数"] = cashflow_df["经营活动现金净流量"] / cashflow_df["归母净利润"] * 100

    # 资产负债指标
    balance_df = pd.DataFrame({
        "年份": ["2023年末", "2024年末", "2025年末"],
        "总资产": [4895756, 5717882, 7131439],
        "归母净资产": [2448189, 2799438, 3535299],
        "应收账款": [0, 1071382, 1151881],
        "存货": [0, 695551, 807900],
        "ROE": [21.66, 16.52, 16.34],
    })
    balance_df["负债合计"] = balance_df["总资产"] - balance_df["归母净资产"]
    balance_df["资产负债率"] = balance_df["负债合计"] / balance_df["总资产"] * 100

    # 分季度数据
    quarterly_df = pd.DataFrame({
        "季度": ["Q1", "Q2", "Q3", "Q4"],
        "营业收入": [897791, 1153145, 1115325, 1344224],
        "归母净利润": [132283, 164556, 128574, 79587],
        "扣非净利润": [123379, 143765, 121666, 106240],
        "经营现金流": [26255, 275752, 91059, 275037],
    })
    quarterly_df["净利率"] = quarterly_df["归母净利润"] / quarterly_df["营业收入"] * 100

    # 产品线数据（产品口径）
    prod_labels = ["工业自动化与数字化", "新能源汽车动力系统", "新兴产业(机器人等)", "其他"]
    product_df = pd.DataFrame({
        "产品": prod_labels,
        "收入2025": [2224540, 2032258, 179502, 74184],
        "收入2024": [1872722, 1607976, 155009, 68388],
        "毛利率2025": [40.27, 16.10, 0, 0],
        "毛利率2024": [38.62, 16.38, 0, 0],
        "占比2025": [49.32, 45.06, 3.98, 1.64],
    })
    product_df["同比增速"] = (product_df["收入2025"] - product_df["收入2024"]) / product_df["收入2024"] * 100

    # 地区数据
    region_df = pd.DataFrame({
        "地区": ["中国内地", "境外"],
        "收入2025": [4245595, 264889],
        "收入2024": [3500162, 203933],
        "毛利率2025": [28.55, 29.89],
        "毛利率2024": [28.54, 31.46],
        "占比2025": [94.13, 5.87],
    })
    region_df["同比增速"] = (region_df["收入2025"] - region_df["收入2024"]) / region_df["收入2024"] * 100

    # 费用数据
    expense_df = pd.DataFrame({
        "费用项目": ["销售费用", "管理费用", "研发费用"],
        "金额2025": [153557, 182508, 425577],
        "金额2024": [148088, 154135, 314708],
    })
    expense_df["同比增速"] = (expense_df["金额2025"] - expense_df["金额2024"]) / expense_df["金额2024"] * 100

    # 研发费用趋势
    rd_df = pd.DataFrame({
        "年份": ["2023年", "2024年", "2025年"],
        "研发费用": [262415, 314708, 425577],
        "研发费用率": [8.63, 8.50, 9.44],
    })

    # 研发人员学历结构
    rd_edu_df = pd.DataFrame({
        "学历": ["博士", "硕士", "本科", "大专及以下"],
        "人数2025": [94, 3461, 3290, 777],
        "人数2024": [58, 2591, 2184, 685],
    })

    # 产销量数据
    volume_df = pd.DataFrame({
        "板块": ["智能制造", "新能源汽车"],
        "销售量2025": [25971863, 5933895],
        "生产量2025": [25499533, 6108223],
        "库存量2025": [1361822, 724156],
        "销售量2024": [19785481, 4619378],
        "生产量2024": [20084736, 4845348],
        "库存量2024": [1834152, 549828],
    })

    # 雷达图数据
    radar_df = pd.DataFrame({
        "维度": ["毛利率", "净利率", "研发费用率", "销售费用率", "ROE"],
        "2023年": [0, 15.59, 8.63, 0, 21.66],
        "2024年": [28.70, 11.57, 8.50, 4.00, 16.52],
        "2025年": [28.95, 11.20, 9.44, 3.40, 16.34],
    })

    # 分红数据
    dividend_data = {
        "每股分红": 0.50,
        "分红总额": 135332,
        "分红比例": 26.8,
        "总股本": 2706636087,
        "EPS基本2025": 1.87,
        "EPS基本2024": 1.60,
        "EPS稀释2025": 1.85,
    }

    # 瀑布图数据
    waterfall_data = {
        "x": ["营业收入", "营业成本", "毛利润", "销售费用", "管理费用", "研发费用", "财务收益", "其他收益", "归母净利润"],
        "y": [4510484, -3202000, 1308484, -153557, -182508, -425577, 6572, 714375, 505000],
        "measure": ["absolute", "relative", "total", "relative", "relative", "relative", "relative", "relative", "total"],
    }

    return {
        "profit": profit_df,
        "cashflow": cashflow_df,
        "balance": balance_df,
        "quarterly": quarterly_df,
        "product": product_df,
        "region": region_df,
        "expense": expense_df,
        "rd": rd_df,
        "rd_edu": rd_edu_df,
        "volume": volume_df,
        "radar": radar_df,
        "dividend": dividend_data,
        "waterfall": waterfall_data,
    }


# =============================================================================
# 样式层
# =============================================================================
def inject_css():
    """注入全局CSS样式。"""
    st.markdown("""
<style>
.stApp {
    background-color: #F5F7FA;
    color: #1A2B4A;
    font-family: 'Segoe UI','PingFang SC','Microsoft YaHei',sans-serif;
}
.main-header {
    background: linear-gradient(135deg, #1B3A8C 0%, #2B5299 60%, #1B3A8C 100%);
    border-left: 6px solid #2BBFBF;
    border-radius: 14px;
    box-shadow: 0 4px 20px rgba(27,58,140,0.18);
    padding: 22px 30px 18px 30px;
    margin-bottom: 20px;
}
.main-header h1 { color: #FFFFFF; font-size: 1.9rem; font-weight: 700; margin: 0 0 6px 0; }
.main-header p  { color: #A8C4E8; font-size: 0.88rem; margin: 0; }
[data-testid="metric-container"] {
    background: #FFFFFF;
    border: 1px solid #E0E8F5;
    border-radius: 12px;
    border-top: 4px solid #1B3A8C;
    box-shadow: 0 2px 12px rgba(27,58,140,0.08);
    padding: 12px 16px;
}
[data-testid="metric-container"]:hover { box-shadow: 0 6px 24px rgba(27,58,140,0.15); }
[data-testid="stMetricLabel"]  { color: #6B7A99 !important; font-size: 0.82rem !important; font-weight: 600 !important; }
[data-testid="stMetricValue"]  { color: #1B3A8C !important; font-size: 1.5rem !important; font-weight: 700 !important; }
[data-testid="stMetricDelta"] svg { display: none; }
[data-testid="stMetricDelta"]  { font-size: 0.8rem; font-weight: 600; }
button[data-baseweb="tab"] { color: #6B7A99; font-weight: 600; font-size: 0.88rem; border-radius: 8px; }
button[data-baseweb="tab"][aria-selected="true"] { background: #1B3A8C !important; color: #FFFFFF !important; border-radius: 8px; }
[data-testid="stSidebar"] { background: #FFFFFF; border-right: 2px solid #E0E8F5; }
h3 { color: #1B3A8C !important; border-bottom: 2px solid #2BBFBF; padding-bottom: 6px; margin-bottom: 16px !important; }
.insight-box       { background: #EEF3FC; border-left: 5px solid #1B3A8C; border-radius: 10px; padding: 13px 18px; font-size: 0.87rem; margin: 8px 0; line-height: 1.6; }
.insight-box.green { background: #EAF7F0; border-left-color: #27AE60; }
.insight-box.red   { background: #FEF0EE; border-left-color: #E74C3C; }
.insight-box.teal  { background: #E8F8F8; border-left-color: #2BBFBF; }
.stDownloadButton > button { background: #1B3A8C; color: white; border: none; border-radius: 8px; font-weight: 600; }
.stDownloadButton > button:hover { background: #2BBFBF; color: white; }
.sidebar-logo { background: linear-gradient(135deg, #1B3A8C, #2B5299); border-radius: 12px; padding: 16px; text-align: center; margin-bottom: 16px; }
.sidebar-logo .cn  { font-size: 1.1rem; font-weight: 700; color: #FFFFFF; }
.sidebar-logo .tk  { font-size: 0.8rem; color: #A8C4E8; }
.sidebar-logo .dt  { font-size: 0.75rem; color: #2BBFBF; margin-top: 4px; }
</style>
""", unsafe_allow_html=True)


# =============================================================================
# 图表统一布局
# =============================================================================
def base_layout(**kwargs):
    """图表统一布局配置。"""
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


# =============================================================================
# KPI卡片
# =============================================================================
def kpi_card(col, label, value, delta_val=None, note=None):
    """KPI卡片组件。"""
    with col:
        st.metric(label=label, value=value, delta=delta_val)
        if note:
            st.caption(note)


# =============================================================================
# Tab1：CEO概览圈
# =============================================================================
def render_tab_ceo(data):
    """Tab1：CEO概览圈。"""
    profit    = data["profit"]
    quarterly = data["quarterly"]
    radar     = data["radar"]

    st.markdown("### 📊 核心经营指标（FY2025）")
    c1, c2, c3, c4, c5, c6 = st.columns(6)
    kpi_card(c1, "营业总收入",    "451.05亿元",  note="同比 +21.77%")
    kpi_card(c2, "归母净利润",    "50.50亿元",   note="同比 +17.84%")
    kpi_card(c3, "扣非归母净利润","49.51亿元",   note="同比 +22.66%")
    kpi_card(c4, "研发投入",      "42.56亿元",   note="研发费用率 9.44%")
    kpi_card(c5, "基本EPS",       "1.87 元/股",  note="同比 +16.88%")
    kpi_card(c6, "现金分红比例",  "26.8%",       note="每股0.50元（含税）")

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### 🏦 资产健康度（FY2025末）")
    a1, a2, a3, a4 = st.columns(4)
    kpi_card(a1, "总资产",       "713.14亿元", note="同比 +24.72%")
    kpi_card(a2, "归母净资产",   "353.53亿元", note="同比 +26.29%")
    kpi_card(a3, "加权平均ROE",  "16.34%",     note="较2024年 -0.18pct")
    kpi_card(a4, "境外业务增速", "+29.89%",    note="境外收入占比5.87%")

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### 📈 三年财务趋势 & 盈利质量雷达")
    col_l, col_r = st.columns([3, 2])

    with col_l:
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_trace(go.Bar(
            x=profit["年份"], y=profit["营业收入"],
            name="营业收入（万元）",
            marker_color=COLORS["primary"], opacity=0.82,
            text=[f"{v/10000:.1f}亿" for v in profit["营业收入"]],
            textposition="outside",
            hovertemplate="<b>%{x}</b><br>营业收入：%{y:,.0f} 万元<extra></extra>",
        ), secondary_y=False)
        fig.add_trace(go.Scatter(
            x=profit["年份"], y=profit["归母净利润"],
            name="归母净利润（万元）",
            mode="lines+markers+text",
            line=dict(color=COLORS["secondary"], width=2.5),
            marker=dict(symbol="diamond", size=10, color=COLORS["secondary"]),
            text=[f"{v/10000:.1f}亿" for v in profit["归母净利润"]],
            textposition="top center",
            hovertemplate="<b>%{x}</b><br>归母净利润：%{y:,.0f} 万元<extra></extra>",
        ), secondary_y=False)
        fig.add_trace(go.Scatter(
            x=profit["年份"], y=profit["净利率"],
            name="净利率（%）",
            mode="lines+markers",
            line=dict(color=COLORS["success"], width=2, dash="dot"),
            marker=dict(size=7, color=COLORS["success"]),
            hovertemplate="<b>%{x}</b><br>净利率：%{y:.2f}%<extra></extra>",
        ), secondary_y=True)
        fig.update_layout(**base_layout(
            title="营业收入 / 归母净利润 / 净利率（三年趋势）", height=420,
            legend=dict(orientation="h", y=-0.18, x=0.5, xanchor="center",
                        bgcolor="rgba(255,255,255,0.8)", bordercolor="#E0E8F5", borderwidth=1)
        ))
        fig.update_yaxes(title_text="金额（万元）", gridcolor=COLORS["grid_color"], secondary_y=False)
        fig.update_yaxes(title_text="净利率（%）",  gridcolor=COLORS["grid_color"], secondary_y=True)
        st.plotly_chart(fig, use_container_width=True)

    with col_r:
        dims = radar["维度"].tolist()
        dims_c = dims + [dims[0]]
        def safe(col):
            v = radar[col].tolist()
            v = [x if x else 0 for x in v]
            return v + [v[0]]
        fig_r = go.Figure()
        for yr, clr, dsh in [("2023年", COLORS["neutral"], "dot"),
                              ("2024年", COLORS["secondary"], "dash"),
                              ("2025年", COLORS["primary"], "solid")]:
            fig_r.add_trace(go.Scatterpolar(
                r=safe(yr), theta=dims_c, fill="toself", name=yr,
                line=dict(color=clr, dash=dsh, width=2),
                hovertemplate="<b>%{theta}</b><br>数值：%{r:.2f}%<extra></extra>",
            ))
        fig_r.update_layout(**base_layout(
            title="盈利质量雷达图（三年对比）", height=420,
            polar=dict(
                radialaxis=dict(visible=True, range=[0, 45], gridcolor=COLORS["grid_color"]),
                angularaxis=dict(gridcolor=COLORS["grid_color"])
            ),
            legend=dict(orientation="h", y=-0.15, x=0.5, xanchor="center",
                        bgcolor="rgba(255,255,255,0.8)", bordercolor="#E0E8F5", borderwidth=1)
        ))
        st.plotly_chart(fig_r, use_container_width=True)

    st.markdown("### 🗓️ 分季度营收节奏（FY2025）")
    fig_q = make_subplots(rows=1, cols=2,
                          subplot_titles=("季度营业收入（万元）", "季度净利率（%）"),
                          horizontal_spacing=0.1)
    q_colors = [COLORS["neutral"], COLORS["primary"], COLORS["primary"], COLORS["secondary"]]
    fig_q.add_trace(go.Bar(
        x=quarterly["季度"], y=quarterly["营业收入"],
        marker_color=q_colors,
        text=[f"{v/10000:.1f}亿" for v in quarterly["营业收入"]],
        textposition="outside",
        hovertemplate="<b>%{x}</b><br>营业收入：%{y:,.0f} 万元<extra></extra>",
    ), row=1, col=1)
    fig_q.add_trace(go.Scatter(
        x=quarterly["季度"], y=quarterly["净利率"],
        mode="lines+markers+text",
        line=dict(color=COLORS["secondary"], width=2.5),
        marker=dict(size=9, color=COLORS["secondary"]),
        text=[f"{v:.1f}%" for v in quarterly["净利率"]],
        textposition="top center",
        hovertemplate="<b>%{x}</b><br>净利率：%{y:.2f}%<extra></extra>",
    ), row=1, col=2)
    fig_q.update_layout(**base_layout(height=400, showlegend=False))
    fig_q.update_yaxes(gridcolor=COLORS["grid_color"])
    st.plotly_chart(fig_q, use_container_width=True)

    st.markdown("### 💡 竞争情报洞察")
    st.markdown("""
<div class="insight-box green">
⚡ <b>营收规模突破451亿元，同比+21.77%</b>，连续两年保持20%以上高增速，
说明汇川技术在工控+新能源双赛道已形成规模化增长飞轮。
<b>西门子DI视角：</b>汇川在中国市场的营收体量已接近西门子DI中国区业务量级，
需高度警惕其在中低端工控市场的价格渗透和客户锁定速度。
</div><br>
<div class="insight-box red">
⚠️ <b>净利率从2023年15.59%降至2025年11.20%</b>，ROE从21.66%降至16.34%，
说明新能源汽车业务（毛利率仅16.10%）的高速扩张正在稀释整体盈利质量。
<b>西门子DI视角：</b>这是汇川的结构性隐患——若新能源汽车竞争进一步加剧，
其利润空间将持续承压，西门子DI可借此强调高端自动化的高价值定位。
</div><br>
<div class="insight-box teal">
🔍 <b>Q4净利润仅7.96亿元，净利率5.92%</b>，远低于Q1-Q3均值，
说明Q4存在明显的费用集中确认或计提压力。
<b>西门子DI视角：</b>Q3末是抢占汇川客户预算份额的最佳窗口期。
</div>
""", unsafe_allow_html=True)


# =============================================================================
# Tab2：产品线分析
# =============================================================================
def render_tab_product(data):
    """Tab2：产品线分析。"""
    product = data["product"]
    volume  = data["volume"]

    st.markdown("### 🏭 产品线收入结构（FY2025）")
    col1, col2 = st.columns(2)

    with col1:
        fig_pie = go.Figure(go.Pie(
            labels=product["产品"],
            values=product["收入2025"],
            hole=0.52,
            marker=dict(colors=PRODUCT_COLORS[:4], line=dict(color="#FFFFFF", width=2)),
            textinfo="label+percent",
            hovertemplate="<b>%{label}</b><br>收入：%{value:,.0f} 万元<br>占比：%{percent}<extra></extra>",
        ))
        fig_pie.add_annotation(text="<b>总收入</b><br>451.05亿元",
                               x=0.5, y=0.5, showarrow=False,
                               font=dict(size=13, color=COLORS["primary"]))
        fig_pie.update_layout(**base_layout(title="产品线收入占比（FY2025）", height=360, showlegend=False))
        st.plotly_chart(fig_pie, use_container_width=True)

    with col2:
        growth_vals = product["同比增速"].tolist()
        bar_colors = [COLORS["success"] if v >= 0 else COLORS["danger"] for v in growth_vals]
        fig_g = go.Figure(go.Bar(
            y=product["产品"], x=growth_vals, orientation="h",
            marker_color=bar_colors,
            text=[f"{v:+.2f}%" for v in growth_vals],
            textposition="outside",
            hovertemplate="<b>%{y}</b><br>同比增速：%{x:.2f}%<extra></extra>",
        ))
        fig_g.add_vline(x=0, line_dash="dash", line_color=COLORS["text_muted"], line_width=1)
        fig_g.add_vline(x=21.77, line_dash="dot", line_color=COLORS["primary"], line_width=2,
                        annotation_text="整体增速 21.77%",
                        annotation_position="top right",
                        annotation_font=dict(color=COLORS["primary"], size=11))
        fig_g.update_layout(**base_layout(title="产品线同比增速（FY2025）", height=360, showlegend=False))
        st.plotly_chart(fig_g, use_container_width=True)

    st.markdown("### 💰 产品线收入 vs 毛利率（主要产品）")
    fig_dual = make_subplots(specs=[[{"secondary_y": True}]])
    labels2 = ["工业自动化与数字化", "新能源汽车动力系统"]
    fig_dual.add_trace(go.Bar(x=labels2, y=[1872722, 1607976], name="2024年收入",
                              marker_color=COLORS["neutral"], opacity=0.75,
                              hovertemplate="<b>%{x}</b><br>2024年收入：%{y:,.0f} 万元<extra></extra>"),
                       secondary_y=False)
    fig_dual.add_trace(go.Bar(x=labels2, y=[2224540, 2032258], name="2025年收入",
                              marker_color=COLORS["primary"], opacity=0.85,
                              text=["222.5亿", "203.2亿"], textposition="outside",
                              hovertemplate="<b>%{x}</b><br>2025年收入：%{y:,.0f} 万元<extra></extra>"),
                       secondary_y=False)
    fig_dual.add_trace(go.Scatter(x=labels2, y=[40.27, 16.10], name="2025年毛利率",
                                  mode="markers+lines+text",
                                  marker=dict(symbol="star", size=13, color=COLORS["secondary"]),
                                  line=dict(color=COLORS["secondary"], width=2),
                                  text=["40.27%", "16.10%"], textposition="top center",
                                  hovertemplate="<b>%{x}</b><br>2025年毛利率：%{y:.2f}%<extra></extra>"),
                       secondary_y=True)
    fig_dual.add_trace(go.Scatter(x=labels2, y=[38.62, 16.38], name="2024年毛利率",
                                  mode="markers+lines",
                                  marker=dict(symbol="star", size=10, color=COLORS["neutral"]),
                                  line=dict(color=COLORS["neutral"], width=1.5, dash="dot"),
                                  hovertemplate="<b>%{x}</b><br>2024年毛利率：%{y:.2f}%<extra></extra>"),
                       secondary_y=True)
    fig_dual.update_layout(**base_layout(
        title="主要产品线收入 & 毛利率对比（FY2024 vs FY2025）", height=420, barmode="group",
        legend=dict(orientation="h", y=-0.18, x=0.5, xanchor="center",
                    bgcolor="rgba(255,255,255,0.8)", bordercolor="#E0E8F5", borderwidth=1)
    ))
    fig_dual.update_yaxes(title_text="收入（万元）", gridcolor=COLORS["grid_color"], secondary_y=False)
    fig_dual.update_yaxes(title_text="毛利率（%）",  gridcolor=COLORS["grid_color"], secondary_y=True)
    st.plotly_chart(fig_dual, use_container_width=True)

    st.markdown("### 📦 主要产品产销量对比（FY2025 vs FY2024）")
    fig_vol = go.Figure()
    fig_vol.add_trace(go.Bar(name="2025年销售量", x=volume["板块"], y=volume["销售量2025"],
                             marker_color=COLORS["primary"],
                             hovertemplate="<b>%{x}</b><br>2025年销售量：%{y:,.0f} PCS<extra></extra>"))
    fig_vol.add_trace(go.Bar(name="2025年生产量", x=volume["板块"], y=volume["生产量2025"],
                             marker_color=COLORS["secondary"],
                             hovertemplate="<b>%{x}</b><br>2025年生产量：%{y:,.0f} PCS<extra></extra>"))
    fig_vol.add_trace(go.Bar(name="2024年销售量", x=volume["板块"], y=volume["销售量2024"],
                             marker_color=COLORS["neutral"],
                             hovertemplate="<b>%{x}</b><br>2024年销售量：%{y:,.0f} PCS<extra></extra>"))
    fig_vol.update_layout(**base_layout(
        title="主要产品产销量对比（PCS）", height=400, barmode="group",
        legend=dict(orientation="h", y=-0.18, x=0.5, xanchor="center",
                    bgcolor="rgba(255,255,255,0.8)", bordercolor="#E0E8F5", borderwidth=1)
    ))
    st.plotly_chart(fig_vol, use_container_width=True)

    st.markdown("### 💡 竞争情报洞察")
    st.markdown("""
<div class="insight-box green">
⚡ <b>工业自动化与数字化产品毛利率40.27%，同比提升1.65pct</b>，
说明汇川在工控核心产品上的定价能力持续增强，已具备与日系品牌正面竞争的毛利水平。
<b>西门子DI视角：</b>需在高端应用场景（精密运动控制、功能安全、工业软件集成）构建差异化壁垒。
</div><br>
<div class="insight-box red">
⚠️ <b>新能源汽车业务收入占比已达45.06%，毛利率仅16.10%</b>，
说明汇川正面临"增收不增利"的结构性压力，主机厂降本压力持续向供应链传导。
<b>西门子DI视角：</b>这是汇川的战略软肋，西门子DI可借此强调工业软件和高端自动化的高价值定位。
</div><br>
<div class="insight-box teal">
🔍 <b>智能制造板块销售量同比+31.27%，远超收入增速18.79%</b>，量增价降趋势明显。
<b>西门子DI视角：</b>西门子DI应加速在高端定制化、行业解决方案等高附加值领域的布局。
</div>
""", unsafe_allow_html=True)


# =============================================================================
# Tab3：市场与渠道
# =============================================================================
def render_tab_market(data):
    """Tab3：市场与渠道。"""
    region = data["region"]

    st.markdown("### 🌏 地区收入分布（FY2025）")
    col1, col2 = st.columns([3, 2])

    with col1:
        fig_bar = go.Figure(go.Bar(
            y=region["地区"], x=region["收入2025"], orientation="h",
            marker_color=[COLORS["primary"], COLORS["secondary"]],
            text=[f"{v/10000:.1f}亿" for v in region["收入2025"]],
            textposition="outside",
            hovertemplate="<b>%{y}</b><br>收入：%{x:,.0f} 万元<extra></extra>",
        ))
        fig_bar.update_layout(**base_layout(title="地区收入分布（FY2025）", height=300, showlegend=False))
        st.plotly_chart(fig_bar, use_container_width=True)

        fig_m = go.Figure()
        fig_m.add_trace(go.Bar(x=region["地区"], y=region["毛利率2024"], name="2024年毛利率",
                               marker_color=COLORS["neutral"],
                               hovertemplate="<b>%{x}</b><br>2024年毛利率：%{y:.2f}%<extra></extra>"))
        fig_m.add_trace(go.Bar(x=region["地区"], y=region["毛利率2025"], name="2025年毛利率",
                               marker_color=COLORS["primary"],
                               text=[f"{v:.2f}%" for v in region["毛利率2025"]],
                               textposition="outside",
                               hovertemplate="<b>%{x}</b><br>2025年毛利率：%{y:.2f}%<extra></extra>"))
        fig_m.update_layout(**base_layout(
            title="地区毛利率对比（FY2024 vs FY2025）", height=300, barmode="group",
            legend=dict(orientation="h", y=-0.22, x=0.5, xanchor="center",
                        bgcolor="rgba(255,255,255,0.8)", bordercolor="#E0E8F5", borderwidth=1)
        ))
        st.plotly_chart(fig_m, use_container_width=True)

    with col2:
        growth_colors = [COLORS["success"] if v >= 21.77 else COLORS["primary"]
                         for v in region["同比增速"]]
        fig_rg = go.Figure(go.Bar(
            y=region["地区"], x=region["同比增速"], orientation="h",
            marker_color=growth_colors,
            text=[f"{v:+.2f}%" for v in region["同比增速"]],
            textposition="outside",
            hovertemplate="<b>%{y}</b><br>同比增速：%{x:.2f}%<extra></extra>",
        ))
        fig_rg.add_vline(x=21.77, line_dash="dot", line_color=COLORS["primary"], line_width=2,
                         annotation_text="整体增速 21.77%",
                         annotation_position="top right",
                         annotation_font=dict(color=COLORS["primary"], size=11))
        fig_rg.update_layout(**base_layout(title="地区增速（FY2025）", height=300, showlegend=False))
        st.plotly_chart(fig_rg, use_container_width=True)

        fig_geo = go.Figure(go.Pie(
            labels=["境内", "境外"],
            values=[4245595, 264889],
            hole=0.52,
            marker=dict(colors=[COLORS["primary"], COLORS["secondary"]],
                        line=dict(color="#FFFFFF", width=2)),
            textinfo="label+percent",
            hovertemplate="<b>%{label}</b><br>收入：%{value:,.0f} 万元<br>占比：%{percent}<extra></extra>",
        ))
        fig_geo.add_annotation(text="<b>境内/境外</b><br>收入占比",
                               x=0.5, y=0.5, showarrow=False,
                               font=dict(size=11, color=COLORS["primary"]))
        fig_geo.update_layout(**base_layout(title="境内 vs 境外收入占比", height=300, showlegend=False))
        st.plotly_chart(fig_geo, use_container_width=True)

    st.info("📌 渠道披露说明：汇川技术2025年年报中，销售渠道未单独拆分直销与经销的收入及毛利率数据，如需细分数据请参考投资者关系公告。")

    st.markdown("### 💡 竞争情报洞察")
    st.markdown("""
<div class="insight-box red">
⚠️ <b>境外收入占比仅5.87%（约26.5亿元），同比增速+29.89%</b>，
说明汇川的国际化进程仍处于早期阶段，海外市场尚未形成规模。
<b>西门子DI视角：</b>汇川海外增速接近30%，若持续3-5年，将在东南亚、中东等新兴市场形成竞争压力，西门子DI需提前布局。
</div><br>
<div class="insight-box green">
⚡ <b>中国内地收入4,245,595万元，同比+21.30%，毛利率28.55%</b>，
说明汇川在本土市场的规模优势和渠道深度持续强化。
<b>西门子DI视角：</b>需在关键行业（锂电、光伏、汽车）加强本地化服务能力和快速响应机制。
</div><br>
<div class="insight-box teal">
🔍 <b>境外毛利率29.89%略高于境内28.55%</b>，说明汇川在海外市场尚未陷入价格战。
<b>西门子DI视角：</b>西门子DI在海外市场的价格优势窗口期有限，需加速技术壁垒和行业认证的差异化。
</div>
""", unsafe_allow_html=True)


# =============================================================================
# Tab4：费用与研发
# =============================================================================
def render_tab_rd(data):
    """Tab4：费用与研发。"""
    expense = data["expense"]
    rd      = data["rd"]
    rd_edu  = data["rd_edu"]
    wf      = data["waterfall"]

    st.markdown("### 💸 三大费用对比（FY2024 vs FY2025）")
    col1, col2 = st.columns(2)

    with col1:
        fig_e = go.Figure()
        fig_e.add_trace(go.Bar(x=expense["费用项目"], y=expense["金额2024"], name="2024年",
                               marker_color=COLORS["neutral"],
                               hovertemplate="<b>%{x}</b><br>2024年：%{y:,.0f} 万元<extra></extra>"))
        fig_e.add_trace(go.Bar(x=expense["费用项目"], y=expense["金额2025"], name="2025年",
                               marker_color=COLORS["primary"],
                               text=[f"{v/10000:.1f}亿" for v in expense["金额2025"]],
                               textposition="outside",
                               hovertemplate="<b>%{x}</b><br>2025年：%{y:,.0f} 万元<extra></extra>"))
        fig_e.update_layout(**base_layout(
            title="三大费用对比（FY2024 vs FY2025）", height=400, barmode="group",
            legend=dict(orientation="h", y=-0.18, x=0.5, xanchor="center",
                        bgcolor="rgba(255,255,255,0.8)", bordercolor="#E0E8F5", borderwidth=1)
        ))
        st.plotly_chart(fig_e, use_container_width=True)

    with col2:
        eg_colors = [COLORS["danger"] if v > 21.77 else COLORS["success"]
                     for v in expense["同比增速"]]
        fig_eg = go.Figure(go.Bar(
            x=expense["费用项目"], y=expense["同比增速"],
            marker_color=eg_colors,
            text=[f"{v:+.2f}%" for v in expense["同比增速"]],
            textposition="outside",
            hovertemplate="<b>%{x}</b><br>同比增速：%{y:.2f}%<extra></extra>",
        ))
        fig_eg.add_hline(y=21.77, line_dash="dot", line_color=COLORS["primary"], line_width=2,
                         annotation_text="营收增速 21.77%",
                         annotation_position="top right",
                         annotation_font=dict(color=COLORS["primary"], size=11))
        fig_eg.update_layout(**base_layout(title="费用增速 vs 营收增速（FY2025）", height=400, showlegend=False))
        st.plotly_chart(fig_eg, use_container_width=True)

    st.markdown("### 🔬 研发费用趋势（近3年）")
    col3, col4 = st.columns(2)

    with col3:
        fig_rd = make_subplots(specs=[[{"secondary_y": True}]])
        fig_rd.add_trace(go.Bar(
            x=rd["年份"], y=rd["研发费用"],
            name="研发费用（万元）", marker_color=COLORS["primary"], opacity=0.82,
            text=[f"{v/10000:.1f}亿" for v in rd["研发费用"]],
            textposition="outside",
            hovertemplate="<b>%{x}</b><br>研发费用：%{y:,.0f} 万元<extra></extra>",
        ), secondary_y=False)
        fig_rd.add_trace(go.Scatter(
            x=rd["年份"], y=rd["研发费用率"],
            name="研发费用率（%）",
            mode="lines+markers+text",
            line=dict(color=COLORS["secondary"], width=2.5),
            marker=dict(symbol="diamond", size=10, color=COLORS["secondary"]),
            text=[f"{v:.2f}%" for v in rd["研发费用率"]],
            textposition="top center",
            hovertemplate="<b>%{x}</b><br>研发费用率：%{y:.2f}%<extra></extra>",
        ), secondary_y=True)
        fig_rd.update_layout(**base_layout(
            title="研发费用 & 研发费用率趋势", height=400,
            legend=dict(orientation="h", y=-0.18, x=0.5, xanchor="center",
                        bgcolor="rgba(255,255,255,0.8)", bordercolor="#E0E8F5", borderwidth=1)
        ))
        fig_rd.update_yaxes(title_text="研发费用（万元）", gridcolor=COLORS["grid_color"], secondary_y=False)
        fig_rd.update_yaxes(title_text="研发费用率（%）",  gridcolor=COLORS["grid_color"], secondary_y=True)
        st.plotly_chart(fig_rd, use_container_width=True)

    with col4:
        fig_edu = go.Figure(go.Pie(
            labels=rd_edu["学历"],
            values=rd_edu["人数2025"],
            hole=0.42,
            marker=dict(colors=PRODUCT_COLORS[:4], line=dict(color="#FFFFFF", width=2)),
            textinfo="label+percent+value",
            hovertemplate="<b>%{label}</b><br>人数：%{value} 人<br>占比：%{percent}<extra></extra>",
        ))
        fig_edu.add_annotation(text="<b>研发人员</b><br>7,670人",
                               x=0.5, y=0.5, showarrow=False,
                               font=dict(size=12, color=COLORS["primary"]))
        fig_edu.update_layout(**base_layout(title="研发人员学历结构（FY2025）", height=400, showlegend=False))
        st.plotly_chart(fig_edu, use_container_width=True)

    st.markdown("### 🌊 利润瀑布图（FY2025，万元）")
    fig_wf = go.Figure(go.Waterfall(
        orientation="v",
        measure=wf["measure"],
        x=wf["x"],
        y=wf["y"],
        text=[f"{v:+,.0f}" if m == "relative" else f"{abs(v):,.0f}"
              for v, m in zip(wf["y"], wf["measure"])],
        textposition="outside",
        textfont=dict(size=10),
        increasing=dict(marker=dict(color=COLORS["success"])),
        decreasing=dict(marker=dict(color=COLORS["danger"])),
        totals=dict(marker=dict(color=COLORS["primary"])),
        connector=dict(line=dict(color=COLORS["grid_color"], width=1.5, dash="dot")),
        hovertemplate="<b>%{x}</b><br>金额：%{y:,.0f} 万元<extra></extra>",
    ))
    fig_wf.update_layout(**base_layout(
        title="FY2025 利润瀑布图（营业收入 → 归母净利润，万元）",
        height=470, showlegend=False,
    ))
    st.plotly_chart(fig_wf, use_container_width=True)
    st.caption("⚠️ 注：营业成本为估算值（营业收入×(1-综合毛利率28.95%)≈3,202,000万元）；其他收益含政府补助等非经常性项目。")

    st.markdown("### 💡 竞争情报洞察")
    st.markdown("""
<div class="insight-box red">
⚠️ <b>研发费用同比+35.23%（42.56亿元），远超营收增速21.77%</b>，
研发费用率从8.50%提升至9.44%，说明汇川正在加速研发投入以缩小与国际品牌的技术差距。
<b>西门子DI视角：</b>汇川在工业软件、控制层核心技术上的研发提速是最值得关注的信号，
西门子DI需持续强化在数字孪生、工业AI、功能安全等高端技术领域的领先优势。
</div><br>
<div class="insight-box green">
⚡ <b>研发人员从5,538人增至7,670人（+38.5%），硕士占比高达45.1%</b>，
说明汇川正在系统性地提升研发团队质量。
<b>西门子DI视角：</b>汇川的高学历研发团队将在2-3年内形成技术成果，
西门子DI需在专利布局、技术标准制定和行业认证上保持领先。
</div><br>
<div class="insight-box teal">
🔍 <b>销售费用增速仅3.69%，远低于营收增速21.77%</b>，说明汇川的销售效率在持续提升。
<b>西门子DI视角：</b>汇川依托经销商网络和存量客户复购实现低成本增长，
西门子DI需在关键客户深度绑定和解决方案粘性上加大投入。
</div>
""", unsafe_allow_html=True)


# =============================================================================
# Tab5：数据导出
# =============================================================================
def render_tab_export(data):
    """Tab5：数据导出。"""
    st.markdown("### 📥 数据导出中心")

    tables = {
        "盈利指标（近3年）":           data["profit"],
        "现金流指标（近3年）":          data["cashflow"],
        "资产负债指标（近3年末）":       data["balance"],
        "分季度数据（FY2025）":         data["quarterly"],
        "产品线数据（FY2025）":         data["product"],
        "地区数据（FY2025）":           data["region"],
        "费用数据（FY2025）":           data["expense"],
        "研发费用趋势（近3年）":         data["rd"],
        "研发人员学历结构（FY2025）":    data["rd_edu"],
        "产销量数据（FY2025）":         data["volume"],
    }

    col_sel, col_search = st.columns([2, 2])
    with col_sel:
        selected = st.selectbox("📋 选择数据表", list(tables.keys()))
    with col_search:
        kw = st.text_input("🔍 关键词过滤", placeholder="输入关键词...")

    df_show = tables[selected].copy()
    if kw:
        mask = df_show.astype(str).apply(lambda c: c.str.contains(kw, case=False, na=False)).any(axis=1)
        df_show = df_show[mask]

    st.dataframe(df_show, use_container_width=True, height=400)

    c1, c2 = st.columns(2)
    with c1:
        st.download_button(
            label=f"⬇️ 下载当前表（{selected}）",
            data=df_show.to_csv(index=False, encoding="utf-8-sig"),
            file_name=f"汇川FY2025_{selected}.csv",
            mime="text/csv"
        )
    with c2:
        all_dfs = []
        for name, df in tables.items():
            tmp = df.copy()
            tmp.insert(0, "数据表", name)
            all_dfs.append(tmp)
        st.download_button(
            label="⬇️ 下载全量数据包（所有表）",
            data=pd.concat(all_dfs, ignore_index=True).to_csv(index=False, encoding="utf-8-sig"),
            file_name="汇川FY2025_全量数据.csv",
            mime="text/csv"
        )

    st.info("""
📌 数据说明
- 数据来源：深圳市汇川技术股份有限公司 2025年年度报告（公开披露）
- 财务口径：合并报表，人民币计价
- 数据单位：金额类指标单位为万元（人民币）；产销量单位为PCS；比率类为%
- 数据截止：2025年12月31日
- 免责声明：本看板数据仅供西门子数字化工业（DI）内部竞争研究使用，不构成投资建议。
""")

    st.markdown("### 💰 利润分配方案（FY2025）")
    div = data["dividend"]
    d1, d2, d3 = st.columns(3)
    with d1:
        st.metric("每股现金分红（含税）", f"{div['每股分红']:.2f} 元/股")
        st.caption("每10股派发现金5元（含税）")
    with d2:
        st.metric("现金分红总额", f"{div['分红总额']:,.0f} 万元")
        st.caption(f"分红比例：{div['分红比例']:.1f}%")
    with d3:
        st.metric("基本EPS（FY2025）", f"{div['EPS基本2025']:.2f} 元/股")
        st.caption(f"稀释EPS：{div['EPS稀释2025']:.2f} 元/股")

    st.markdown("#### 📐 股息率动态计算")
    price = st.number_input("请输入当前股价（元）", min_value=0.01, max_value=9999.0,
                            value=50.0, step=0.5,
                            help="输入汇川技术（300124）当前市场股价，自动计算股息率")
    dy   = div["每股分红"] / price * 100
    pe   = price / div["EPS基本2025"]
    mcap = price * div["总股本"] / 10000

    y1, y2, y3 = st.columns(3)
    with y1:
        st.metric("股息率（含税）", f"{dy:.2f}%", delta=f"基于股价 {price:.2f} 元")
    with y2:
        st.metric("市盈率（PE）", f"{pe:.1f}x", delta=f"EPS {div['EPS基本2025']:.2f} 元")
    with y3:
        st.metric("市值估算", f"{mcap/10000:.0f} 亿元",
                  delta=f"总股本 {div['总股本']/1e8:.2f} 亿股")


# =============================================================================
# 侧边栏
# =============================================================================
def render_sidebar():
    """渲染侧边栏。"""
    with st.sidebar:
        st.markdown("""
<div class="sidebar-logo">
    <div style="font-size:2rem;">🏭</div>
    <div class="cn">汇川技术</div>
    <div class="tk">300124 · 深交所创业板</div>
    <div class="dt">FY2025 竞争情报看板</div>
</div>
""", unsafe_allow_html=True)

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
        st.markdown("#### ⚔️ 与西门子DI竞争重叠度")
        st.error("🔴 高度重叠")
        st.markdown("- 变频器 / 伺服系统\n- PLC / HMI\n- 工业机器人\n- 工业软件（数字化）")

        st.markdown("#### 🎯 分析视角")
        view_mode = st.radio("选择分析视角", ["全面分析", "增长聚焦", "盈利聚焦"], index=0)

        st.markdown("---")
        st.caption("📅 数据截止：2025年12月31日")
        st.caption("📄 数据来源：汇川技术2025年年度报告")
        st.caption("🔒 仅供西门子DI内部竞争研究使用")

    return view_mode


# =============================================================================
# 主函数
# =============================================================================
def main():
    """主函数：注入样式、加载数据、渲染看板。"""
    inject_css()
    data = load_financial_data()

    st.markdown("""
<div class="main-header">
    <h1>🏭 汇川技术（300124）· FY2025 竞争情报看板</h1>
    <p>深圳市汇川技术股份有限公司 · 2025年度财务报告深度分析 ·
    西门子数字化工业（DI）竞争情报团队专用 ·
    数据来源：汇川技术2025年年度报告（公开披露）</p>
</div>
""", unsafe_allow_html=True)

    render_sidebar()

    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 CEO概览圈",
        "🏭 产品线分析",
        "🌏 市场与渠道",
        "🔬 费用与研发",
        "📥 数据导出",
    ])

    with tab1: render_tab_ceo(data)
    with tab2: render_tab_product(data)
    with tab3: render_tab_market(data)
    with tab4: render_tab_rd(data)
    with tab5: render_tab_export(data)

    st.markdown("---")
    st.caption("""
⚠️ 免责声明：本看板由西门子数字化工业（DI）竞争情报团队生成，
所有数据来源于汇川技术2025年年度报告公开披露内容，仅供西门子内部竞争研究使用，
不构成任何投资建议。部分估算指标已在相应位置注明，请以原始财报数据为准。
未经授权，禁止对外传播或商业使用。
""")


if __name__ == "__main__":
    main()

# =============================================================================
# 运行说明：
# pip install streamlit plotly pandas numpy
# streamlit run huichuan_FY2025_dashboard.py
# =============================================================================
