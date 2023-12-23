import datetime
from app import app, db
from app.models import Interview, InterviewStatus


datetime_format = '%Y-%m-%dT%H:%M:%S.%f'


with app.app_context():
    interviews = [
        Interview(
            interviewee_name='Meowing Cat',
            interviewer_name='Cat Meows',
            interview_datetime=datetime.datetime.strptime('2024-01-01T0:0:0.0', datetime_format),
            interview_duration_min=60,
            status=InterviewStatus.SCHEDULED.serialize(),
            created_at=datetime.datetime.strptime('2023-12-01T0:0:0.0', datetime_format),
            updated_at=datetime.datetime.strptime('2023-12-19T0:0:0.0', datetime_format)
        ),
        Interview(
            interviewee_name='Meower Horse',
            interviewer_name='Horse Meows',
            interview_datetime=datetime.datetime.strptime('2024-01-02T0:0:0.0', datetime_format),
            interview_duration_min=45,
            status=InterviewStatus.SCHEDULED.serialize(),
            created_at=datetime.datetime.strptime('2023-12-2T0:0:0.0', datetime_format),
            updated_at=datetime.datetime.strptime('2023-12-18T0:0:0.0', datetime_format)
        ),
    ]

    db.session.add_all(interviews)
    db.session.commit()

print("Database seeded with sample data.")
