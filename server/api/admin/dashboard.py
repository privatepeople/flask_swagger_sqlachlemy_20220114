import datetime

from flask import g
from flask_restful import Resource
from flask_restful_swagger_2 import swagger

from server import db
from server.model import Users, LectureUser, Lectures
from server.api.utils import token_required, admin_required

class AdminDashboard(Resource):
    
    @swagger.doc({
        'tags':['admin'],
        'description':'관리자 - 대쉬보드',
        'parameters': [
            {
                'name': 'X-Http-Token',
                'description': '사용자 인증용 헤더 - 관리자만 OK',
                'in': 'header',
                'type': 'string',
                'required': True,
            }
        ],
        'responses': {
            '200': {
                'description': '관리자 조회 성공'
            }
        }
    })
    @token_required
    @admin_required
    def get(self):
        """ 관리자 - 대쉬보드 """
        
        # 탈퇴하지 않은 회원 수? => SELECT / users 테이블 활용 => Users 모델 import
        
        
        # first() 한줄, all() 목록,  count() 검색된 갯수
        users_count = Users.query\
            .filter(Users.email != 'retired')\
            .count() 
            
        # 연습 - 자바 강의의 매출 총액 (집계함수) => (ORM) JOIN 활용.
        
        # query( SELECT 컬럼 선택처럼 여러 항목 가능. )
        # db.func.집계함수(컬럼)  => 집계함수 동작
        
        # filter 나열 => JOIN / ON 을 한번에 명시.
        # filter 나열 2 => JOIN이 끝나면, WHERE절처럼 실제 필터 조건.
        
        # group_by => 어떤 값을 기준으로 그룹지을지 
        
        lecture_fee_amount = db.session.query( Lectures.title, db.func.sum(Lectures.fee) )\
            .filter(Lectures.id == LectureUser.lecture_id)\
            .filter(LectureUser.user_id == Users.id)\
            .group_by(Lectures.id)\
            .all()
            
        # print(lecture_fee_amount)  =>  JSON응답으로 내려갈 수 없다. 가공 처리 필요
        
        amount_list = [ {'lecture_title': row[0], 'amount':int(row[1])} for row in lecture_fee_amount ]
        
        
        # 남성 회원수 / 여성 회원수 => 조건 : 탈퇴하지 않은 인원.
        gender_user_count_list = db.session.query( Users.is_male, db.func.count(Users.id) )\
            .filter(Users.retired_at == None)\
            .group_by(Users.is_male)\
            .all()
            
        gender_user_counts = [ {'is_male':row[0], 'user_count':int(row[1])}  for row in gender_user_count_list ] 
            
        
        # 최근 10일간의 일자별 매출 총 계.
        
        # 지금으로 부터 10일전은 몇일인가? 구해서 쿼리에 반영하자.
        
        now = datetime.datetime.utcnow()  # DB가 표준시간대 사용 => 계산도 표준시간대 기준
        
        diff_days = datetime.timedelta(days= -10)  # 10일 이전으로 계산 해줄 변수.
        
        ten_days_ago = now + diff_days  # 10일 전 날짜 구해주기.

        amount_by_date_list = db.session.query( db.func.date(LectureUser.created_at),  db.func.sum(Lectures.fee) )\
            .filter(Lectures.id == LectureUser.lecture_id)\
            .filter(LectureUser.created_at > ten_days_ago)\
            .group_by( db.func.date(LectureUser.created_at))\
            .all()
            
        date_amounts = []
        
        # 매출이 없는 날은, DB 쿼리 결과도 아예 없다. => 목록에 아예 등록 안됨.
        # 날짜는 무조건 10개,  매출이 없는날은 0원 처리.
        
        # 10일전 ~ 오늘 까지를 for문으로.
        
        for i in range(0, 11):
            
            # 시간/분/초 까지 날짜에 들어감. => 2022-01-11 양식으로 변경. => 
            
            amount_dict = {
                'date': ten_days_ago.strftime('%Y-%m-%d'),
                'amount': 0,
            }
            
            # 매출이 발생한날이라면? amount 금액 수정.
            
            for row in amount_by_date_list:
                # DB 쿼리 결과에서, 이번 날짜와 같은 날짜 발견
                if str(row[0]) == amount_dict['date']:
                    amount_dict['amount'] = int( row[1] )
            
            # 응답으로 등록
            date_amounts.append(amount_dict)
            
            # 해당 날짜에서 하루 지난 날로 변경.
            ten_days_ago +=  datetime.timedelta(days=1)
        
        # for row in amount_by_date_list:
        #     amount_dict = {
        #         'date': str(row[0]),
        #         'amount': int(row[1]),
        #     }
        #     date_amounts.append(amount_dict)
        
        return {
            'code':200,
            'message': '관리자용 각종 통계 api',
            'data': {
                'live_user_count': users_count,
                'lecture_amount': amount_list,  # 각 강의 별 총합
                'gender_user_counts': gender_user_counts,  # 성별에 따른 사용자 수
                'date_amounts': date_amounts, # 최근 10일간의 날짜별 매출 총액
            }
        }