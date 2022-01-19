import requests

from flask import current_app, g
from flask_restful import Resource, reqparse
from flask_restful_swagger_2 import swagger

from server import db
from server.model import Users
from server.api.utils import token_required

get_parser = reqparse.RequestParser()
get_parser.add_argument('email', type=str, required=True, location='args')
get_parser.add_argument('name', type=str, required=True, location='args')
get_parser.add_argument('phone', type=str, required=True, location='args')

class UserPasswordFind(Resource):
    
    @swagger.doc({
        'tags': ['user'],  # 어떤 종류의 기능인지 분류.
        'description': '비밀번호 찾기',
        'parameters': [
            {
                'name': 'email',
                'description': '비번 찾을 이메일',
                'in': 'query',
                'type': 'string',
                'required': True
            },
            {
                'name': 'name',
                'description': '사용중인 이름',
                'in': 'query',
                'type': 'string',
                'required': True
            },
            {
                'name': 'phone',
                'description': '사용중인 폰번 - 둘다 맞아야 문자로 전송.',
                'in': 'query',
                'type': 'string',
                'required': True
            },
        ],
        'responses': {
            # 200일때의 응답 예시, 400일때의 예시 등.
            '200': {
                'description': '비밀번호가 이메일로 전송됨',
            },
            '400': {
                'description': '이름/폰번중 하나 틀림',
            }
        }
    })
    def get(self):
        """ 비밀번호 찾기 (이메일로 전송) """
        
        args = get_parser.parse_args()
        
        user = Users.query\
            .filter(Users.name == args['email'])\
            .first()
        
        if user is None:
            return {
                'code': 400,
                'message': '해당 계정의 사용자는 없습니다'
            }, 400
            
        # 이메일로 사용자 검색 성공
        # 폰번도 비교 => "-"을 모두 삭제하고 나서 비교해보자.
        # 이름도 비교
            
        input_phone = args['phone'].replace('-', '')
        user_phone = user.phone.replace('-', '')
        
        if input_phone != user_phone or args['name'] != user.name:
            return {
                'code': 400,
                'message': '개인정보가 맞지 않습니다.'
            }, 400
            
            
        # 메일전송 api => mailgun.com 사이트 활용
        # => 도메인 주소 구매 후, 사이트에 세팅까지 마친 후에 활용 가능
        
        # 어느 사이트(주소) / 메쏘드 / 파라미터 세가지 세팅. requests 모듈
        
        return {
            'code': 200,
            'message': '비밀번호를 이메일로 전송했습니다. (임시)'
        }