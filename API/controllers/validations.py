from models.database import db, Validations

def get_all():
    registers = Validations.query.all()
    return [{
        'id': rec.id, 
        'descryption': rec.descryption
    } for rec in registers]

def get_by_id(id):
    rec = Validations.query.get(id)
    if rec:
        return {
            'id': rec.id, 
            'descryption': rec.descryption
        }
    return None
