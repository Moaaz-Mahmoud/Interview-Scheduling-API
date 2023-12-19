from datetime import datetime
from sqlalchemy.orm import validates
from app import db
from enum import Enum


class InterviewStatus(Enum):
    SCHEDULED = 'scheduled'
    ONGOING = 'ongoing'
    CANCELED = 'canceled'
    COMPLETED = 'completed'


class Interview(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    interviewee_name = db.Column(db.String(255), nullable=False)
    interviewer_name = db.Column(db.String(255), nullable=False)

    interview_datetime = db.Column(db.DateTime, nullable=False)
    interview_duration_min = db.Column(db.Integer, nullable=False)

    status = db.Column(db.Enum(InterviewStatus), default=InterviewStatus.SCHEDULED, nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    @validates('interview_duration_min')
    def validate_interview_duration(self, key, value):
        if value <= 0:
            raise ValueError("Interview duration must be greater than 0.")
        return value

