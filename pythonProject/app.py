import streamlit as st
from resume_parser import extract_text, extract_skills
from job_matcher import calculate_match
from db import insert_resume
from report_generator import generate_report
import pandas as pd
import mysql.connector
import re
import spacy
from nltk.corpus import stopwords

# Load SpaCy's language model for lemmatization
nlp = spacy.load("en_core_web_sm")

# Define a list of common programming languages, libraries, and tools to match
tech_keywords = [
    "python", "java", "c++", "c#", "javascript", "ruby", "sql", "html", "css", "react", "angular", "vue",
    "node.js", "express", "django", "flask", "tensorflow", "keras", "pytorch", "scikit-learn", "pandas",
    "numpy", "matplotlib", "seaborn", "tableau", "powerbi", "spark", "hadoop", "docker", "kubernetes",
    "aws", "azure", "gcp", "google cloud", "git", "github", "jenkins", "ci/cd", "elasticsearch", "kafka",
    "mongodb", "postgresql", "mysql", "redis", "apache", "nginx", "graphql", "restful api", "flask",
    "rabbitmq", "tensorflow", "scrapy", "bash", "gitlab", "flutter", "swift", "objective-c", "protobuf",
    "vhdl", "scala", "latex", "tableau", "matplotlib", "seaborn", "mocking", "docker", "kubernetes"
]

# Remove common stopwords (non-technical words) to prevent matching false positives
stop_words = set(stopwords.words("english"))


def extract_skills(text):
    """
    Extracts technical skills from a given text using regex and NLP.
    This function uses regex to find tech terms and applies NLP lemmatization to ensure accurate matches.
    """
    # Preprocess the text using SpaCy NLP
    doc = nlp(text.lower())  # Convert text to lowercase for uniformity

    # Filter out non-technical words using stopwords and lemmatization
    filtered_tokens = [token.lemma_ for token in doc if
                       token.text not in stop_words and token.pos_ in ['NOUN', 'PROPN']]

    # Create a list of extracted skills based on the predefined tech_keywords list
    matched_skills = []
    for word in filtered_tokens:
        # Check if the word is in the tech_keywords list
        if word in tech_keywords:
            matched_skills.append(word)

    # Return unique skills (no duplicates)
    return list(set(matched_skills))


# --- Predefined Job Descriptions ---
# --- Expanded Job Descriptions with Comprehensive Skillsets ---

job_descriptions = {
    "Data Scientist": """
    Job Description:
    We are seeking a Data Scientist with experience in analyzing complex datasets, applying machine learning techniques, and creating data-driven solutions for business problems.

    Required Skills:
    - Python, R, SQL
    - Machine Learning (scikit-learn, XGBoost, LightGBM)
    - Deep Learning (TensorFlow, Keras, PyTorch)
    - Data Analysis (Pandas, Numpy)
    - Data Visualization (Matplotlib, Seaborn, Tableau, Power BI)
    - Big Data (Hadoop, Spark)
    - Statistical Analysis
    - Natural Language Processing (spaCy, NLTK)
    - Cloud platforms (AWS, GCP, Azure)
    - Version Control (Git, GitHub)
    - Data Cleaning & Preprocessing
    - Feature Engineering
    - Model Evaluation (Cross-Validation, Hyperparameter Tuning)
    """,

    "Frontend Developer": """
    Job Description:
    A Frontend Developer is responsible for creating and maintaining visually appealing and user-friendly web applications.

    Required Skills:
    - HTML, CSS, JavaScript
    - React.js, Redux
    - RESTful APIs, AJAX
    - Responsive Web Design (Bootstrap, Media Queries)
    - CSS Preprocessors (SASS, LESS)
    - Version Control (Git, GitHub)
    - Cross-Browser Compatibility
    - Webpack, Babel
    - Agile/Scrum Development
    - Unit Testing (Jest, Mocha, Enzyme)
    - UX/UI Principles
    - Web Performance Optimization
    - TypeScript
    - Node.js (for Full-Stack Development)
    """,

    "Machine Learning Engineer": """
    Job Description:
    We are looking for a Machine Learning Engineer to help design and implement machine learning models in production environments.

    Required Skills:
    - Python, Java, C++
    - Machine Learning Algorithms (Supervised, Unsupervised, Reinforcement Learning)
    - Deep Learning (TensorFlow, Keras, PyTorch)
    - Model Deployment (Flask, FastAPI, Docker, Kubernetes)
    - Data Preprocessing (Pandas, NumPy)
    - SQL & NoSQL Databases
    - Cloud Platforms (AWS, Azure, GCP)
    - Big Data Technologies (Spark, Hadoop)
    - CI/CD for ML (Jenkins, GitLab)
    - Version Control (Git, GitHub)
    - Model Monitoring & Maintenance
    - NLP (spaCy, BERT, GPT)
    """,

    "Backend Developer": """
    Job Description:
    A Backend Developer is responsible for building server-side web applications and working with databases.

    Required Skills:
    - Python, Java, Node.js, C#
    - Backend Frameworks (Django, Flask, Express.js, Spring Boot)
    - RESTful APIs, GraphQL
    - Database Management (SQL, PostgreSQL, MongoDB, Redis)
    - Server Management (Linux, Apache, Nginx)
    - Cloud Platforms (AWS, GCP, Azure)
    - Docker, Kubernetes
    - Authentication & Authorization (OAuth, JWT)
    - Message Brokers (RabbitMQ, Kafka)
    - Unit Testing & Integration Testing (pytest, Mocha)
    - Version Control (Git, GitHub)
    - Continuous Integration & Deployment (CI/CD)
    - Microservices Architecture
    """,

    "DevOps Engineer": """
    Job Description:
    We are looking for a DevOps Engineer to automate and manage infrastructure, improve deployment pipelines, and ensure continuous delivery.

    Required Skills:
    - Linux/Unix systems administration
    - Cloud Platforms (AWS, Azure, GCP)
    - Docker, Kubernetes
    - CI/CD Tools (Jenkins, GitLab CI)
    - Infrastructure as Code (Terraform, Ansible)
    - Version Control (Git, GitHub)
    - Monitoring (Prometheus, Grafana, Nagios)
    - Scripting (Bash, Python)
    - Networking (TCP/IP, DNS, HTTP)
    - Virtualization (VMware, Docker)
    - Configuration Management (Chef, Puppet)
    - Logging (ELK Stack, Splunk)
    - Automation Tools (Puppet, Chef)
    """,

    "Full Stack Developer": """
    Job Description:
    Full Stack Developer responsible for both the frontend and backend aspects of web development.

    Required Skills:
    - HTML, CSS, JavaScript, React.js, Angular, Vue.js
    - Node.js, Express.js, Django, Flask
    - Databases (MySQL, PostgreSQL, MongoDB)
    - REST APIs, GraphQL
    - Git, GitHub
    - Docker, Kubernetes
    - Authentication (OAuth, JWT, Passport.js)
    - Unit Testing & End-to-End Testing (Jest, Mocha, Cypress)
    - Cloud Platforms (AWS, GCP, Azure)
    - CI/CD pipelines (Jenkins, GitLab CI)
    - Microservices Architecture
    - Agile/Scrum Methodology
    """,

    "Data Engineer": """
    Job Description:
    Data Engineers build systems to collect, manage, and analyze data for decision-making.

    Required Skills:
    - Python, Java, Scala
    - ETL (Extract, Transform, Load)
    - SQL, NoSQL (Hadoop, MongoDB, Cassandra)
    - Big Data (Apache Spark, Kafka, Hive)
    - Data Warehousing (Snowflake, Redshift, BigQuery)
    - Cloud Platforms (AWS, Azure, GCP)
    - Data Pipeline Orchestration (Apache Airflow)
    - Version Control (Git)
    - Containers (Docker, Kubernetes)
    - Apache Kafka, Hadoop
    - Data Modeling
    - Batch Processing & Stream Processing
    """,

    "UX/UI Designer": """
    Job Description:
    We are seeking a UX/UI Designer to create user-centered design solutions for digital products.

    Required Skills:
    - UI/UX Design (Wireframing, Prototyping)
    - Design Tools (Figma, Adobe XD, Sketch)
    - HTML, CSS, JavaScript (for prototyping)
    - User Research & Personas
    - User Testing (A/B Testing, Usability Testing)
    - Responsive Web Design
    - Interaction Design
    - Design Systems
    - Agile/Scrum Environment
    - Accessibility Standards (WCAG)
    - Design Thinking Methodology
    """
}



# --- Streamlit Page Settings ---
st.set_page_config(page_title="Smart Resume Analyzer (Role Based)", layout="wide")
st.title("📄 Smart Resume Analyzer - Role Based")

# --- Resume Upload ---
uploaded_file = st.file_uploader("📤 Upload Resume (PDF)", type="pdf")

# --- Role Input ---
job_role = st.text_input("🎯 Enter the Job Role You Are Applying For (e.g., Data Scientist, Frontend Developer)")

if uploaded_file and job_role:
    text = extract_text(uploaded_file)
    skills = extract_skills(text)

    # Get Job Description based on Role
    selected_jd = job_descriptions.get(job_role.strip(), None)

    if selected_jd:
        job_keywords = extract_skills(selected_jd)

        name = st.text_input("👤 Your Name")
        email = st.text_input("📧 Your Email")

        if st.button("🔍 Analyze Resume"):
            match_score = calculate_match(skills, job_keywords)
            insert_resume(name, email, ", ".join(skills), match_score)

            matched = sorted(list(set(skills).intersection(set(job_keywords))))
            missing = sorted(list(set(job_keywords) - set(skills)))

            st.markdown("## ✅ Matched Skills")
            st.write(", ".join(matched) if matched else "None")

            st.markdown("## ❌ Missing Skills")
            st.write(", ".join(missing) if missing else "None")

            st.markdown("### 💡 Suggestions for Improvement")
            if missing:
                st.info("Consider learning or highlighting these skills: " + ", ".join(missing))
            else:
                st.success("Awesome! You match all the required skills! 🚀")

            # Generate and Download Report
            report_file = generate_report(name, email, matched, missing, match_score, skills)
            with open(report_file, "rb") as file:
                st.download_button(label="📄 Download PDF Report", data=file, file_name=report_file,
                                   mime="application/pdf")

            st.success(f"Match Score: {match_score}% - Stored Successfully!")

    else:
        st.error(
            "🚫 No job description found for this role. Please enter a valid role like 'Data Scientist' or 'Frontend Developer'.")

# --- Admin Dashboard ---
st.sidebar.title("🔐 Admin Dashboard")


def fetch_all_resumes():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="resume_tool"
    )
    df = pd.read_sql("SELECT * FROM resumes", conn)
    conn.close()
    return df


if st.sidebar.checkbox("View All Resumes"):
    st.subheader("📊 Uploaded Resume Data")
    df = fetch_all_resumes()

    name_filter = st.text_input("🔍 Search by Name")
    min_score = st.slider("🎯 Minimum Match Score", 0, 100, 0)

    filtered_df = df[df['match_score'] >= min_score]
    if name_filter:
        filtered_df = filtered_df[filtered_df['name'].str.contains(name_filter, case=False)]

    st.dataframe(filtered_df)
