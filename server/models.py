from config import db, bcrypt


class User(db.Model):
    id       = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    email    = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)  # bcrypt hash
    notes    = db.relationship("Note", backref="user", cascade="all, delete")

    def set_password(self, plain):
        self.password = bcrypt.generate_password_hash(plain).decode("utf-8")

    def check_password(self, plain):
        return bcrypt.check_password_hash(self.password, plain)

    def to_dict(self):
        return {"id": self.id, "username": self.username, "email": self.email}


class Note(db.Model):
    id      = db.Column(db.Integer, primary_key=True)
    title   = db.Column(db.String, nullable=False)
    content = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    def to_dict(self):
        return {
            "id":      self.id,
            "title":   self.title,
            "content": self.content,
            "user_id": self.user_id
        }