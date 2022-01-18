from flask_restful import Resource, reqparse
from werkzeug.datastructures import FileStorage # 파라미터로 파일을 받을때 필요한 클래스
from flask_restful_swagger_2 import swagger

put_parser = reqparse.RequestParser()
# 파일을 받는 파라미터는, FileStorage, files에서, 추가 행동 : append
put_parser.add_argument('profile_image', type=FileStorage, required=True, location='files', action='append')
put_parser.add_argument('user_id', type=int, required=True, location='form')

class UserProfileImage(Resource):
    
    @swagger.doc({
        'tags': ['user'],  # 어떤 종류의 기능인지 분류.
        'description': '사용자 프로필사진 등록',
        'parameters': [
            {
                'name': 'user_id',
                'description': '누구의 프사 등록?',
                'in': 'formData',
                'type': 'integer',
                'required': True
            },
            {
                'name': 'profile_image',
                'description': '실제로 첨부할 사진',
                'in': 'formData',
                'type': 'file',
                'required': True
            },
        ],
        'responses': {
            # 200일때의 응답 예시, 400일때의 예시 등.
            '200': {
                'description': '등록 성공',
            },
            '400': {
                'description': '등록 실패',
            }
        }
    })
    
    def put(self):
        """ 사용자 프로필사진 등록 """
        return {
            '임시': '사용자 프사 등록 가능'
        }