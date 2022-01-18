from flask_restful import Resource

class LectureDetail(Resource):
    
    def get(self, lecture_id):
        return {
            '임시': f"{lecture_id}번 강의 상세 조회"
        }