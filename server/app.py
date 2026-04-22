from flask import request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from config import app, db
from models import User, Note


# ── CORS — lets the React frontend on port 4000 talk to this API ──────────
@app.after_request
def add_cors(response):
    response.headers["Access-Control-Allow-Origin"]  = "*"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, PATCH, DELETE, OPTIONS"
    return response

@app.route("/<path:path>", methods=["OPTIONS"])
def options(path):
    return {}, 200


# ── SIGNUP ────────────────────────────────────────────────────────────────
@app.route("/signup", methods=["POST"])
def signup():
    data = request.get_json()

    if not data.get("username") or not data.get("email") or not data.get("password"):
        return jsonify({"errors": ["Username, email, and password are required."]}), 422

    if User.query.filter_by(username=data["username"]).first():
        return jsonify({"errors": ["Username already taken."]}), 422

    user = User(username=data["username"], email=data["email"])
    user.set_password(data["password"])
    db.session.add(user)
    db.session.commit()

    token = create_access_token(identity=user.id)
    return jsonify({"user": user.to_dict(), "token": token}), 201


# ── LOGIN ─────────────────────────────────────────────────────────────────
@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data.get("username")).first()

    if not user or not user.check_password(data.get("password", "")):
        return jsonify({"errors": ["Invalid username or password."]}), 401

    token = create_access_token(identity=user.id)
    return jsonify({"user": user.to_dict(), "token": token}), 200


# ── ME ────────────────────────────────────────────────────────────────────
@app.route("/me", methods=["GET"])
@jwt_required()
def me():
    user = User.query.get(get_jwt_identity())
    if not user:
        return jsonify({"errors": ["Not found."]}), 404
    return jsonify(user.to_dict()), 200


# ── NOTES LIST + CREATE ───────────────────────────────────────────────────
@app.route("/notes", methods=["GET", "POST"])
@jwt_required()
def notes():
    user_id = get_jwt_identity()

    if request.method == "GET":
        page = request.args.get("page", 1, type=int)
        p    = Note.query.filter_by(user_id=user_id).paginate(page=page, per_page=5)
        return jsonify({
            "notes":        [n.to_dict() for n in p.items],
            "total_pages":  p.pages,
            "current_page": p.page
        }), 200

    data = request.get_json()
    if not data.get("title") or not data.get("content"):
        return jsonify({"errors": ["Title and content are required."]}), 422

    note = Note(title=data["title"], content=data["content"], user_id=user_id)
    db.session.add(note)
    db.session.commit()
    return jsonify(note.to_dict()), 201


# ── NOTE UPDATE + DELETE ──────────────────────────────────────────────────
@app.route("/notes/<int:id>", methods=["PATCH", "DELETE"])
@jwt_required()
def note_detail(id):
    user_id = get_jwt_identity()
    note    = Note.query.get(id)

    if not note:
        return jsonify({"errors": ["Note not found."]}), 404
    if note.user_id != user_id:
        return jsonify({"errors": ["Unauthorized."]}), 403

    if request.method == "DELETE":
        db.session.delete(note)
        db.session.commit()
        return jsonify({}), 204

    data = request.get_json()
    if "title"   in data: note.title   = data["title"]
    if "content" in data: note.content = data["content"]
    db.session.commit()
    return jsonify(note.to_dict()), 200


if __name__ == "__main__":
    app.run(port=5555, debug=True)