from flask_restful import reqparse


def get_request_parser():
    parser = reqparse.RequestParser()

    parser.add_argument('interviewee_name',
                        type=str,
                        required=False,
                        help='Name of the interviewee'
                        )
    parser.add_argument('interviewer_name',
                        type=str,
                        required=False,
                        help='Name of the interviewer'
                        )
    parser.add_argument('interview_datetime',
                        type=str,
                        required=False,
                        help='Datetime of the interview (YYYY-MM-DD HH:MM:SS)'
                        )
    parser.add_argument('interview_duration_min',
                        type=int,
                        required=False,
                        help='Duration of the interview'
                        )
    parser.add_argument('status',
                        type=str,
                        required=False,
                        help='Status of the interview [SCHEDULED, ONGOING, CANCELED, COMPLETED]'
                        )
    parser.add_argument('created_at',
                        type=str,
                        required=False,
                        help='Creation datetime of the record'
                        )
    parser.add_argument('updated_at',
                        type=str,
                        required=False,
                        help='Last update datetime of the record'
                        )

    return parser
