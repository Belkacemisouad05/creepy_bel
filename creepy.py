import json
import random
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters
from deep_translator import GoogleTranslator

TOKEN = "8582418856:AAHc5Nrh2l8YlVF7_WYVD9A5iRQeEY3oVv4"

MEMORY_FILE = "memory.json"

# ================== الذاكرة ==================
def load_memory():
    try:
        with open(MEMORY_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, dict):
                return data
            return {}
    except:
        return {}

def save_memory(memory):
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(memory, f, ensure_ascii=False, indent=2)

memory = load_memory()

# ================== الجمل المميزة ==================
SPECIAL_RESPONSES = {
    "سينسي": "صندوق أسود يقبع في ظلامه ضوء أبيض 🖤✨",
    "نصرو": "صندوق أسود يقبع في ظلامه ضوء أبيض 🖤✨",
    "نصرالدين": "صندوق أسود يقبع في ظلامه ضوء أبيض 🖤✨",
    "بن هجيرة": "صندوق أسود يقبع في ظلامه ضوء أبيض 🖤✨",

    "طابت ليلتك": "تحياتي 🌙✨",
    "good night": "تحياتي 🌙✨",
    "سلام": "وعليكم السلام يا ملكة 👑",
    "hello": "أهلا وسهلا 👑",

    "كريبي": "هاااي أنا هما 🤍 اتفضلي اسألي كوداساي ✨",
    "creepy": "هاااي أنا هما 🤍",

    "dayskidy": "في ماذا تحتاجين المساعدة يا ملكة؟ 👑",
}

SOUAD_RESPONSES = [
    "الملكة سعاد في خدمة الشعب 👑",
    "تاج الملكة لا يُمس ♟️👑",
    "سعاد… اسم يسبق الهيبة ✨",
    "الملكة سعاد فوق الجميع 👑🖤"
]

ALLOWED_NAMES = ["سعاد", "souad", "شيماء", "chaimaa"]

# ================== لغات برمجة ==================
PROGRAMMING_KEYWORDS = {
    "python": "لغة Python تُستعمل في الذكاء الاصطناعي، الويب، الأتمتة.",
    "java": "Java لغة قوية للتطبيقات الكبيرة.",
    "c++": "C++ لغة سريعة وقوية.",
    "javascript": "JavaScript لبرمجة الويب.",
    "html": "HTML لبناء هيكل الصفحات.",
    "css": "CSS لتصميم الصفحات."
}

# ================== المعالج ==================
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    text_lower = text.lower()

    # ---- إغلاق ----
    if text_lower in ["اخرج", "اغلق", "exit", "close"]:
        await update.message.reply_text("تم الإغلاق بأمر الملكة 👑")
        await context.application.stop()
        return

    # ---- جمل مميزة (كلمة وحدها) ----
    if text_lower in SPECIAL_RESPONSES:
        await update.message.reply_text(SPECIAL_RESPONSES[text_lower])
        return

    # ---- سعاد ----
    if text_lower == "سعاد" or text_lower == "souad":
        await update.message.reply_text(random.choice(SOUAD_RESPONSES))
        return

    # ---- أسماء بنات أخرى ----
    if text_lower.isalpha():
        if text_lower not in [n.lower() for n in ALLOWED_NAMES]:
            await update.message.reply_text(
                "هذا الاسم سيختفي أمام ظل جلالة الملكة سعاد 👑🖤"
            )
            return

    # ---- حفظ في الذاكرة ----
    if text_lower.startswith("احفظها"):
        content = text.replace("احفظها", "").strip()
        if content:
            memory[content] = "معلومة محفوظة"
            save_memory(memory)
            await update.message.reply_text("تم الحفظ في ذاكرة كريبي 🧠✨")
        else:
            await update.message.reply_text("وش نحبس؟ عطيني المعلومة يا ملكة 👑")
        return

    # ---- استرجاع من الذاكرة ----
    if text in memory:
        await update.message.reply_text(memory[text])
        return

    # ---- برمجة ----
    for lang in PROGRAMMING_KEYWORDS:
        if lang in text_lower:
            await update.message.reply_text(PROGRAMMING_KEYWORDS[lang])
            return

    # ---- ترجمة ----
    if text_lower.startswith("ترجم"):
        try:
            sentence = text.replace("ترجم", "").strip()
            translated = GoogleTranslator(source="auto", target="ar").translate(sentence)
            await update.message.reply_text(translated)
        except:
            await update.message.reply_text("ما قدرتش نترجم 😔")
        return

    # ---- افتراضي ----
    await update.message.reply_text(
        "ما فهمتش مليح، قولي أكثر يا ملكة 👑✨"
    )
    # ================== تشغيل البوت ==================
def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("👑 Creepy is running...")
    app.run_polling()

if __name__ == "__main__":
    main()