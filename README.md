# وكيل الأسهم الذكي 📈

مشروع ذكاء اصطناعي متكامل: تحليل بيانات أسهم حقيقية، تدريب 4 خوارزميات، اختيار الأفضل، ضبط Hyperparameters، ووكيل ذكاء اصطناعي يرد على أسئلتك بالعربية عبر Groq، مع أداة أخبار من RapidAPI.

## المتطلبات (Requirements)

- تحليل وتنظيف البيانات + Visualization
- تدريب 4 خوارزميات واختيار أفضل نتيجة
- Hyperparameter Tuning للمودل الأفضل
- وكيل ذكاء اصطناعي يرد بالعربية (Groq مجاني)
- أداة RapidAPI مضمّنة في الوكيل

## التثبيت والتشغيل

```bash
pip install -r requirements.txt
# أنشئ حساب مجاني وأخذ مفتاح Groq من: https://console.groq.com
# (اختياري) مفتاح RapidAPI من: https://rapidapi.com/apidojo/api/apidojo-yahoo-finance-v1
streamlit run app.py
```

## هيكل الملفات

- `data_prep.py` – تحميل وتحضير بيانات السهم (yfinance) + مؤشرات فنية
- `analysis_plot.py` – رسوم بيانية (سعر، توزيع، ارتباط) ومقاييس
- `train_model.py` – 4 خوارزميات + اختيار الأفضل + GridSearchCV + حفظ المودل
- `agent.py` – الوكيل الذكي: Groq + RapidAPI + المودل (أدوات)
- `app.py` – واجهة Streamlit بالعربي