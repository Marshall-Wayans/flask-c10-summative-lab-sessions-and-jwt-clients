# Notes API

A simple Flask REST API for managing personal notes with JWT authentication.

## Description

Users sign up, log in, and manage their own notes. Users can only see and edit their own notes.

## Installation

First, clone the repository and navigate into the server folder. Once you're inside, install the dependencies using pipenv and activate the virtual environment.

After that, run the database migrations to set up your tables, then seed the database with some starter data.

The server runs on http://localhost:5000 by default. To start it, use pipenv to run Flask.

---

## Authentication

Every note-related endpoint requires you to be logged in. When you log in via the login route, you get back a JWT token. You'll need to include that token in the Authorization header of any request you make to a protected route, using the Bearer scheme.

---

## Endpoints

### Auth

| Method | Route | Description | Auth Required |
|--------|-------|-------------|---------------|
| POST | `/signup` | Register a new user | No |
| POST | `/login` | Log in and receive a JWT token | No |
| POST | `/logout` | Log out and invalidate the session | Yes |

### Notes

| Method | Route | Description | Auth Required |
|--------|-------|-------------|---------------|
| GET | `/notes` | Get all notes belonging to the current user | Yes |
| POST | `/notes` | Create a new note | Yes |
| GET | `/notes/:id` | Fetch a specific note by ID | Yes |
| PUT | `/notes/:id` | Update an existing note | Yes |
| DELETE | `/notes/:id` | Delete a note | Yes |

---

## Seed Data

The seed file creates two users — alice and bob — each with three notes. The password for both accounts is password123.

---

## Tech Stack

- **Framework:** Flask
- **Auth:** Flask-JWT-Extended and Flask-Bcrypt
- **Database:** SQLite via Flask-SQLAlchemy
- **Migrations:** Flask-Migrate