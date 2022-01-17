from flask_restful import Resource
from flask_restful_swagger_2 import swagger

class Lecture(Resource):
    
    @swagger.doc({
        'tags': ['lecture'], # 어떤 종류의 기능인지 분류.
        'description': '수강 취소',
        'parameters': [
            # dict로 파라미터들 명시
        ],
        'responses': {
            # 200일때의 응답 예시, 400일때의 예시 등.
            '200': {
                'description': '수강취소 성공',
            },
            '400': {
                'description': '수강취소 실패',
            }
        }
    })
    def delete(self):
        """수강 취소"""
        
        return {
            '임시': '수강 취소 기능'
        }