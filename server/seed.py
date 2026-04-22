from config import app, db, bcrypt
from models import User, Note

with app.app_context():
    # Clear old data
    Note.query.delete()
    User.query.delete()
    db.session.commit()

    # Create 2 users
    hashed = bcrypt.generate_password_hash("password123").decode("utf-8")

    alice = User(username="alice", email="alice@email.com", password=hashed)
    bob   = User(username="bob",   email="bob@email.com",   password=hashed)

    db.session.add_all([alice, bob])
    db.session.commit()

    # Give each user 3 notes
    notes = [
        Note(title="Alice Note 1", content="Alice's first note.",  user_id=alice.id),
        Note(title="Alice Note 2", content="Alice's second note.", user_id=alice.id),
        Note(title="Alice Note 3", content="Alice's third note.",  user_id=alice.id),
        Note(title="Bob Note 1",   content="Bob's first note.",    user_id=bob.id),
        Note(title="Bob Note 2",   content="Bob's second note.",   user_id=bob.id),
        Note(title="Bob Note 3",   content="Bob's third note.",    user_id=bob.id),
    ]

    db.session.add_all(notes)
    db.session.commit()

    print("Seeded: 2 users, 6 notes. Password for both is: password123")