from flask_restful import Resource

class AdminDashboard(Resource):
    
    def get(self):
        return {
            'code': 200,
            'message': '관리자용 각종 통계 api'
        }