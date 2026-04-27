from models.database import db, Components

def get_all():
    registers = Components.query.all()
    return [{
        'id': rec.id, 
        'descryption': rec.descryption
    } for rec in registers]

def get_by_id(id):
    rec = Components.query.get(id)
    if rec:
        return {
            'id': rec.id, 
            'descryption': rec.descryption
        }
    return None