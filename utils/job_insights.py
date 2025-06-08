# utils/job_insights.py

job_insights_data = {
    "Data Scientist": {
        "description": "Analyze and interpret complex data to drive business decisions.",
        "top_skills": ["Python", "Machine Learning", "Statistics", "Data Visualization", "SQL"],
        "average_salary": "85,000 - 120,000 USD",
        "growth_outlook": "High demand with increasing opportunities."
    },
    "Web Developer": {
        "description": "Build and maintain websites and web applications.",
        "top_skills": ["HTML", "CSS", "JavaScript", "React.js", "Node.js"],
        "average_salary": "60,000 - 90,000 USD",
        "growth_outlook": "Steady demand, especially for frontend and full-stack roles."
    },
    "AI Engineer": {
        "description": "Design and develop AI models and algorithms to solve business problems.",
        "top_skills": ["Python", "Deep Learning", "TensorFlow", "PyTorch", "Mathematics"],
        "average_salary": "100,000 - 140,000 USD",
        "growth_outlook": "Rapid growth with emerging AI technologies."
    },
    "Cybersecurity Analyst": {
        "description": "Protect systems and networks from cyber threats and attacks.",
        "top_skills": ["Network Security", "Ethical Hacking", "SIEM Tools", "Incident Response", "Firewalls"],
        "average_salary": "70,000 - 110,000 USD",
        "growth_outlook": "Increasing importance due to rising cyber threats."
    },
    "DevOps Engineer": {
        "description": "Bridge the gap between development and operations for faster delivery.",
        "top_skills": ["Docker", "Kubernetes", "CI/CD", "AWS", "Linux"],
        "average_salary": "80,000 - 120,000 USD",
        "growth_outlook": "Strong demand with growing cloud adoption."
    },
    "Mobile App Developer": {
        "description": "Create mobile applications for Android and iOS platforms.",
        "top_skills": ["Flutter", "React Native", "Kotlin", "Swift", "Java"],
        "average_salary": "65,000 - 100,000 USD",
        "growth_outlook": "Steady growth due to increasing mobile usage."
    },
    "Cloud Engineer": {
        "description": "Design, develop and manage cloud infrastructure.",
        "top_skills": ["AWS", "Azure", "Google Cloud", "Terraform", "Networking"],
        "average_salary": "90,000 - 130,000 USD",
        "growth_outlook": "High demand as businesses migrate to cloud."
    },
    "Data Analyst": {
        "description": "Interpret data and provide actionable insights to stakeholders.",
        "top_skills": ["SQL", "Excel", "Tableau", "Power BI", "Data Cleaning"],
        "average_salary": "55,000 - 80,000 USD",
        "growth_outlook": "Consistent demand across industries."
    }
}

def get_job_insights(role=None):
    """
    Returns job insights for the given role.
    If no role is provided or role not found, returns general insights.
    """
    if role and role in job_insights_data:
        return {
            "role": role,
            "insights": job_insights_data[role]
        }
    else:
        return {
            "message": "Role not found or not specified. Please provide a valid role.",
            "available_roles": list(job_insights_data.keys())
        }
