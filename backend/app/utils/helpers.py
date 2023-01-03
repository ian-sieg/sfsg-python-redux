from app.db import get_db
from app.models import User
# @bp.route('/get-user', methods=['GET'])
def get_user(uid):
    db = get_db()
    user = db.query(User).filter(User.id == uid).one()
    return {"id": user.id, "username": user.username, "email": user.email}