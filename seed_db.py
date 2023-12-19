import datetime

from app import app, db
from app.models import Interview, InterviewStatus

datetime_format = '%Y-%m-%d'


with app.app_context():
    interviews = [
        Interview(
            interviewee_name='Meowing Cat',
            interviewer_name='Cat Meows',
            interview_datetime=datetime.datetime.strptime('2024-01-01', datetime_format),
            interview_duration_min=60,
            status=InterviewStatus.SCHEDULED,
            created_at=datetime.datetime.strptime('2023-12-01', datetime_format),
            updated_at=datetime.datetime.strptime('2023-12-19', datetime_format)
        ),
        Interview(
            interviewee_name='Meower Horse',
            interviewer_name='Horse Meows',
            interview_datetime=datetime.datetime.strptime('2024-01-02', datetime_format),
            interview_duration_min=45,
            status=InterviewStatus.SCHEDULED,
            created_at=datetime.datetime.strptime('2023-12-2', datetime_format),
            updated_at=datetime.datetime.strptime('2023-12-18', datetime_format)
        ),
    ]

    db.session.add_all(interviews)
    db.session.commit()

print("Database seeded with sample data.")
