from app import db

class Interview(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    interviewee_name = db.Column(db.String(255), nullable=False)
    interview_date = db.Column(db.String(50), nullable=False)
    interview_duration = db.Column(db.String(50), nullable=False)
