from server import db


class LectureUser(db.Model):
    __tablename__ = 'lecture_user'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    lecture_id = db.Column(db.Integer, db.ForeignKey('lectures.id'))
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    
    # dict 로 변경해주는 함수 X