# 📈 SKAN AI – Smart Stock Agent

**An AI-powered stock analysis and prediction platform with an intelligent conversational agent.**

SKAN AI is an integrated machine learning project that analyzes real stock market data, trains and evaluates four machine learning algorithms, selects the best-performing model, and applies hyperparameter tuning to improve its performance.

The project also includes an AI-powered assistant that answers questions in Arabic using Groq and integrates financial news through RapidAPI.

## ✨ Key Features

- **Live Market Data:** Fetches real stock market data using Yahoo Finance (`yfinance`).
- **Data Analysis:** Cleans, prepares, and analyzes stock data.
- **Data Visualization:** Generates charts for stock prices, distributions, and correlations.
- **Machine Learning:** Trains and compares four machine learning algorithms.
- **Model Selection:** Automatically selects the best-performing model.
- **Hyperparameter Tuning:** Uses `GridSearchCV` to optimize the selected model.
- **AI Chat Agent:** Answers stock-related questions in Arabic using Groq.
- **Financial News:** Integrates a news tool through RapidAPI.
- **Interactive Dashboard:** Provides an Arabic interface built with Streamlit.

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| Streamlit | Interactive web interface |
| Pandas & NumPy | Data processing |
| Scikit-learn | Machine learning and tuning |
| Matplotlib / Seaborn | Data visualization |
| yfinance | Stock market data |
| Groq | AI conversational agent |
| RapidAPI | Financial news integration |

## 📂 Project Structure

```text
SKAN-AI/
│
├── agent.py
├── analysis_plot.py
├── app.py
├── data_prep.py
├── train_model.py
├── requirements.txt
├── run.bat
├── README.md
│
└── model/
    ├── model.pkl
    └── meta.pkl
```

## ⚙️ Installation & Setup

### 1. Clone the repository

```bash
git clone https://github.com/Ala-22/SKAN-AI.git
cd SKAN-AI
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure API Keys

Create a `.env` file in the project root directory and add your API credentials:

```env
GROQ_API_KEY=your_groq_api_key
RAPIDAPI_KEY=your_rapidapi_key
```

- Get a Groq API key: https://console.groq.com
- Get a RapidAPI key: https://rapidapi.com/apidojo/api/apidojo-yahoo-finance-v1

*The RapidAPI key is optional if you do not intend to use the news integration.*

### 4. Run the application

```bash
streamlit run app.py
```

Open the local URL displayed in your terminal to access the application.

## 📊 Machine Learning Workflow

1. Fetch historical stock market data.
2. Clean and prepare the dataset.
3. Analyze and visualize the data.
4. Train four machine learning algorithms.
5. Compare model performance.
6. Select the best-performing model.
7. Apply hyperparameter tuning using GridSearchCV.
8. Save the trained model for use in the application.

## 🤖 AI Agent

The intelligent agent combines:
- Groq-powered conversational responses.
- Access to the trained machine learning model.
- Financial news integration through RapidAPI.
- Arabic-language interaction.

## 🔐 Security Notes

- Never upload API keys, passwords, or private credentials.
- Keep your `.env` file out of GitHub.
- Use your own API keys when running the project.

## 👩‍💻 Developer

**Ala-22**

GitHub: https://github.com/Ala-22

---

*SKAN AI – Smart insights from stock market data.*


# وكيل الأسهم الذكي📈

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
