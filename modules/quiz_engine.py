import requests
import random
import html

# Map category names to OpenTDB category IDs
CATEGORY_IDS = {
    "General Knowledge": 9,
    "Books": 10,
    "Film": 11,
    "Music": 12,
    "Science": 17,
    "Sports": 21,
    "History": 23,
    "Politics": 24,
    "Art": 25,
    "Celebrities": 26,
    "Animals": 27,
    "Vehicles": 28
}

def get_question(category_id, difficulty):
    try:
        url = f"https://opentdb.com/api.php?amount=1&category={category_id}&difficulty={difficulty.lower()}&type=multiple"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        # ✅ Add this to debug if category returns nothing
        if data["response_code"] != 0 or not data["results"]:
            print(f"⚠️ OpenTDB returned: {data}")
            return {"error": f"No questions available for category {category_id} [{difficulty}] right now."}

        question_data = data["results"][0]
        question_data["question"] = html.unescape(question_data["question"])
        question_data["correct_answer"] = html.unescape(question_data["correct_answer"])
        question_data["incorrect_answers"] = [html.unescape(ans) for ans in question_data["incorrect_answers"]]

        return question_data

    except Exception as e:
        print(f"🚨 Exception while fetching question: {e}")
        return {"error": f"Error fetching question: {str(e)}"}