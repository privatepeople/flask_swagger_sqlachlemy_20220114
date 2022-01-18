# DB의 users 테이블에 연결되는 클래스
from server import db

import datetime

class Users(db.Model):
    # SQLAlchemy 라이브러리의 Model 클래스 활용.
    
    # 1. 어느 테이블? 연결 명시
    __tablename__ = 'users' # DB 테이블 이름
    
    # 2. 어떤 변수 / 어떤 컬럼 연결 명시 => 변수 이름이 컬럼 이름과 같아야함.
    id = db.Column(db.Integer, primary_key=True)  # id컬럼은, int / 기본키 라고 명시.
    email = db.Column(db.String(50), nullable=False, default='이메일 미입력') # email 컬럼은, 50자 문구, null 불가, 기본값 있다.
    password = db.Column(db.String(50), nullable=False)
    name = db.Column(db.String(20), nullable=False)
    phone = db.Column(db.String(15))  # nullable의 기본값은 null 허용.
    birth_year = db.Column(db.Integer, nullable=False, default=1995)
    profile_img_url = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp()) # 일반 datetime.datetiem.now() => 작업 PC 서버의 시간이 기록됨. => DB 현재시간 아님.
    retired_at = db.Column(db.DateTime)
    
    # cf) Feeds테이블에서, Users로 외래키를 들고 연결 설정함.
    #  Users의 입장에서는 => Feeds테이블에서 본인을 참조하는 row들이 여러개 있을 예정.
    my_feeds = db.relationship('Feeds')
    
    
    # 3. 객체 -> dict로 변환 메쏘드 (JSON 응답 내려주는 용도)
    
    # 사용자 입장에서는 게시글 정보가 항상 필요한건 아님.
    
    def get_data_object(self, need_feeds=False):
        data = {
            'id': self.id,
            'email': self.email,
            'name': self.name,
            'phone': self.phone,
            'birth_year': self.birth_year,
            'profile_img_url': f"https://s3.ap-northeast-2.amazonaws.com/lsh.python/{self.profile_img_url}" if self.profile_img_url else None, # 프사가 있다면, S3주소로 가공해서. 없다면 None
            'created_at': str(self.created_at),  # SQLAlchemy의 DateTime은 JSON응답 처리 불가. => str으로 변환해서 리턴.
            'retired_at': str(self.retired_at) if self.retired_at else None,
        }
        
        if need_feeds:
            data['my_feeds'] = [ feed.get_data_object(need_writer=False)  for feed in self.my_feeds ]
        
        # print(f"내 게시글들 : {self.my_feeds}")
        
        
        return data