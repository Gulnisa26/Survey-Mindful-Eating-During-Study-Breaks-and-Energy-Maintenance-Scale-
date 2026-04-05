import streamlit as st
import json
from datetime import datetime

# --- Version ---
version_float = 1.0

# --- Validation Functions ---
def validate_name(name: str) -> bool:
    return name.isalpha() and len(name) > 0

def validate_dob(dob: str) -> bool:
    try:
        datetime.strptime(dob, "%Y-%m-%d")
        return True
    except ValueError:
        return False

# --- Score Interpretation ---
def interpret_score(score: int) -> str:
    if 0 <= score <= 15:
        return "Excellent mindful eating"
    elif 16 <= score <= 30:
        return "Good energy maintenance — continue"
    elif 31 <= score <= 45:
        return "Moderate practice — slow down eating"
    elif 46 <= score <= 60:
        return "Low maintenance — focus on nutrition"
    elif 61 <= score <= 75:
        return "Very low mindful eating — immediate action needed"
    else:
        return "Score out of expected range"

# --- Save JSON Function ---
def save_json(filename, data):
    with open(filename, "w") as f:
        json.dump(data, f, indent=2)

# --- 15 Survey Questions ---
questions = [
    {"q": "How mindful are you when eating during study breaks?",
     "opts": [("Very mindful",0), ("Good",1), ("Moderate",2), ("Poor",3), ("Not mindful",4)]},
    {"q": "How well does your food maintain your energy levels?",
     "opts": [("Very good",0), ("Good",1), ("Moderate",2), ("Poor",3), ("Very poor",4)]},
    {"q": "How often do you choose healthy snacks during study?",
     "opts": [("Always",0), ("Often",1), ("Sometimes",2), ("Rarely",3), ("Never",4)]},
    {"q": "How aware are you of your hunger while studying?",
     "opts": [("Very aware",0), ("Somewhat aware",1), ("Neutral",2), ("Sometimes unaware",3), ("Not aware",4)]},
    {"q": "How often do you eat too quickly during breaks?",
     "opts": [("Never",0), ("Rarely",1), ("Sometimes",2), ("Often",3), ("Always",4)]},
    {"q": "How well do you stay hydrated while studying?",
     "opts": [("Very well",0), ("Good",1), ("Moderate",2), ("Poor",3), ("Very poor",4)]},
    {"q": "How often do you rely on sugary snacks for energy?",
     "opts": [("Never",0), ("Rarely",1), ("Sometimes",2), ("Often",3), ("Always",4)]},
    {"q": "How focused do you feel after eating?",
     "opts": [("Very focused",0), ("Focused",1), ("Neutral",2), ("Somewhat distracted",3), ("Very distracted",4)]},
    {"q": "How often do you skip meals during study sessions?",
     "opts": [("Never",0), ("Rarely",1), ("Sometimes",2), ("Often",3), ("Always",4)]},
    {"q": "How satisfied do you feel after eating during breaks?",
     "opts": [("Very satisfied",0), ("Satisfied",1), ("Neutral",2), ("Unsatisfied",3), ("Very unsatisfied",4)]},
    {"q": "How often do you plan your meals ahead while studying?",
     "opts": [("Always",0), ("Often",1), ("Sometimes",2), ("Rarely",3), ("Never",4)]},
    {"q": "How often do you eat mindlessly while doing other tasks?",
     "opts": [("Never",0), ("Rarely",1), ("Sometimes",2), ("Often",3), ("Always",4)]},
    {"q": "How well do you manage snack portions during study?",
     "opts": [("Very well",0), ("Well",1), ("Moderate",2), ("Poor",3), ("Very poor",4)]},
    {"q": "How often do you eat snacks for emotional reasons while studying?",
     "opts": [("Never",0), ("Rarely",1), ("Sometimes",2), ("Often",3), ("Always",4)]},
    {"q": "How often do you feel sluggish after eating during study breaks?",
     "opts": [("Never",0), ("Rarely",1), ("Sometimes",2), ("Often",3), ("Always",4)]}
]

# --- Streamlit Page ---
st.set_page_config(page_title="Mindful Eating Survey")
st.title("📝 Mindful Eating During Study Breaks Survey")
st.info("Please fill out your details and answer all questions honestly.")

# --- User Info ---
name = st.text_input("Given Name")
surname = st.text_input("Surname")
dob = st.text_input("Date of Birth (YYYY-MM-DD)")
sid = st.text_input("Student ID (digits only)")

if st.button("Start Survey"):
    errors = []
    if not validate_name(name):
        errors.append("Invalid given name.")
    if not validate_name(surname):
        errors.append("Invalid surname.")
    if not validate_dob(dob):
        errors.append("Invalid date of birth format. Use YYYY-MM-DD.")
    if not sid.isdigit():
        errors.append("Student ID must be digits only.")

    if errors:
        for e in errors:
            st.error(e)
    else:
        st.success("All inputs are valid. Proceed to answer the questions below.")

        total_score = 0
        answers = []

        for idx, q in enumerate(questions):
            choice = st.selectbox(f"Q{idx+1}. {q['q']}", [opt[0] for opt in q["opts"]], key=f"q{idx}")
            score = next(score for label, score in q["opts"] if label == choice)
            total_score += score
            answers.append({"question": q["q"], "selected_option": choice, "score": score})

        status = interpret_score(total_score)

        st.markdown(f"## ✅ Your Result: {status}")
        st.markdown(f"**Total Score:** {total_score}")

        # Save results to JSON
        record = {
            "name": name,
            "surname": surname,
            "dob": dob,
            "student_id": sid,
            "total_score": total_score,
            "result": status,
            "answers": answers,
            "version": version_float
        }

        json_filename = f"{sid}_result.json"
        save_json(json_filename, record)

        st.success(f"Your results are saved as {json_filename}")
        st.download_button("Download your result JSON", json.dumps(record, indent=2), file_name=json_filename)