# utils/courses.py

def recommend_courses(user_skills):
    """
    Recommend courses based on user's current skills.
    Suggest courses for skills that user doesn't have but are in demand.
    """
    # Example course catalog: skill -> course details
    course_catalog = {
        "Python": {"title": "Python for Everybody", "provider": "Coursera", "url": "https://www.coursera.org/specializations/python"},
        "SQL": {"title": "SQL Fundamentals", "provider": "Udemy", "url": "https://www.udemy.com/course/sql-fundamentals/"},
        "Tableau": {"title": "Data Visualization with Tableau", "provider": "edX", "url": "https://www.edx.org/course/data-visualization-with-tableau"},
        "Machine Learning": {"title": "Machine Learning by Andrew Ng", "provider": "Coursera", "url": "https://www.coursera.org/learn/machine-learning"},
        "AWS": {"title": "AWS Certified Solutions Architect", "provider": "AWS", "url": "https://aws.amazon.com/certification/certified-solutions-architect-associate/"},
        "Git": {"title": "Version Control with Git", "provider": "Udacity", "url": "https://www.udacity.com/course/version-control-with-git--ud123"},
        "Docker": {"title": "Docker for Beginners", "provider": "Pluralsight", "url": "https://www.pluralsight.com/courses/docker"},
        "JavaScript": {"title": "JavaScript Basics", "provider": "Codecademy", "url": "https://www.codecademy.com/learn/introduction-to-javascript"},
        "React": {"title": "React - The Complete Guide", "provider": "Udemy", "url": "https://www.udemy.com/course/react-the-complete-guide-incl-redux/"},
        "Data Structures": {"title": "Data Structures and Algorithms", "provider": "Coursera", "url": "https://www.coursera.org/specializations/data-structures-algorithms"},
        # Add more skills and courses as needed
    }

    # Normalize user skills (case-insensitive)
    user_skills_lower = set([skill.lower() for skill in user_skills])

    recommendations = []
    for skill, course_info in course_catalog.items():
        if skill.lower() not in user_skills_lower:
            recommendations.append({
                "skill": skill,
                "course_title": course_info["title"],
                "provider": course_info["provider"],
                "url": course_info["url"]
            })

    # Optionally, sort recommendations alphabetically by skill
    recommendations.sort(key=lambda x: x["skill"])

    return {
        "recommended_courses": recommendations,
        "total_recommendations": len(recommendations)
    }
