# utils/overview.py

def get_user_overview(user_id=None):
    """
    Simulate fetching a summary overview for a user:
    - Number of completed courses
    - Number of pending skills to learn
    - Recent job recommendations count
    - Skill gap summary
    - etc.
    
    Args:
        user_id (str or int): Optional user identifier
    
    Returns:
        dict: Overview summary data
    """

    # Dummy data - replace with real data fetching and calculations
    overview_data = {
        "user_id": user_id,
        "completed_courses": 5,
        "pending_courses": 3,
        "skill_gaps": ["Machine Learning", "Docker", "Kubernetes"],
        "recent_job_recommendations": 8,
        "last_login": "2025-06-01T14:25:00Z",
        "profile_completion": 75,  # in percentage
        "next_recommended_course": {
            "title": "Introduction to Kubernetes",
            "provider": "Coursera",
            "url": "https://www.coursera.org/learn/kubernetes"
        }
    }

    return overview_data
