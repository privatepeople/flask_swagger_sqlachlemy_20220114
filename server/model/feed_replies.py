from server import db

class FeedReplies(db.Model):
    __tablename__ = 'feed_replies'
    
    id = db.Column(db.Integer, primary_key=True)
    feed_id = db.Column(db.Integer, db.ForeignKey('feeds.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    content = db.Column(db.TEXT, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    
    
    def get_data_object(self):
        data = {
            'id': self.id,
            'feed_id': self.feed_id,
            'user_id': self.user_id,
            'content': self.content,
            'created_at': str(self.created_at),
        }
        
        print('내 부모 : ', self.feed)
        
        return data