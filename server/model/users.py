# DB의 users 테이블에 연결되는 클래스
from server import db

class Users(db.Model):
    # SQLAlchemy 라이브러리의 Model 클래스 활용.
    
    # 1. 어느 테이블? 연결 명시
    __tablename__ = 'users' # DB 테이블 이름
    
    # 2. 어떤 변수 / 어떤 컬럼 연결 명시 => 변수 이름이 컬럼 이름과 같아야함.
    id = db.Column(db.Integer, primary_key=True) # id컬럼은 int / 기본키라고 명시
    email = db.Column(db.String(50), nullable=False, default='이메일 미입력') # email 컬럼은, 50자 문구, null 불가, 기본값 있다.
    password = db.Column(db.String(50), nullable=False)
    name = db.Column(db.String(20), nullable=False)
    phone = db.Column(db.String(15)) # nullable의 기본값은 null 허용.
    
    # 3. 객체 -> dict로 변환 메쏘드 (응답 내려주는 용도)
    
    def get_data_object(self):
        data = {
            'id': self.id,
            'email': self.email,
            'name': self.name,
            'phone_num': self.phone
        }
        
        return data