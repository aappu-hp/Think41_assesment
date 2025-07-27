# backend/app/crud.py
def get_all(session, Model):
    return session.query(Model).all()

def get_by_id(session, Model, _id):
    return session.query(Model).get(_id)

def create(session, obj):
    session.add(obj)
    session.commit()
    session.refresh(obj)
    return obj
