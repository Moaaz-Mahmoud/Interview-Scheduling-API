from app import app, db
from app.models import Interview

with app.app_context():
    interviews = [
        Interview(interviewee_name='Meowing Cat', interview_date='2024-01-01', interview_duration='1 hour'),
        Interview(interviewee_name='Meower Horse', interview_date='2024-01-02', interview_duration='45 minutes'),
    ]

    db.session.add_all(interviews)
    db.session.commit()

print("Database seeded with sample data.")
