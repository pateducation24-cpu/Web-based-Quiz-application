# System Architecture

```mermaid
flowchart LR
    Browser[Web Browser] --> URLs[Django URLconf]
    URLs --> Views[QuizApp Views]
    Views --> Auth[Django Authentication]
    Views --> Session[Session Store]
    Views --> ORM[Django ORM]
    ORM --> DB[(SQLite Database)]
    Views --> Templates[Django Templates]
    Views --> JSON[Answer JSON Response]
    Templates --> Browser
    JSON --> Browser
    Admin[Django Admin] --> ORM
```

The browser is the presentation client. Django URL patterns dispatch requests to view functions. Views coordinate authentication, session state, ORM operations, template rendering, and JSON responses. SQLite stores application and Django framework data.
