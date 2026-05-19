import pytest
from unittest.mock import MagicMock
from models import UserSession, ChatMessage, QuizRequest, QuizItem
from chat_service import ChatService

class TestChatService:
    
    @pytest.fixture
    def mock_repo(self):
        repo = MagicMock()
        
        def fake_save(obj):
            if getattr(obj, "id", None) is None:
                obj.id = 999
        
        repo.save.side_effect = fake_save
        return repo

    @pytest.fixture
    def mock_ai(self):
        return MagicMock()

    @pytest.fixture
    def chat_service(self, mock_repo, mock_ai):
        return ChatService(session_repository=mock_repo, ai_service=mock_ai)

    def test_start_new_learning_session(self, chat_service, mock_repo):
        session = chat_service.start_session()
        assert isinstance(session, UserSession)
        assert session.id == 999 
        mock_repo.save.assert_called_with(session)

    def test_send_message_and_receive_response(self, chat_service, mock_repo, mock_ai):
        fake_session = UserSession(id=1)
        mock_repo.get_by_id.return_value = fake_session
        mock_ai.get_explanation.return_value = "This is a mocked explanation."

        response = chat_service.send_message(session_id=1, content="What is Python?")

        assert response == "This is a mocked explanation."
        mock_ai.get_explanation.assert_called_once_with("What is Python?")
        
        assert len(fake_session.messages) == 2
        assert fake_session.messages[0].role == "user"
        assert fake_session.messages[1].role == "assistant"

    def test_generate_quiz(self, chat_service, mock_repo, mock_ai):
        fake_session = UserSession(id=1)
        mock_repo.get_by_id.return_value = fake_session
        
        mock_ai.get_quiz.return_value = {
            "quiz": {
                "topic": "Python",
                "questions": [
                    {"question": "What is a list?", "answer": "A data structure"}
                ]
            }
        }

        quiz_request = chat_service.generate_quiz(session_id=1, topic="Python")

        mock_ai.get_quiz.assert_called_once_with("Python")
        assert quiz_request.topic == "Python"
        assert len(quiz_request.quiz_items) == 1
        assert quiz_request.quiz_items[0].question_text == "What is a list?"

    def test_evaluate_user_answer(self, chat_service, mock_ai):
        mock_ai.evaluate_answer.return_value = {"is_correct": True, "feedback": "Great job!"}

        result = chat_service.evaluate_answer(
            question_text="What is Mocking?", 
            correct_answer="Simulating objects",
            user_answer="Creating fake objects"
        )

        assert result["is_correct"] is True
        assert result["feedback"] == "Great job!"

    def test_handle_llm_service_failures_gracefully(self, chat_service, mock_repo, mock_ai):
        fake_session = UserSession(id=1)
        mock_repo.get_by_id.return_value = fake_session
        mock_ai.get_explanation.side_effect = Exception("Connection Error")

        response = chat_service.send_message(session_id=1, content="Hello")

        assert "unavailable" in response.lower()
        assert fake_session.messages[-1].content == response