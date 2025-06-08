
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

from flask_cors import CORS

from flask import request, jsonify
import fitz  # PyMuPDF
import io 
from docx import Document

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024  # 5MB





# Your routes and other app setup below...


# Utils imports
#from utils.curriculum_analysis import extract_topics, compare_with_industry_standards
#from utils.skill_gap import analyze_skills
from utils.courses import recommend_courses
from utils.job_insights import get_job_insights
from utils.overview import get_user_overview


app.secret_key = 'your_secret_key_here'  # Replace with a strong secret key in production
CORS(app)

# DB Connection and init
def get_db_connection():
    conn = sqlite3.connect('careercoach.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Routes
@app.route('/')
def home():
    return render_template('home.html')


@app.route('/auth')
def auth():
    return render_template('auth.html')

@app.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')

    if not email or not password:
        return "Invalid credentials. Please try again.", 400

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
    user = cursor.fetchone()
    conn.close()

    if user and check_password_hash(user['password'], password):
        session['user_id'] = user['id']
        session['user_name'] = user['name']
        session['user_email'] = user['email']
        return redirect(url_for('dashboard_overview'))
    else:
        return "Invalid credentials. Please try again.", 400

@app.route('/register', methods=['POST'])
def register():
    name = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password')
    confirm = request.form.get('confirm_password')

    if not (name and email and password and confirm):
        return "All fields are required!", 400

    if password != confirm:
        return "Passwords do not match!", 400

    hashed_password = generate_password_hash(password)  # uses default 'pbkdf2:sha256'


    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('INSERT INTO users (name, email, password) VALUES (?, ?, ?)',
                       (name, email, hashed_password))
        conn.commit()
    except sqlite3.IntegrityError:
        conn.close()
        return "Email already registered!", 400
    conn.close()

    # Automatically log in the user after registration
    session['user_name'] = name
    session['user_email'] = email

    return redirect(url_for('dashboard_overview'))

@app.route('/dashboard')
def dashboard_overview():
    if 'user_email' not in session:
        return redirect(url_for('auth'))

    name = session.get('user_name', 'User')
    return render_template('dashboard.html', name=name)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

# Curriculum Analysis
@app.route('/analyze_curriculum', methods=['POST'])
def analyze_curriculum():
    try:
        data = request.form.get('manual_input', '').strip()

        if not data:
            file = request.files.get('file')
            if file and file.filename:
                contents = file.read()
                full_text = ""

                if file.content_type == "application/pdf":
                    pdf_stream = io.BytesIO(contents)
                    doc = fitz.open(stream=pdf_stream, filetype="pdf")
                    for page in doc:
                        full_text += page.get_text()

                elif file.content_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                    docx_stream = io.BytesIO(contents)
                    document = Document(docx_stream)
                    for para in document.paragraphs:
                        full_text += para.text + "\n"

                elif file.content_type == "text/plain":
                    full_text = contents.decode('utf-8')

                else:
                    return jsonify({"message": "Unsupported file type"}), 400
            else:
                return jsonify({"message": "No input provided."}), 400
        else:
            full_text = data

        curriculum_topics = [
            # Programming Fundamentals
            "C Programming", "C++", "Python", "Java", "Object-Oriented Programming",
            # Data & Algorithms
            "Data Structures", "Algorithms", "Design and Analysis of Algorithms",
            # Web Technologies
            "Web Development", "HTML", "CSS", "JavaScript", "React", "Node.js",
            # Databases
            "Database Management Systems", "SQL", "NoSQL", "MongoDB",
            # OS & System
            "Operating Systems", "Shell Scripting", "System Programming",
            # Networks & Security
            "Computer Networks", "Network Security", "Cyber Security", "Cryptography",
            # Software Engineering
            "Software Engineering", "Software Testing", "Agile Methodologies", "DevOps",
            # Cloud & Deployment
            "Cloud Computing", "AWS", "Azure", "Docker", "Kubernetes",
            # ML & AI
            "Machine Learning", "Artificial Intelligence", "Data Science", "Data Visualization", "Pandas", "NumPy", "Matplotlib",
            # Architecture
            "Computer Organization", "Computer Architecture", "Microprocessors",
            # Math & Theory
            "Discrete Mathematics", "Linear Algebra", "Probability and Statistics", "Theory of Computation", "Compiler Design",
            # Miscellaneous
            "Mobile App Development", "Human Computer Interaction", "Information Security", "Project Management", "Ethical Hacking", "Blockchain Technology", "Internet of Things", "Big Data"
        ]

        text_lower = full_text.lower()
        covered = [topic for topic in curriculum_topics if topic.lower() in text_lower]
        not_covered = [topic for topic in curriculum_topics if topic.lower() not in text_lower]

        return jsonify({
            "covered_topics": covered,
            "not_covered_topics": not_covered
        })

    except Exception as e:
        return jsonify({"message": f"Error: {str(e)}"}), 500



# Skill Gap

@app.route('/skill_gap', methods=['POST'])
def skill_gap():
    try:
        data = request.get_json()
        print("📥 Received from frontend:", data)

        if not data:
            return jsonify({'error': 'No data received'}), 400

        user_skills = data.get('skills', [])
        role = data.get('role', '').lower().strip()

        # sample data
        skills_required = {
             "frontend developer": ["HTML", "CSS", "JavaScript", "React", "Responsive Design", "Version Control", "API Integration"],
            "backend developer": ["Python", "Node.js", "SQL", "MongoDB", "REST APIs", "Authentication", "Docker"],
            "data analyst": ["Python", "Pandas", "NumPy", "SQL", "Data Visualization", "Excel", "Statistics"],
            "machine learning engineer": ["Python", "Machine Learning", "Data Preprocessing", "Pandas", "NumPy", "Scikit-learn", "Model Evaluation"],
            "full stack developer": ["HTML", "CSS", "JavaScript", "React", "Node.js", "SQL", "MongoDB", "APIs", "Authentication"],
            "cloud engineer": ["AWS", "Azure", "Docker", "Kubernetes", "Linux", "CI/CD", "Networking"],
            "cybersecurity analyst": ["Network Security", "Cyber Security", "Cryptography", "Firewalls", "Linux", "Ethical Hacking"],


        }

        if role not in skills_required:
            return jsonify({'error': f'Unknown role: {role}'}), 400

        required_skills = skills_required[role]
        missing = [skill for skill in required_skills if skill not in user_skills]

        return jsonify({'missing_skills': missing})
    except Exception as e:
        return jsonify({'error': str(e)}), 500





# Course Recommendation
@app.route('/recommend_courses', methods=['POST'])
def recommend_courses():
    try:
        data = request.get_json()
        skills_needed = data.get('skills', [])

        if not skills_needed:
            return jsonify({"error": "No skills provided"}), 400

        # Dummy course data with tags
        courses = [
            {
                "title": "Python for Everybody",
                "description": "Learn Python basics and advance to data structures and web access.",
                "platform": "Coursera",
                "link": "https://www.coursera.org/specializations/python",
                "level": "Beginner",
                "tags": ["Python"]
            },
            {
                "title": "Deep Learning Specialization",
                "description": "Master deep learning, neural networks, and advanced AI models.",
                "platform": "Coursera",
                "link": "https://www.coursera.org/specializations/deep-learning",
                "level": "Advanced",
                "tags": ["Deep Learning", "AI", "Machine Learning"]
            },
            {
                "title": "Responsive Web Design",
                "description": "Build responsive websites using HTML, CSS, and modern design techniques.",
                "platform": "freeCodeCamp",
                "link": "https://www.freecodecamp.org/learn/responsive-web-design/",
                "level": "Beginner",
                "tags": ["HTML", "CSS", "Web Design"]
            },
            {
                "title": "DevOps with Docker & Kubernetes",
                "description": "Get hands-on experience with containerization and orchestration tools.",
                "platform": "Udemy",
                "link": "https://www.udemy.com/course/docker-and-kubernetes-the-complete-guide/",
                "level": "Intermediate",
                "tags": ["DevOps", "Docker", "Kubernetes"]
            },
            {
                "title": "Data Science Professional Certificate",
                "description": "Comprehensive data science training including Python and machine learning.",
                "platform": "edX",
                "link": "https://www.edx.org/professional-certificate/ibm-data-science",
                "level": "Intermediate",
                "tags": ["Data Science", "Python", "Machine Learning"]
            },
            {
                "title": "AWS Certified Solutions Architect",
                "description": "Prepare for AWS certification with cloud architecture fundamentals.",
                "platform": "AWS Training",
                "link": "https://aws.amazon.com/certification/certified-solutions-architect-associate/",
                "level": "Advanced",
                "tags": ["Cloud", "AWS", "Architecture"]
            },
            {
                "title": "Introduction to Cybersecurity",
                "description": "Learn fundamentals of cybersecurity and how to protect digital assets.",
                "platform": "Cisco Networking Academy",
                "link": "https://www.netacad.com/courses/cybersecurity/intro-cybersecurity",
                "level": "Beginner",
                "tags": ["Cybersecurity", "Security"]
            },
            {
                "title": "Full-Stack Web Development",
                "description": "Become a full-stack developer with React, Node.js, and databases.",
                "platform": "Coursera",
                "link": "https://www.coursera.org/specializations/full-stack-react",
                "level": "Intermediate",
                "tags": ["Full-Stack", "React", "Node.js", "JavaScript"]
            }
        ]

        # Match any of the skills with course tags
        matched_courses = []
        for course in courses:
            if any(skill.lower() in [tag.lower() for tag in course["tags"]] for skill in skills_needed):
                matched_courses.append(course)

        return jsonify({
            "skills_provided": skills_needed,
            "matched_courses_count": len(matched_courses),
            "recommended_courses": matched_courses
        })

    except Exception as e:
        return jsonify({"error": f"Something went wrong: {str(e)}"}), 500


# User Overview
@app.route('/user_overview', methods=['GET'])
def user_overview():
    email = session.get('user_email')
    if not email:
        return jsonify({'error': 'User not logged in'}), 403

    overview = get_user_overview(email)
    return jsonify(overview)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)

    
