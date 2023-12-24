import logging
from flask_restful import Resource, reqparse
from sqlalchemy.exc import DatabaseError

from werkzeug.exceptions import NotFound

from app import api, db
from app.models import Interview, InterviewStatus
from datetime import datetime


DATETIME_FORMAT = '%Y-%m-%dT%H:%M:%S.%f'

parser = reqparse.RequestParser()
parser.add_argument('interviewee_name', type=str, required=False, help='Name of the interviewee')
parser.add_argument('interviewer_name', type=str, required=False, help='Name of the interviewer')
parser.add_argument('interview_datetime', type=str, required=False,
                    help='Datetime of the interview (YYYY-MM-DD HH:MM:SS)')
parser.add_argument('interview_duration_min', type=int, required=False, help='Duration of the interview')
parser.add_argument('status',
                    type=str,
                    required=False,
                    help='Status of the interview [SCHEDULED, ONGOING, CANCELED, COMPLETED]')
parser.add_argument('created_at', type=str, required=False, help='Creation datetime of the record')
parser.add_argument('updated_at', type=str, required=False, help='Last update datetime of the record')


class InterviewListResource(Resource):
    def get(self):
        try:
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
            ], 200
        except NotFound as e:
            logging.error(f'404 error: str{e}')
            return {'message': 'Error retrieving interview data'}, 404  # Not found
        except ValueError as e:
            return {'message': f'Serialization error: {str(e)}'}, 500  # Internal server error
        except Exception as e:
            logging.error(f'Unexpected error in get interview (generic exception): {str(e)}')
            return {'message': 'An unexpected error occurred'}, 500  # Internal server error

    def post(self):
        args = parser.parse_args()

        # Add optional parameters defaults to `args` if needed
        created_at = args.get('created_at', datetime.utcnow().isoformat())
        created_at = created_at if created_at is not None else datetime.utcnow().isoformat()
        args['created_at'] = created_at

        updated_at = args.get('updated_at', datetime.utcnow().isoformat())
        updated_at = updated_at if updated_at is not None else datetime.utcnow().isoformat()
        args['updated_at'] = updated_at

        # Handle missing parameters
        if None in args.values():
            return {
                'message': 'Missing parameters',
                'missing parameters': [argument for argument in args.keys() if args[argument] is None]
            }, 400  # Bad request

        # Validate interview_datetime
        interview_datetime = args['interview_datetime']
        try:
            interview_datetime = datetime.strptime(interview_datetime, DATETIME_FORMAT)
        except ValueError as e:
            return {'message': 'Error parsing interview_datetime'}, 400  # Bad request
        except Exception as e:
            logging.error(f'Error parsing interview_datetime (generic exception): {str(e)}')
            return {'message': 'Error parsing interview_datetime'}, 400  # Bad request

        # Validate interview_duration_min
        try:
            interview_duration_min = int(args['interview_duration_min'])
        except ValueError as e:
            return {'message': 'Invalid integer for interview_duration_min'}, 400  # Bad request

        # Validate status
        status = args.get('status', InterviewStatus.SCHEDULED.serialize())
        if not InterviewStatus.validate_str(status):
            return {'message': 'Unable to serialize status'}, 400  # Bad request

        interview = Interview(interviewee_name=args['interviewee_name'],
                              interview_datetime=interview_datetime,
                              interviewer_name=args['interviewer_name'],
                              interview_duration_min=interview_duration_min,
                              status=status,
                              created_at=datetime.strptime(created_at, DATETIME_FORMAT),
                              updated_at=datetime.strptime(updated_at, DATETIME_FORMAT)
                              )

        try:
            db.session.add(interview)
            db.session.commit()
        except DatabaseError as e:
            return {'message': f'Error adding entry to the database: {str(e)}'}, 500  # Internal server error
        except Exception as e:
            logging.error(f'Error adding entry to the database (generic exception): {str(e)}')
            return {'message': f'Unexpected error adding entry to the database'}, 500  # Internal server error

        return {'message': 'Interview created successfully'}, 200
