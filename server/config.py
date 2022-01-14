# 플라스크에 적용 가능한 환경설정 모아두는 클래스
"""
Flask Configuration
"""

class Config(object):
    DEBUG = False
    TESTING = False

class ProductionConfig(Config):
    # 기본 설정 그대로. 실 서버에서도.
    pass

class TestConfig(Config):
    TESTING = True # 테스팅 환경이 맞다고 설정.

class DebugConfig(Config):
    DEBUG = True # 개발모드가 맞다고 설정.