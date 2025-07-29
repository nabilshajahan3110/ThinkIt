import time

def start_timer():
    return time.time()

def calculate_score(user_answer, correct_answer, time_taken):
    """
    Calculate score based on correctness and how fast the user answered.
    - Full score: 10 points
    - Time penalty: Lose 1 point for every 5 seconds
    - Minimum score: 1 point (if correct)
    """
    if user_answer.strip().lower() == correct_answer.strip().lower():
        base_score = 10
        time_penalty = int(time_taken // 5)  # lose 1 point for every 5 seconds
        final_score = max(1, base_score - time_penalty)
        return final_score
    else:
        return 0