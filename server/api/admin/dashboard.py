from flask_restful import Resource

from server import db
from server.model import Users, LectureUser, Lectures

class AdminDashboard(Resource):
    
    def get(self):
        
        # 탈퇴하지 않은 회원 수? => SELECT / users 테이블 활용 => Users 모델 import
        
        
        # first() 한줄, all() 목록, count() 검색된 갯수
        users_count = Users.query\
            .filter(Users.email != 'retired')\
            .count()
            
        # 연습 - 자바 강의의 매출 총액 (집계함수) => (ORM) JOIN 활용.
        
        # query( SELECT 컬럼 선택처럼 여러 항목 가능 )
        # db.func.집계함수(컬럼) => 집계함수 동작
        
        # filter 나열 => JOIN / ON 을 한번에 명시
        # filter 나열 2 => JOIN이 끝나면, WHERE절처럼 실제 필터 조건
        
        # group_by => 어떤 값을 기준으로 그룹지을지
        
        lecture_fee_amount = db.session.query( Lectures.title, db.func.sum(Lectures.fee) )\
            .filter(Lectures.id == LectureUser.lecture_id)\
            .filter(LectureUser.user_id == Users.id)\
            .group_by(Lectures.id)\
            .all()
        
        print(lecture_fee_amount)
        
        return {
            'code': 200,
            'message': '관리자용 각종 통계 api',
            'data': {
                'live_user_count': users_count
            }
        }