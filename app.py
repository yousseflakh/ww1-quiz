import streamlit as st
import time
import random

# إعدادات الصفحة
st.set_page_config(page_title="Quiz Grand Guerre", page_icon="🎖️")

# ستايل CSS مخصص باش تبان اللعبة زوينة
st.markdown("""
    <style>
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        height: 3em;
        background-color: #34495e;
        color: white;
        font-size: 18px;
    }
    .stButton>button:hover {
        background-color: #f39c12;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

# قاعدة البيانات (الأسئلة)
if 'questions' not in st.session_state:
    st.session_state.questions = [
        {"q": "En quelle année la guerre a-t-elle commencé ?", "options": ["1912", "1914", "1916", "1918"], "a": "1914"},
        {"q": "Quel événement a déclenché la guerre ?", "options": ["L'invasion de la Pologne", "L'assassinat de l'archiduc François-Ferdinand", "Le naufrage du Titanic", "La bataille de Verdun"], "a": "L'assassinat de l'archiduc François-Ferdinand"},
        {"q": "Quel pays ne faisait PAS partie de la Triple-Entente ?", "options": ["La France", "Le Royaume-Uni", "L'Allemagne", "La Russie"], "a": "L'Allemagne"},
        {"q": "Qui était le chef de l'armée française ?", "options": ["Foch", "Napoléon", "De Gaulle", "Joffre"], "a": "Joffre"}
    ]


# متغيرات الحالة (Session State)
if 'current_idx' not in st.session_state: st.session_state.current_idx = 0
if 'score' not in st.session_state: st.session_state.score = 0
if 'answered' not in st.session_state: st.session_state.answered = False

# العنوان
st.title("🎖️ Quiz: La Première Guerre Mondiale")
st.write("---")

# منطقة إضافة سؤال (Sidebar)
with st.sidebar:
    st.header("⚙️ Administration")
    with st.expander("Ajouter une question"):
        new_q = st.text_input("Question")
        new_a = st.text_input("Réponse correcte")
        new_o = st.text_area("3 autres options (séparées par virgule)").split(',')
        if st.button("Enregistrer"):
            opts = [new_a] + [o.strip() for o in new_o]
            st.session_state.questions.append({"q": new_q, "options": opts, "a": new_a})
            st.success("Ajouté !")

# عرض السؤال الحالي
if st.session_state.current_idx < len(st.session_state.questions):
    item = st.session_state.questions[st.session_state.current_idx]
    st.subheader(f"Question {st.session_state.current_idx + 1}: {item['q']}")
    
    # خلط الاختيارات مرة واحدة
    if 'current_opts' not in st.session_state or st.session_state.answered == False:
        opts = item['options']
        random.shuffle(opts)
        st.session_state.current_opts = opts

    # عرض الأزرار
    for opt in st.session_state.current_opts:
        if st.button(opt, key=opt):
            st.session_state.answered = True
            with st.spinner('Vérification...'):
                time.sleep(1.5) # وقت التشويق اللي طلبتي
                if opt == item['a']:
                    st.success(f"Correct ! ✅")
                    st.session_state.score += 1
                else:
                    st.error(f"Faux ! ❌ La réponse était : {item['a']}")
            
            # زر المتابعة
            if st.button("Suivant ➔"):
                st.session_state.current_idx += 1
                st.session_state.answered = False
                st.rerun()

else:
    st.balloons()
    st.success(f"Fin du Quiz ! Votre score : {st.session_state.score}/{len(st.session_state.questions)}")
    if st.button("Recommencer"):
        st.session_state.current_idx = 0
        st.session_state.score = 0
        st.rerun()