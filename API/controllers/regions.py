from models.database import db, Regions

def get_all():
    registers = Regions.query.all()
    return [{
        'id': rec.id, 
        'descryption': rec.descryption
    } for rec in registers]

def get_by_id(id):
    rec = Regions.query.get(id)
    if rec:
        return {
            'id': rec.id, 
            'descryption': rec.descryption
        }
    return None
