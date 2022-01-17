# 사용자에 관련된 기능을 수행하는 클래스.
# 메쏘드를 만들때, get / post / put / patch / delete로 ㅁ나들면, 알아서 메쏘드로 세팅되도록.

from flask_restful import Resource, reqparse
from flask_restful_swagger_2 import swagger

from server.model import Users # users 테이블에 연결할 클래스를 가져오기.

from server import db # DB에 INSERT / UPDATE 등의 반영을 하기 위한 변수.

# 각 메쏘드별로 파라미터를 받아보자.

# post메쏘드에서 사용할 파라미터
post_parser = reqparse.RequestParser() # post로 들어오는 파라미터를 확인해볼 변수
post_parser.add_argument('email', type=str, required=True, location='form') #파라미터 이름, 데이터 타입, 필수여부, 첨부된 곳
post_parser.add_argument('password', type=str, required=True, location='form')

# 회원가입에 사용할 4가지 파라미터 추가 / swagger를 통해서도 받아보자.
# put_parser / email, password, name, phone 4가지 변수.
# put 메쏘드에서 받아서 로그로만 출력
# swagger 문서 작업

put_parser = reqparse.RequestParser()
put_parser.add_argument('email', type=str, required=True, location='form')
put_parser.add_argument('password', type=str, required=True, location='form')
put_parser.add_argument('name', type=str, required=True, location='form')
put_parser.add_argument('phone', type=str, required=True, location='form')

class User(Resource):
    
    @swagger.doc({
        'tags': ['user'], # 어떤 종류의 기능인지 분류.
        'description': '사용자 정보 조회',
        'parameters': [
            # dict로 파라미터들 명시
        ],
        'responses': {
            # 200일때의 응답 예시, 400일때의 예시 등.
            '200': {
                'description': '사용자 정보 조회 성공',
            },
            '400': {
                'description': '사용자 정보 조회 실패',
            }
        }
    })
    def get(self):
        """사용자 정보 조회"""
        return {
            "임시": "사용자 정보 조회"
        }
    
    
    @swagger.doc({
        'tags': ['user'], # 어떤 종류의 기능인지 분류.
        'description': '로그인',
        'parameters': [
            {
                'name': 'email',
                'description': '로그인에 사용할 이메일',
                'in': 'formData', # query, formData 중 택일 (header 도 향후 사용)
                'type': 'string', # string, integer, number (float), boolean 중 택일 (향후 file 도 사용 예정),
                'required': True  # 필수 첨부 여부
            },
            {
                'name': 'password',
                'description': '로그인에 사용할 비밀번호',
                'in': 'formData', # query, formData 중 택일 (header 도 향후 사용)
                'type': 'string', # string, integer, number (float), boolean 중 택일 (향후 file 도 사용 예정),
                'required': True  # 필수 첨부 여부
            },
        ],
        'responses': {
            # 200일때의 응답 예시, 400일때의 예시 등.
            '200': {
                'description': '로그인 성공',
            },
            '400': {
                'description': '로그인 실패',
            }
        }
    })
    def post(self):
        """로그인"""
        
        # 받아낸 파라미터들을 dict 변수에 담아두자.
        args = post_parser.parse_args()
        
        # 1단계 검사 : 이메일 있는지?
        # 통과시 2단계 추가 검사 : 비번도 맞는지?
        
        login_user = Users.query\
            .filter(Users.email == args['email'])\
            .first()
            
        # None으로 나온다면? 이메일 부터 틀렸다.
        
        if login_user == None:
            return {
                'code': 400,
                'message': '잘못된 이메일 입니다.'
            }, 400
        
        
        # login_user가 실제로 있는 상황.
        
        # login_user의 password가 실제 존재 vs 파라미터의 패스워드 비교
        # DB에 추가 쿼리 조회 필요 없음
        
        if login_user.password == args['password']:
            # 이메일이 맞는 사용자 -> 비밀번호와 파라미터의 비밀번호가 같다.
            # 로그인 성공
            return {
                'code': 200,
                'message': '로그인 성공',
                'data': {
                    'user': login_user.get_data_object()
                }
            }
        else:
            # 로그인 실패 -> None으로 비어있다.
            return {
                'code': 400,
                'message': '로그인 실패'
            }, 400


    @swagger.doc({
        'tags': ['user'], # 어떤 종류의 기능인지 분류.
        'description': '회원가입',
        'parameters': [
            {
                'name': 'email',
                'description': '회원가입에 사용할 이메일',
                'in': 'formData',
                'type': 'string',
                'required': True
            },
            {
                'name': 'password',
                'description': '회원가입에 사용할 비밀번호',
                'in': 'formData',
                'type': 'string',
                'required': True
            },
            {
                'name': 'name',
                'description': '회원가입에 사용할 본명',
                'in': 'formData',
                'type': 'string',
                'required': True
            },
            {
                'name': 'phone',
                'description': '회원가입에 사용할 전화번호',
                'in': 'formData',
                'type': 'string',
                'required': True
            },
        ],
        'responses': {
            # 200일때의 응답 예시, 400일때의 예시 등.
            '200': {
                'description': '회원가입 성공',
            },
            '400': {
                'description': '이메일 중복 가입 실패',
            }
        }
    })
    def put(self):
        """회원가입"""
        
        args = put_parser.parse_args()
        
        
        # 이미 사용중인 이메일이라면 400 리턴.
        
        already_email_user = Users.query\
            .filter(Users.email == args['email'])\
            .first()
        
        if already_email_user:
            # 이미 이메일을 사용중인 사용자가 있다.
            return {
                'code': 400,
                'message': '이미 사용중인 이메일입니다.'
            }, 400
            
            
        # 이미 사용중인 연락처라면 (폰이라면), 가입 불허.
        
        
        
        
        
        # 파리미터들을 => users 테이블의 row로 추가. (INSERT INTO -> ORM SQLAlchemy로)
        
        # 객체지향 : 새로운 데아터 추가 -> 새 인스턴스를 만들자.
        
        new_user = Users()
        new_user.email = args['email']
        new_user.password = args['password']
        new_user.name = args['name']
        new_user.phone = args['phone']
        
        # new_user의 객체를 -> DB에 등록 준비 -> 확정.
        
        db.session.add(new_user)
        db.session.commit()
        
        return {
            "code": 200,
            "message": '회원가입 성공',
            'data': {
                'user': new_user.get_data_object()
            }
        }