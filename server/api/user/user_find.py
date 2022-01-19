import requests

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
                'description': '사용중인 폰번 - 둘다 맞아야 문자로 전송.',
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
        
        user = Users.query\
            .filter(Users.name == args['name'])\
            .filter(Users.phone == args['phone'])\
            .first()
        
        if user is None:
            return {
                'code': 400,
                'message': '이름 / 폰번 둘다 맞게 입력해야 합니다.'
            }, 400
            
        # 알리고 사이트의 API에 문자 전송 Request 전송. => requests 모듈 활용
        
        # 1. 주소 => apis.aligo.in/send/ 등의 주소.
        
        # 2. 어떤 메쏘드 => POST
        
        # 3. 파라미터 => 명세서 참조
        
        sms_url = 'https://apis.aligo.in/send/'
        
        # dict에 들고갈 파라미터에 담을 값들을 미리 세팅해두자.
        
        send_data = {
            'key': current_app.config['AlIGO_API_KEY'],
            'user_id': 'cho881020',
            'sender': '010-5112-3237',
            'receiver': user.phone,
            'msg': f"가입하신 계정은 [{user.email}]입니다.",
        }
        
        requests.post(url=sms_url, data=send_data)
        
        
        
        return {
            'code': 200,
            'message': '이메일 찾기 - 문자 전송 완료',
        }