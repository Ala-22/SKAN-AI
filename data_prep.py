# -*- coding: utf-8 -*-
# ============================================================
# data_prep.py  ->  تحميل + تنظيف بيانات الأسهم
# الفكرة: نحمّل بيانات سهم حقيقي من yfinance (تتحدث يوميًا)
# ثم ننظّفها (حذف المفقود، إضافة مؤشرات فنية) ونرجع DataFrame
# ============================================================
import pandas as pd
import yfinance as yf

def load_and_clean(symbol="AAPL", period="2y"):
    # 1) تحميل البيانات من yfinance (فتح عالي/منخفض/إغلاق/حجم/إغلاق معدل)
    df = yf.download(symbol, period=period, auto_adjust=False,
                     interval="1d", progress=False)
    # نتأكد من مطابقة الأعمدة حسب الاسم وليس الترتيب (الترتيب يختلف أحيانًا)
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)
    df = df[[c for c in ["Open","High","Low","Close","Adj Close","Volume"] if c in df.columns]]
    df.index.name = "Date"

    # 2) التنظيف: حذف الصفوف المفقودة وترتيب التواريخ
    df = df.dropna().sort_index()

    # 3) هندسة الخصائص (Feature Engineering): مؤشرات فنية شهيرة
    df["MA5"]  = df["Close"].rolling(5).mean()    # متوسط 5 أيام
    df["MA20"] = df["Close"].rolling(20).mean()   # متوسط 20 يوم
    df["Return"] = df["Close"].pct_change()        # نسبة التغير اليومي
    df["Range"]  = df["High"] - df["Low"]          # مدى اليوم (تقلب)
    df["Volume_MA"] = df["Volume"].rolling(20).mean()

    # إزالة الصفوف الفارغة الناتجة عن المتوسطات المتحركة
    df = df.dropna()
    return df    
