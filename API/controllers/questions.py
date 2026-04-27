from models.database import db, Questions

def get_all():
    registers = Questions.query.all()
    return [{
        'id': rec.id, 
        'idQuestionType': rec.idQuestionType,
        'dsQuestionType': rec.questionType.descryption if rec.questionType else None,
        'idRegion': rec.idRegion,
        'dsRegion': rec.region.descryption if rec.region else None,
        'idTheme': rec.idTheme,
        'dsThema': rec.theme.descryption if rec.theme else None,
        'question': rec.question,
        'response1': rec.response1,
        'response2': rec.response2,
        'response3': rec.response3,
        'response4': rec.response4,
        'idValidation1': rec.idValidation1,
        'dsValidation1': rec.validation1.descryption if rec.validation1 else None,
        'idValidation2': rec.idValidation2,
        'dsValidation2': rec.validation2.descryption if rec.validation2 else None,
        'idValidation3': rec.idValidation3,
        'dsValidation3': rec.validation3.descryption if rec.validation3 else None,
        'idValidation4': rec.idValidation4,
        'dsValidation4': rec.validation4.descryption if rec.validation4 else None
    } for rec in registers]

def get_by_id(id):
    rec = Questions.query.get(id)
    if rec:
        return {
            'id': rec.id, 
            'idQuestionType': rec.idQuestionType,
            'dsQuestionType': rec.questionType.descryption if rec.questionType else None,
            'idRegion': rec.idRegion,
            'dsRegion': rec.region.descryption if rec.region else None,
            'idTheme': rec.idTheme,
            'dsThema': rec.theme.descryption if rec.theme else None,
            'question': rec.question,
            'response1': rec.response1,
            'response2': rec.response2,
            'response3': rec.response3,
            'response4': rec.response4,
            'idValidation1': rec.idValidation1,
            'idValidation2': rec.idValidation2,
            'idValidation3': rec.idValidation3,
            'idValidation4': rec.idValidation4
        }
    return None

def create(idQuestionType, idRegion, idTheme, question, response1, response2, response3, response4, picture1, picture2, picture3, picture4, idValidation1, idValidation2, idValidation3, idValidation4):
    new = Questions(idQuestionType=idQuestionType, idRegion=idRegion, idTheme=idTheme, question=question,
                    response1=response1, response2=response2, response3=response3, response4=response4,
                    picture1=picture1, picture2=picture2, picture3=picture3, picture4=picture4,
                    idValidation1=idValidation1, idValidation2=idValidation2, idValidation3=idValidation3, idValidation4=idValidation4)
    db.session.add(new)
    db.session.commit()
    return new

def update(id, idQuestionType, idRegion, idTheme, question, response1, response2, response3, response4, picture1, picture2, picture3, picture4, idValidation1, idValidation2, idValidation3, idValidation4):
    rec = Questions.query.get(id)
    if rec:
        rec.idQuestionType = idQuestionType if idQuestionType is not None else rec.idQuestionType
        rec.idRegion = idRegion if idRegion is not None else rec.idRegion
        rec.idTheme = idTheme if idTheme is not None else rec.idTheme
        rec.question = question if question is not None else rec.question
        rec.response1 = response1 if response1 is not None else rec.response1
        rec.response2 = response2 if response2 is not None else rec.response2
        rec.response3 = response3 if response3 is not None else rec.response3
        rec.response4 = response4 if response4 is not None else rec.response4
        rec.picture1 = picture1 if picture1 is not None else rec.picture1
        rec.picture2 = picture2 if picture2 is not None else rec.picture2
        rec.picture3 = picture3 if picture3 is not None else rec.picture3
        rec.picture4 = picture4 if picture4 is not None else rec.picture4
        rec.idValidation1 = idValidation1 if idValidation1 is not None else rec.idValidation1
        rec.idValidation2 = idValidation2 if idValidation2 is not None else rec.idValidation2
        rec.idValidation3 = idValidation3 if idValidation3 is not None else rec.idValidation3
        rec.idValidation4 = idValidation4 if idValidation4 is not None else rec.idValidation4
        db.session.commit()
    return rec

def delete(id):
    rec = Questions.query.get(id)
    if rec:
        db.session.delete(rec)
        db.session.commit()
        return True
    return False
