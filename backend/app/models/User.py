from app.db import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import validates, relationship
import bcrypt
salt = bcrypt.gensalt()


class User(Base):
    __tablename__ = 'users'
    id = Column(String(100), primary_key=True)
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
    
    # def allUsers():
    #     users = db.query(User).all()
    #     return [{"id": i.id, "public_id": i.public_id, "username": i.username, "email": i.email, "password": i.pwd} for i in users]
    
    # def getUser(uid):
    #     user = db.query(User).filter(User.id == uid).one()
    #     return {"id": user.id, "public_id": user.public_id, "username": user.username, "email": user.email, "password": user.pwd}
    
    # def addUser(username, email, password):
    #     if username and email and password:
    #         try:
    #             user = User(username, email, password)
    #             db.add(user)
    #             db.commit()
    #             return True
    #         except Exception as e:
    #             print(e)
    #             return False
    #     else:
    #         return False
    
    # def deleteUser(uid):
    #     if uid:
    #         try:
    #             user = db.query(User).get(uid)
    #             db.delete(user)
    #             db.commit()
    #         except Exception as e:
    #             print(e)
    #             return False
    #     else:
    #         return False
