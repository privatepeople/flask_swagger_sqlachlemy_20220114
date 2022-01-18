from server import db

class FeedImages(db.Model):
    __tablename__ = 'feed_images'
    
    id = db.Column(db.Integer, primary_key=True)
    feed_id = db.Column(db.Integer, db.ForeignKey('feeds.id')) # users테이블의 id컬럼으로 가는 외래키.
    img_url = db.Column(db.String(200)) # null이면, 특정 강의에 대한 글 아님.
    
    

    def get_data_object(self, need_writer=True):
        data = {
            'id': self.id,
            'feed_id': self.feed_id,
            'img_url': self.img_url,
        }
        

        
        return data