from flask_restful import Resource

class LectureDetail(Resource):
    
    def get(self):
        return {
            '임시': '특정 강의 상세 조회'
        }