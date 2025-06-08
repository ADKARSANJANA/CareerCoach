# utils/skill_gap.py

# This module provides a simple skill gap analysis function
# comparing user skills with required skills for different roles.

industry_skills_by_role = {
    'Data Scientist': ['Python', 'Statistics', 'Machine Learning', 'Tableau', 'Data Preprocessing', 'Cloud Basics'],
    'AI Engineer': ['Python', 'Deep Learning', 'TensorFlow', 'PyTorch', 'Mathematics', 'Cloud Basics', 'Computer Vision'],
    'Web Developer': ['HTML', 'CSS', 'JavaScript', 'React.js', 'Node.js', 'APIs', 'Responsive Design'],
    'DevOps Engineer': ['Linux', 'Docker', 'Kubernetes', 'CI/CD', 'AWS', 'Terraform', 'Monitoring Tools'],
    'Cybersecurity Analyst': ['Network Security', 'Ethical Hacking', 'SIEM Tools', 'Firewalls', 'Incident Response', 'Python', 'Cloud Security'],
    'Cloud Architect': ['AWS', 'Azure', 'Google Cloud', 'Networking', 'Security', 'DevOps', 'Serverless'],
    'Data Analyst': ['Excel', 'SQL', 'Python', 'Power BI', 'Tableau', 'Data Visualization', 'Statistics'],
    'Mobile App Developer': ['Java', 'Kotlin', 'Flutter', 'React Native', 'Firebase', 'UI/UX Design', 'APIs']
}

def analyze_skills(user_skills, role):
    """
    Analyze skill gaps for a given user_skills list against the
    industry skills required for the specified role.

    Args:
        user_skills (list): List of user skills (strings).
        role (str): Role name (e.g., 'Data Scientist').

    Returns:
        dict: Analysis containing:
            - required_skills: full list of required skills for role
            - user_skills: user's current skills
            - missing_skills: list of missing skills
            - coverage_percent: percentage of skills user has
    """
    role_skills = industry_skills_by_role.get(role, [])

    user_skills_set = set(skill.lower() for skill in user_skills)
    role_skills_set = set(skill.lower() for skill in role_skills)

    missing_skills = [skill for skill in role_skills if skill.lower() not in user_skills_set]
    covered_skills = [skill for skill in user_skills if skill.lower() in role_skills_set]

    coverage_percent = round((len(covered_skills) / len(role_skills)) * 100, 2) if role_skills else 0.0

    return {
        "required_skills": role_skills,
        "user_skills": user_skills,
        "missing_skills": missing_skills,
        "coverage_percent": coverage_percent
    }
