# utils/recommender.py

import json
from utils.azure_extract import extract_skills_from_text

# Load mock job roles
def load_job_roles():
    with open('mock_data/job_roles.json', 'r') as file:
        return json.load(file)

# Compare student skills with job role requirements
def analyze_resume_against_role(resume_text, target_role):
    extracted_skills = extract_skills_from_text(resume_text)
    
    job_roles = load_job_roles()
    role_data = job_roles.get(target_role)
    
    if not role_data:
        return {
            "error": "Role not found in database."
        }

    required_skills = role_data['inDemandSkills']
    matched = list(set(extracted_skills) & set(required_skills))
    missing = list(set(required_skills) - set(extracted_skills))

    return {
        "targetRole": target_role,
        "extractedSkills": extracted_skills,
        "requiredSkills": required_skills,
        "matchedSkills": matched,
        "missingSkills": missing,
        "avgSalary": role_data['avgSalary'],
        "jobGrowth": role_data['jobGrowth'],
        "topCompanies": role_data['topCompanies']
    }
