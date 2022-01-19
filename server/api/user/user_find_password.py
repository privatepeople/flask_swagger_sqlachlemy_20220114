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
        """ 비밀번호 찾기 (이메일 전송) """
        
        args = get_parser.parse_args()
        
        user = Users.query\
            .filter(Users.email == args['email'])\
            .first()
        
        if user is None:
            return {
                'code': 400,
                'message': '해당 계정의 사용자는 없습니다.'
            }, 400
        
        # 이메일로 사용자 검색 성공
        # 폰번도 비교. => "-" 을 모두 삭제하고 나서 비교해보자.
        # 이름도 비교.
        
        input_phone = args['phone'].replace('-', '')
        user_phone = user.phone.replace('-',  '')
        
        if input_phone != user_phone or args['name'] != user.name:
            return {
                'code': 400,
                'message': '개인정보가 맞지 않습니다.'
            }, 400
        
        
        # 메일에 뭐라고 보내줄건지 내용 작성
        
        # 실제 비번을 보내주면 안됨 => 실제 비밀번호 자체를 저장해두면 안됨
        # 임시 비밀번호를 랜덤으로 설정 => 새 비밀번호로 update / 메일 발송    
    
        send_content = f"""
        안녕하세요. MySNS입니다.
        비밀번호 안내 드립니다.
        회원님의 비밀번호는 {user.password}입니다.
        """
        
        print(send_content)
        
        # 메일전송 api => mailgun.com 사이트 활용.
        #  => 도메인 주소 구매 후, 사이트에 세팅까지 마친 후에 활용 가능.
        
        # 어느 사이트(주소) / 메쏘드 / 파라미터 세가지 세팅. requests 모듈
        
        mailgun_url = 'https://api.mailgun.net/v3/mg.gudoc.in/messages'
        
        email_data = {
            'from': 'system@gudoc.in', # system@웹주소.com
            'to': user.email, # 비번찾기를 하려는 이메일
            'subject': '[MySNS 비밀번호 안내] 비밀번호 찾기 알림 메일입니다.',
            'text': send_content
        }
        
        requests.post(
            url= mailgun_url,
            data=email_data,
            auth=('api', current_app.config['MAILGUN_API_KEY'])
        )
            
        return {
            'code': 200,
            'message': '비밀번호를 이메일로 전송했습니다. (임시)'
        }