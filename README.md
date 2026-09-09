# QuizApp Django

QuizApp is a web-based multiple-choice quiz platform built with Django. Users can register, authenticate, attempt administrator-created quizzes, receive immediate answer feedback, review mistakes, and inspect personal performance history. Administrators manage quizzes and questions through Django Admin.

## Features

- User registration, login, logout, and password validation
- Quiz catalogue with question counts and descriptions
- Session-backed multiple-choice quiz attempts
- Immediate correctness and score feedback through JSON responses
- Automatic score, percentage, grade, and category breakdown
- Mistake review for completed attempts
- Personal quiz history and average score
- Public aggregate statistics
- Django Admin management for quizzes, questions, results, and answers
- Inline question editing inside the Quiz admin

## Screenshots

The repository currently contains no committed screenshots. Add browser captures of the home, quiz, result, profile, and admin screens under `documentation/screenshots/` before publication, then embed them here.

## Technology Stack

- Python 3.10+ recommended
- Django 6.0.5
- SQLite for local development
- Django Templates, HTML, CSS, and JavaScript
- Django session and authentication frameworks
- Mermaid for architecture and design diagrams

## Architecture

The project follows Django's Model-Template-View architecture. URL patterns dispatch requests to view functions. Views use Django ORM models and sessions, then render templates or return JSON for answer submission. Static CSS and JavaScript provide presentation and client-side interaction.

```text
Browser -> URLconf -> View -> ORM / Session -> Template or JSON response
                                      |
                                  SQLite database
```

## Installation

1. Install Python and verify it is available as `py` on Windows or `python3` on Unix-like systems.
2. Create and activate a virtual environment:

   ```powershell
   py -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

3. Install dependencies:

   ```powershell
   py -m pip install -r requirements.txt
   ```

4. Apply migrations:

   ```powershell
   py manage.py migrate
   ```

5. Create an administrator:

   ```powershell
   py manage.py createsuperuser
   ```

6. Start the development server:

   ```powershell
   py manage.py runserver
   ```

Open `http://127.0.0.1:8000/` for the application and `http://127.0.0.1:8000/admin/` for administration.

## Configuration

Development defaults are defined in `quizproject/settings.py`. For a deployed environment, set:

```powershell
$env:DJANGO_SECRET_KEY = "a-long-random-secret"
$env:DJANGO_DEBUG = "False"
$env:DJANGO_ALLOWED_HOSTS = "example.com,www.example.com"
```

Never commit production secrets. SQLite is suitable for demonstration and small local deployments; PostgreSQL or another managed database is recommended for production.

## Database Setup

The initial application migration is `quizapp/migrations/0001_initial.py`. Run `py manage.py migrate` to create Django authentication, session, admin-log, and QuizApp tables. Local `db.sqlite3` is intentionally ignored by Git.

## Usage

1. Register or log in.
2. Choose an available quiz from the home page.
3. Submit one answer per question.
4. Review the score and category breakdown.
5. Open mistake review or profile history to revisit performance.
6. Administrators create quizzes and questions from `/admin/`.

## Project Structure

```text
quizapp_django/
├── manage.py
├── requirements.txt
├── quizproject/          # Project settings, root URLs, WSGI and ASGI
├── quizapp/              # Domain models, views, URLs, admin, templates and static files
│   ├── migrations/
│   ├── templates/
│   └── static/
├── documentation/        # Mermaid design diagrams
├── PROJECT_REPORT.md     # University project report
└── start_server.bat      # Windows development launcher
```

## Routes

| Route | Purpose | Access |
|---|---|---|
| `/` | Home and quiz catalogue | Public |
| `/statistics/` | Aggregate platform statistics | Public |
| `/register/` | Create an account | Public |
| `/login/` | Authenticate a user | Public |
| `/logout/` | End the current session | Authenticated POST |
| `/quiz/<id>/` | Start a quiz | Authenticated |
| `/quiz/<id>/question/<index>/` | Display a question | Authenticated |
| `/quiz/submit-answer/` | Submit an answer as JSON | Authenticated POST |
| `/quiz/<id>/complete/` | Persist a completed attempt | Authenticated |
| `/result/<id>/` | View an owned result | Authenticated |
| `/result/<id>/review/` | Review owned mistakes | Authenticated |
| `/profile/` | View history and averages | Authenticated |
| `/profile/clear-history/` | Delete own history | Authenticated POST |
| `/admin/` | Manage application data | Staff/superuser |

## Code Quality and Security Notes

The repository uses Django authentication, CSRF middleware, session state, and ORM queries. Result pages now enforce ownership, answer submission is tied to the active quiz session, quiz completion requires a complete active attempt, and statistics use a database aggregate. Before production deployment, add automated tests, move to a production database, configure HTTPS/security headers, and replace the session payload with server-side attempt records.

## Future Improvements

- Add comprehensive automated tests and continuous integration
- Introduce a dedicated `QuizAttempt` model for reliable progress and timing
- Store answer keys as stable option identifiers rather than answer text
- Add pagination, search, filtering, and question banks
- Add accessibility review and responsive screenshot evidence
- Use PostgreSQL and a production WSGI/ASGI deployment

## Author

Patrick Nyan Suah

## License

No license is currently declared in the source repository. Add an explicit license before accepting external contributions or redistributing the project.
