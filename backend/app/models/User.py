from app.db import Base, get_db
from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import validates, relationship
import bcrypt
salt = bcrypt.gensalt()


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(50), nullable=False, unique=True)
    email = Column(String(50), nullable=False, unique=True)
    password = Column(String(110), nullable=False)
    posts = relationship('Post', back_populates='user')
    
    @validates('email')
    def validate_email(self, key, email):
        assert '@' in email
        return email
    
    @validates('password')
    def validate_password(self, key, password):
        assert len(password) > 8
        return bcrypt.hashpw(password.encode('utf-8'), salt)
    
    def verify_password(self, password):
        return bcrypt.checkpw(
            password.encode('utf-8'),
            self.password.encode('utf-8')
        )
