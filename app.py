
from flask import Flask, render_template, request
import re

app = Flask(__name__)

SKILLS = [
    "Python","Java","C","C++","JavaScript","HTML","CSS",
    "SQL","Git","Docker","Flask","React","Node.js","MongoDB"
]

def analyze_resume(text):
    found = [s for s in SKILLS if s.lower() in text.lower()]
    missing = [s for s in SKILLS if s not in found]

    score = 0
    score += min(len(found) * 5, 50)

    if "project" in text.lower():
        score += 20
    if "internship" in text.lower() or "experience" in text.lower():
        score += 20
    if "github" in text.lower():
        score += 10

    score = min(score, 100)

    suggestions = []
    if len(found) < 5:
        suggestions.append("Add more technical skills.")
    if "github" not in text.lower():
        suggestions.append("Add GitHub profile link.")
    if "project" not in text.lower():
        suggestions.append("Include projects section.")
    if "experience" not in text.lower():
        suggestions.append("Add experience/internship details.")

    return score, found, missing, suggestions

@app.route("/", methods=["GET","POST"])
def home():
    result = None
    if request.method == "POST":
        resume = request.form.get("resume")
        score, found, missing, suggestions = analyze_resume(resume)
        result = {
            "score": score,
            "found": found,
            "missing": missing,
            "suggestions": suggestions
        }
    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)
