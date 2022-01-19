# 토큰을 발급하고 / 발급된 토큰이 들어오면 사용자가 누구인지 분석하는 등의 기능 담당.
# jwt에 관한 기능 모아두는 모듈

from functools import wraps
import jwt

from flask import current_app, g # g: global 프로젝트 전역에서 공유할 수 있는 공간.
from flask_restful import reqparse

from server.model import Users

token_parser = reqparse.RequestParser()
token_parser.add_argument('X-Http-Token', type=str, required=True, location='headers') # 토큰을 받아오는 파서.

# 토큰 만드는 함수  =>  사용자를 인증하는 용도. => 어떤 사용자에대한 토큰?
def encode_token(user):
    
    # 발급된 토큰을 곧바로 리턴.
    # 1. 사용자의 어떤 항목들로? 토큰 구성요소. => 나중에 복호화해서 꺼낼것도 고려. dict를 넣어서 암호화.
    # 2. 어떤 비밀키를 섞어서 암호화.
    # 3. 어떤 알고리즘으로 암호화.
    return jwt.encode(
        {'id': user.id, 'email': user.email, 'password': user.password_hashed},  # password변수는 쓰기전용. 실제 DB 기록값 활용으로 변경
        current_app.config['JWT_SECRET'],
        algorithm=current_app.config['JWT_ALGORITHM'],
        )  # 이 실행 결과가 곧바로 토큰 str로 나옴.
    
# 토큰값을 가지고 -> Users로 변환하는 함수.
def decode_token(token):
    
    try:
        # 이미 암호화가 된 str => 복호화 => 이전에 넣었던 dict 추출.
        # 1. 어떤 토큰을 ?
        # 2. 어떤 비밀키로 복호화
        # 3. 어떤 알고리즘
        decoded_dict = jwt.decode(
            token,
            current_app.config['JWT_SECRET'],
            algorithms=current_app.config['JWT_ALGORITHM']
        )
        
        user = Users.query\
            .filter(Users.id == decoded_dict['id'])\
            .filter(Users.email == decoded_dict['email'])\
            .filter(Users.password == decoded_dict['password'])\
            .first()
            
        # 제대로 토큰이 들어왔다면 => 복호화 시 제대로된 정보 => 사용자 추출 리턴.
            
        return user
    except jwt.exceptions.DecodeError:
        # 잘못 된 토큰이 들어오면, 복호화 실패 => 예외처리에 의해 이 코드로 빠짐.
        return None  # 사용자도 찾아내지 못했다고 리턴.
    
    
# 데코레이터 사용 =>  추가함수에 적힌 코드를 먼저 실행하고 -> 실제 함수 이어서 진행.
# @추가함수
# def 함수이름:

def token_required(func):
    @wraps(func)
    def decorator(*args, **kwargs): # 어떤 모양의 함수던 가능.
        # 실제 함수 내용이 시작되기전에, 먼저 해줄 함수.
        
        # 1. 토큰 파라미터를 받자.
        args = token_parser.parse_args()
        
        # 2. 그 토큰으로 실제 사용자 추출해보자.
        user = decode_token(args['X-Http-Token'])
        
        # 3.1. 사용자가 제대로 나왔다 => 올바른 토큰 => 원래 함수의 내용 실행
        if user:
            
            # 토큰으로 사용자를 찾아냈다면 => 원본 함수에서도, 그 사용자를 가져다 쓰면 편하겠다.
            # 전역변수를 이용해서, 사용자를 전달하자.
            g.user = user
            
            return func(*args, **kwargs) # 원본 함수 내용 실행. 결과 리턴.
        
        # 3.2. 사용자가 안나왔다 (None) => 잘못된 토큰 => 403 에러 리턴.
        else:
            return {
                'code': 403,
                'message': '올바르지 않은 토큰입니다.'
            }, 403
            
    # token_required 이름표가 붙은 함수들에게 => decorator 함수 전달
    return decorator