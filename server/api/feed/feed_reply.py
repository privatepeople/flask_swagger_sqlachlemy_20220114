from flask import current_app, g
from flask_restful import Resource, reqparse
from flask_restful_swagger_2 import swagger

from server import db
from server.model import FeedReplies
from server.api.utils import token_required

post_parser = reqparse.RequestParser()
post_parser.add_argument('feed_id', type=int, required=True, location='form')
post_parser.add_argument('content', type=str, required=True, location='form')

class FeedReply(Resource):
    
    @swagger.doc({
        'tags': ['feed/reply'],
        'description': '게시글에 댓글 작성하기',
        'parameters': [
            {
                'name': 'X-Http-Token',
                'description': '어느 사용자인지를, 토큰으로',
                'in': 'header',
                'type': 'string',
                'required': True
            },
            {
                'name': 'feed_id',
                'description': '어느 피드에 남긴 댓글인지',
                'in': 'formData',
                'type': 'integer',
                'required': True
            },
            {
                'name': 'content',
                'description': '댓글 내용',
                'in': 'formData',
                'type': 'string',
                'required': True
            },
            
        ],
        'responses': {
            '200': {
                'description': '등록 성공',
            },
            '400': {
                'description': '등록 실패',
            }
        }
    })
    @token_required
    def post(self):
        """ 댓글 등록하기 """
        args = post_parser.parse_args()
        
        user = g.user  # 전역변수에 저장된, 토큰에서 뽑아낸 사용자를 변수에 저장.
                
        return {
            'code': 200,
            'message': '댓글 등록 성공',
            # 'data': {
            #     'feed': new_feed.get_data_object()
            # }
        }
    