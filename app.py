import streamlit as st
import time
import random

# إعداد الصفحة
st.set_page_config(page_title="Quiz WW1", page_icon="🎖️")

# ستايل CSS باش نلونوا الأزرار ونخليوها تشبه للتطبيق اللي شفتي
st.markdown("""
    <style>
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        height: 3.5em;
        font-size: 18px;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# --- إدارة الحالة (Session State) ---
# هاد الجزء كيعوض __init__ باش البرنامج يعقل على المعلومات
if 'questions' not in st.session_state:
    st.session_state.questions = [
        {"question": "En quelle année la Première Guerre mondiale a-t-elle commencé ?", "options": ["1912", "1914", "1916", "1918"], "answer": "1914"},
        {"question": "Quel événement a déclenché la guerre ?", "options": ["L'invasion de la Pologne", "L'assassinat de l'archiduc François-Ferdinand", "Le naufrage du Titanic", "La bataille de Verdun"], "answer": "L'assassinat de l'archiduc François-Ferdinand"},
        {"question": "Quel pays ne faisait PAS partie de la Triple-Entente ?", "options": ["La France", "Le Royaume-Uni", "L'Allemagne", "La Russie"], "answer": "L'Allemagne"},
        {"question": "Comment appelait-on les soldats français ?", "options": ["Les Gars", "Les Poilus", "Les Bleus", "Les Braves"], "answer": "Les Poilus"},
        {"question": "Quand l'armistice a-t-il été signé ?", "options": ["11 novembre 1918", "14 juillet 1919", "8 mai 1945", "1er septembre 1914"], "answer": "11 novembre 1918"}
    ]

if 'current_question' not in st.session_state: st.session_state.current_question = 0
if 'score' not in st.session_state: st.session_state.score = 0
if 'ans_status' not in st.session_state: st.session_state.ans_status = None # None, 'waiting', or 'done'
if 'selected_option' not in st.session_state: st.session_state.selected_option = None

# --- بوطون إضافة سؤال (Sidebar) ---
with st.sidebar:
    st.header("➕ Ajouter une Question")
    with st.form("add_q_form", clear_on_submit=True):
        q_text = st.text_input("La question :")
        ans_text = st.text_input("Réponse correcte :")
        opt2 = st.text_input("Option fausse 1 :")
        opt3 = st.text_input("Option fausse 2 :")
        opt4 = st.text_input("Option fausse 3 :")
        submit = st.form_submit_button("Enregistrer")
        
        if submit and q_text and ans_text:
            new_q = {
                "question": q_text,
                "options": [ans_text, opt2, opt3, opt4],
                "answer": ans_text
            }
            st.session_state.questions.append(new_q)
            st.success("Question ajoutée !")

# --- عرض اللعبة ---
st.title("🎖️ Quiz: La Première Guerre Mondiale")

if st.session_state.current_question < len(st.session_state.questions):
    q_data = st.session_state.questions[st.session_state.current_question]
    
    st.write(f"### Question {st.session_state.current_question + 1}:")
    st.info(q_data['question'])

    # خلط الاختيارات وتثبيتها باش ما يتبدلوش ملي نكليكي
    if f"opts_{st.session_state.current_question}" not in st.session_state:
        shuffled = list(q_data['options'])
        random.shuffle(shuffled)
        st.session_state[f"opts_{st.session_state.current_question}"] = shuffled
    
    options = st.session_state[f"opts_{st.session_state.current_question}"]

    # عرض أزرار الأجوبة
    for opt in options:
        # تحديد اللون بناءً على الحالة (التشويق)
        if st.session_state.ans_status == 'waiting' and st.session_state.selected_option == opt:
            button_type = "secondary" # برتقالي/رمادي للتشويق
            st.button(f"⏳ {opt}", disabled=True)
        elif st.session_state.ans_status == 'done':
            if opt == q_data['answer']:
                st.button(f"✅ {opt}", key=f"correct_{opt}", type="primary") # أخضر
            elif opt == st.session_state.selected_option:
                st.button(f"❌ {opt}", key=f"wrong_{opt}") # أحمر (تلقائي)
            else:
                st.button(opt, disabled=True, key=f"dis_{opt}")
        else:
            # الحالة العادية قبل الكليك
            if st.button(opt, key=f"opt_{opt}"):
                st.session_state.selected_option = opt
                st.session_state.ans_status = 'waiting'
                st.rerun()

    # محاكاة التشويق (Suspense)
    if st.session_state.ans_status == 'waiting':
        time.sleep(1.5) # المدة اللي طلبتي
        if st.session_state.selected_option == q_data['answer']:
            st.session_state.score += 1
        st.session_state.ans_status = 'done'
        st.rerun()

    # زر Suivant
    if st.session_state.ans_status == 'done':
        st.write("---")
        if st.button("Suivant ➔", type="primary"):
            st.session_state.current_question += 1
            st.session_state.ans_status = None
            st.session_state.selected_option = None
            st.rerun()

else:
    # النهاية
    st.balloons()
    st.success(f"### Fin du Quiz! \n\n **Votre score final est : {st.session_state.score}/{len(st.session_state.questions)}**")
    if st.button("Recommencer"):
        st.session_state.current_question = 0
        st.session_state.score = 0
        st.rerun()

# الرصيد (Score) لتحت
st.sidebar.write(f"## 🏆 Score: {st.session_state.score}")