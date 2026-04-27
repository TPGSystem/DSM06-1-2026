from models.database import db, Teachers
from werkzeug.security import check_password_hash

def authenticate(email, password):
    teacher = Teachers.query.filter_by(eMail=email).first()
    if teacher and check_password_hash(teacher.password, password):
        return teacher
    return None

def get_all():
    return Teachers.query.all()

def get_by_id(id):
    return db.session.get(Teachers, id)

def create(name, eMail, password):
    new = Teachers(name=name, eMail=eMail, password=password)
    db.session.add(new)
    db.session.commit()
    return new

def update(id, name, eMail, password):
    rec = db.session.get(Teachers, id)
    if rec:
        rec.name = name if name is not None else rec.name
        rec.eMail = eMail if eMail is not None else rec.eMail
        if password:
            rec.password = password
        db.session.commit()
    return rec

def delete(id):
    rec = db.session.get(Teachers, id)
    if rec:
        db.session.delete(rec)
        db.session.commit()
    return rec
