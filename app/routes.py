from flask_restful import Resource, reqparse
from app import api, db
from app.models import Interview


parser = reqparse.RequestParser()
parser.add_argument('interviewee_name', type=str, required=True, help='Name of the interviewee')
parser.add_argument('interview_date', type=str, required=True, help='Date of the interview')
parser.add_argument('interview_duration', type=str, required=True, help='Duration of the interview')


class InterviewResource(Resource):
    def get(self, interview_id):
        interview = Interview.query.get_or_404(interview_id)
        return {'interviewee_name': interview.interviewee_name,
                'interview_date': interview.interview_date,
                'interview_duration': interview.interview_duration}

    def put(self, interview_id):
        args = parser.parse_args()
        interview = Interview.query.get_or_404(interview_id)
        interview.interviewee_name = args['interviewee_name']
        interview.interview_date = args['interview_date']
        interview.interview_duration = args['interview_duration']
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
        return [{'interviewee_name': interview.interviewee_name,
                 'interview_date': interview.interview_date,
                 'interview_duration': interview.interview_duration} for interview in interviews]

    def post(self):
        args = parser.parse_args()
        interview = Interview(interviewee_name=args['interviewee_name'],
                              interview_date=args['interview_date'],
                              interview_duration=args['interview_duration'])
        db.session.add(interview)
        db.session.commit()
        return {'message': 'Interview created successfully'}


api.add_resource(InterviewListResource, '/interviews')
api.add_resource(InterviewResource, '/interviews/<int:interview_id>')
