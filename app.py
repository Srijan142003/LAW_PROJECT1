
# import os
# import re
# import json
# import requests
# from flask import Flask, render_template, request, jsonify, session, redirect, url_for, flash
# from werkzeug.utils import secure_filename
# from werkzeug.security import generate_password_hash, check_password_hash
# import PyPDF2
# import docx
# from functools import wraps
# from dotenv import load_dotenv
# from datetime import datetime

# # --- Load Environment Variables ---
# load_dotenv()

# # --- App Configuration ---
# app = Flask(__name__)
# app.secret_key = 'your_super_secret_key_for_sessions_and_flash_messages'
# UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "uploads")
# os.makedirs(UPLOAD_FOLDER, exist_ok=True)
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# ALLOWED_EXTENSIONS = {'pdf', 'docx', 'txt'}

# # --- Data File Paths ---
# USERS_FILE = 'users.json'
# CHAT_LOGS_FILE = 'chat_logs.json'
# ADMIN_DATA_FILE = 'admin_data.json'

# # --- Initialize Data Files ---
# def initialize_data_files():
#     if not os.path.exists(USERS_FILE):
#         with open(USERS_FILE, 'w') as f: json.dump({}, f)
#     if not os.path.exists(CHAT_LOGS_FILE):
#         with open(CHAT_LOGS_FILE, 'w') as f: json.dump({}, f)
#     if not os.path.exists(ADMIN_DATA_FILE):
#         with open(ADMIN_DATA_FILE, 'w') as f:
#             json.dump({
#                 "user_visits": {},
#                 "verdict_feedback": [],
#                 "case_type_counts": {}
#             }, f, indent=4)

# initialize_data_files()

# # --- Data Loading/Saving Functions ---
# def load_knowledge_base():
#     try:
#         with open('knowledge_base.json', 'r', encoding='utf-8') as f: return json.load(f)
#     except (FileNotFoundError, json.JSONDecodeError): return []

# knowledge_base = load_knowledge_base()

# def load_users():
#     with open(USERS_FILE, 'r') as f: return json.load(f)

# def save_users(users):
#     with open(USERS_FILE, 'w') as f: json.dump(users, f, indent=4)

# def load_chat_history(username):
#     # This can be used for a more persistent chat memory if needed later
#     with open(CHAT_LOGS_FILE, 'r') as f: logs = json.load(f)
#     return logs.get(username, [])

# def save_chat_history(username, history):
#     # This can be used for a more persistent chat memory if needed later
#     with open(CHAT_LOGS_FILE, 'r') as f: logs = json.load(f)
#     logs[username] = history
#     with open(CHAT_LOGS_FILE, 'w') as f: json.dump(logs, f, indent=4)

# def load_admin_data():
#     with open(ADMIN_DATA_FILE, 'r') as f: return json.load(f)

# def save_admin_data(data):
#     with open(ADMIN_DATA_FILE, 'w') as f: json.dump(data, f, indent=4)

# # --- Decorators & Helpers ---
# def login_required(f):
#     @wraps(f)
#     def decorated_function(*args, **kwargs):
#         if 'username' not in session:
#             flash('Please log in to access this page.', 'warning')
#             return redirect(url_for('login'))
#         return f(*args, **kwargs)
#     return decorated_function

# def admin_required(f):
#     @wraps(f)
#     def decorated_function(*args, **kwargs):
#         if 'username' not in session or session['username'] != 'admin':
#             flash('You do not have permission to access this page.', 'danger')
#             return redirect(url_for('home'))
#         return f(*args, **kwargs)
#     return decorated_function

# def allowed_file(filename):
#     return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# def search_knowledge_base(user_query):
#     relevant_docs = []
#     query_words = set(user_query.lower().split())
#     for item in knowledge_base:
#         title_words = set(item.get('title', '').lower().split())
#         summary_words = set(item.get('gemini_summary', '').lower().split())
#         if query_words & title_words or query_words & summary_words:
#             relevant_docs.append(item['text'])
#     return "\n\n---\n\n".join(relevant_docs[:2])

# # --- Gemini AI Processing Function ---
# def process_with_gemini(history: list, system_prompt: str) -> str:
#     api_key = os.getenv('GEMINI_API_KEY')
#     if not api_key:
#         return "Error: GEMINI_API_KEY not set. Check your .env file."
#     url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
#     headers = {"Content-Type": "application/json"}
#     data = { "contents": history, "systemInstruction": { "role": "model", "parts": [{"text": system_prompt}] } }
#     try:
#         response = requests.post(url, headers=headers, data=json.dumps(data))
#         response.raise_for_status()
#         result = response.json()
#         if "candidates" not in result or not result["candidates"]:
#              if 'promptFeedback' in result:
#                  return "Response blocked due to safety concerns."
#              return "Error: The AI returned an empty response."
#         return result["candidates"][0]["content"]["parts"][0]["text"]
#     except requests.exceptions.RequestException:
#         return "Error: Connection to AI service failed."
#     except (KeyError, IndexError):
#         return "Error: Could not parse AI response."

# # --- Authentication Routes ---
# @app.route('/register', methods=['GET', 'POST'])
# def register():
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']
#         users = load_users()
#         if username in users:
#             flash('Username already exists.', 'danger')
#             return redirect(url_for('register'))
#         hashed_password = generate_password_hash(password)
#         users[username] = hashed_password
#         save_users(users)
#         flash('Account created successfully! Please log in.', 'success')
#         return redirect(url_for('login'))
#     return render_template('register.html')

# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']
#         users = load_users()
#         if username not in users or not check_password_hash(users.get(username), password):
#             flash('Invalid username or password.', 'danger')
#             return redirect(url_for('login'))
#         session['username'] = username
#         admin_data = load_admin_data()
#         admin_data['user_visits'][username] = admin_data['user_visits'].get(username, 0) + 1
#         save_admin_data(admin_data)
#         return redirect(url_for('home'))
#     return render_template('login.html')

# @app.route('/logout')
# def logout():
#     session.pop('username', None)
#     flash('You have been logged out.', 'info')
#     return redirect(url_for('login'))

# # --- Main Application Routes ---
# @app.route('/')
# def index():
#     if 'username' in session:
#         return redirect(url_for('home'))
#     return redirect(url_for('login'))

# @app.route('/home')
# @login_required
# def home():
#     return render_template('home.html')

# @app.route('/trial', methods=['GET', 'POST'])
# @login_required
# def trial():
#     if request.method == 'POST':
#         accuser_statement = request.form.get('accuser_statement', '').strip()
#         defender_statement = request.form.get('defender_statement', '').strip()
#         file_text = '' # Placeholder for file content
        
#         structured_input = (f"Accuser's Statement:\n{accuser_statement}\n\n" f"Defender's Statement:\n{defender_statement}\n\n")
#         ai_prompt = (
#             "You are an AI Judge. Based on the provided statements, "
#             "provide an unbiased, structured verdict. Your verdict MUST include three distinct sections, "
#             "clearly marked with Roman numerals: I. Summary of Arguments, II. Findings of Fact, and III. Final Order."
#         )
#         verdict_output = process_with_gemini([{"role": "user", "parts": [{"text": structured_input}]}], system_prompt=ai_prompt)

#         # More Robust Verdict Parsing
#         summary = "Summary could not be parsed."
#         findings = "Findings could not be parsed."
#         order = "Order could not be parsed."

#         summary_match = re.search(r'I\.\s*Summary of Arguments(.*?)(?=II\.\s*Findings of Fact|$)', verdict_output, re.IGNORECASE | re.DOTALL)
#         if summary_match:
#             summary = summary_match.group(1).strip()

#         findings_match = re.search(r'II\.\s*Findings of Fact(.*?)(?=III\.\s*Final Order|$)', verdict_output, re.IGNORECASE | re.DOTALL)
#         if findings_match:
#             findings = findings_match.group(1).strip()

#         order_match = re.search(r'III\.\s*Final Order(.*)', verdict_output, re.IGNORECASE | re.DOTALL)
#         if order_match:
#             order = order_match.group(1).strip()
        
#         return render_template('result.html', summary=summary, findings=findings, order=order,
#                                accuser_statement=accuser_statement, defender_statement=defender_statement)
    
#     return render_template('trial.html')

# @app.route('/consult')
# @login_required
# def consult():
#     # We use the session to store the current conversation's history
#     session['current_chat_history'] = []
#     return render_template('consult.html', chat_history=session['current_chat_history'])

# @app.route('/chat', methods=['POST'])
# @login_required
# def chat():
#     user_message = request.json.get('message')
#     if not user_message: return jsonify({'error': 'No message provided'}), 400

#     chat_history = session.get('current_chat_history', [])
#     chat_history.append({"role": "user", "parts": [{"text": user_message}]})

#     context = search_knowledge_base(user_message)

#     # New Realistic Chatbot Persona
#     chatbot_prompt = (
#         "You are 'Nyay Mitra,' an AI simulating a sharp, practical Indian lawyer. Your goal is to provide clear, actionable guidance. Your tone is professional, direct, and empathetic.\n\n"
#         "**Your Communication Rules:**\n"
#         "1.  **Be Concise:** Avoid long paragraphs. Use bullet points (`*`) or numbered lists for step-by-step advice.\n"
#         "2.  **Be Practical:** Give realistic suggestions. Instead of just 'see a lawyer,' suggest *what kind* of lawyer and *what documents* to prepare (e.g., 'Gather your property deed and any written agreements.').\n"
#         "3.  **Ask Questions:** If the user's query is vague, ask clarifying questions to understand their specific situation before giving advice.\n"
#         "4.  **Stay in Character:** You are an experienced advisor helping a client, not a textbook.\n\n"
#         f"**Reference Information (Use if relevant):**\n{context}\n\n"
#         "**Mandatory Disclaimer:** You MUST end every response with the following text on a new line, exactly as written:\n"
#         "---\n"
#         "*Disclaimer: I am an AI assistant and this is for informational purposes only, not legal advice. Always consult a qualified human lawyer for your case.*"
#     )

#     ai_response_text = process_with_gemini(chat_history, system_prompt=chatbot_prompt)
#     chat_history.append({"role": "model", "parts": [{"text": ai_response_text}]})
    
#     session['current_chat_history'] = chat_history
    
#     return jsonify({'response': ai_response_text})

# # --- Admin Routes ---
# @app.route('/submit_feedback', methods=['POST'])
# @login_required
# def submit_feedback():
#     feedback_text = request.form.get('remarks')
#     case_type = request.form.get('case_type')
#     rating = request.form.get('rating')
#     if not feedback_text or not case_type or not rating:
#         flash('Please fill out all feedback fields.', 'warning')
#         return redirect(request.referrer)
#     admin_data = load_admin_data()
#     new_feedback = {
#         "username": session['username'], "feedback": feedback_text,
#         "rating": rating, "case_type": case_type,
#         "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#     }
#     admin_data['verdict_feedback'].append(new_feedback)
#     admin_data['case_type_counts'][case_type] = admin_data['case_type_counts'].get(case_type, 0) + 1
#     save_admin_data(admin_data)
#     flash('Thank you for your feedback!', 'success')
#     return redirect(url_for('home'))

# @app.route('/admin')
# @admin_required
# def admin_dashboard():
#     admin_data = load_admin_data()
#     sorted_visits = sorted(admin_data['user_visits'].items(), key=lambda item: item[1], reverse=True)
#     return render_template('admin.html', 
#                            user_visits=sorted_visits,
#                            feedback_list=admin_data['verdict_feedback'],
#                            case_counts=admin_data['case_type_counts'])

# if __name__ == '__main__':
#     app.run(debug=True)


import os
import re
import json
import requests
import time
from flask import Flask, render_template, request, jsonify, session, redirect, url_for, flash
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
import PyPDF2
import docx
from functools import wraps
from dotenv import load_dotenv
from datetime import datetime

# --- Load Environment Variables ---
load_dotenv()

# --- App Configuration ---
app = Flask(__name__)
app.secret_key = 'your_super_secret_key_for_sessions_and_flash_messages'
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'pdf', 'docx', 'txt'}

# --- Data File Paths ---
USERS_FILE = 'users.json'
USER_MEMORY_FILE = 'user_memory_store.json'
ADMIN_DATA_FILE = 'admin_data.json'

# --- Initialize Data Files ---
def initialize_data_files():
    if not os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'w') as f: json.dump({}, f)
    if not os.path.exists(USER_MEMORY_FILE):
        with open(USER_MEMORY_FILE, 'w') as f: json.dump({}, f)
    if not os.path.exists(ADMIN_DATA_FILE):
        with open(ADMIN_DATA_FILE, 'w') as f:
            json.dump({"user_visits": {}, "verdict_feedback": [], "case_type_counts": {}}, f)

initialize_data_files()

# --- Data Loading/Saving Functions ---
def load_users():
    with open(USERS_FILE, 'r') as f: return json.load(f)

def save_users(users):
    with open(USERS_FILE, 'w') as f: json.dump(users, f, indent=4)

def load_memory_store():
    with open(USER_MEMORY_FILE, 'r') as f: return json.load(f)

def save_memory_store(data):
    with open(USER_MEMORY_FILE, 'w') as f: json.dump(data, f, indent=4)

def load_admin_data():
    with open(ADMIN_DATA_FILE, 'r') as f: return json.load(f)

def save_admin_data(data):
    with open(ADMIN_DATA_FILE, 'w') as f: json.dump(data, f, indent=4)

# --- Decorators & Helpers ---
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session or session['username'] != 'admin':
            flash('You do not have permission to access this page.', 'danger')
            return redirect(url_for('home'))
        return f(*args, **kwargs)
    return decorated_function

# --- AI-Powered Memory Functions ---
def get_case_label_from_ai(text: str) -> str:
    prompt = ("Analyze the following legal text and classify it into one of these categories: "
              "'Criminal Law', 'Civil Law', 'Family Law', 'Corporate Law', 'Property Law', 'Other'. "
              "Respond with ONLY the category name.")
    history = [{"role": "user", "parts": [{"text": text}]}]
    label = process_with_gemini(history, system_prompt=prompt).strip().replace("Law", "").strip()
    return f"{label} Law" if label != "Other" else "Other"

def find_relevant_past_cases(username: str, new_label: str) -> str:
    memory_store = load_memory_store()
    user_memory = memory_store.get(username, {})
    past_context = []
    for trial in user_memory.get('court_trials', []):
        if trial.get('label') == new_label:
            past_context.append(f"- Past Trial Verdict: {trial.get('verdict_summary', 'N/A')}")
    for convo in user_memory.get('consultations', []):
        if convo.get('label') == new_label:
            past_context.append(f"- Past Consultation Summary: {convo.get('conversation_summary', 'N/A')}")
    if not past_context:
        return "No relevant past cases found in your memory."
    return "For your reference, here are summaries of your past cases with a similar label:\n" + "\n".join(past_context)

# --- Gemini AI Processing ---
def process_with_gemini(history: list, system_prompt: str) -> str:
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key: return "Error: GEMINI_API_KEY not set."
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    headers = {"Content-Type": "application/json"}
    data = {"contents": history, "systemInstruction": {"role": "model", "parts": [{"text": system_prompt}]}}
    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        response.raise_for_status()
        result = response.json()
        if "candidates" not in result or not result["candidates"]:
            if 'promptFeedback' in result:
                return "I am unable to respond to this request due to safety restrictions."
            return "Error: The AI returned an empty response."
        return result["candidates"][0]["content"]["parts"][0]["text"]
    except requests.exceptions.RequestException:
        return "Error: Could not connect to the AI service. Please check your network and API key."
    except Exception:
        return "An unexpected error occurred while communicating with the AI service."


# --- Routes (Authentication, Main) ---
@app.route('/')
def index():
    if 'username' in session: return redirect(url_for('home'))
    return redirect(url_for('login'))

@app.route('/home')
@login_required
def home():
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users = load_users()
        if username in users:
            flash('Username already exists.', 'danger')
            return redirect(url_for('register'))
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        users[username] = hashed_password
        save_users(users)
        flash('Account created! Please log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users = load_users()
        if username not in users or not check_password_hash(users.get(username), password):
            flash('Invalid username or password.', 'danger')
            return redirect(url_for('login'))
        session['username'] = username
        admin_data = load_admin_data()
        admin_data['user_visits'][username] = admin_data['user_visits'].get(username, 0) + 1
        save_admin_data(admin_data)
        return redirect(url_for('home'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

@app.route('/trial', methods=['GET', 'POST'])
@login_required
def trial():
    if request.method == 'POST':
        accuser_statement = request.form.get('accuser_statement', '').strip()
        defender_statement = request.form.get('defender_statement', '').strip()
        case_label = request.form.get('case_type')
        if not case_label:
            flash('Please select a case type.', 'warning')
            return redirect(url_for('trial'))
        
        structured_input = (f"Accuser's Statement:\n{accuser_statement}\n\n" f"Defender's Statement:\n{defender_statement}")
        username = session['username']
        context_from_memory = find_relevant_past_cases(username, case_label)
        
        ai_prompt = (f"You are an AI Judge. Provide a verdict with three distinct, clearly marked sections: "
                     f"I. Summary of Arguments, II. Findings of Fact, and III. Final Order. "
                     f"Consider this context from the user's past related cases:\n{context_from_memory}")
        verdict_output = process_with_gemini([{"role": "user", "parts": [{"text": structured_input}]}], system_prompt=ai_prompt)

        summary = "Summary could not be parsed."
        findings = "Findings could not be parsed."
        order = "Order could not be parsed."

        summary_match = re.search(r'I\.\s*(?:Summary of Arguments)?(.*?)(?=II\.|$)', verdict_output, re.IGNORECASE | re.DOTALL)
        if summary_match:
            summary = summary_match.group(1).strip()

        if "II." in verdict_output.upper():
            findings_match = re.search(r'II\.\s*(?:Findings of Fact)?(.*?)(?=III\.|$)', verdict_output, re.IGNORECASE | re.DOTALL)
            if findings_match:
                findings = findings_match.group(1).strip()
        
        if "III." in verdict_output.upper():
            order_match = re.search(r'III\.\s*(?:Final Order)?(.*?)$', verdict_output, re.IGNORECASE | re.DOTALL)
            if order_match:
                order = order_match.group(1).strip()

        memory_store = load_memory_store()
        if username not in memory_store:
            memory_store[username] = {"court_trials": [], "consultations": []}
        
        new_trial_record = {
            "case_id": f"ct_{int(time.time())}", "label": case_label, "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "verdict_summary": summary, "full_input": structured_input, "full_verdict": verdict_output
        }
        memory_store[username]['court_trials'].append(new_trial_record)
        save_memory_store(memory_store)
        
        return render_template('result.html', summary=summary, findings=findings, order=order, accuser_statement=accuser_statement, defender_statement=defender_statement)
    return render_template('trial.html')

@app.route('/consult')
@login_required
def consult():
    session['current_chat_history'] = []
    session.pop('current_convo_id', None)
    return render_template('consult.html', chat_history=[])

@app.route('/chat', methods=['POST'])
@login_required
def chat():
    user_message = request.json.get('message')
    username = session['username']
    chat_history = session.get('current_chat_history', [])
    chat_history.append({"role": "user", "parts": [{"text": user_message}]})

    if len(chat_history) == 1:
        session['current_chat_label'] = get_case_label_from_ai(user_message)
    
    chat_label = session.get('current_chat_label')
    context_from_memory = find_relevant_past_cases(username, chat_label)

    chatbot_prompt = (
        "You are 'Nyay Mitra,' an AI simulating a sharp, practical Indian lawyer. Your goal is to provide clear, actionable guidance.\n\n"
        "**Your Formatting Rules (IMPORTANT):**\n"
        "1.  **Use HTML for all formatting.**\n"
        "2.  For bullet points, use `<ul>` and `<li>` tags. (e.g., `<ul><li>First point</li><li>Second point</li></ul>`).\n"
        "3.  Use `<br>` for line breaks.\n"
        "4.  Use `<strong>` for bold text.\n\n"
        "**Your Communication Rules:**\n"
        "1.  **Be Concise:** Avoid long paragraphs. Use HTML lists for step-by-step advice.\n"
        "2.  **Be Practical:** Give realistic suggestions (e.g., 'Gather your property deed...').\n"
        "3.  **Ask Questions:** If the user's query is vague, ask clarifying questions.\n\n"
        f"**Reference from past conversations on this topic ({chat_label}):**\n{context_from_memory}\n\n"
        "**Mandatory Disclaimer:** You MUST end every response with the following HTML block on a new line, exactly as written:\n"
        "<hr>\n"
        "<em>Disclaimer: I am an AI assistant and this is for informational purposes only, not legal advice. Always consult a qualified human lawyer for your case.</em>"
    )
    
    ai_response_text = process_with_gemini(chat_history, system_prompt=chatbot_prompt)
    chat_history.append({"role": "model", "parts": [{"text": ai_response_text}]})
    session['current_chat_history'] = chat_history

    memory_store = load_memory_store()
    if username not in memory_store:
        memory_store[username] = {"court_trials": [], "consultations": []}

    convo_id = session.get('current_convo_id')
    if not convo_id:
        convo_id = f"cc_{int(time.time())}"
        session['current_convo_id'] = convo_id
        summary_prompt = "Summarize this legal conversation in one sentence for future reference."
        convo_summary = process_with_gemini(chat_history + [{"role": "user", "parts": [{"text": summary_prompt}]}], system_prompt="")
        new_convo_record = {
            "convo_id": convo_id, "label": chat_label, "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "conversation_summary": convo_summary, "full_history": chat_history
        }
        memory_store[username]['consultations'].append(new_convo_record)
    else:
        for convo in memory_store[username]['consultations']:
            if convo['convo_id'] == convo_id:
                convo['full_history'] = chat_history
                break
    save_memory_store(memory_store)

    return jsonify({'response': ai_response_text})

@app.route('/submit_feedback', methods=['POST'])
@login_required
def submit_feedback():
    feedback_text = request.form.get('remarks')
    case_type = request.form.get('case_type')
    rating = request.form.get('rating')

    if not case_type or not rating:
        flash('Please fill out all required feedback fields.', 'warning')
        return redirect(request.referrer)

    admin_data = load_admin_data()
    
    new_feedback = {
        "username": session['username'], "feedback": feedback_text, "rating": rating,
        "case_type": case_type, "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    admin_data['verdict_feedback'].append(new_feedback)
    admin_data['case_type_counts'][case_type] = admin_data['case_type_counts'].get(case_type, 0) + 1
    save_admin_data(admin_data)
    
    flash('Thank you for your feedback!', 'success')
    return redirect(url_for('home'))

@app.route('/admin')
@admin_required
def admin_dashboard():
    admin_data = load_admin_data()
    sorted_visits = sorted(admin_data['user_visits'].items(), key=lambda item: item[1], reverse=True)
    return render_template('admin.html', 
                           user_visits=sorted_visits,
                           feedback_list=admin_data['verdict_feedback'],
                           case_counts=admin_data['case_type_counts'])

if __name__ == '__main__':
    app.run(debug=True)




