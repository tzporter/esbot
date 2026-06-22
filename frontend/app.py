import streamlit as st
import requests

# --- CONFIGURATION ---
BASE_URL = "http://127.0.0.1:8000/api/v1"

st.set_page_config(page_title="ESBot Learning Assistant", page_icon="🎓", layout="wide")

# --- HELPER API FUNCTIONS ---
def fetch_sessions():
    try:
        response = requests.get(f"{BASE_URL}/sessions")
        return response.json() if response.status_code == 200 else []
    except requests.exceptions.ConnectionError:
        st.error("Could not connect to the backend server. Is FastAPI running?")
        return []

def create_new_session(title):
    response = requests.post(f"{BASE_URL}/sessions", json={"user_id": "anonymous", "title": title})
    return response.json() if response.status_code == 200 else None

def delete_session(session_id):
    requests.delete(f"{BASE_URL}/sessions/{session_id}")

def fetch_messages(session_id):
    response = requests.get(f"{BASE_URL}/sessions/{session_id}/messages")
    return response.json() if response.status_code == 200 else []

def send_chat_message(session_id, content):
    response = requests.post(f"{BASE_URL}/sessions/{session_id}/messages", json={"content": content})
    return response.json() if response.status_code == 200 else None

def generate_quiz(session_id, topic):
    response = requests.post(f"{BASE_URL}/sessions/{session_id}/quiz", json={"topic": topic})
    return response.json() if response.status_code == 200 else None

def submit_quiz_answer(quiz_item_id, user_answer):
    response = requests.post(f"{BASE_URL}/quiz-items/{quiz_item_id}/submit", json={"user_answer": user_answer})
    return response.json() if response.status_code == 200 else None


# --- SIDEBAR: SESSION MANAGEMENT ---
st.sidebar.title("📁 Learning Sessions")

# Form to create a new workspace session
with st.sidebar.form("new_session_form", clear_on_submit=True):
    new_title = st.text_input("New Session Title", placeholder="e.g., Python Basics", key="new_session_title_input")
    submit_btn = st.form_submit_button("Create Session") # maps to new-session-btn
    if submit_btn and new_title.strip():
        new_sess = create_new_session(new_title)
        if new_sess:
            st.success(f"Created: {new_title}")
            st.rerun()

# List active sessions
sessions = fetch_sessions()
if sessions:
    session_titles = {s["id"]: s.get("title") or f"Session {s['id']}" for s in sessions}
    
    selected_id = st.sidebar.radio(
        "Select Active Workspace:", 
        options=list(session_titles.keys()), 
        format_func=lambda x: session_titles[x],
        key="session_radio_list"
    )
    
    if st.sidebar.button("🗑️ Delete Selected Session", use_container_width=True, key="delete_session_btn"):
        delete_session(selected_id)
        st.toast("Session deleted.")
        st.rerun()
else:
    st.sidebar.info("Create a session to begin.")
    selected_id = None

# --- MAIN APP ROUTING ---
if not selected_id:
    st.title("🎓 AI Learning Workspace")
    st.info("Welcome! Please select an existing learning session from the sidebar or create a new one to get started.")
else:
    st.title(f"Workspace: {session_titles[selected_id]}")
    
    tab_chat, tab_quiz = st.tabs(["💬 Explanations & Chat", "📝 AI Knowledge Quiz"])

    # ----------------------------------------------------
    # TAB 1: EXPLANATION CHAT
    # ----------------------------------------------------
    with tab_chat:
        st.subheader("Ask questions or dive into topics")
        
        messages = fetch_messages(selected_id)
        for msg in messages:
            with st.chat_message(msg["role"]):
                st.write(msg["content"])
                
        if user_prompt := st.chat_input("Ask a technical question...", key="chat_message_input"):
            with st.chat_message("user"):
                st.write(user_prompt)
                
            with st.chat_message("assistant"):
                with st.spinner("Analyzing context..."):
                    backend_response = send_chat_message(selected_id, user_prompt)
                    if backend_response:
                        st.write(backend_response["response"])
                        st.rerun()

    # ----------------------------------------------------
    # TAB 2: KNOWLEDGE QUIZ
    # ----------------------------------------------------
    with tab_quiz:
        st.subheader("Test Your Knowledge")
        
        if "current_quiz" not in st.session_state:
            st.session_state.current_quiz = None
        if "evaluation_results" not in st.session_state:
            st.session_state.evaluation_results = {}

        with st.form("quiz_generation_panel"):
            quiz_topic = st.text_input("What topic would you like to be quizzed on?", placeholder="e.g., Context Managers", key="quiz_topic_input")
            if st.form_submit_button("✨ Generate AI Quiz"):
                with st.spinner("Synthesizing questions..."):
                    quiz_data = generate_quiz(selected_id, quiz_topic)
                    if quiz_data and "quiz" in quiz_data:
                        st.session_state.current_quiz = quiz_data["quiz"]
                        st.session_state.evaluation_results = {} 
                        st.success("Quiz loaded!")
                    else:
                        st.error("Failed to generate quiz metadata.")

        if st.session_state.current_quiz:
            st.write(f"### Topic: {st.session_state.current_quiz.get('topic')}")
            questions = st.session_state.current_quiz.get("questions", [])
            
            for index, question in enumerate(questions):
                q_id = question["id"]
                q_text = question.get("question_text") or question.get("question") or "Missing Question Text"
                
                st.markdown(f"--- \n **Question {index + 1}:** {q_text}")
                user_ans = st.text_input("Your Answer:", key=f"ans_input_{q_id}")
                
                if st.button("Submit Answer", key=f"btn_sub_{q_id}"):
                    if not user_ans.strip():
                        st.warning("Please type an answer before submitting.")
                    else:
                        with st.spinner("Evaluating response..."):
                            eval_res = submit_quiz_answer(q_id, user_ans)
                            if eval_res:
                                st.session_state.evaluation_results[q_id] = eval_res
                
                if q_id in st.session_state.evaluation_results:
                    res = st.session_state.evaluation_results[q_id]
                    if res.get("needs_clarification"):
                        st.info(f"🤔 **Clarification Needed:** {res['clarification_question']}")
                    else:
                        if res.get("is_correct"):
                            st.success(f"✅ **Correct!** \n\n {res['feedback']}")
                        else:
                            st.error(f"❌ **Incorrect/Needs Improvement** \n\n {res['feedback']}")