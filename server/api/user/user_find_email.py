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

class UserEmailFind(Resource):
    
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
            .first()
        
        if user is None:
            return {
                'code': 400,
                'message': '해당 이름의 사용자는 없습니다.'
            }, 400
        
        # 이름으로 사용자 검색 성공
        # 폰번도 비교. => "-" 을 모두 삭제하고 나서 비교해보자.
        
        input_phone = args['phone'].replace('-', '')
        user_phone = user.phone.replace('-',  '')
        
        if input_phone != user_phone:
            return {
                'code': 400,
                'message': '이름은 맞지만 폰번이 다릅니다.'
            }, 400
        
            
        # 알리고 사이트의 API에 문자 전송 Request 전송. => requests 모듈 활용
        
        # 1. 주소 => apis.aligo.in/send/ 등의 주소.
        
        # 2. 어떤 메쏘드 => POST
        
        # 3. 파라미터 => 명세서 참조
        
        sms_url = 'https://apis.aligo.in/send/'
        
        # dict에 들고갈 파라미터에 담을 값들을 미리 세팅해두자.
        
        send_data = {
            'key': current_app.config['ALIGO_API_KEY'],
            'user_id': 'cho881020',
            'sender': '010-5112-3237',
            'receiver': user.phone,
            'msg': f"-MySNS 계정안내-\n가입하신 계정은 [{user.email}]입니다.",
        }
        
        # requests의 요청에 대한 결과를 변수에 담자.
        response = requests.post(url=sms_url, data=send_data)
        
        # 응답의 본문이 json으로 올 예정 => json형태로 가공해서 받자.
        respJson = response.json()
        
        # 결과 코드가 1인게 성공. => 우리 서버도 200 리턴.
        # 그 외의 값 => 알리고에서 문제 => 그 내용을 그대로 500 으로 리턴.
        #  400 : Bad Request -> 요청 보낸쪽에서 문제.
        #  403 : 권한 -> 권한 문제
        #  404 : 해당 주소 기능 없음
        #  500 : 서버 내부의 문제. (Interer Server Error)
        
        if int(respJson['result_code']) != 1:
            # 정상 전송 실패
            return {
                'code': 500,
                'message': respJson['message']   # 알리고 에서 왜 실패했는지는 받은 문구 그대로 리턴.
            }, 500
        else:
            # 정상 전송 성공
            return {
                'code': 200,
                'message': '이메일 찾기 - 문자 전송 완료',
            }