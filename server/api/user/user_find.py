from flask import current_app, g
from flask_restful import Resource, reqparse
from flask_restful_swagger_2 import swagger

from server import db
from server.model import Users
from server.api.utils import token_required

get_parser = reqparse.RequestParser()
get_parser.add_argument('name', type=str, required=True, location='args')
get_parser.add_argument('phone', type=str, required=True, location='args')

class UserFind(Resource):
    
    @swagger.doc({
        'tags': ['user'],  # 어떤 종류의 기능인지 분류.
        'description': '아이디 찾기',
        'parameters': [
            {
                'name': 'name',
                'description': '사용중인 이름',
                'in': 'query',
                'type': 'string',
                'required': True
            },
            {
                'name': 'phone',
                'description': '사용중인 폰번 - 둘다 맞아야 문자로 전송',
                'in': 'query',
                'type': 'string',
                'required': True
            },
        ],
        'responses': {
            # 200일때의 응답 예시, 400일때의 예시 등.
            '200': {
                'description': '이메일이 문자로 전송됨',
            },
            '400': {
                'description': '이름/폰번중 하나 틀림',
            }
        }
    })
    def get(self):
        """ 이메일 찾기 (문자 전송) """
        
        args = get_parser.parse_args()

        
        
        return {
            'code': 200,
            'message': '이메일 찾기 - 문자 전송 완료',
        }