from base import db

class LoginVO(db.Model):
    __tablename__ = 'login_table'
    login_id = db.Column('login_id',db.Integer, primary_key=True, autoincrement=True)
    login_email = db.Column('login_email',db.String(50), unique=True,
                        nullable=False)
    login_password = db.Column('login_password',db.String(50), unique=True, nullable=False)
    login_role = db.Column('login_role',db.String(50), unique=True, nullable=False)
    login_status = db.Column('login_status',db.String(50), unique=True, nullable=False)

    def as_dict(self):
        return {
            'login_id': self.login_id,
            'login_email': self.login_email,
            'login_password': self.login_password,
            'login_role': self.login_role,
            'login_status': self.login_status
        }

db.create_all()