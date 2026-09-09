# Quiz Activity Diagram

```mermaid
flowchart TD
    Start([Start]) --> Auth{Authenticated?}
    Auth -- No --> Login[Log in or register]
    Login --> Auth
    Auth -- Yes --> Select[Select quiz]
    Select --> Load[Load questions into session]
    Load --> Question[Display current question]
    Question --> Submit[Submit answer]
    Submit --> Validate{Answer valid for active question?}
    Validate -- No --> Error[Return validation error]
    Error --> Question
    Validate -- Yes --> Score[Update score and answer history]
    Score --> More{More questions?}
    More -- Yes --> Question
    More -- No --> Save[Create QuizResult and UserAnswer rows]
    Save --> Result[Display grade and category breakdown]
    Result --> Review[Optional mistake review]
    Review --> End([End])
