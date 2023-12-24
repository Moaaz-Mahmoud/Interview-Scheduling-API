import logging
from flask_restful import Resource, reqparse
from enum import Enum

from werkzeug.exceptions import NotFound

from app import api, db
from app.models import Interview, InterviewStatus
from datetime import datetime
import config


datetime_format = '%Y-%m-%dT%H:%M:%S.%f'

parser = reqparse.RequestParser()
parser.add_argument('interviewee_name', type=str, required=False, help='Name of the interviewee')
parser.add_argument('interviewer_name', type=str, required=False, help='Name of the interviewer')
parser.add_argument('interview_datetime', type=str, required=False,
                    help='Datetime of the interview (YYYY-MM-DD HH:MM:SS)')
parser.add_argument('interview_duration_min', type=int, required=False, help='Duration of the interview')
parser.add_argument('status',
                    # type=db.Enum(InterviewStatus, values_callable=lambda x: [str(status.value)
                    #                                                          for status in InterviewStatus]),
                    type=str,
                    required=False,
                    help='Status of the interview [SCHEDULED, ONGOING, CANCELED, COMPLETED]')
parser.add_argument('created_at', type=str, required=False, help='Creation datetime of the record')
parser.add_argument('updated_at', type=str, required=False, help='Last update datetime of the record')


class InterviewResource(Resource):
    def get(self, interview_id):
        try:
            interview = Interview.query.get_or_404(interview_id)
            return {
                'id': interview.id,
                'interviewee_name': interview.interviewee_name,
                'interviewer_name': interview.interviewer_name,
                'interview_datetime': interview.interview_datetime.isoformat(),
                'interview_duration_min': interview.interview_duration_min,
                'status': interview.status.serialize(),
                'created_at': interview.created_at.isoformat(),
                'updated_at': interview.updated_at.isoformat()
            }
        except NotFound as e:
            logging.error(f'404 error: str{e}')
            return {'message': 'Interview not found'}, 404
        except ValueError as e:
            return {'message': f'Serialization error: {str(e)}'}, 500
        except Exception as e:
            logging.error(f'Unexpected error in get interview: {str(e)}')
            return {'message': 'An unexpected error occurred'}, 500

    def post(self):
        args = parser.parse_args()

        status = args.get('status', InterviewStatus.SCHEDULED.serialize())
        created_at = args.get('created_at', datetime.utcnow().isoformat())
        created_at = created_at if created_at is not None else datetime.utcnow().isoformat()
        updated_at = args.get('updated_at', datetime.utcnow().isoformat())
        updated_at = updated_at if updated_at is not None else datetime.utcnow().isoformat()

        interview = Interview(interviewee_name=args['interviewee_name'],
                              interview_datetime=datetime.strptime(args['interview_datetime'], datetime_format),
                              interviewer_name=args['interviewer_name'],
                              interview_duration_min=args['interview_duration_min'],
                              status=status,
                              created_at=datetime.strptime(created_at, datetime_format),
                              updated_at=datetime.strptime(updated_at, datetime_format)
                              )

        db.session.add(interview)
        db.session.commit()

        return {'message': 'Interview created successfully'}

    def put(self, interview_id):
        interview = Interview.query.get_or_404(interview_id)
        args = parser.parse_args(strict=False)

        if args['interviewee_name']:
            interview.interviewee_name = args['interviewee_name']

        if args['interviewer_name']:
            interview.interviewer_name = args['interviewer_name']

        if args['interview_datetime']:
            interview.interview_datetime = datetime.strptime(args['interview_datetime'], datetime_format)

        if args['interview_duration_min']:
            interview.interview_duration_min = args['interview_duration_min']

        if args.get('status', interview.status.serialize()):
            interview.status = args.get('status', interview.status.serialize())

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
                'interviewer_name': interview.interviewer_name,
                'interview_datetime': interview.interview_datetime.isoformat(),
                'interview_duration_min': interview.interview_duration_min,
                'status': interview.status.serialize(),
                'created_at': interview.created_at.isoformat(),
                'updated_at': interview.updated_at.isoformat()
            } for interview in interviews
        ]


api.add_resource(InterviewListResource, '/interviews')
api.add_resource(InterviewResource, '/interviews/<int:interview_id>')
