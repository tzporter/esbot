from models import UserSession, ChatMessage, QuizRequest, QuizItem

class ChatService:
    def __init__(self, session_repository, ai_service):
        self.repo = session_repository
        self.ai = ai_service

    def start_session(self) -> UserSession:
        session = UserSession()
        self.repo.save(session)
        return session

    def send_message(self, session_id: int, content: str) -> str:
        session = self.repo.get_by_id(session_id)
        
        session.add_message(content=content, role="user")
        self.repo.save(session)

        try:
            ai_response = self.ai.get_explanation(content)
        except Exception:
            ai_response = "AI service is currently unavailable. Please try again later."

        session.add_message(content=ai_response, role="assistant")
        self.repo.save(session)
        return ai_response

    def generate_quiz(self, session_id: int, topic: str):
        session = self.repo.get_by_id(session_id)
        
        try:
            quiz_data = self.ai.get_quiz(topic)
            
            qr = session.add_quiz_request(topic=topic, difficulty="medium")
            
            self.repo.save(qr) 
            
            for item in quiz_data.get("quiz", {}).get("questions", []):
                qr.add_item(
                    question_text=item["question"], 
                    correct_answer=item["answer"]
                )
                
            self.repo.save(session)
            return qr
        except Exception:
            raise ValueError("Failed to generate quiz due to AI error.")

    def evaluate_answer(self, question_text: str, correct_answer: str, user_answer: str) -> dict:
        try:
            result = self.ai.evaluate_answer(
                question=question_text, 
                correct_answer=correct_answer, 
                user_answer=user_answer
            )
            return result
        except Exception:
            return {"is_correct": False, "feedback": "Feedback currently unavailable due to AI service error."}