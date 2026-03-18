from flask import Flask, request, jsonify, render_template, redirect, url_for
from database import SessionLocal, Textbook, ChatSession, ChatMessage, User
from pdf_helper import read_pdf_text
import requests
from google import genai
import os
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from functools import wraps
import random
import string
import time

load_dotenv()

app = Flask(__name__)
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# --- HELPER FUNCTIONS ---
def generate_user_id():
    """Generate a unique 4-digit random ID"""
    return ''.join(random.choices(string.digits, k=4))

def hash_password(password):
    """Hash the password"""
    return generate_password_hash(password)

def verify_password(password, hashed):
    """Verify password against hash"""
    return check_password_hash(hashed, password)

def get_user_from_session():
    """Get user ID from session header"""
    user_id = request.headers.get('X-User-ID')
    return user_id

def require_auth(f):
    """Decorator to require authentication"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user_id = get_user_from_session()
        if not user_id:
            return jsonify({"error": "Unauthorized"}), 401
        db = SessionLocal()
        user = db.query(User).filter(User.user_id == user_id).first()
        db.close()
        if not user:
            return jsonify({"error": "Invalid user"}), 401
        return f(*args, **kwargs)
    return decorated_function

ALLOWED_UPLOAD_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg', 'bmp', 'tiff'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_UPLOAD_EXTENSIONS

# --- AUTH ROUTES ---

@app.route('/login')
def login_page():
    return render_template('login.html')

@app.route('/register')
def register_page():
    return render_template('register.html')

@app.route('/api/auth/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username', '').strip()
    password = data.get('password', '')
    
    # Validation
    if not username or len(username) < 3 or len(username) > 50:
        return jsonify({"error": "Username must be 3-50 characters"}), 400
    
    if not password or len(password) < 6:
        return jsonify({"error": "Password must be at least 6 characters"}), 400
    
    # Check if username already exists
    db = SessionLocal()
    existing_user = db.query(User).filter(User.username == username).first()
    if existing_user:
        db.close()
        return jsonify({"error": "Username already exists"}), 409
    
    # Generate unique user ID
    user_id = generate_user_id()
    max_attempts = 100
    attempts = 0
    while db.query(User).filter(User.user_id == user_id).first() and attempts < max_attempts:
        user_id = generate_user_id()
        attempts += 1
    
    if attempts >= max_attempts:
        db.close()
        return jsonify({"error": "Could not generate unique ID"}), 500
    
    # Create new user
    hashed_password = hash_password(password)
    new_user = User(user_id=user_id, username=username, password=hashed_password)
    
    try:
        db.add(new_user)
        db.commit()
        db.close()
        return jsonify({
            "message": "User registered successfully",
            "user_id": user_id,
            "username": username
        }), 201
    except Exception as e:
        db.close()
        return jsonify({"error": "Registration failed"}), 500

@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username', '').strip()
    password = data.get('password', '')
    
    if not username or not password:
        return jsonify({"error": "Username and password required"}), 400
    
    db = SessionLocal()
    user = db.query(User).filter(User.username == username).first()
    db.close()
    
    if not user or not verify_password(password, user.password):
        return jsonify({"error": "Invalid username or password"}), 401
    
    return jsonify({
        "message": "Login successful",
        "user_id": user.user_id,
        "username": user.username
    }), 200

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/classes', methods=['GET'])
def get_classes():
    session = SessionLocal()
    classes = session.query(Textbook.class_level).distinct().order_by(Textbook.class_level).all()
    session.close()
    return jsonify([c[0] for c in classes])

@app.route('/api/subjects/<int:class_id>', methods=['GET'])
def get_subjects(class_id):
    session = SessionLocal()
    subjects = session.query(Textbook.book).filter(Textbook.class_level == class_id).all()
    session.close()
    return jsonify([s[0] for s in subjects])

@app.route('/api/upload', methods=['POST'])
@require_auth
def upload_file():
    # Accept a file and extract text (pdf/image) via OCR if needed.
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files['file']
    if not file or file.filename == '':
        return jsonify({"error": "No file selected"}), 400

    if not allowed_file(file.filename):
        return jsonify({"error": "Unsupported file format. Supported: pdf, jpg, jpeg, png, bmp, tiff"}), 400

    # Save the uploaded file into the cache folder so caching logic works
    cache_dir = os.path.join(os.path.dirname(__file__), 'books', 'cache')
    os.makedirs(cache_dir, exist_ok=True)

    filename = secure_filename(file.filename)
    unique_name = f"{int(time.time())}_{filename}"
    filepath = os.path.join(cache_dir, unique_name)
    file.save(filepath)

    extracted_text = read_pdf_text(filepath)
    if extracted_text is None:
        return jsonify({"error": "Failed to extract text from the uploaded file"}), 500

    return jsonify({
        "message": "File processed successfully",
        "filename": filename,
        "cached_path": filepath + ".txt",
        "text": extracted_text
    }), 200

@app.route('/api/cleanup-upload', methods=['POST'])
@require_auth
def cleanup_upload():
    """Delete uploaded files from the cache folder"""
    data = request.json
    cached_path = data.get('cached_path')
    
    if not cached_path:
        return jsonify({"error": "No path provided"}), 400
    
    # Security: ensure the path is within the cache directory
    cache_dir = os.path.join(os.path.dirname(__file__), 'books', 'cache')
    cache_dir = os.path.abspath(cache_dir)
    abs_path = os.path.abspath(cached_path)
    
    if not abs_path.startswith(cache_dir):
        return jsonify({"error": "Invalid path"}), 400
    
    try:
        # Delete the original uploaded file if it exists
        original_file = cached_path.rstrip('.txt')
        if os.path.exists(original_file):
            os.remove(original_file)
        
        # Delete the cached .txt file
        if os.path.exists(cached_path):
            os.remove(cached_path)
        
        return jsonify({"success": True}), 200
    except Exception as e:
        print(f"Cleanup error: {e}")
        return jsonify({"error": "Failed to cleanup files"}), 500

# --- NEW ENDPOINTS FOR CHAT HISTORY ---

@app.route('/api/sessions', methods=['GET'])
@require_auth
def get_sessions():
    user_id = get_user_from_session()
    db = SessionLocal()
    sessions = db.query(ChatSession).filter(ChatSession.user_id == user_id).order_by(ChatSession.created_at.desc()).all()
    session_list = [{"id": s.id, "title": s.title} for s in sessions]
    db.close()
    return jsonify(session_list)

@app.route('/api/sessions/<int:session_id>', methods=['GET'])
@require_auth
def get_session_data(session_id):
    user_id = get_user_from_session()
    db = SessionLocal()
    session_info = db.query(ChatSession).filter(
        ChatSession.id == session_id,
        ChatSession.user_id == user_id
    ).first()
    if not session_info:
        db.close()
        return jsonify({"error": "Session not found"}), 404
        
    messages = db.query(ChatMessage).filter(ChatMessage.session_id == session_id).order_by(ChatMessage.created_at).all()
    msg_list = [{"sender": m.sender, "text": m.message} for m in messages]
    
    response_data = {
        "class_level": session_info.class_level,
        "subject": session_info.subject,
        "messages": msg_list
    }
    db.close()
    return jsonify(response_data)

# --- UPDATED CHAT ROUTE ---

@app.route('/api/chat', methods=['POST'])
@require_auth
def chat():
    user_id = get_user_from_session()
    data = request.json
    user_msg = data.get('message')
    class_id = data.get('class_level')
    subject = data.get('subject')
    session_id = data.get('session_id') # Might be None for a new chat

    db = SessionLocal()

    # 1. Handle Session Creation
    if not session_id:
        title = f"{subject.replace('-', ' ').title()} (Class {class_id})"
        new_session = ChatSession(user_id=user_id, title=title, class_level=class_id, subject=subject)
        db.add(new_session)
        db.commit()
        db.refresh(new_session)
        session_id = new_session.id

    # 2. Verify user owns this session (if it exists)
    if session_id:
        session_info = db.query(ChatSession).filter(ChatSession.id == session_id).first()
        if not session_info or session_info.user_id != user_id:
            db.close()
            return jsonify({"error": "Unauthorized access to session"}), 403

    # 3. Save User Message
    user_message_record = ChatMessage(session_id=session_id, sender="user", message=user_msg)
    db.add(user_message_record)
    db.commit()

    # 4. Determine which context to use (uploaded file OR textbook)
    uploaded_text = data.get('uploaded_text')
    
    if uploaded_text:
        # Use ONLY the uploaded file content
        combined_context = uploaded_text
    else:
        # Use textbook content (original behavior)
        record = db.query(Textbook).filter(Textbook.class_level == class_id, Textbook.book == subject).first()
        if not record:
            db.close()
            return jsonify({"reply": "Textbook not found in database.", "session_id": session_id})

        pdf_text = read_pdf_text(record.filepath)
        if not pdf_text:
            db.close()
            return jsonify({"reply": "Could not read the PDF file.", "session_id": session_id})
        
        combined_context = pdf_text

    # 5. Retrieve Past Conversation History (Last 10 messages for context)
    past_messages = db.query(ChatMessage).filter(ChatMessage.session_id == session_id).order_by(ChatMessage.created_at).all()
    history_text = "\n".join([f"{m.sender.capitalize()}: {m.message}" for m in past_messages[-10:]])

    db.close()

    # 6. Compress text with ScaleDown
    try:
        compression_stats = None
        url = "https://api.scaledown.xyz/compress/raw/"
        headers = {'x-api-key': os.getenv("SCALEDOWN_API_KEY"), 'Content-Type': 'application/json'}
        compressed_response = requests.post(
            url, headers=headers,
            json={"context": combined_context, "prompt": user_msg, "model": "gemini-2.5-flash", "scaledown": {"rate": "auto"}}
        )
        compressed_response.raise_for_status()
        
        # Save the full API response JSON
        sd_data = compressed_response.json() 
        
        # Extract the context for Gemini
        compressed_context = sd_data['results']['compressed_prompt']
        print(sd_data)
        # Build the stats payload to send to the frontend
        res = sd_data.get('results', {})
        compression_stats = {
            "original_tokens": res.get("original_prompt_tokens", 0),
            "compressed_tokens": res.get("compressed_prompt_tokens", 0),
            "ratio": round(100-res.get("compression_ratio", 0) * 100, 1),
            "latency": sd_data.get("latency_ms", 0)
        }

    except Exception as e:
        print(f"ScaleDown failed: {e}")
        compressed_context = combined_context[:10000]

    # 7. Ask Gemini
    final_prompt = f"""
    System:you are a patient encourageing tutor for indian high school students.
    if any case you can not find any context then you can answer with your own but never mention that the text is not exist in the provided textbook content.
    never disappoint the user by saying that sorry;
     Explain concept clearly using simple language and everyday examples.
     Answer only from the provided textbook context.try your best to answer from the provided textbook context.
     remember explanation sholud be very very simple words.
     sometimes motivate the user;

     the context is:{compressed_context}
    
    Chat History:
    {history_text}
    """

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=final_prompt
        )
        bot_reply = response.text
    except Exception as e:
        print(f"Gemini failed: {e}")
        bot_reply = "My systems are currently experiencing a hiccup. Please try asking again."

    # 8. Save Bot Message
    db = SessionLocal()
    bot_message_record = ChatMessage(session_id=session_id, sender="bot", message=bot_reply)
    db.add(bot_message_record)
    db.commit()
    db.close()

    # Modify the return statement to include the stats
    return jsonify({
        "reply": bot_reply, 
        "session_id": session_id,
        "stats": compression_stats
    })

@app.route('/api/sessions/<int:session_id>', methods=['DELETE'])
@require_auth
def delete_session(session_id):
    user_id = get_user_from_session()
    db = SessionLocal()
    session_to_delete = db.query(ChatSession).filter(
        ChatSession.id == session_id,
        ChatSession.user_id == user_id
    ).first()
    
    if not session_to_delete:
        db.close()
        return jsonify({"error": "Session not found"}), 404
        
    db.delete(session_to_delete)
    db.commit()
    db.close()
    return jsonify({"success": True})

if __name__ == '__main__':
    app.run(debug=True, port=5000)