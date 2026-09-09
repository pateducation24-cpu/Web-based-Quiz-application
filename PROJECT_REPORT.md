# Web-Based Quiz Application

## Title Page

**Project Title:** Web-Based Quiz Application (QuizApp)  
**Student:** Patrick Nyan Suah  
**University:** Institutional name not specified in the source repository  
**Department:** Department not specified in the source repository  
**Academic Year:** 2026  

This report describes the Django project contained in this repository. Institutional details should be completed on the final printed submission cover sheet if required by the university.

## Certificate

This is to certify that the project entitled **Web-Based Quiz Application (QuizApp)** is a software development project prepared by **Patrick Nyan Suah** during the 2026 academic year. The work demonstrates the analysis, design, implementation, and testing of a database-backed web application using the Django framework. The project is presented for academic evaluation in accordance with the requirements of the relevant programme.

**Supervisor:** ____________________  
**Signature:** _____________________  
**Date:** _________________________  

## Acknowledgement

I acknowledge the guidance of my lecturers, supervisor, classmates, and the wider Python and Django developer community during the development of this project. The Django documentation, Python standard library documentation, and open-source web development practices provided the technical foundation for authentication, database access, URL routing, template rendering, sessions, and administration. I am also grateful to everyone who provided feedback on the usability of online assessment systems and helped clarify the need for simple, immediate, and reviewable quiz feedback.

## Abstract

QuizApp is a web-based multiple-choice assessment system developed with Python and Django. The system addresses a common educational need: providing learners with a convenient way to practise knowledge, receive immediate feedback, and monitor performance over time. Traditional paper-based quizzes require manual marking, provide delayed feedback, and make it difficult to maintain a personal history of performance. QuizApp provides a centralised workflow in which an administrator creates quizzes and questions, users register and authenticate, users attempt available quizzes, and the application calculates and stores results automatically.

The application uses Django's Model-Template-View architecture. The data layer contains models for quizzes, questions, quiz results, and individual user answers. Django's built-in User model provides identity and authentication, while the session framework temporarily maintains the active quiz state during an attempt. URL patterns connect browser requests to view functions. Templates present the home page, authentication screens, quiz questions, results, mistake review, profile history, and aggregate statistics. A JSON endpoint handles answer submission so that correctness, earned points, and the next question can be returned without a complete page reload. Administrators use Django Admin to manage quizzes and questions, including inline question editing.

The project demonstrates several important web application concepts: relational database design, foreign-key relationships, authentication and authorization, form validation, CSRF protection, session management, server-side rendering, and administrative workflows. Quiz results contain the total score, possible score, percentage, completion timestamp, and answer-level records. The result and profile views support reflection by showing category performance, mistakes, and historical averages.

During preparation for publication, the codebase was reviewed for maintainability and security. Result pages were restricted to the owner of the result, answer submissions were associated with the active session quiz and current question index, and quiz completion was prevented unless the active session represented a completed attempt. Statistics use a database aggregate rather than loading every result into Python. Configuration now reads the secret key, debug flag, and allowed hosts from environment variables with development-safe defaults. The repository also includes dependency metadata, a Django-specific ignore file, a professional README, Mermaid design diagrams, and this academic report.

The current implementation is appropriate for a university demonstration and small local deployment. Further production work should introduce automated tests, a dedicated server-side attempt model, a production database, secure deployment configuration, accessibility testing, and continuous integration. Even with these future improvements, the system provides a coherent and extensible foundation for computer-based formative assessment.

## Chapter 1: Introduction

### 1.1 Background

Online assessment has become an important part of digital learning. A quiz application can reduce marking effort, standardise scoring, and give learners feedback immediately after an attempt. It can also preserve performance information so that learners and instructors can identify areas that need additional practice. The growth of web frameworks makes it possible to build these capabilities with a relatively small, maintainable codebase.

QuizApp was designed as a focused learning and assessment platform. The application presents administrator-created quizzes containing multiple-choice questions. Each question has four answer options, a category, a difficulty level, and a point value. A learner's answers are evaluated during the attempt and stored with the final result.

### 1.2 Problem Definition

Manual quizzes are time-consuming to prepare, distribute, mark, and review. Learners may not receive feedback while the topic is still fresh, and instructors may lack a reliable history of individual performance. A simple online system is therefore needed to manage question banks, authenticate users, calculate results consistently, and support mistake review.

### 1.3 Motivation

The project was motivated by the practical value of immediate feedback and by the opportunity to apply full-stack web development concepts. Django provides mature components for authentication, database access, forms, templates, sessions, and administration, making it suitable for implementing a complete educational prototype.

### 1.4 Scope

The project includes user registration and login, quiz browsing, multiple-choice attempts, score calculation, result persistence, category summaries, mistake review, user history, public statistics, and administrator management. It does not currently include live multiplayer competition, question authoring workflows for non-admin instructors, automated email, payment, mobile-native clients, or a production hosting configuration.

### 1.5 Objectives

- Develop a usable browser-based quiz platform.
- Provide secure user authentication using Django facilities.
- Allow administrators to create quizzes and questions.
- Evaluate answers and calculate scores consistently.
- Store results and individual answers for later review.
- Present useful personal and aggregate statistics.
- Prepare maintainable documentation suitable for GitHub and university assessment.

## Chapter 2: Literature Review

### 2.1 Online Learning Systems

Online learning systems combine content delivery, learner identity, assessment, and progress tracking. Learning management systems commonly organise material into courses, activities, assignments, and assessments. Their value is not limited to replacing paper: digital systems can record events, calculate marks consistently, and make feedback available immediately. Research on formative assessment frequently emphasises the value of feedback that helps a learner understand both the outcome and the next learning action.

A small project such as QuizApp does not attempt to reproduce an entire learning management system. Instead, it isolates one high-value workflow: self-contained quiz practice. This narrower scope makes it possible to provide a complete experience with authentication, content management, assessment, and reporting while keeping the domain model understandable.

### 2.2 Quiz and Assessment Systems

Computer-based quiz systems generally contain a question bank, an assessment attempt, an answer record, and a scoring process. Multiple-choice questions are particularly suitable for automated evaluation because the expected answer can be compared consistently with the submitted value. Categories and difficulty labels allow the application to provide more informative feedback than a single total score.

A robust assessment system must distinguish between content and attempt data. Quiz and Question represent reusable content, while QuizResult and UserAnswer represent a particular learner's interaction with that content. QuizApp follows this distinction. In the current implementation, temporary attempt state is held in the Django session and converted to persistent rows when the quiz is completed. A future server-side attempt model would improve recovery and auditing for longer or higher-stakes assessments.

### 2.3 Existing Solutions

Commercial learning platforms offer extensive authoring, analytics, question randomisation, timing, grading policies, and integration with institutional identity systems. Open-source platforms provide similar features with different deployment and customisation trade-offs. These systems are powerful but can be excessive for a small academic project or a local teaching scenario.

QuizApp occupies a smaller and more transparent design space. Its administrator workflow is Django Admin, its persistence layer is the Django ORM, and its presentation layer consists of ordinary templates and static assets. This makes the application easy to inspect, modify, and use as a learning artefact. The trade-off is that advanced features such as question pools, detailed permissions, audit trails, and large-scale analytics are not yet included.

### 2.4 Technologies Used

Python provides the programming language and standard library. Django supplies URL routing, request handling, templates, ORM mapping, authentication, sessions, CSRF middleware, password validation, migrations, and administration. SQLite provides a portable relational database for development. HTML structures pages, CSS supplies the visual presentation, and JavaScript provides client-side effects and asynchronous answer submission. Mermaid diagrams communicate the architecture and database relationships in a version-controlled format.

The Model-Template-View pattern supports separation of concerns. Models define persistent entities and relationships. Views coordinate request processing and business rules. Templates render presentation. This separation improves maintainability compared with placing database logic directly in HTML or duplicating scoring logic across pages.

### 2.5 Review Summary

The literature and existing-solution review indicates that effective assessment software needs reliable identity, clear question presentation, deterministic scoring, meaningful feedback, and privacy controls. QuizApp implements the core of these requirements and creates a foundation for future extensions such as timed attempts, randomised questions, instructor analytics, and accessibility improvements.

## Chapter 3: Requirement Analysis

### 3.1 Functional Requirements

1. Guests shall view available quiz counts and public statistics.
2. Guests shall register with Django's password validation rules.
3. Registered users shall log in and log out.
4. Authenticated users shall start quizzes containing questions.
5. The system shall display one question at a time.
6. The system shall evaluate submitted answers and return correctness and points.
7. The system shall save a completed result and each answer.
8. Users shall view their result, grade, category breakdown, and mistakes.
9. Users shall view and delete their own quiz history.
10. Administrators shall create and edit quizzes and questions.
11. The system shall calculate aggregate quiz statistics.

### 3.2 Non-Functional Requirements

- **Usability:** navigation and feedback should be understandable to a first-time learner.
- **Security:** authentication, password validation, CSRF protection, and ownership checks must protect user data.
- **Maintainability:** application logic should use Django conventions and documented routes.
- **Performance:** aggregate values should be calculated efficiently and database queries should remain appropriate for the project scale.
- **Portability:** local setup should work with Python, Django, and SQLite.
- **Reliability:** invalid question indexes and incomplete attempts should not create fabricated results.
- **Extensibility:** models and routes should support future question and analytics features.

### 3.3 Hardware Requirements

- Dual-core processor or better
- 4 GB RAM minimum, 8 GB recommended
- At least 500 MB available disk space for the project and Python environment
- Keyboard, pointing device, and a modern web browser
- Network connection for initial dependency installation; local operation does not require continuous internet access

### 3.4 Software Requirements

- Windows, Linux, or macOS
- Python 3.10 or later recommended
- Django 6.0.5
- SQLite 3, included with standard Python distributions
- Modern browser such as Chrome, Edge, Firefox, or Safari
- Git for version control

### 3.5 Feasibility Study

**Technical feasibility:** The project uses mature, documented technologies. Django includes the required authentication, ORM, session, and admin features, reducing implementation risk. SQLite is sufficient for local demonstration.

**Operational feasibility:** A user can register, choose a quiz, answer questions, and review the result through a conventional browser workflow. An administrator can create content using a familiar admin interface.

**Economic feasibility:** The software stack is open source and the application can run on an ordinary student computer. No commercial service is required for local deployment.

## Chapter 4: System Design

### 4.1 Architecture Diagram

The system uses Django's Model-Template-View architecture. The browser sends requests to the root URL configuration, which includes the QuizApp URL configuration. Views authenticate users, read and write model data, manage session state, and render templates. The answer endpoint returns JSON for asynchronous feedback. The detailed diagram is in `documentation/system-architecture.md`.

### 4.2 Module Design

- **Authentication module:** registration, login, logout, password validation, and login-required protection.
- **Quiz module:** quiz selection, session initialisation, question display, answer evaluation, and completion.
- **Result module:** persistent score, percentage, grade, category breakdown, and mistake review.
- **Profile module:** personal result history, quiz count, average percentage, and history deletion.
- **Statistics module:** public counts and average platform percentage.
- **Administration module:** CRUD management for quizzes, questions, results, and answers.

### 4.3 User Flow

A guest opens the home page and either browses public information, registers, or logs in. An authenticated user selects a quiz. The application loads question data into the session and displays the first question. Each valid answer updates the session score and answer history. After the final answer, the application persists the result and related answer rows, clears the temporary state, and redirects to the result page. The user may then review mistakes or inspect the profile history.

### 4.4 Class Relationships

`Quiz` has many `Question` objects. `Quiz` also has many `QuizResult` objects. `QuizResult` belongs to a Django `User` and has many `UserAnswer` objects. Each `UserAnswer` references a `Question`. `Quiz.created_by` optionally references the user who created the quiz. These relationships are represented by Django foreign keys and cascade or set-null deletion rules defined in the models.

### 4.5 Database Design

The database design is relational. Reusable quiz content is separate from user-specific attempts. The database also contains Django framework tables for users, groups, permissions, sessions, and admin log entries. The Mermaid ER diagram is in `documentation/er-diagram.md`.

## Chapter 5: Database Design

### 5.1 Quiz Table

The `quizapp_quiz` table stores a quiz title, description, creation and update timestamps, and the optional creator. It is the parent of questions and results. The model orders quizzes by newest creation time.

### 5.2 Question Table

The `quizapp_question` table stores the question text, four answer options, the expected answer, category, difficulty, and point value. Each question belongs to one quiz. The model orders questions by category and difficulty. The current answer key is text-based; a stable option code would be a stronger future design because editing option text would not change the identity of an answer.

### 5.3 QuizResult Table

The `quizapp_quizresult` table records the user, quiz, score, total possible points, percentage, time taken, and completion timestamp. It represents one completed attempt. The user relation is nullable in the current schema, although normal application flow requires authentication.

### 5.4 UserAnswer Table

The `quizapp_useranswer` table records the result, question, submitted answer text, correctness, and points earned. It supports mistake review and category summaries. Deleting a result deletes its associated answers through the configured cascade relationship.

### 5.5 Django Framework Tables

Django's migration system creates standard tables for users, groups, permissions, sessions, and administrative actions. These tables support authentication, authorization, session persistence, and audit information.

### 5.6 ER Diagram

The complete entity relationship diagram is maintained as Mermaid source in `documentation/er-diagram.md` so it can be rendered by GitHub-compatible tools.

## Chapter 6: Implementation

### 6.1 Authentication Module

The application uses Django's `UserCreationForm` and `AuthenticationForm`. Password validators enforce minimum length, common-password rejection, numeric-password rejection, and similarity checks. Login-required decorators protect quiz attempts, results, profile pages, and history deletion. Django's admin applies staff and superuser checks independently of the public application.

### 6.2 Quiz Module

When a user starts a quiz, the application loads its questions and stores the active quiz identifier, question data, current index, score, and answers in the session. The answer endpoint compares the submitted answer with the stored answer key and returns a JSON response containing correctness, points, current score, and the next index. The prepared version verifies that the request belongs to the active session quiz and current question index.

### 6.3 Result Module

After a complete session, the system calculates total possible points and percentage, creates a `QuizResult`, then creates a `UserAnswer` row for each recorded answer. Result pages calculate a letter grade and category breakdown. Ownership checks ensure an authenticated user can view only their own result pages.

### 6.4 Admin Module

The admin configuration registers all four application models. `QuizAdmin` displays quiz names, question counts, and dates, and provides an inline question editor. Search and filters are configured for questions and results. The creator is assigned automatically when a new quiz is saved through the admin interface.

### 6.5 Database Operations

Django ORM queries retrieve quizzes, questions, results, and answers. Aggregation is used for profile averages and platform statistics. Migrations provide repeatable schema creation. SQLite is used for local development and is excluded from version control because it is environment data rather than application source.

## Chapter 7: Testing

The following test plan covers the main user, data, and security workflows. The Actual Result column records the current verification status; executable automated coverage should be expanded in `quizapp/tests.py` before production deployment.

| Test ID | Objective | Input | Expected Result | Actual Result |
|---|---|---|---|---|
| TC-01 | Load home page | GET `/` | Home page renders quiz counts | Pending execution; Django system checks contain no reported errors |
| TC-02 | Register valid user | Valid username and matching strong passwords | Account is created and user is logged in | Pending execution |
| TC-03 | Reject weak password | Common or short password | Form displays validation error and creates no user | Pending execution |
| TC-04 | Login valid user | Correct username and password | User is redirected to home | Pending execution |
| TC-05 | Reject invalid login | Wrong password | Authentication fails without a session | Pending execution |
| TC-06 | Protect quiz start | Anonymous GET `/quiz/1/` | User is redirected to login | Covered by `login_required`; runtime execution pending |
| TC-07 | Start populated quiz | Authenticated GET for a quiz with questions | Session is initialised and first question is shown | Pending execution |
| TC-08 | Start empty quiz | Authenticated GET for a quiz without questions | Error message is shown and user returns to quiz catalogue | Pending execution |
| TC-09 | Submit correct answer | POST active quiz and correct option | JSON marks answer correct and awards points | Pending execution |
| TC-10 | Submit invalid index | POST negative, non-numeric, or future index | Request returns validation error and score is unchanged | Validation path implemented; runtime execution pending |
| TC-11 | Submit answer for another quiz | POST mismatched quiz ID | Request is rejected | Session binding implemented; runtime execution pending |
| TC-12 | Complete incomplete quiz | Direct GET before final answer | No fabricated result is created; user returns to active quiz | Guard implemented; runtime execution pending |
| TC-13 | View own result | Authenticated user requests own result ID | Result page renders grade and category data | Ownership query implemented; runtime execution pending |
| TC-14 | View another user's result | Authenticated user requests another result ID | Response is 404 rather than exposing data | Ownership query implemented; runtime execution pending |
| TC-15 | Clear history | Authenticated POST with CSRF token | Only current user's results are deleted | Pending execution |
| TC-16 | View statistics | GET `/statistics/` | Counts and average percentage render | Aggregate query implemented; runtime execution pending |
| TC-17 | Admin access | Staff user opens `/admin/` | Admin dashboard is available | Pending execution |
| TC-18 | Non-staff admin access | Normal user opens `/admin/` | Django denies admin access | Provided by Django admin; runtime execution pending |

## Chapter 8: Results and Discussion

The home screen provides a central entry point and displays available quizzes and platform counts. The authentication screens support account creation and login. The quiz screen presents one question at a time and communicates progress. Immediate answer feedback gives the learner a clear indication of correctness and earned points.

The result screen communicates the total score, percentage, letter grade, and category-level performance. Mistake review allows the user to revisit incorrect answers. The profile screen provides historical results and an average score, supporting longitudinal self-assessment. Statistics provide a high-level view of the platform.

The admin screen is important because quiz content is data-driven rather than hard-coded into templates. Administrators can create a quiz and enter questions through inline editing. This separation allows content to change without modifying application code.

The main limitation is that quiz state is held in the session until completion. This is convenient for a small prototype but limits recovery if a browser session is lost and makes detailed attempt auditing more difficult. A dedicated attempt model is the natural next step for a production assessment platform.

## Chapter 9: Future Scope

1. Replace temporary session attempts with a `QuizAttempt` model and server-side answer records.
2. Add timed quizzes and persist start and finish timestamps.
3. Randomise questions and answer options using a reproducible attempt order.
4. Store correct answers as option identifiers rather than editable text.
5. Add instructor roles and object-level permissions.
6. Add search, pagination, tags, and question-bank reuse.
7. Provide downloadable result reports and instructor analytics.
8. Add accessibility testing, keyboard navigation, and screen-reader labels.
9. Add automated unit, integration, and browser tests in continuous integration.
10. Deploy with PostgreSQL, HTTPS, secure cookies, a managed secret, and a production WSGI/ASGI server.
11. Add an explicit open-source license and versioned release process.
12. Add screenshot evidence and a deployment guide to the repository.

## Chapter 10: Conclusion

QuizApp demonstrates the design and implementation of a complete database-backed web application for online formative assessment. The project begins with a clear practical problem: manual quizzes require effort to mark, feedback arrives late, and learners have little structured evidence of their progress. By combining Django authentication, session management, templates, ORM models, and administration, the application turns that problem into a coherent browser-based workflow.

The implemented system allows guests to discover the platform, users to register and log in, and authenticated learners to attempt administrator-created quizzes. Questions contain multiple options, categories, difficulty labels, and point values. During an attempt, the application provides immediate answer feedback and maintains temporary state. At completion, it persists a result and individual answer records. The result page then transforms raw answers into a score, percentage, grade, and category breakdown. Mistake review and profile history add educational value because they help the learner identify areas for revision rather than treating the score as the only outcome.

The application also demonstrates sound separation of concerns. Models describe persistent entities and foreign-key relationships. Views coordinate request processing and business rules. Templates provide the user interface, while static assets provide client-side presentation and interaction. Django's built-in authentication, password validation, CSRF middleware, migrations, and admin site reduce the amount of security-sensitive infrastructure that must be written manually. The admin configuration allows content management without hard-coding individual questions into the application.

The preparation review identified important engineering considerations. User-specific result pages must enforce ownership, and active quiz requests must be tied to session state to avoid fabricated or cross-quiz submissions. Database aggregation is preferable to loading all results when calculating an average. Production settings must not depend on a committed secret key or development debug mode. These improvements and recommendations make the repository clearer and more responsible as a university submission.

The current project is deliberately modest in scope, which is appropriate for an academic prototype. It provides enough functionality to demonstrate requirements analysis, relational database design, authentication, server-side rendering, asynchronous interaction, administration, and testing strategy. It also leaves a clear path for future work. A server-side attempt model, stronger role management, question randomisation, accessibility testing, automated test coverage, PostgreSQL, and continuous integration would move the system closer to production quality.

In conclusion, QuizApp is a useful and extensible foundation for computer-based formative assessment. It meets the core objective of delivering quizzes and meaningful feedback through a maintainable Django application, while its documented limitations provide realistic opportunities for further development and research.

## References

1. Django Software Foundation. *Django Documentation*. https://docs.djangoproject.com/
2. Python Software Foundation. *Python Documentation*. https://docs.python.org/3/
3. Django Software Foundation. *Writing Your First Django App*. https://docs.djangoproject.com/en/stable/intro/tutorial01/
4. Django Software Foundation. *Authentication in Web Requests*. https://docs.djangoproject.com/en/stable/topics/auth/default/
5. Django Software Foundation. *Django Security*. https://docs.djangoproject.com/en/stable/topics/security/
6. Django Software Foundation. *Django Database Access Optimization*. https://docs.djangoproject.com/en/stable/topics/db/optimization/
7. GitHub. *Basic Writing and Formatting Syntax*. https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github
8. Mermaid. *Mermaid Diagram Syntax*. https://mermaid.js.org/intro/
9. Black, P. and Wiliam, D. (1998). Inside the Black Box: Raising Standards Through Classroom Assessment. *Phi Delta Kappan*, 80(2), 139-148.
10. Nielsen, J. (1994). *Usability Engineering*. Morgan Kaufmann.
