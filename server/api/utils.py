# 토큰을 발급하고/ 발급된 토큰이 들어오면 사용자가 누구인지 분석하는 등의 기능 담당.
# jwt에 관한 기능 모아두는 모듈

import jwt

from flask import current_app

# 토큰 만드는 함수 => 사용자를 인증하는 용도. => 어떤 사용자에 대한 토큰?
def encode_token(user):
    
    # 발급된 토큰을 곧바로 리턴.
    # 1. 사용자의 어떤 항목들로? 토큰 구성요소. => 나중에 복호화해서 꺼낼것도 고려. dict를 넣어서 암호화.
    # 2. 어떤 비밀키를 섞어서 암호화.
    # 3. 어떤 알고리즘으로 암호화.
    return jwt.encode(
        {'id': user.id, 'email': user.email, 'password': user.password},
        current_app.config['JWT_SECRET'],
        algorithm=current_app.config['JWT_ALGORITHM'],
        ) # 이 실행결과가 곧바로 토큰 str로 나옴.