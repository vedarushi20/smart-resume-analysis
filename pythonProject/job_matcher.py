def calculate_match(resume_skills, job_skills):
    if not job_skills:
        return 0.0  # Prevent division by zero

    match = set(resume_skills).intersection(set(job_skills))
    return round((len(match) / len(job_skills)) * 100, 2)
