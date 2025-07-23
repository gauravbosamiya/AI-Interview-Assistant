import os
import sys
import datetime
import re
import streamlit as st
import streamlit_authenticator as stauth
from dotenv import load_dotenv
from passlib.hash import bcrypt

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from api.mongo import user_collection 
from frontend.upload_file import upload_document
from frontend.text_to_speech import text_to_speech_with_speed
from frontend.speech_to_text import transcribe_speech
import time

load_dotenv()


def insert_user(email, username, password):
    data_joined = str(datetime.datetime.now())
    return user_collection.insert_one({
        'email': email,
        'username': username,
        'password': password,
        'date_joined': data_joined
    })

def is_email_taken(email):
    return user_collection.find_one({"email": email}) is not None

def is_username_taken(username):
    return user_collection.find_one({"username": username}) is not None

def fetch_users():
    return list(user_collection.find())

def validate_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_username(username):
    pattern = r'^[a-zA-Z0-9_]+$'
    return re.match(pattern, username) is not None


def sign_up():
    with st.form(key="signup", clear_on_submit=True):
        st.subheader("Create New Account")
        email = st.text_input("Email", placeholder="Enter your email")
        username = st.text_input("Username", placeholder="Enter your username").strip().lower()
        password = st.text_input("Password", type="password", placeholder="Enter password")
        confirm_password = st.text_input("Confirm Password", type="password", placeholder="Confirm password")
        submitted = st.form_submit_button("Sign Up")

        if submitted:
            if not validate_email(email):
                st.warning("Invalid email format.")
                return
            if is_email_taken(email):
                st.warning("Email already registered.")
                return
            if not validate_username(username):
                st.warning("Username must be alphanumeric.")
                return
            if len(username) < 2:
                st.warning("Username too short.")
                return
            if is_username_taken(username):
                st.warning("Username already exists.")
                return
            if len(password) < 6:
                st.warning("Password must be at least 6 characters.")
                return
            if password != confirm_password:
                st.warning("Passwords do not match.")
                return

            hashed_password = bcrypt.hash(password)

            insert_user(email, username.lower(), hashed_password)
            st.success("Account created! You can now log in.")

def ask_next_question(auto_play=True):
    if st.session_state.get("interview_quit", False):
        st.info("You have quit the interview.")
        return

    questions = st.session_state.get("questions", [])
    index = st.session_state.get("question_index", 0)

    if not questions:
        st.warning("No questions found. Please upload a resume first.")
        return

    if "answers" not in st.session_state:
        st.session_state["answers"] = {}

    if index < len(questions):
        question_text = questions[index]
        st.info(f"Question {index + 1}: {question_text}")

        if not st.session_state.get("has_spoken", False):
            text_to_speech_with_speed(question_text)
            st.session_state["has_spoken"] = True
            st.rerun()  

        if st.session_state["has_spoken"] and not st.session_state.get("answered", False):
            with st.spinner("Listening for your answer..."):
                answer_text = transcribe_speech()
                if answer_text:
                    st.success(f"✅ Answer: {answer_text}")
                    st.session_state["answers"][index] = answer_text
                    st.session_state["answered"] = True
                else:
                    st.warning("Could not transcribe your answer.")

        # Step 3: Auto-advance to next question
        if st.session_state.get("answered", False):
            time.sleep(2)  # brief pause before next question
            st.session_state["question_index"] += 1
            st.session_state["has_spoken"] = False
            st.session_state["answered"] = False
            st.rerun()

        # Quit button always available
        if st.button("❌ Quit Interview"):
            st.session_state["interview_quit"] = True
            st.warning("You quit your interview.")
    else:
        st.success("✅ Interview completed.")
        st.write("📝 Your responses:")
        for i, question in enumerate(questions):
            answer = st.session_state["answers"].get(i, "No answer.")
            st.markdown(f"**Q{i+1}: {question}**  \n**A:** {answer}")





def main():
    st.set_page_config(page_title="AI Interview Assistant", layout="wide")
    st.title("AI Interview Assistant")

    try:
        users = fetch_users()
        # print(users)
        credentials = {"usernames": {}}
        for user in users:
            credentials["usernames"][user["username"]] = {
                "name": user["email"],
                "password": user["password"]
            }

        authenticator = stauth.Authenticate(
            credentials=credentials,
            cookie_name="streamlit_auth",
            key="abcdef",
            cookie_expiry_days=1
        )

        email, authentication_status, username = authenticator.login("Login")

        if authentication_status:
            st.success(f"Welcome {username}!")
            upload_document(username)
            st.divider()
            if "interview_quit" not in st.session_state:
                 st.session_state["interview_quit"] = False
            ask_next_question()
            authenticator.logout(button_name="Log out")

        elif authentication_status is False:
            st.error("Invalid username or password")
            with st.expander("📝 Don't have an account? Sign up here"):
                sign_up()
        else:
            st.info("Please log in to continue.")
            with st.expander("📝 Don't have an account? Sign up here"):
                sign_up()

    except Exception as e:
        st.error(f"Error: {str(e)}")


if __name__ == "__main__":
    main()
