from flask_restful import Resource
from flask_restful_swagger_2 import swagger

from server.model import Lectures

class Lecture(Resource):
    
    @swagger.doc({
        'tags': ['lecture'],  # 어떤 종류의 기능인지 분류.
        'description': '수강 취소',
        'parameters': [
            # dict로 파라미터들 명시.
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
        
    @swagger.doc({
        'tags': ['lecture'],  # 어떤 종류의 기능인지 분류.
        'description': '강의 목록 조회 - 가나다순',
        'parameters': [
            # dict로 파라미터들 명시.
        ],
        'responses': {
            # 200일때의 응답 예시, 400일때의 예시 등.
            '200': {
                'description': '조회 성공',
            },
            '400': {
                'description': '조회 실패',
            }
        }
    })
    def get(self):
        """강의 목록 조회"""
        
        lecture_rows = Lectures.query.order_by(Lectures.title).all()
        
        lectures = [ row.get_data_object()  for row in lecture_rows ]
        
        return {
            'code': 200,
            'message': '모든 강의 목록',
            'data': {
                'lectures': lectures
            }
        }
        