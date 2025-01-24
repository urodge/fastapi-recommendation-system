import pandas as pd
import numpy as np
from fastapi import FastAPI
from pydantic import BaseModel

# Initialize FastAPI app
app = FastAPI()

# Example input data model
class QuizData(BaseModel):
    current_quiz: dict
    historical_data: list

# Mock Current Quiz Data
current_quiz_data = {
    "questions": [
        {"id": 1, "topic": "Physics", "difficulty": "medium", "is_correct": True},
        {"id": 2, "topic": "Biology", "difficulty": "hard", "is_correct": False},
        {"id": 3, "topic": "Chemistry", "difficulty": "easy", "is_correct": True},
        {"id": 4, "topic": "Physics", "difficulty": "hard", "is_correct": False},
    ]
}

# Mock Historical Quiz Data
historical_quiz_data = [
    {"quiz_id": 1, "scores": 60, "responses": {"1": 1, "2": 0, "3": 1, "4": 0}},
    {"quiz_id": 2, "scores": 70, "responses": {"1": 1, "2": 1, "3": 1, "4": 0}},
    {"quiz_id": 3, "scores": 50, "responses": {"1": 0, "2": 0, "3": 1, "4": 1}},
    {"quiz_id": 4, "scores": 80, "responses": {"1": 1, "2": 1, "3": 1, "4": 1}},
    {"quiz_id": 5, "scores": 90, "responses": {"1": 1, "2": 1, "3": 1, "4": 1}},
]

# Analyze current quiz data
def analyze_current_quiz(data):
    df = pd.DataFrame(data['questions'])
    topic_accuracy = df.groupby('topic')['is_correct'].mean()
    difficulty_accuracy = df.groupby('difficulty')['is_correct'].mean()
    return {
        "topic_accuracy": topic_accuracy.to_dict(),
        "difficulty_accuracy": difficulty_accuracy.to_dict(),
    }

# Analyze historical quiz data
def analyze_historical_quiz(data):
    scores = [quiz["scores"] for quiz in data]
    avg_score = np.mean(scores)
    trends = "improving" if scores[-1] > scores[0] else "declining"
    return {
        "average_score": avg_score,
        "trend": trends,
        "scores": scores,
    }

# Generate personalized recommendations
def generate_recommendations(current_analysis, historical_analysis):
    recommendations = []
    
    # Weak topics
    weak_topics = [topic for topic, acc in current_analysis['topic_accuracy'].items() if acc < 0.5]
    if weak_topics:
        recommendations.append(f"Focus on these weak topics: {', '.join(weak_topics)}")
    
    # Difficulty improvement
    hard_acc = current_analysis['difficulty_accuracy'].get("hard", 1)
    if hard_acc < 0.5:
        recommendations.append("Practice more hard questions to improve confidence.")
    
    # Improvement trends
    if historical_analysis['trend'] == "declining":
        recommendations.append("Your performance is declining. Revisit earlier topics and focus on practice.")
    
    return recommendations

# API endpoint for recommendations
@app.post("/recommendations/")
async def get_recommendations():
    current_analysis = analyze_current_quiz(current_quiz_data)
    historical_analysis = analyze_historical_quiz(historical_quiz_data)
    recommendations = generate_recommendations(current_analysis, historical_analysis)
    return {
        "current_analysis": current_analysis,
        "historical_analysis": historical_analysis,
        "recommendations": recommendations,
    }
