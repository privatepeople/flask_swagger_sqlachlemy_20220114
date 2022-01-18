from server import db

class Lectures(db.Model):
    __tablename__ = 'lectures'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(20), nullable=False)
    campus = db.Column(db.String(20), nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    teacher = db.relationship('Users') # 강의의 입장에서, 강사를 찾아가자. 가능함.
    # 정석 : 부모가 => 자식을 여러개 보유. + 부모를 찾아올 길.
    # 편의 : 자식의 입장에서 => 부모를 찾아가자.
    
    
    feeds = db.relationship('Feeds', backref='lecture')
    
    def get_data_object(self, need_teacher_info=False):
        data = {
            'id': self.id,
            'title': self.title,
            'campus': self.campus,
            'teacher_id': self.teacher_id,
        }
        
        if need_teacher_info:
            data['teacher'] = self.teacher.get_data_object()
        
        return data