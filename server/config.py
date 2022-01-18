# 플라스크에 적용 가능한 환경설정 모아두는 클래스
"""
Flask Configuration
"""

class Config(object):
    DEBUG = False
    TESTING = False
    
    # SQLAlchemy가 접속할 DB 연결 정보(URL)
    # SQLAlchemy 라이브러리가, 어떤 변수를 끌어다 쓸지도 미리 지정되어있음. => 변수이름 바꾸면 안됨.
    # SQLALCHEMY_DATABASE_URL = "mysql+pymysql://아이디:비밀번호@DB호스트주소/논리DB이름"
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://admin:wpfh1945!!"+\
        "@lshdatabase.cddsnovvbqm5.ap-northeast-2.rds.amazonaws.com/my_sns_ckj"
        
    # DB 변경 추적 기능 꺼두기
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # S3 접속 정보들을 변수들로 저장
    AWS_ACCESS_KEY_ID = 'AKIAU4ZXNAN67DUZ6PIL'
    AWS_SECRET_ACCESS_KEY = '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'
    AWS_S3_BUCKET_NAME = 'lsh.python'
    
    # 토큰 발급용 암호화 로직 이름 / 사용할 키값
    JWT_ALGORITHM = 'HS512'
    JWT_SECRET = 'my_strong_key' # 임시 문구. 원하는대로 변경. (타인 노출 되면 안됨)

class ProductionConfig(Config):
    # 기본 설정 그대로. 실 서버에서도.
    pass

class TestConfig(Config):
    TESTING = True # 테스팅 환경이 맞다고 설정.

class DebugConfig(Config):
    DEBUG = True # 개발모드가 맞다고 설정.