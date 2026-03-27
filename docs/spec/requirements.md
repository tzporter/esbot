During the lecture, we discussed fundamental aspects of systems engineering, 
particularly focusing on systematically deriving clear and precise requirements. 
Now, using the provided introductory description of the ESBot application, 
please identify, document, and clearly specify the functional and non-functional system requirements. 
Your documentation should comprehensively reflect the key functionalities that ESBot must offer to its intended users.

Application Domain:
- People and Organizations: HE Students, Professors and Staff
- Existing Systems and Hardware: HE campuses, PC-Pools, Course Software and Content (e.g. Moodle), Large Language Models
- Processes: learn knew knowldedge; test, evaluate and refine understanding; provide examples; provide clarification; track learning progress
- Concepts: Learning Session, Educational Content, Quiz

Problem Space:
- General Chatbots are unstructured and unfocused
- General Chatbots aren't grounded to ensure comprehensible and truthful responses
- Students intake knowledge passively, without active involvement
- Students don't recieve immediate feedback on their work

Solution Domain:
- A three tier architecture composed of a web-based user interface, a RESTful API backend, and persistent storage
- Integration with externaly or locally hosted LLMs
- Stuctured chat flow that generates explanations and quizes based on course material
- provide pedagological feedback to student answers
- save interactions for future revisiting
- Ensure "comprehensible and pedagogically useful" responses through structured prompts and response validation

  User Requirements (Quoted from docs/esbot.md):
  - 1: Conversational Learning Interface
  - 2: Explanation and Example Generation
  - 3: Quiz and Practice Generation
  - 4: Answer Evaluation
  - 5: Session Management
  - 6: Backend API Access

 Functional Requirements
    1.1: User must be able to enter questions in plain text.
    1.2: 
    2.1: Chatbot must respond with individual-specific responses
    2.2: Chatbot responses must be structured, with specific formatting for each type of response
    2.1: Explanations 
    
