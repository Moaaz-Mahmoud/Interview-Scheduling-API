import logging
from flask_restful import Resource, abort
from sqlalchemy.exc import DatabaseError
from werkzeug.exceptions import NotFound
from app import db
from app.models import Interview, InterviewStatus
from datetime import datetime
from app.resources.parser import get_request_parser


DATETIME_FORMAT = '%Y-%m-%dT%H:%M:%S.%f'

parser = get_request_parser()


class InterviewListResource(Resource):
    @staticmethod
    def get():
        try:
            interviews = Interview.query.all()
            return [
                {
                    'id': interview.id,
                    'interviewee_name': interview.interviewee_name,
                    'interviewer_name': interview.interviewer_name,
                    'interview_datetime': interview.interview_datetime.isoformat(),
                    'interview_duration_min': interview.interview_duration_min,
                    'status': interview.status.serialize(),
                    'created_at': interview.created_at.isoformat(),
                    'updated_at': interview.updated_at.isoformat()
                } for interview in interviews
            ]
        except NotFound as e:
            logging.error(f'404 error: str{e}')
            abort(
                404,
                message='Error retrieving interview data'
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
    def post():
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
            abort(
                400,
                message='Missing parameters',
                missing_parameters=[argument for argument in args.keys() if args[argument] is None]
            )

        # Validate interview_datetime
        interview_datetime = args['interview_datetime']
        try:
            interview_datetime = datetime.strptime(interview_datetime, DATETIME_FORMAT)
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

        # Validate interview_duration_min
        try:
            interview_duration_min = int(args['interview_duration_min'])
        except ValueError:
            abort(
                400,
                message='Invalid integer for interview_duration_min'
            )

        # Validate status
        status = args.get('status', InterviewStatus.SCHEDULED.serialize())
        if not InterviewStatus.validate_str(status):
            abort(
                400,
                message='Unable to serialize status'
            )

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

        return {'message': 'Interview created successfully'}
