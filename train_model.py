# -*- coding: utf-8 -*-
# ============================================================
# train_model.py -> تدريب 4 خوارزميات واختيار الأفضل + Hyperparameter Tuning
# الخوارزميات: LinearRegression, RandomForest, GradientBoosting, SVR
# الهدف: توقع سعر الإغلاق لليوم التالي من مؤشرات الأيام السابقة
# ============================================================
import pandas as pd, numpy as np, joblib, os
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.svm import SVR
from sklearn.metrics import r2_score, root_mean_squared_error


#نجهز مكان نحفظ فيه المودل المدرب. لازم يكون تلقائي عشان يشتغل على أي جهاز.
MODEL_DIR = os.path.join(os.path.dirname(__file__), "model")
os.makedirs(MODEL_DIR, exist_ok=True)

def make_xy(df):
    """ننبئ سعر إغلاق اليوم التالي بمؤشرات اليوم نفسه"""
    features = ["Open","High","Low","Close","Volume","MA5","MA20","Return","Range","Volume_MA"]
    X = df[features].iloc[:-1].values
    y = df["Close"].shift(-1).iloc[:-1].values   # سعر الإغلاق التالي
    return X, y

def train(df, symbol="AAPL"):
    X, y = make_xy(df)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2,
                                                        shuffle=False, random_state=42)

    models = {
        "Linear Regression": LinearRegression(),
        "Random Forest":     RandomForestRegressor(n_estimators=150, random_state=42, n_jobs=-1),
        "Gradient Boosting": GradientBoostingRegressor(n_estimators=150, random_state=42),
        "SVR":               SVR(kernel="rbf"),
    }

    results = {}            #التدريب والاختيار
    best_name, best_model, best_m = None, None, -1e9
    for name, model in models.items():
        model.fit(X_train, y_train)
        pred = model.predict(X_test)
        r2 = r2_score(y_test, pred)
        rmse = root_mean_squared_error(y_test, pred)
        results[name] = {"R2": round(r2, 4), "RMSE": round(rmse, 4)}
        if r2 > best_m:
            best_m, best_name, best_model = r2, name, model

    # Hyperparameter Tuning على أفضل مودل (GridSearchCV)
    tuned = _tune(best_name, best_model, X_train, y_train)
    tuned.fit(X_train, y_train)
    pred_best = tuned.predict(X_test)
    results["best_after_tuning"] = {
        "model": best_name,
        "R2": round(r2_score(y_test, pred_best), 4),
        "RMSE": round(root_mean_squared_error(y_test, pred_best), 4),
        "best_params": tuned.best_params_ if hasattr(tuned, "best_params_") else "n/a",
    }

    joblib.dump(tuned, os.path.join(MODEL_DIR, "model.pkl"))
    joblib.dump({"features": list(df.columns), "symbol": symbol},
                os.path.join(MODEL_DIR, "meta.pkl"))
    return results, tuned

def _tune(name, model, X_train, y_train):
    """شبكة بحث بسيطة تختلف حسب نوع المودل لتسريع التنفيذ"""
    if name == "Random Forest":
        grid = {"n_estimators": [100, 200], "max_depth": [10, 20]}
    elif name == "Gradient Boosting":
        grid = {"n_estimators": [100, 200], "learning_rate": [0.05, 0.1]}
    elif name == "SVR":
        grid = {"C": [1, 10], "epsilon": [0.01, 0.1]}
    else:  # Linear Regression → لا تفرّط
        grid = {"fit_intercept": [True, False]}
    return GridSearchCV(model, grid, cv=3, scoring="r2", n_jobs=-1)
