from models.database import db, QuestionsTypes

def get_all():
    registers = QuestionsTypes.query.all()
    return [{
        'id': rec.id, 
        'descryption': rec.descryption
    } for rec in registers]

def get_by_id(id):
    rec = QuestionsTypes.query.get(id)
    if rec:
        return {
            'id': rec.id, 
            'descryption': rec.descryption
        }
    return None
