from datetime import datetime

from utils.database import Column, Model, SurrogatePK, db, relationship


ad_category_table = db.Table(
    'ad_category',
    Column('category_id', db.ForeignKey('categories.id'), primary_key=True),
    Column('ad_id', db.ForeignKey('ads.id'), primary_key=True)
)


class Category(SurrogatePK, Model):
    __tablename__ = 'categories'

    name = Column(db.String(80), unique=True, nullable=False)
    ads = relationship('Ad', secondary=ad_category_table, back_populates='categories')

    def __init__(self, name, **kwargs):
        db.Model.__init__(self, name=name, **kwargs)

    def __repr__(self):
        return self.name


class Ad(SurrogatePK, Model):
    __tablename__ = 'ads'

    user_id = Column(db.Integer, db.ForeignKey('users.id'))
    text_description = Column(db.Text, nullable=False)
    location = Column(db.String(100), nullable=False)
    price = Column(db.Integer, nullable=False)
    user_phone_number = Column(db.String(100), nullable=True)
    categories = relationship('Category', secondary=ad_category_table, back_populates='ads')
    is_paid = Column(db.Boolean, default=False)

    def __init__(self, **kwargs):
        db.Model.__init__(self, **kwargs)

    def __repr__(self):
        return f'<Ad {self.text_description}>'


class Message(SurrogatePK, Model):
    __tablename__ = 'messages'

    sender_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    recipient_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    text = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return f'<Message {self.text}>'
