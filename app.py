# -*- coding: utf-8 -*-
# ============================================================
# app.py -> واجهة Streamlit: تجمع التحليل + التدريب + الشات
# تشغيل:  streamlit run app.py
# ============================================================
import os, joblib
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import data_prep, analysis_plot, train_model, agent

# ---------- ثيم الرسومات البيانية (داكن فاخر) ----------
plt.rcParams.update({
    "figure.facecolor":   "#0D1117",
    "axes.facecolor":     "#10151E",
    "axes.edgecolor":     "#273141",
    "axes.labelcolor":    "#97A2B3",
    "axes.titlecolor":    "#F3EEE4",
    "axes.titlesize":     14,
    "text.color":         "#C9D2DE",
    "xtick.color":        "#7D8794",
    "ytick.color":        "#7D8794",
    "grid.color":         "#1D2531",
    "grid.alpha":         0.6,
    "axes.spines.top":    False,
    "axes.spines.right":  False,
    "font.family":        "Segoe UI",
})

# ---------- إعدادات عامة ----------
st.set_page_config(
    page_title="Skan AI — Smart Stock Intelligence",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================
# CSS: الثيم الفاخر (ذهبي + داكن) + خطوط عربية/إنجليزية
# ============================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cairo:wght@300;400;600;700;800;900&family=Playfair+Display:ital,wght@0,500;0,600;0,700;1,500;1,600;1,700&display=swap');

:root{
  --bg:#0A0D12; --panel:#121722; --panel2:#0E131B;
  --border:#222B3A; --gold:#D4AF37; --gold-l:#F0D47A; --gold-soft:#E9C46A;
  --text:#F3EEE4; --muted:#97A2B3;
}

html, body, .stApp, [class*="st-"], [data-testid="stMarkdownContainer"] p,
[data-testid="stMarkdownContainer"] li { font-family:'Cairo','Segoe UI',sans-serif; }

.stApp{
  background:
    radial-gradient(1100px 520px at 88% -8%, rgba(212,175,55,.12), transparent 60%),
    radial-gradient(900px 460px at -8% 108%, rgba(212,175,55,.07), transparent 55%),
    linear-gradient(180deg,#090C11 0%,#0C1017 100%);
  color:var(--text);
}
#MainMenu, footer { visibility:hidden; }
header[data-testid="stHeader"] { background:transparent; }
.main .block-container { padding-top:1.2rem; max-width:1120px; }

/* ---------- الترويسة (Hero) ---------- */
.hero{
  text-align:center;
  padding:42px 24px 30px;
  background:
    radial-gradient(600px 220px at 50% 0%, rgba(212,175,55,.16), transparent 70%),
    linear-gradient(180deg,#141A26,#0E131B);
  border:1px solid rgba(212,175,55,.28);
  border-radius:22px;
  margin-bottom:26px;
  position:relative;
  overflow:hidden;
  box-shadow:0 18px 50px rgba(0,0,0,.5), inset 0 1px 0 rgba(212,175,55,.15);
}
.hero::before{
  content:""; position:absolute; inset:0;
  background:repeating-linear-gradient(90deg, rgba(255,255,255,.015) 0 1px, transparent 1px 90px);
  pointer-events:none;
}
.hero-eyebrow{
  letter-spacing:.42em; font-size:.72rem; color:var(--gold-soft);
  text-transform:uppercase; font-weight:600; opacity:.9; margin-bottom:14px;
}
.hero-en{
  font-family:'Playfair Display',serif; font-style:italic;
  font-size:3.1rem; font-weight:700; color:var(--text); margin:0; line-height:1.1;
}
.glow{
  background:linear-gradient(120deg,#F5E6B8,#D4AF37,#FFF3C9,#D4AF37,#B8932A);
  background-size:220% auto;
  -webkit-background-clip:text; background-clip:text; color:transparent;
  -webkit-text-fill-color:transparent;
  animation:shine 6s linear infinite;
}
@keyframes shine{ to{ background-position:220% center; } }
.hero-ar{
  font-family:'Cairo',sans-serif; font-size:1.35rem; font-weight:800;
  color:var(--gold-soft); margin:10px 0 4px;
}
.hero-sub{ color:var(--muted); font-size:.98rem; margin:4px auto; max-width:760px; line-height:1.8; }
.hero-sub.ar{ color:#B9C2CF; }
.hero-tags{ margin-top:20px; display:flex; gap:10px; justify-content:center; flex-wrap:wrap; }
.hero-tags span{
  background:rgba(212,175,55,.12);
  border:1px solid rgba(212,175,55,.35);
  color:var(--gold-l);
  border-radius:40px; padding:6px 16px; font-size:.82rem; font-weight:600;
}

/* ---------- عناوين الأقسام ---------- */
.sec-lbl{
  letter-spacing:.24em; font-size:.7rem; font-weight:700; color:var(--gold);
  text-transform:uppercase; margin-bottom:6px; text-align:center;
}
.sec-title{ text-align:center; color:var(--text); font-size:1.25rem; font-weight:800; margin:0 0 18px; }
.en-thin{ font-family:'Playfair Display',serif; font-style:italic; color:var(--muted); font-weight:500; font-size:1.05rem; }

/* ---------- قسم "عن المشروع" ---------- */
.about{
  background:linear-gradient(180deg,#121722,#0E131B);
  border:1px solid var(--border); border-radius:20px;
  padding:26px 22px 22px; margin-bottom:24px;
}
.ab-grid{ display:grid; grid-template-columns:repeat(auto-fit,minmax(230px,1fr)); gap:14px; }
.ab-card{
  background:#0F141C; border:1px solid #222B3A; border-radius:14px;
  padding:16px 16px 12px; text-align:center;
  transition:transform .2s ease, border-color .2s ease, box-shadow .2s ease;
}
.ab-card:hover{
  transform:translateY(-3px);
  border-color:rgba(212,175,55,.55);
  box-shadow:0 10px 26px rgba(0,0,0,.45);
}
.ab-ico{ font-size:1.7rem; }
.ab-card b{ display:block; color:var(--text); font-size:.98rem; margin-top:6px; }
.ab-card em{ display:block; font-family:'Playfair Display',serif; font-style:italic;
  color:var(--gold); font-size:.78rem; letter-spacing:.06em; margin:2px 0 8px; }
.ab-card p{ color:var(--muted); font-size:.8rem; line-height:1.6; margin:0; }

/* ---------- خطوات العمل ---------- */
.steps{ margin-bottom:24px; }
.step-row{ display:grid; grid-template-columns:repeat(auto-fit,minmax(220px,1fr)); gap:14px; }
.step{
  position:relative; background:linear-gradient(180deg,#121722,#0E131B);
  border:1px solid var(--border); border-radius:16px; padding:18px 16px 14px;
  text-align:center;
}
.step .snum{
  width:38px; height:38px; margin:0 auto 10px; border-radius:50%;
  background:linear-gradient(135deg,#D4AF37,#B8932A); color:#0A0D12;
  font-weight:800; font-size:1.05rem; display:flex; align-items:center; justify-content:center;
  box-shadow:0 6px 16px rgba(212,175,55,.4);
}
.step b{ display:block; color:var(--text); font-size:.98rem; }
.step em{ display:block; font-family:'Playfair Display',serif; font-style:italic;
  color:var(--gold); font-size:.76rem; letter-spacing:.05em; margin:2px 0 8px; }
.step p{ color:var(--muted); font-size:.8rem; line-height:1.6; margin:0; }

/* ---------- بطاقات المراحل ---------- */
.card-head{
  display:flex; align-items:center; gap:10px;
  background:linear-gradient(180deg,#121722,#0E131B);
  border:1px solid rgba(212,175,55,.3); border-left:4px solid var(--gold);
  border-radius:14px; padding:13px 16px; margin:18px 0 14px;
  color:var(--text); font-weight:800; font-size:1.05rem;
}
.card-head .en{ font-family:'Playfair Display',serif; font-style:italic; color:var(--gold); font-weight:500; font-size:.9rem; }

/* ---------- أزرار Streamlit ---------- */
.stButton > button{
  background:linear-gradient(135deg,#D4AF37 0%,#E9C46A 45%,#B8932A 100%);
  color:#0A0D12 !important; font-weight:800; border:none;
  border-radius:12px; padding:.65rem 1.2rem; font-size:1rem;
  transition:all .22s ease; box-shadow:0 6px 18px rgba(212,175,55,.25);
}
.stButton > button:hover{
  transform:translateY(-1px);
  box-shadow:0 10px 26px rgba(212,175,55,.45);
}
.stButton > button:disabled{ background:#2A3140; color:#7D8794 !important; box-shadow:none; }

/* ---------- حقول الإدخال والقوائم ---------- */
.stSelectbox div[data-baseweb="select"] > div,
.stTextInput div[data-baseweb="input"] > div,
.stTextArea textarea{
  background:#0E131B; border:1px solid #222B3A; border-radius:12px; color:var(--text);
}
.stTextArea textarea:focus{ border-color:rgba(212,175,55,.6); }
[data-baseweb="select"] span, [data-baseweb="input"] input,
.stTextArea textarea, [data-testid="stSelectbox"] label p{ color:var(--text); }

/* ---------- التبويبات ---------- */
.stTabs [data-baseweb="tab-list"]{ gap:10px; background:transparent; }
.stTabs [data-baseweb="tab"]{
  background:#0E131B; border:1px solid #222B3A; border-radius:12px;
  padding:8px 18px; color:var(--muted); font-weight:700;
}
.stTabs [aria-selected="true"]{
  background:linear-gradient(135deg,#D4AF37,#E9C46A);
  color:#0A0D12; border:1px solid #D4AF37;
}
.stTabs [data-baseweb="tab-highlight"], .stTabs [data-baseweb="tab-border"]{ background:transparent; }

/* ---------- البطاقات الإحصائية ---------- */
[data-testid="stMetric"]{
  background:linear-gradient(165deg,#141A26,#0E131B);
  border:1px solid rgba(212,175,55,.28); border-radius:14px;
  padding:14px 16px; box-shadow:0 8px 22px rgba(0,0,0,.35);
}
[data-testid="stMetric"] label{ color:var(--muted); font-size:.82rem; }
[data-testid="stMetricValue"]{ color:var(--gold-l); font-size:1.4rem; font-weight:800; }
[data-testid="stMetricDelta"], [data-testid="stMetricDelta"] [data-testid="stMetricDelta"]{ color:#7BCFA6; }

/* ---------- رسائل الحالة ---------- */
.stAlert{ border-radius:12px; border:1px solid var(--border); }
.stSuccess{ background:rgba(151,207,166,.1); }
.stWarning{ background:rgba(212,175,55,.1); }

/* ---------- الرد من الوكيل ---------- */
.agent-answer{
  background:linear-gradient(180deg,#141A26,#0E131B);
  border:1px solid rgba(212,175,55,.35); border-right:4px solid var(--gold);
  border-radius:14px; padding:16px 18px; margin-top:10px;
  color:#D8DEE8; line-height:1.9; font-size:.95rem;
}
.agent-answer b{ color:var(--gold-soft); }

/* ---------- تذييل ---------- */
.footer{
  margin-top:34px; text-align:center; color:#5E6A7A; font-size:.78rem;
  border-top:1px solid #1B2230; padding-top:16px; letter-spacing:.06em;
}

/* ---------- الشريط الجانبي ---------- */
section[data-testid="stSidebar"]{
  background:linear-gradient(180deg,#0D1118,#0A0D12);
  border-right:1px solid #1B2230;
}
section[data-testid="stSidebar"] h1, section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3, section[data-testid="stSidebar"] label p,
section[data-testid="stSidebar"] .stCaption{ color:var(--text); }
</style>
""", unsafe_allow_html=True)

# ============================================================
# HERO — ترحيب / وصف أول
# ============================================================
st.markdown("""
<div class="hero">
  <div class="hero-eyebrow">S K A N &nbsp;·&nbsp; A I</div>
  <h1 class="hero-en">Welcome To <span class="glow">My AI</span></h1>
  <h2 class="hero-ar">مرحباً بك في ذكائي الاصطناعي</h2>
  <p class="hero-sub ar">وكيل الأسهم الذكي: يحلّل بيانات السوق الحية، يدرب 4 خوارزميات تعذّب وتختار الأفضل،
     ويجيب عن أسئلتك بالعربية أو الإنجليزية — كل ذلك في خطوات سهلة من هنا.</p>
  <p class="hero-sub en">The smart stock agent: analyzes live market data, trains 4 models with hyperparameter tuning,
     and answers your questions in Arabic or English — all in a few easy steps right here.</p>
  <div class="hero-tags">
    <span>📊 Live Market Data</span>
    <span>🧠 4 ML Models + Tuning</span>
    <span>🗣️ AI Chat Agent</span>
    <span>🌐 العربية &amp; English</span>
  </div>
</div>
""", unsafe_allow_html=True)

# ============================================================
# قسم الشرح الثاني — عن المشروع
# ============================================================
st.markdown("""
<div class="about">
  <div class="sec-lbl">About The Project</div>
  <h3 class="sec-title">ماذا يفعل هذا الذكاء الاصطناعي؟ <span class="en-thin">— What does this AI do?</span></h3>
  <div class="ab-grid">
    <div class="ab-card">
      <div class="ab-ico">📈</div>
      <b>تحليل بيانات حقيقية</b> <em>Live Market Data</em>
      <p>تحميل وتنظيف بيانات 11 سهم وعملة من السوق مباشرة مع مؤشرات فنية جاهزة للتحليل.</p>
    </div>
    <div class="ab-card">
      <div class="ab-ico">🧠</div>
      <b>4 خوارزميات ذكاء اصطناعي</b> <em>4 ML Models</em>
      <p>Linear Regression, Random Forest, Gradient Boosting, وSVR — يتدرّبون ويتنافسون على أفضل دقة.</p>
    </div>
    <div class="ab-card">
      <div class="ab-ico">⚙️</div>
      <b>ضبط ذكي للـ Hyperparameters</b> <em>Auto Tuning</em>
      <p>GridSearchCV يضبط إعدادات الخوارزمية الفائزة تلقائيًا لتصل لأعلى دقة توقع.</p>
    </div>
    <div class="ab-card">
      <div class="ab-ico">🎯</div>
      <b>توقع سعر الغد</b> <em>Next-Day Forecast</em>
      <p>نموذج مدرب يتنبأ بسعر إغلاق اليوم التالي لكل سهم تختاره بنفسك.</p>
    </div>
    <div class="ab-card">
      <div class="ab-ico">🗣️</div>
      <b>وكيل محادثة ذكي</b> <em>AI Chat Agent</em>
      <p>اسأل عن الاتجاه والتوقعات فيجيبك وكيل مدعوم بـ Groq بلغة سؤالك.</p>
    </div>
    <div class="ab-card">
      <div class="ab-ico">🌐</div>
      <b>عربي وإنجليزي</b> <em>Bilingual</em>
      <p>الواجهة والأجوبة تدعم العربية والإنجليزية بالكامل — اختر ما يناسبك.</p>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

# ============================================================
# خطوات العمل
# ============================================================
st.markdown("""
<div class="steps">
  <div class="sec-lbl">How It Works</div>
  <h3 class="sec-title">ثلاث خطوات فقط <span class="en-thin">— Three Simple Steps</span></h3>
  <div class="step-row">
    <div class="step">
      <div class="snum">1</div>
      <b>حمّل وافعص البيانات</b> <em>Load &amp; Clean</em>
      <p>اختر السهم والفترة ثم اضغط زر التحميل لتظهر التحليلات والرسوم البيانية فورًا.</p>
    </div>
    <div class="step">
      <div class="snum">2</div>
      <b>درّب الخوارزميات</b> <em>Train &amp; Tune</em>
      <p>أربع خوارزميات تتنافس، والأفضل يُضبط تلقائيًا ويُحفظ جاهزًا للتنبؤ.</p>
    </div>
    <div class="step">
      <div class="snum">3</div>
      <b>اسأل الوكيل</b> <em>Ask The Agent</em>
      <p>اكتب سؤالك بالعربية أو الإنجليزية واحصل على جواب مدعوم بالمودل المدرب.</p>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

# ============================================================
# الشريط الجانبي — الإعدادات
# ============================================================
with st.sidebar:
    st.markdown("### ⚙️ الإعدادات ")
    st.caption("Settings")
    def label(ticker, name): return f"{name} ({ticker})"
    symbol_labels = {
        "AAPL": "أبل (AAPL)",
        "MSFT": "مايكروسوفت (MSFT)",
        "GOOGL": "قوقل (GOOGL)",
        "TSLA": "تسلا (TSLA)",
        "AMZN": "أمازون (AMZN)",
        "2222.SR": "أرامكو (2222.SR)",
        "7203.SR": "الراجحي (7203.SR)",
        "1020.SR": "سابك (1020.SR)",
        "1150.SR": "البنك الأهلي (1150.SR)",
        "BTC-USD": "بتكوين (BTC-USD)",
        "ETH-USD": "إيثريوم (ETH-USD)",
    }
    symbol = st.selectbox("📌 السهم — Stock", list(symbol_labels),
                          format_func=lambda s: symbol_labels[s], index=0)
    period = st.selectbox("🗓️ فترة البيانات — Period", ["1 سنة", "2 سنة", "5 سنة"], index=1)
    period_map = {"1 سنة": "1y", "2 سنة": "2y", "5 سنة": "5y"}
    groq_key = st.text_input("🔑 مفتاح Groq — API Key", type="password",
                             help="من console.groq.com — مجاني  /  From console.groq.com — free")
    st.markdown("---")
    st.caption("المراحل — Stages: ① تحميل ← ② تدريب ← ③ محادثة")

# ============================================================
# المرحلة ① — تحميل وتنظيف البيانات
# ============================================================
st.markdown("""<div class="card-head">① التحميل والتحليل &nbsp;<span class="en">Load &amp; Analyze</span></div>""",
            unsafe_allow_html=True)
if st.button("🚀 تحميل وتنظيف بيانات السهم — Load & Clean", use_container_width=True):
    with st.spinner("جارٍ تحميل البيانات من السوق..."):
        df = data_prep.load_and_clean(symbol, period_map[period])
        st.session_state["df"], st.session_state["sym"] = df, symbol
        st.session_state["prd"] = period
    st.success(f"تم تحميل {len(df)} صفًا لسهم {symbol} / Loaded {len(df)} rows for {symbol}")

# إعادة تحميل تلقائي عند تغيير الرمز أو الفترة
if "df" in st.session_state and (st.session_state["sym"] != symbol
                                 or st.session_state["prd"] != period):
    with st.spinner("جارٍ التحديث..."):
        st.session_state["df"] = data_prep.load_and_clean(symbol, period_map[period])
        st.session_state["sym"] = symbol
        st.session_state["prd"] = period

if "df" in st.session_state:
    df = st.session_state["df"]
    last_close = df["Close"].iloc[-1]
    prev_close = df["Close"].iloc[-2]
    change = (last_close - prev_close) / prev_close * 100
    vals = [
        ("أحدث سعر إغلاق", "Latest Close", f"{last_close:.2f}", None),
        ("التغير اليومي %", "Daily Change %", f"{change:+.2f}%", f"{change:+.2f}%"),
        ("متوسط السعر", "Avg Price", f"{df['Close'].mean():.2f}", None),
        ("عدد أيام التداول", "Trading Days", f"{len(df):,}", None),
    ]
    cols = st.columns(4)
    for col, (ar, en, val, delta) in zip(cols, vals):
        col.metric(f"{ar} / {en}", val, delta=delta)

    tab1, tab2, tab3 = st.tabs(["📊 الرسوم — Charts", "📋 البيانات — Data", "📈 الملخص — Summary"])
    with tab1:
        st.write("##### الرسوم التحليلية / Analysis Charts")
        for fig in analysis_plot.make_plots(df):
            st.pyplot(fig)
    with tab2:
        st.write("##### عينة من البيانات / Data Sample")
        st.dataframe(df.tail(10), use_container_width=True)
    with tab3:
        summ, stats = analysis_plot.analysis_summary(df)
        col1, col2 = st.columns(2)
        with col1:
            st.write("**ملخص التحليل / Summary**")
            st.json(summ)
        with col2:
            st.write("**المقاييس الإحصائية / Statistics**")
            st.dataframe(stats, use_container_width=True)

# ============================================================
# المرحلة ② — تدريب الخوارزميات
# ============================================================
st.markdown("""<div class="card-head">② التدريب والضبط &nbsp;<span class="en">Train &amp; Tune</span></div>""",
            unsafe_allow_html=True)
if st.button("⚡ ابدأ التدريب — Train 4 Models + Hyperparameter Tuning", use_container_width=True):
    if "df" not in st.session_state:
        st.warning("حمّل البيانات أولًا (المرحلة ①) — Load data first (Step ①)")
    else:
        with st.spinner("جارٍ تدريب الخوارزميات وضبط الهايبر باراميترز..."):
            results, tuned = train_model.train(st.session_state["df"],
                                               st.session_state["sym"])
        st.session_state["model"] = tuned

        st.write("### مقارنة الخوارزميات الأربع / Model Comparison")
        rows = []
        for k, v in results.items():
            if k == "best_after_tuning":
                continue
            if isinstance(v, dict):
                rows.append({"Algorithm": k, "R² Accuracy": v["R2"],
                             "RMSE Error": v["RMSE"]})
        st.dataframe(pd.DataFrame(rows), use_container_width=True)

        best = results["best_after_tuning"]
        st.markdown(f"""<div class="agent-answer">
        <b>أفضل خوارزمية — Best Model: {best['model']}</b><br>
        الدقة بعد التحسين (R²) — Accuracy after tuning: {best['R2']}
        &nbsp;|&nbsp; RMSE: {best['RMSE']}<br>
        أفضل إعدادات — Best Hyperparameters: {best['best_params']}
        </div>""", unsafe_allow_html=True)
        st.success("تم حفظ المودل في model/model.pkl / Model saved to model/model.pkl")

# ============================================================
# المرحلة ③ — محادثة عربية
# ============================================================
st.markdown("""<div class="card-head">③ محادثة الوكيل &nbsp;<span class="en">Ask The Agent</span></div>""",
            unsafe_allow_html=True)
q = st.text_area("اسأل الوكيل — Ask the agent (answers in your language)",
                 placeholder="مثال: هل السهم في اتجاه صاعد؟ ما السعر المتوقع غدًا؟\nExample: Is the stock trending up? What's the expected price tomorrow?",
                 height=100)
if q.strip() and "model" not in st.session_state:
    st.warning("درّب المودل أولًا (المرحلة ②) ثم اكتب سؤالك — Train the model first (Step ②)")
if q.strip() and "model" in st.session_state:
    last = st.session_state["df"].iloc[-1]
    with st.spinner("الوكيل يفكّر... / Agent is thinking..."):
        ans = agent.agent_answer(q, groq_key, st.session_state["model"],
                                 last, symbol)
    st.markdown(f"<div class='agent-answer'><b>الوكيل — Agent:</b><br>{ans}</div>",
                unsafe_allow_html=True)

st.markdown("""<div class="footer">SKAN AI · BUILT WITH ❤ · تحليل • تدريب • محادثة</div>""",
            unsafe_allow_html=True)