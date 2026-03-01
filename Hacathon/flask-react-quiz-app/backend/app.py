from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/dashboard')
def dashboard():
    return render_template("dashboard.html")

@app.route('/api/quiz', methods=['POST'])
def quiz_submit():
    try:
        data = request.get_json()

        user_id = data.get('user_id', 'Student')
        scores = data.get('scores', [50, 50, 50])
        confidence = data.get('confidence', 70)

        accuracy = sum(scores) / len(scores)
        mastery = (accuracy * 0.7) + (confidence * 0.3)

        # Confidence mismatch logic
        if accuracy >= 70 and confidence < 50:
            status = "⚠ Low Confidence - Needs Encouragement"
        elif accuracy < 50 and confidence > 80:
            status = "⚠ Overconfident - Needs Practice"
        else:
            status = "✅ Balanced Understanding"

        # Roadmap
        if mastery < 60:
            roadmap = [
                "Revise Foundations",
                "Solve Basic Questions",
                "Take Reinforcement Quiz"
            ]
        elif mastery < 80:
            roadmap = [
                "Solve Intermediate Questions",
                "Timed Practice",
                "Concept Strengthening"
            ]
        else:
            roadmap = [
                "Advanced Problems",
                "Mini Project",
                "Weekly Mastery Review"
            ]

        return jsonify({
            "success": True,
            "user_id": user_id,
            "accuracy": round(accuracy, 1),
            "confidence": confidence,
            "mastery": round(mastery, 1),
            "status": status,
            "roadmap": roadmap
        })

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400


if __name__ == '__main__':
    app.run(debug=True, port=5000)