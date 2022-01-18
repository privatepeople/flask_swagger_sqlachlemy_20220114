from server import db

class Lectures(db.Model):
    __tablename__ = 'lectures'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(20), nullable=False)
    campus = db.Column(db.String(20), nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    teacher = db.relationship('Users')
    
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