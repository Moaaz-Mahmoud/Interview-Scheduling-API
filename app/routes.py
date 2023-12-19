from flask_restful import Resource, reqparse
from app import api, db
from app.models import Interview
from datetime import datetime


parser = reqparse.RequestParser()
parser.add_argument('interviewee_name', type=str, required=True, help='Name of the interviewee')
parser.add_argument('interviewer_name', type=str, required=True, help='Name of the interviewer')
parser.add_argument('interview_datetime', type=str, required=True, help='Datetime of the interview (YYYY-MM-DD HH:MM:SS)')
parser.add_argument('interview_duration_min', type=str, required=True, help='Duration of the interview')


class InterviewResource(Resource):
    def get(self, interview_id):
        interview = Interview.query.get_or_404(interview_id)
        return {
            'id': interview.id,
            'interviewee_name': interview.interviewee_name,
            'interviewer_name': interview.interviewer_name,
            'interview_datetime': interview.interview_datetime.isoformat(),
            'interview_duration_min': interview.interview_duration_min,
            'status': interview.status,
            'created_at': interview.created_at.isoformat(),
            'updated_at': interview.updated_at.isoformat()
        }

    def put(self, interview_id):
        args = parser.parse_args()
        interview = Interview.query.get_or_404(interview_id)

        interview.interviewee_name = args['interviewee_name']
        interview.interviewer_name = args['interviewer_name']
        interview.interview_datetime = datetime.strptime(args['interview_datetime'], '%Y-%m-%d %H:%M:%S')
        interview.interview_duration_min = args['interview_duration_min']
        interview.status = args['status']

        interview.updated_at = datetime.utcnow()

        db.session.commit()
        return {'message': 'Interview updated successfully'}

    def delete(self, interview_id):
        interview = Interview.query.get_or_404(interview_id)
        db.session.delete(interview)
        db.session.commit()
        return {'message': 'Interview deleted successfully'}


class InterviewListResource(Resource):
    def get(self):
        interviews = Interview.query.all()
        return [
            {
                'interviewee_name': interview.interviewee_name,
                'interview_date': interview.interview_date,
                'interview_datetime': interview.interview_datetime.isoformat(),
                'interview_duration_min': interview.interview_duration_min,
                'status': interview.status,
                'created_at': interview.created_at.isoformat(),
                'updated_at': interview.updated_at.isoformat()
            } for interview in interviews
        ]

    def post(self):
        args = parser.parse_args()
        interview = Interview(interviewee_name=args['interviewee_name'],
                              interview_datetime=args['interview_date'],
                              interviewer_name=args['interviewer_name'],
                              interview_duration_min=args['interview_duration_min'],
                              status=args['status'],
                              created_at=args['created_at'],
                              updated_at=args['updated_at'],)
        db.session.add(interview)
        db.session.commit()
        return {'message': 'Interview created successfully'}


api.add_resource(InterviewListResource, '/interviews')
api.add_resource(InterviewResource, '/interviews/<int:interview_id>')
