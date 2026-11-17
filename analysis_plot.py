# -*- coding: utf-8 -*-
# ============================================================
# analysis_plot.py -> تحليل البيانات + رسم Visualization
# نرسم: الإغلاق عبر الزمن، توزيع المقابل، معامل الارتباط الحراري،
# ونعرض جدول معلومات التحليل وعدد الناقص
# ============================================================
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# ضبط الخط العربي في الرسوميات (يظهر بشكل مقروء)
plt.rcParams["font.family"] = "Segoe UI"

GOLD = "#D4AF37"
GOLD_SOFT = "#E9C46A"
TEAL = "#4BD6C9"
BLUE = "#8AB4F8"

def make_plots(df):
    """يرسم 3 رسوم بيانية ويرجع list of figures"""
    fig1, ax1 = plt.subplots(figsize=(10, 4))
    ax1.plot(df.index, df["Close"], color=GOLD, lw=1.6, label="Close")
    ax1.plot(df.index, df["MA20"], color=TEAL, lw=1, label="MA20")
    ax1.set_title("سعر الإغلاق والمتوسط المتحرك — Close Price & Moving Average")
    ax1.legend(frameon=False)
    ax1.grid(True)
    fig1.tight_layout()

    fig2, ax2 = plt.subplots(figsize=(8, 4))
    ax2.hist(df["Return"].dropna(), bins=60, color=GOLD_SOFT, alpha=0.85)
    ax2.set_title("توزيع نسب التغير اليومي — Daily Returns Distribution")
    ax2.grid(True)
    fig2.tight_layout()

    fig3, ax3 = plt.subplots(figsize=(8, 5))
    sns.heatmap(df[["Open","High","Low","Close","Volume","MA5","MA20","Return","Range"]].corr(),
                annot=True, cmap="magma", fmt=".2f", ax=ax3,
                linewidths=0.5, linecolor="#1D2531",
                annot_kws={"color": "#F3EEE4"},
                cbar_kws={"label": ""})
    ax3.set_title("خريطة الارتباط بين المتغيرات — Correlation Heatmap")
    ax3.tick_params(colors="#97A2B3")
    if ax3.xaxis.label:
        ax3.xaxis.label.set_color("#97A2B3")
    if ax3.yaxis.label:
        ax3.yaxis.label.set_color("#97A2B3")
    fig3.tight_layout()

    return [fig1, fig2, fig3]

def analysis_summary(df):
    """ملخص التحليل: عدد الصفوف، الأعمدة، الناقص، مقاييس مركزية"""
    missing = int(df.isna().sum().sum())
    summary = {
        "عدد الصفوف — Rows": len(df),
        "عدد الأعمدة — Columns": df.shape[1],
        "القيم المفقودة بعد التنظيف — Missing (cleaned)": missing,
        "أقدم تاريخ — Oldest Date": str(df.index.min().date()),
        "أحدث تاريخ — Latest Date": str(df.index.max().date()),
    }
    stats = df[["Open","High","Low","Close","Volume"]].describe().loc[["mean","std","min","max"]]
    return summary, stats