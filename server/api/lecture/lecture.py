from flask_restful import Resource

class Lecture(Resource):
    def delete(self):
        return {
            '임시': '수강 취소 기능'
        }