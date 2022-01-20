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
        
        # print(lecture_fee_amount) => JSON 응답으로 내려갈 수 없다. 가공 처리
        
        amount_list = [{'lecture_title': row[0], 'amount': int(row[1])} for row in lecture_fee_amount]

            
        # 남성 회원수 / 여성 회원수 => 조건 : 탈퇴하지 않은 인원
        gender_user_count_list = db.session.query(Users.is_male, db.func.count(Users.id))\
            .filter(Users.retired_at == None)\
            .group_by(Users.is_male)\
            .all()
        
        gender_user_counts = [ {'is_male': row[0], 'user_count': int(row[1])} for row in gender_user_count_list ]
            
        
        # 최근 10일(2022-01-10 이후)간의 일자별 매출 총계
        
        amount_by_date_list = db.session.query(db.func.date(LectureUser.created_at), db.func.sum(Lectures.fee))\
            .filter(Lectures.id == LectureUser.lecture_id)\
            .filter(LectureUser.created_at > '2022-01-10')\
            .group_by(db.func.date(LectureUser.created_at))\
            .all()

        date_amounts = []
        
        for row in amount_by_date_list:
            amount_dict = {
                'date': str(row[0]),
                'amount': int(row[1]),
            }
            date_amounts.append(amount_dict)

        return {
            'code': 200,
            'message': '관리자용 각종 통계 api',
            'data': {
                'live_user_count': users_count,
                'lecture_amount': amount_list, # 각 강의 별 총합
                'gender_user_counts': gender_user_counts, # 성별에 따른 사용자 수
                'date_amounts': date_amounts, # 최근 10일간의 날짜별 매출 금액
            }
        }