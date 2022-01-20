import datetime

from flask import g
from flask_restful import Resource, reqparse
from flask_restful_swagger_2 import swagger

from server import db
from server.model import Lectures
from server.api.utils import token_required, admin_required

post_parser = reqparse.RequestParser()
post_parser.add_argument('title', type=str, required=True, location='form')
post_parser.add_argument('campus', type=str, required=True, location='form')
post_parser.add_argument('fee', type=int, required=True, location='form')

patch_parser = reqparse.RequestParser()
patch_parser.add_argument('lecture_id', type=int, required=True, location='form')
patch_parser.add_argument('field', type=str, required=True, location='form')
patch_parser.add_argument('value', type=str, required=True, location='form')

class AdminLecture(Resource):
    
    @swagger.doc({
        'tags':['admin'],
        'description':'관리자 - 강의 과목 추가',
        'parameters': [
            {
                'name': 'X-Http-Token',
                'description': '사용자 인증용 헤더 - 관리자만 OK',
                'in': 'header',
                'type': 'string',
                'required': True,
            },
            {
                'name': 'title',
                'description': '강의의 제목',
                'in': 'formData',
                'type': 'string',
                'required': True,
            },
            {
                'name': 'campus',
                'description': '강의가 열리는 캠퍼스 이름',
                'in': 'formData',
                'type': 'string',
                'required': True,
            },
            {
                'name': 'fee',
                'description': '수강료',
                'in': 'formData',
                'type': 'integer',
                'required': True,
            },
        ],
        'responses': {
            '200': {
                'description': '관리자 강의 등록 성공'
            }
        }
    })
    @token_required
    @admin_required
    def post(self):
        """ 관리자 - 강의 추가 등록 """
        
        args = post_parser.parse_args()
        
        lecture = Lectures()
        lecture.title = args['title']
        lecture.campus = args['campus']
        lecture.fee = args['fee']
        
        db.session.add(lecture)
        db.session.commit()
        
        return {
            'code':200,
            'message': '관리자 - 강의 추가등록 성공',
        }
        
    @swagger.doc({
        'tags':['admin'],
        'description':'관리자 - 강의 과목의 정보항목 수정',
        'parameters': [
            {
                'name': 'X-Http-Token',
                'description': '사용자 인증용 헤더 - 관리자만 OK',
                'in': 'header',
                'type': 'string',
                'required': True,
            },
            {
                'name': 'lecture_id',
                'description': '몇번 강의를 수정하고 싶은지',
                'in': 'formData',
                'type': 'integer',
                'required': True,
            },
            {
                'name': 'field',
                'description': '어느 항목을 수정하고 싶은지 - title, campus, fee, teacher_id 중 택일',
                'in': 'formData',
                'type': 'string',
                'enum': ['title', 'campus', 'fee', 'teacher_id'],
                'required': True,
            },
            {
                'name': 'value',
                'description': '어떤 값으로 수정해줄건지 실제 입력값',
                'in': 'formData',
                'type': 'string', # int값이 필요하면 형변환.
                'required': True,
            },
        ],
        'responses': {
            '200': {
                'description': '관리자 강의 정보 수정 성공'
            }
        }
    })
    @token_required
    @admin_required
    def patch(self):
        """ 관리자 - 강의 정보항목 수정 """
        
        args = patch_parser.parse_args()
        
        # 실존하는 강의를 수정하는지?
        
        lecture = Lectures.query.filter(Lectures.id == args['lecture_id']).first()
        
        if lecture == None:
            return {
                'code': 400,
                'message': '해당 강의는 존재하지 않습니다.'
            }, 400
            
        if args['field'] == 'title':
            lecture.title = args['value']  
        elif args['field'] == 'campus':
            lecture.campus = args['value']
        elif args['field'] == 'fee':
            lecture.fee = int(args['value'])
        elif args['field'] == 'teacher_id':
            lecture.teacher_id = int(args['value'])
        else:
            return {
                'code': 400,
                'message': 'field 항목에 지원하지 않는 값이 들어왔습니다.'
            }
        
        db.session.add(lecture)
        db.session.commit()
        
        return {
            'code':200,
            'message': '관리자 - 강의 항목 변경 성공',
        }