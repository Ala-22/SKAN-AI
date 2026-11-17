# -*- coding: utf-8 -*-
# ============================================================
# agent.py -> وكيل ذكاء اصطناعي يرد بالعربي
# الأداة: المودل المدرب (توقع السعر)
# يتحدث مع Groq (LLM مجاني)
# ============================================================
import numpy as np

def forecast_tool(model, last_row):
    """توقع سعر اليوم التالي من المودل المدرب"""
    feats = ["Open","High","Low","Close","Volume","MA5","MA20","Return","Range","Volume_MA"]
    x = np.array([last_row[f] for f in feats]).reshape(1, -1)
    price = float(model.predict(x)[0])
    return f"السعر المتوقع لإغلاق الغد: {price:.2f}"

def agent_answer(question, groq_key, model, last_row, symbol):
    """يوظّف Groq ليُجيب بالعربي"""
    if not groq_key:
        return "ضع مفتاح Groq أولًا (راجع README)."

    # تنظيف المفتاح
    groq_key = groq_key.strip()
    if len(groq_key) < 10:
        return f"المفتاح قصير جدًا ({len(groq_key)} حرف). تأكد من نسخ المفتاح الكامل من console.groq.com"

    from groq import Groq
    client = Groq(api_key=groq_key)

    system = f"""
أنت وكيل ذكاء اصطناعي متخصص بالأسهم.
صُمِّمتَ وبُنيت بواسطة المهندسة آلاء الرجوي (Alaa Al-Rajwi).
إذا سُئلتَ عن من صنعك أو من أنشأك أو من صممك، قل بفخر إنك من صنع المهندسة آلاء الرجوي.
السهم المدروس: {symbol}.
لديك أداة واحدة: التوقع. إذا المستخدم سأل عن السعر المتوقع، أعطه الرقم التالي:
{forecast_tool(model, last_row)}
الرد دائمًا بنفس لغة سؤال المستخدم: إن سأل بالعربية رد بالعربية، وإن سأل بالإنجليزية رد بالإنجليزية.
الأجوبة قصيرة ومفهومة.
"""
    user = f"سؤال المستخدم: {question}"

    models = ["llama-3.3-70b-versatile", "llama-3.1-8b-instant",
              "openai/gpt-oss-120b", "openai/gpt-oss-20b"]
    last_err = None
    for m in models:
        try:
            resp = client.chat.completions.create(
                model=m,
                messages=[{"role": "system", "content": system},
                          {"role": "user", "content": user}],
                temperature=0.7, max_tokens=400)
            return resp.choices[0].message.content
        except Exception as e:
            last_err = e
    return f"جميع المودلات غير متاحة على حسابك. راجع مودلاتك في console.groq.com. آخر خطأ: {last_err}"