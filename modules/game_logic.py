import random
from modules.quiz_engine import get_question

def generate_question(category_id: int, difficulty: str) -> dict:
    """Fetch a trivia question from OpenTDB using category ID and difficulty."""
    data = get_question(category_id, difficulty)

    if not data or "error" in data:
        return {
            "question": f"Error generating question for {category_id} [{difficulty}]",
            "options": ["N/A"],
            "answer": "N/A"
        }

    # Combine correct and incorrect answers and shuffle them
    options = data["incorrect_answers"] + [data["correct_answer"]]
    random.shuffle(options)

    return {
        "question": data["question"],
        "options": options,
        "answer": data["correct_answer"]
    }

def check_answer(user_answer: str, correct_answer: str) -> bool:
    return user_answer.strip().lower() == correct_answer.strip().lower()