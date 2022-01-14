# 사용자에 관련된 기능을 수행하는 클래스.
# 메쏘드를 만들때, get / post / put / patch / delete로 ㅁ나들면, 알아서 메쏘드로 세팅되도록.

from flask_restful import Resource

class User(Resource):
    
    def get(self):
        return {
            "임시": "사용자 정보 조회"
        }
    
    def post(self):
        return {
            "임시": "로그인 기능"
        }
    
    def put(self):
        return {
            "임시": "회원가입 기능"
        }