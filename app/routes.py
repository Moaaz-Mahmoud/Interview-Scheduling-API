from app import api
from app.resources.interview_list_resource import InterviewListResource
from app.resources.interview_resource import InterviewResource

api.add_resource(InterviewListResource, '/interviews')
api.add_resource(InterviewResource, '/interviews/<int:interview_id>')
