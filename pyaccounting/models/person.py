# third-party imports
from flask_login import UserMixin

# Local library imports
from pyaccounting import db, login_manager, bcrypt

# setup user_loader
@login_manager.user_loader
def load_user(user_id):
    return PersonModel.query.get(int(user_id))


class PersonModel(UserMixin, db.Model):
    """ Create a Person table """
    __tablename__ = 'persons'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(60), index=True, unique=True)
    email = db.Column(db.String(60), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    image_file = db.Column(db.String(20), nullable=False, default='default.png')
    is_admin = db.Column(db.Boolean, default=False)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(),
            onupdate=db.func.current_timestamp())

    @property
    def password(self):
        """
        Prevent pasword from being accessed
        """
        raise AttributeError('password is not a readable attribute.')

    @password.setter
    def password(self, password):
        """
        Set password to a hashed password
        """
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        """
        Check if hashed password matches actual password
        """
        return bcrypt.check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {
                'id': self.id,
                'username': self.username,
                'email': self.email,
                }

    def __repr__(self):
        return f"<Person: '{self.username}' '{self.email}'>"

