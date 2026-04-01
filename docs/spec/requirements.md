# Requirements

## Application Domain:
- People and Organizations: HE Students, Professors and Staff
- Existing Systems and Hardware: HE campuses, PC-Pools, Course Software and Content (e.g. Moodle), Large Language Models
- Processes: learn new knowledge; test, evaluate and refine understanding; provide examples; provide clarification; track learning progress
- Concepts: Learning Session, Educational Content, Quiz

## Problem Space:
- General Chatbots are unstructured and unfocused
- General Chatbots aren't grounded to ensure comprehensible and truthful responses
- Students intake knowledge passively, without active involvement
- Students don't recieve immediate feedback on their work

## Solution Domain:
- A three tier architecture composed of a web-based user interface, a RESTful API backend, and persistent storage
- Integration with externaly or locally hosted LLMs
- Stuctured chat flow that generates explanations and quizes based on course material
- provide pedagological feedback to student answers
- save interactions for future revisiting
- Ensure "comprehensible and pedagogically useful" responses through structured prompts and response validation

## Functional Requirements (Based on `docs/esbot.md`):
- 1: Conversational Learning Interface
    - 1.1: User must be able to enter questions in plain text.
    - 1.2: Chatbot must respond in plain text
    - 1.3: Full session must be accessible by user
    - 1.4: User must be able to easily distinguish between chatbot and User messages and understand the flow of the conversation visibly
    - 1.5: User must be able to switch between multiple learning sessions pertaining to different subjects
    
- 2: Explanation and Example Generation
    - 2.1: Chatbot responses must be structured in an easily understandable and interpretable format
    - 2.2: Chatbot's answers must be grounded in the course content and implicitly understood knowledge
    - 2.3: Chatbot's answers must effectively convey information so that it is understood by the student
    - 2.4: Chatbot's Explanations and Examples must answer what is requested by the user
    - 2.5: Chatbot's responses must be individualized and specific
    
- 3: Quiz and Practice Generation
    - 3.1: Users must be able to trigger quiz and practice generation reliably and only when intended
    - 3.2: Quiz questions must meet all requirements outlined in section 2 
    - 3.6: New problems should be generated dynamically, based on the user's performance
    
- 4: Answer Evaluation
    - 4.1: Feedback must be provided when answers are given
    - 4.2: Feedback must meet all requirements outlined in section 2
    - 4.3: Feedback must indicate how correct the user's answer was
    
- 5: Session Management
    - 5.1: All interactions between the user and chatbot must be stored
    - 5.2: Storage must be persisent
    - 5.2: Interactions must be fetched when user signs in
    - 5.3: Interactions must be presented in chronological order
    - 5.4: Interactions must be stored in such a fashion that requirements in section 1 are able to be met
    - 5.5: Interactions be secure, and not leaked between users
    
- 6: Backend API Access
    - 6.1: The Backend layer must run independently of the front end
    - 6.2: The Backend must meet the requirements outlined by the REST architectural style
 
## Non-Functional Requirements (Based on `docs/esbot.md`, and Lab Slide-1)
- 7: Usability
  - 7.1: The system shall provide an intuitive user interface accessible to first-time users without prior training.
  - 7.2: The user interface shall enable pleasing and satisfying interaction to encourage active engagement.
  - 7.3: Learning interactions must be structured to remain comprehensible and pedagogically useful.
  
- 8: Performance Efficiency
  - 8.1: The system shall respond to user queries within a 2–5 second timeframe under normal load.
  - 8.2: The system must maintain these response times for up to 50 concurrent users.
  - 8.3: Resource utilization should be optimized to allow the application to remain lightweight and web-based.

- 9: Reliability
  - 9.1: The system shall handle failures of external AI services gracefully.
  - 9.2: In the event of an AI service interruption, the system must provide meaningful fallback responses instead of system errors.

- 10: Security
  - 10.1: The system shall protect all stored session data and user interaction history.
  - 10.2: Basic input validation must be implemented to mitigate malicious inputs and prompt injections.
  - 10.3: The system must ensure that data access is restricted solely to authorized users for their specific sessions.

- 11: Maintainability and Testability
  - 11.1: The system must follow a modular three-tier architecture to ensure clear separation of concerns.
  - 11.2: The backend must be designed to support the mocking of AI inference components for automated testing.
  - 11.3: The system shall provide logging and monitoring capabilities to trace system behavior and identify potential failures.

- 12: Scalability and Portability
  - 12.1: The backend and AI inference components must be capable of independent scaling to handle increased user demand.
  - 12.2: The application must be accessible via standard web browsers across various devices without requiring local installation.

- 13: Functional Sustainibility
  - 13.1: The system must manage the non-deterministic nature of AI outputs by validating responses before presentation where possible.



Google Gemini was used in the development of these requirements as a form of checking and revising my work. All AI-edited content was thoroughly checked.
