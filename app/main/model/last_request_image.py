from .. import db, flask_bcrypt


class LastRequestImage(db.Model):

    __tablename__ = "dbo.tb_last_request_image"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    key = db.Column(db.String(255), unique=True, nullable=False)
    data_init = db.Column(db.DateTime, nullable=False)
    data_last_request = db.Column(db.DateTime, nullable=False)
