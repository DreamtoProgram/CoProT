from app import db

class Problem(db.Model):

    __tablename__ = 'problems'

    problem_id = db.Column(
        db.Integer,
        primary_key =True,
        autoincrement = True
    )

    problem_name = db.Column(
        db.String(300),
        nullable = False
    )

    difficulty = db.Column(
        db.String(20),
        nullable = False
    )

    attempts = db.Column(
        db.Integer,
        default = 1
    )

    has_universal_pattern = db.Column(
    db.Boolean,
    default=False
    )