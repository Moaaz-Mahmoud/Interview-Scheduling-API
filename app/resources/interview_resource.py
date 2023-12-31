from datetime import datetime
from werkzeug.exceptions import NotFound
import logging
from flask_restful import Resource, abort
from sqlalchemy.exc import DatabaseError
from app import db
from app.models import Interview, InterviewStatus
from app.resources.parser import get_request_parser


DATETIME_FORMAT = '%Y-%m-%dT%H:%M:%S.%f'

parser = get_request_parser()


class InterviewResource(Resource):
    @staticmethod
    def get(interview_id):
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
            logging.error(f'Entry not found. ERROR: str{e}')
            abort(
                404,
                message='Interview not found'
            )
        except ValueError as e:
            abort(
                500,
                message=f'Serialization error: {str(e)}'
            )
        except Exception as e:
            logging.error(f'Unexpected error in get interview (generic exception): {str(e)}')
            abort(
                500,
                message='An unexpected error occurred'
            )

    @staticmethod
    def put(interview_id):
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
            except ValueError:
                abort(
                    400,
                    message='Error parsing interview_datetime'
                )
            except Exception as e:
                logging.error(f'Error parsing interview_datetime (generic exception): {str(e)}')
                abort(
                    400,
                    message='Error parsing interview_datetime'
                )

        # TODO: Revisit the error handling for this field
        if args['interview_duration_min']:
            # Validate interview_duration_min
            try:
                duration = int(args['interview_duration_min'])
                interview.interview_duration_min = duration
            except ValueError:
                abort(
                    400,
                    message='Invalid integer for interview_duration_min'
                )

        if args.get('status', interview.status.serialize()):
            # Validate status
            status = args.get('status', InterviewStatus.SCHEDULED.serialize())
            if not InterviewStatus.validate_str(status):
                abort(
                    400,
                    message='Unable to serialize status'
                )
            interview.status = status

        interview.updated_at = datetime.utcnow()

        try:
            db.session.commit()
        except DatabaseError as e:
            abort(
                500,
                message=f'Error adding entry to the database: {str(e)}'
            )
        except Exception as e:
            logging.error(f'Error adding entry to the database (generic exception): {str(e)}')
            abort(
                500,
                message=f'Unexpected error adding entry to the database'
            )

        return {'message': 'Interview updated successfully'}

    @staticmethod
    def delete(interview_id):
        try:
            interview = Interview.query.get_or_404(interview_id)
        except NotFound as e:
            logging.error(f'Entry not found. ERROR: str{e}')
            abort(
                404,
                message='Interview not found'
            )
        except ValueError as e:
            abort(
                500,
                message=f'Serialization error: {str(e)}'
            )
        except Exception as e:
            logging.error(f'Unexpected error in get interview (generic exception): {str(e)}')
            abort(
                500,
                message='An unexpected error occurred'
            )

        try:
            db.session.delete(interview)
            db.session.commit()
        except DatabaseError as e:
            abort(
                500,
                message=f'Error adding entry to the database: {str(e)}'
            )
        except Exception as e:
            logging.error(f'Error adding entry to the database (generic exception): {str(e)}')
            abort(
                500,
                message=f'Unexpected error adding entry to the database'
            )

        return {'message': 'Interview deleted successfully'}
