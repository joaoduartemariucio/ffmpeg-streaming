from app.main import db, flask_bcrypt


class AppSecretKey(db.Model):

    __tablename__ = "dbo.tb_app_secret_key"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    app_name = db.Column(db.String(255), unique=True, nullable=False)
    app_secret = db.Column(db.String(100), nullable=False)
    create_secret_in = db.Column(db.DateTime, nullable=False)

    @property
    def app_secret(self):
        raise AttributeError('app_secret: write-only field')

    @app_secret.setter
    def app_secret(self, app_secret):
        self.app_secret = flask_bcrypt.generate_password_hash(app_secret).decode('utf-8')

    def check_password(self, app_secret):
        return flask_bcrypt.check_password_hash(self.app_secret, app_secret)

    def __repr__(self):
        return "<AppSecretKey '{}'>".format(self.app_name)