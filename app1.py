import streamlit as st
import json
import os
import time
import hashlib
from datetime import datetime
import pandas as pd
from io import BytesIO
from PIL import Image  


# Initialize session state
def init_session_state():
    if 'problems' not in st.session_state:
        st.session_state.problems = [
            {
                "id": 1,
                "title": "Regular Expression Matching",
                "description": """
Given an input string `s` and a pattern `p`, implement regular expression matching with support for '.' and '*' where:
- '.' matches any single character.
- '*' matches zero or more of the preceding element.
The matching should cover the entire input string (not partial).
                """,
                "difficulty": "Hard",
                "example": {
                    "input": "s = 'aa', p = 'a'",
                    "output": "false"
                },
                "solution": "",
                "solved": False,
                "max_score": 25
            },
            {
                "id": 2,
                "title": "Integer to English Words",
                "description": """
Convert a non-negative integer `num` to its English words representation.
                """,
                "difficulty": "Hard",
                "example": {
                    "input": "num = 12345",
                    "output": "'Twelve Thousand Three Hundred Forty Five'"
                },
                "solution": "",
                "solved": False,
                "max_score": 25
            },
            {
                "id": 3,
                "title": "Burst Balloons",
                "description": """
You are given `n` balloons, indexed from `0` to `n - 1`. Each balloon is painted with a number on it represented by an array `nums`.
You are asked to burst all the balloons. If you burst the ith balloon, you will get `nums[i-1] * nums[i] * nums[i+1]` coins.
Return the maximum coins you can collect by bursting the balloons wisely.
                """,
                "difficulty": "Hard",
                "example": {
                    "input": "nums = [3,1,5,8]",
                    "output": "167"
                },
                "solution": "",
                "solved": False,
                "max_score": 25
            },
            {
                "id": 4,
                "title": "Count All Valid Pickup/Delivery Options",
                "description": """
Given `n` orders, each order consists of a pickup and a delivery service. Count all valid pickup/delivery possible sequences such that delivery is always after its pickup.
                """,
                "difficulty": "Hard",
                "example": {
                    "input": "n = 2",
                    "output": "6"
                },
                "solution": "",
                "solved": False,
                "max_score": 25
            }
        ]
    
    if 'start_time' not in st.session_state:
        st.session_state.start_time = time.time()
    
    if 'completed' not in st.session_state:
        st.session_state.completed = False
    
    if 'data_file' not in st.session_state:
        st.session_state.data_file = "user_data.json"
        
    # Load existing data
    if not os.path.exists(st.session_state.data_file):
        with open(st.session_state.data_file, 'w') as f:
            json.dump({"users": {}, "admin_password": hashlib.sha256("admin123".encode()).hexdigest()}, f)

# Load user data
def load_data():
    try:
        with open(st.session_state.data_file, 'r') as f:
            return json.load(f)
    except:
        return {"users": {}, "admin_password": hashlib.sha256("admin123".encode()).hexdigest()}

# Save user data
def save_data(data):
    with open(st.session_state.data_file, 'w') as f:
        json.dump(data, f)

# Authentication
def login_form():
    # Logo section with fallback to text
    col_logo, col_title = st.columns([1, 3])
    with col_logo:
        try:
            logo = Image.open("algo.png")  # Make sure the file is in your project directory
            st.image(logo, width=150)  # Adjust width as needed
        except FileNotFoundError:
            st.markdown("""
            <div style="margin-bottom:10px">
                <h2 style="color:#2196F3;margin-bottom:0">ALGO PROTOCOLS</h2>
            </div>
            """, unsafe_allow_html=True)
    
    with col_title:
        st.title("ALGO PROTOCOLS Hackathon ")
    
    st.subheader("Test your Java skills with these challenging problems")
    
    col1, col2 = st.columns(2)
    with col1:
        with st.form("User Login"):
            st.subheader("Participant Login")
            username = st.text_input("Username", placeholder="Enter your username", key="user_username")
            submitted_user = st.form_submit_button("Login as Participant")
            
            if submitted_user and username:
                st.session_state.logged_in = True
                st.session_state.username = username
                st.session_state.role = "user"
                
                # Load or create user data
                data = load_data()
                if username not in data["users"]:
                    data["users"][username] = {
                        "problems": {},
                        "start_time": datetime.now().isoformat(),
                        "completed": False,
                        "total_score": 0
                    }
                    save_data(data)
                
                st.rerun()
    
    with col2:
        with st.form("Admin Login"):
            st.subheader("Admin Login")
            password = st.text_input("Password", type="password", placeholder="Admin password", key="admin_password")
            submitted_admin = st.form_submit_button("Login as Admin")
            
            if submitted_admin:
                data = load_data()
                hashed_password = hashlib.sha256(password.encode()).hexdigest()
                if hashed_password == data["admin_password"]:
                    st.session_state.logged_in = True
                    st.session_state.role = "admin"
                    st.rerun()
                else:
                    st.error("Incorrect admin password")

# Problem view
def show_problem(problem):
    st.subheader(f"Problem {problem['id']}: {problem['title']}")
    st.markdown(f"**Difficulty:** :red[{problem['difficulty']}]")
    
    with st.expander("Problem Description"):
        st.write(problem['description'])
        st.markdown("**Example:**")
        st.code(f"Input: {problem['example']['input']}\nOutput: {problem['example']['output']}", language="text")
    
    st.subheader("Your Java Solution")
    solution = st.text_area("Write your solution here", height=300, 
                           value=problem['solution'] or f"class Solution {{\n    public Object solve() {{\n        // Your Java code here\n        return null;\n    }}\n}}",
                           key=f"solution_{problem['id']}")
    
    if st.button(f"Submit Solution for Problem {problem['id']}", key=f"submit_{problem['id']}"):
        # Save solution to user data
        data = load_data()
        if st.session_state.username in data["users"]:
            user_data = data["users"][st.session_state.username]
            user_data["problems"][str(problem['id'])] = {
                "solution": solution,
                "submitted_at": datetime.now().isoformat(),
                "score": None,  # To be evaluated by admin
                "feedback": ""
            }
            save_data(data)
        
        problem['solution'] = solution
        problem['solved'] = True
        st.success("Solution submitted successfully!")
        time.sleep(1)
        st.rerun()

# Thank you page
def thank_you_page():
    st.balloons()
    st.title("🎉 Challenge Completed! 🎉")
    st.subheader(f"Congratulations {st.session_state.username}!")
    
    end_time = time.time()
    time_taken = end_time - st.session_state.start_time
    minutes, seconds = divmod(time_taken, 60)
    
    # Load user data
    data = load_data()
    user_data = data["users"].get(st.session_state.username, {})
    total_score = user_data.get("total_score", 0)
    
    st.markdown(f"""
    <div style="background:#0e1a40;padding:30px;border-radius:15px;margin:20px 0">
        <h2 style="color:white;text-align:center">You solved all 4 problems in {int(minutes)}m {int(seconds)}s!</h2>
    </div>
    """, unsafe_allow_html=True)
    
    # Show score only if evaluated
    if total_score > 0:
        st.markdown(f"""
        <div style="background:#1b5e20;padding:20px;border-radius:10px;margin-bottom:30px;text-align:center">
            <h2 style="color:white">Your Final Score: {total_score}/100</h2>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.info("Your solutions are pending evaluation by the admin")
    
    st.subheader("Your Solutions")
    for problem in st.session_state.problems:
        problem_id = str(problem['id'])
        problem_data = user_data.get("problems", {}).get(problem_id, {})
        
        with st.expander(f"Problem {problem['id']}: {problem['title']}"):
            st.code(problem_data.get("solution", ""), language="java")
    
    st.markdown("""
    <div style="text-align:center;margin-top:50px">
        <h3>Want more challenges?</h3>
        <p>Check out the original problems on LeetCode:</p>
        <ul style="list-style:none;padding:0">
            <li><a href="https://leetcode.com/problems/regular-expression-matching/">Regular Expression Matching</a></li>
            <li><a href="https://leetcode.com/problems/integer-to-english-words/">Integer to English Words</a></li>
            <li><a href="https://leetcode.com/problems/burst-balloons/">Burst Balloons</a></li>
            <li><a href="https://leetcode.com/problems/count-all-valid-pickup-and-delivery-options/">Count Valid Pickup/Delivery Options</a></li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# Convert data to Excel format
def convert_to_excel(data):
    # Prepare data for Excel
    excel_data = []
    
    for username, user_data in data["users"].items():
        row = {
            "Username": username,
            "Start Time": user_data.get("start_time", ""),
            "Completed": "Yes" if user_data.get("completed", False) else "No",
            "Total Score": user_data.get("total_score", 0)
        }
        
        # Add problem-specific data
        for problem in st.session_state.problems:
            pid = str(problem['id'])
            problem_data = user_data.get("problems", {}).get(pid, {})
            
            row[f"Problem {pid} Solution"] = problem_data.get("solution", "")
            row[f"Problem {pid} Score"] = problem_data.get("score", "")
            row[f"Problem {pid} Feedback"] = problem_data.get("feedback", "")
            row[f"Problem {pid} Submitted At"] = problem_data.get("submitted_at", "")
        
        excel_data.append(row)
    
    # Create DataFrame
    df = pd.DataFrame(excel_data)
    
    # Create Excel file in memory
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='User Submissions')
        
        # Add summary sheet
        summary_data = []
        for problem in st.session_state.problems:
            summary_data.append({
                "Problem ID": problem['id'],
                "Title": problem['title'],
                "Difficulty": problem['difficulty'],
                "Max Score": problem['max_score']
            })
        
        summary_df = pd.DataFrame(summary_data)
        summary_df.to_excel(writer, index=False, sheet_name='Problem Summary')
        
        # Formatting - autofit columns
        for sheet in writer.sheets:
            worksheet = writer.sheets[sheet]
            for column in worksheet.columns:
                max_length = 0
                column = [cell for cell in column]
                for cell in column:
                    try:
                        if len(str(cell.value)) > max_length:
                            max_length = len(cell.value)
                    except:
                        pass
                adjusted_width = (max_length + 2)
                worksheet.column_dimensions[column[0].column_letter].width = adjusted_width
    
    output.seek(0)
    return output

# Admin dashboard
def admin_dashboard():
    st.title("Admin Dashboard 🔐")
    st.subheader("Evaluate Participant Solutions")
    
    data = load_data()
    users = list(data["users"].keys())
    
    if not users:
        st.info("No participants yet")
        return
    
    selected_user = st.selectbox("Select Participant", users)
    user_data = data["users"][selected_user]
    
    st.subheader(f"Solutions from {selected_user}")
    
    # Show user summary
    solved_count = sum(1 for pid in user_data["problems"] if user_data["problems"][pid]["solution"])
    total_score = user_data.get("total_score", 0)
    
    col1, col2 = st.columns(2)
    col1.metric("Problems Solved", f"{solved_count}/4")
    col2.metric("Total Score", f"{total_score}/100")
    
    # Show problems and solutions
    for problem in st.session_state.problems:
        problem_id = str(problem['id'])
        problem_data = user_data.get("problems", {}).get(problem_id, {})
        
        if not problem_data:
            continue
            
        with st.expander(f"Problem {problem['id']}: {problem['title']}"):
            st.markdown(f"**Submitted at:** {problem_data.get('submitted_at', 'Unknown')}")
            
            # Display solution
            st.code(problem_data.get("solution", "No solution submitted"), language="java")
            
            # Evaluation form
            with st.form(f"eval_{selected_user}_{problem_id}"):
                score = st.slider(
                    "Score", 
                    0, 
                    problem['max_score'], 
                    value=problem_data.get("score", 0) or 0,
                    key=f"score_{selected_user}_{problem_id}"
                )
                feedback = st.text_area(
                    "Feedback", 
                    value=problem_data.get("feedback", ""),
                    placeholder="Enter your feedback here",
                    key=f"feedback_{selected_user}_{problem_id}"
                )
                
                if st.form_submit_button("Save Evaluation"):
                    # Update score and feedback
                    problem_data["score"] = score
                    problem_data["feedback"] = feedback
                    
                    # Update total score
                    total_score = 0
                    for pid in user_data["problems"]:
                        total_score += user_data["problems"][pid].get("score", 0)
                    user_data["total_score"] = total_score
                    
                    # Save data
                    data["users"][selected_user] = user_data
                    save_data(data)
                    st.success("Evaluation saved!")
    
    # Export data to Excel
    st.divider()
    st.subheader("Data Export")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📊 Export to Excel"):
            try:
                excel_file = convert_to_excel(data)
                st.download_button(
                    label="⬇️ Download Excel File",
                    data=excel_file,
                    file_name="leetcode_submissions.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
            except Exception as e:
                st.error(f"Error creating Excel file: {e}")
    
    with col2:
        st.download_button(
            label="📥 Download Raw JSON",
            data=json.dumps(data, indent=2),
            file_name="user_data.json",
            mime="application/json"
        )

# Main app
def main():
    # Page configuration
    st.set_page_config(
        page_title="LeetCode Challenge",
        layout="wide",
        page_icon="🔥",
        initial_sidebar_state="collapsed"
    )
    
    # Custom CSS
    st.markdown("""
    <style>
    /* Main styling */
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
        color: white;
    }
    
    /* Headers */
    h1, h2, h3, h4, h5, h6 {
        color: white !important;
    }
    
    /* Buttons */
    .stButton>button {
        background: linear-gradient(45deg, #2196F3, #21CBF3);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 10px 24px;
        font-weight: bold;
        transition: all 0.3s;
    }
    
    .stButton>button:hover {
        transform: scale(1.05);
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    
    /* Text areas */
    .stTextArea textarea {
        background-color: #0e1a40;
        color: #ffffff;
        border: 1px solid #2196F3;
        border-radius: 8px;
        font-family: 'Courier New', monospace;
    }
    
    /* Expanders */
    .stExpander {
        background-color: rgba(10, 20, 50, 0.8);
        border: 1px solid #2196F3;
        border-radius: 8px;
        padding: 10px;
        margin-bottom: 15px;
    }
    
    /* Progress bar */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, #2196F3, #21CBF3);
    }
    
    /* Code blocks */
    .stCodeBlock {
        border-radius: 8px;
        background-color: #0e1a40;
    }
    
    /* Admin dashboard */
    .stSelectbox div[data-baseweb="select"] > div {
        background-color: #0e1a40;
        color: white;
    }
    
    /* Download buttons */
    .stDownloadButton>button {
        background: linear-gradient(45deg, #00c853, #64dd17) !important;
        width: 100%;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Initialize session state
    init_session_state()
    
    # Check if user is logged in
    if not st.session_state.get('logged_in', False):
        login_form()
        return
    
    # Admin view
    if st.session_state.role == "admin":
        admin_dashboard()
        return
    
    # Navigation header
    st.title(f" Hackathon  by ALGO PROTOCOLS")
    st.subheader(f"Welcome, {st.session_state.username}!")
    
    # Load user data
    data = load_data()
    user_data = data["users"].get(st.session_state.username, {})
    
    # Show progress
    solved_count = sum(1 for pid in user_data.get("problems", {}) 
                      if user_data["problems"][pid].get("solution"))
    total_problems = len(st.session_state.problems)
    progress = solved_count / total_problems
    
    st.markdown(f"**Progress:** {solved_count}/{total_problems} problems solved")
    st.progress(progress)
    
    # Calculate time taken
    start_time = datetime.fromisoformat(user_data.get("start_time", datetime.now().isoformat()))
    time_taken = (datetime.now() - start_time).total_seconds()
    minutes, seconds = divmod(time_taken, 60)
    st.caption(f"Time elapsed: {int(minutes)} minutes {int(seconds)} seconds")
    
    # Check if all problems are solved
    if solved_count == total_problems:
        st.session_state.completed = True
        user_data["completed"] = True
        data["users"][st.session_state.username] = user_data
        save_data(data)
    
    # Show thank you page if completed
    if st.session_state.completed or user_data.get("completed", False):
        thank_you_page()
        return
    
    # Show current unsolved problem
    for problem in st.session_state.problems:
        problem_id = str(problem['id'])
        if problem_id not in user_data.get("problems", {}):
            show_problem(problem)
            break
        elif not user_data["problems"][problem_id].get("solution", ""):
            show_problem(problem)
            break

if __name__ == "__main__":
    main()