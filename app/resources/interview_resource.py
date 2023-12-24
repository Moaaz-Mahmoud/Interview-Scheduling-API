import logging
from flask_restful import Resource, reqparse
from sqlalchemy.exc import DatabaseError

from werkzeug.exceptions import NotFound

from app import db
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
            }, 200
        except NotFound as e:
            logging.error(f'Entry not found. ERROR: str{e}')
            return {'message': 'Interview not found'}, 404  # Not found
        except ValueError as e:
            return {'message': f'Serialization error: {str(e)}'}, 500  # Internal server error
        except Exception as e:
            logging.error(f'Unexpected error in get interview (generic exception): {str(e)}')
            return {'message': 'An unexpected error occurred'}, 500  # Internal server error

    def put(self, interview_id):
        interview = Interview.query.get_or_404(interview_id)
        args = parser.parse_args(strict=False)

        if args['interviewee_name']:
            interview.interviewee_name = args['interviewee_name']

        if args['interviewer_name']:
            interview.interviewer_name = args['interviewer_name']

        if args['interview_datetime']:
            # Validate interview_datetime
            interview_datetime_raw = args['interview_datetime']
            try:
                interview.interview_datetime = datetime.strptime(interview_datetime_raw, DATETIME_FORMAT)
            except ValueError as e:
                return {'message': 'Error parsing interview_datetime'}, 400  # Bad request
            except Exception as e:
                logging.error(f'Error parsing interview_datetime (generic exception): {str(e)}')
                return {'message': 'Error parsing interview_datetime'}, 400  # Bad request

        # TODO: Revisit the error handling for this field
        if args['interview_duration_min']:
            # Validate interview_duration_min
            try:
                duration = int(args['interview_duration_min'])
                interview.interview_duration_min = duration
            except ValueError as e:
                return {'message': 'Invalid integer for interview_duration_min'}, 400  # Bad request

        if args.get('status', interview.status.serialize()):
            # Validate status
            status = args.get('status', InterviewStatus.SCHEDULED.serialize())
            if not InterviewStatus.validate_str(status):
                return {'message': 'Unable to serialize status'}, 400  # Bad request
            interview.status = status

        interview.updated_at = datetime.utcnow()

        try:
            db.session.commit()
        except DatabaseError as e:
            return {'message': f'Error adding entry to the database: {str(e)}'}, 500  # Internal server error
        except Exception as e:
            logging.error(f'Error adding entry to the database (generic exception): {str(e)}')
            return {'message': f'Unexpected error adding entry to the database'}, 500  # Internal server error

        return {'message': 'Interview updated successfully'}, 200

    def delete(self, interview_id):
        try:
            interview = Interview.query.get_or_404(interview_id)
        except NotFound as e:
            logging.error(f'Entry not found. ERROR: str{e}')
            return {'message': 'Interview not found'}, 404  # Not found
        except ValueError as e:
            return {'message': f'Serialization error: {str(e)}'}, 500  # Internal server error
        except Exception as e:
            logging.error(f'Unexpected error in get interview (generic exception): {str(e)}')
            return {'message': 'An unexpected error occurred'}, 500  # Internal server error

        try:
            db.session.delete(interview)
            db.session.commit()
        except DatabaseError as e:
            return {'message': f'Error adding entry to the database: {str(e)}'}, 500  # Internal server error
        except Exception as e:
            logging.error(f'Error adding entry to the database (generic exception): {str(e)}')
            return {'message': f'Unexpected error adding entry to the database'}, 500  # Internal server error

        return {'message': 'Interview deleted successfully'}, 200
