from flask import Flask, render_template, request, jsonify, send_from_directory
import os
import sys
import json
import sqlite3

_BACKEND_DIR = os.path.dirname(os.path.abspath(__file__))
if _BACKEND_DIR not in sys.path:
    sys.path.insert(0, _BACKEND_DIR)

ROOT = os.path.join(_BACKEND_DIR, '..')
app = Flask(__name__, template_folder=ROOT, static_folder=ROOT, static_url_path='')
app.secret_key = 'learning-iq-secret'

import db
from auth import encode_token, decode_token

def get_user_id():
    auth = request.headers.get('Authorization') or request.cookies.get('token')
    if auth and auth.startswith('Bearer '):
        auth = auth[7:]
    if not auth:
        auth = request.args.get('token')
    payload = decode_token(auth) if auth else None
    return (payload.get('user_id'), payload) if payload else (None, None)

def get_conn():
    return sqlite3.connect(db.DB_PATH)

# ----- CORS -----
@app.after_request
def add_cors(res):
    res.headers['Access-Control-Allow-Origin'] = '*'
    res.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, OPTIONS'
    res.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    return res

# ----- Pages -----
@app.route('/')
def home():
    return render_template("index.html")

@app.route('/dashboard')
def dashboard():
    return render_template("dashboard.html")

@app.route('/subjects')
def subjects():
    return render_template("subjects.html")

@app.route('/subject/<int:sid>')
def subject_detail(sid):
    return render_template("subject-detail.html")

@app.route('/maths')
def maths():
    return render_template("maths.html")

@app.route('/course')
def course():
    return render_template("course.html")

@app.route('/profile')
def profile():
    return render_template("profile.html")

@app.route('/leaderboard')
def leaderboard():
    return render_template("leaderboard.html")

@app.route('/login')
def login_page():
    return render_template("login.html")

@app.route('/main.js')
def serve_main_js():
    return send_from_directory(ROOT, 'main.js')

@app.route('/style.css')
def serve_style_css():
    return send_from_directory(ROOT, 'style.css')

# ----- Auth API -----
@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.get_json() or {}
    email = (data.get('email') or '').strip()
    password = data.get('password') or ''
    conn = get_conn()
    c = conn.cursor()
    c.execute("SELECT id, name, email FROM user WHERE email = ?", (email,))
    row = c.fetchone()
    conn.close()
    if not row:
        return jsonify({"success": False, "error": "User not found"}), 401
    uid, name, em = row
    token = encode_token(uid, name, em)
    return jsonify({"success": True, "token": token, "user": {"id": uid, "name": name, "email": em}})

@app.route('/api/auth/register', methods=['POST'])
def register():
    data = request.get_json() or {}
    name = (data.get('name') or '').strip()
    email = (data.get('email') or '').strip()
    college = (data.get('college') or '').strip()
    stream = (data.get('stream') or '').strip()
    if not name or not email:
        return jsonify({"success": False, "error": "Name and email required"}), 400
    conn = get_conn()
    c = conn.cursor()
    try:
        c.execute(
            "INSERT INTO user (name, email, college, stream) VALUES (?,?,?,?)",
            (name, email, college, stream)
        )
        uid = c.lastrowid
        conn.commit()
        token = encode_token(uid, name, email)
        return jsonify({"success": True, "token": token, "user": {"id": uid, "name": name, "email": email}})
    except sqlite3.IntegrityError:
        return jsonify({"success": False, "error": "Email already registered"}), 400
    finally:
        conn.close()

# ----- User (optional auth; fallback to user_id=1) -----
@app.route('/api/user/<int:user_id>')
def get_user(user_id):
    uid, _ = get_user_id()
    if uid:
        user_id = uid
    conn = get_conn()
    c = conn.cursor()
    c.execute(
        "SELECT id, name, email, college, stream, streak, xp, enrolled_courses, mastery_map, theme FROM user WHERE id = ?",
        (user_id,)
    )
    row = c.fetchone()
    conn.close()
    if not row:
        return jsonify({"error": "User not found"}), 404
    u = {
        "id": row[0], "name": row[1], "email": row[2], "college": row[3], "stream": row[4],
        "streak": row[5], "xp": row[6], "enrolled_courses": json.loads(row[7] or "[]"),
        "mastery_map": json.loads(row[8] or "{}"), "theme": row[9] or "light"
    }
    return jsonify(u)

@app.route('/api/user/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    uid, _ = get_user_id()
    if uid and uid != user_id:
        return jsonify({"error": "Forbidden"}), 403
    data = request.get_json() or {}
    conn = get_conn()
    c = conn.cursor()
    updates = []
    vals = []
    for k, v in [("name", data.get("name")), ("college", data.get("college")), ("stream", data.get("stream")), ("theme", data.get("theme"))]:
        if v is not None:
            updates.append(f"{k} = ?")
            vals.append(v)
    if updates:
        vals.append(user_id)
        c.execute("UPDATE user SET " + ", ".join(updates) + " WHERE id = ?", vals)
        conn.commit()
    conn.close()
    return jsonify({"success": True})

# ----- Subjects & Topics -----
@app.route('/api/subjects')
def api_subjects():
    conn = get_conn()
    c = conn.cursor()
    c.execute("SELECT id, name, description, estimated_weeks FROM subject ORDER BY id")
    rows = c.fetchall()
    subjects = [{"id": r[0], "name": r[1], "description": r[2], "estimated_weeks": r[3]} for r in rows]
    conn.close()
    return jsonify(subjects)

@app.route('/api/subjects/<int:sid>/topics')
def api_subject_topics(sid):
    conn = get_conn()
    c = conn.cursor()
    c.execute(
        "SELECT id, name, difficulty, estimated_time_mins, week_number, prerequisites FROM topic WHERE subject_id = ? ORDER BY week_number, id",
        (sid,)
    )
    rows = c.fetchall()
    topics = []
    for r in rows:
        topics.append({
            "id": r[0], "name": r[1], "difficulty": r[2], "estimated_time_mins": r[3],
            "week_number": r[4], "prerequisites": json.loads(r[5] or "[]")
        })
    conn.close()
    return jsonify(topics)

@app.route('/api/topics')
def get_topics():
    conn = get_conn()
    c = conn.cursor()
    c.execute("""
        SELECT t.id, t.name, t.subject_id, t.estimated_time_mins, t.week_number, s.name as subject_name
        FROM topic t JOIN subject s ON t.subject_id = s.id ORDER BY s.id, t.week_number
    """)
    rows = c.fetchall()
    c.execute("SELECT topic_id, questions FROM quiz")
    quiz_map = {r[0]: json.loads(r[1]) for r in c.fetchall()}
    conn.close()
    topics = []
    for r in rows:
        tid, name, sid, mins, week, subj = r
        topics.append({
            "id": tid, "name": name, "subject_id": sid, "subject_name": subj,
            "estimated_time_mins": mins, "week_number": week,
            "quiz": quiz_map.get(tid, [])
        })
    return jsonify(topics)

# ----- Progress & Mastery -----
@app.route('/api/progress/<int:user_id>/<topic_id>', methods=['POST'])
def update_progress(user_id, topic_id):
    data = request.get_json() or {}
    score = int(data.get('score', 0))
    time_seconds = data.get('time_seconds')
    confidence = data.get('confidence', 70)
    conn = get_conn()
    c = conn.cursor()
    c.execute("SELECT mastery_map FROM user WHERE id = ?", (user_id,))
    row = c.fetchone()
    if not row:
        conn.close()
        return jsonify({"error": "User not found"}), 404
    mastery = json.loads(row[0] or "{}")
    mastery[str(topic_id)] = score
    c.execute("UPDATE user SET mastery_map = ? WHERE id = ?", (json.dumps(mastery), user_id))
    c.execute(
        "INSERT INTO quiz_attempt (user_id, topic_id, score, time_seconds, confidence) VALUES (?,?,?,?,?)",
        (user_id, topic_id, score, time_seconds, confidence)
    )
    conn.commit()
    conn.close()
    return jsonify({"success": True, "score": score})

# ----- AI: Recommendations (analyze quiz results, time, accuracy, revision; 7-day roadmap) -----
@app.route('/api/recommendations/<int:user_id>')
def get_recommendations(user_id):
    conn = get_conn()
    c = conn.cursor()
    c.execute("SELECT mastery_map, streak FROM user WHERE id = ?", (user_id,))
    row = c.fetchone()
    if not row:
        conn.close()
        return jsonify({"recommendations": json.dumps(_fallback_rec())})
    mastery = json.loads(row[0] or "{}")
    streak = row[1] or 0
    c.execute("SELECT topic_id, score, reattempt_count FROM quiz_attempt WHERE user_id = ? ORDER BY created_at DESC", (user_id,))
    attempts = c.fetchall()
    conn.close()
    weak = [(tid, s) for tid, s in mastery.items() if float(s) < 60]
    weak.sort(key=lambda x: float(x[1]))
    next_topic = weak[0][0] if weak else "1"
    c2 = get_conn().cursor()
    c2.execute("SELECT name FROM topic WHERE id = ?", (int(next_topic),))
    r = c2.fetchone()
    next_name = r[0] if r else "Arrays"
    c2.connection.close()
    daily_plan = [
        f"Day 1: {next_name} basics (45 min)",
        "Day 2: Practice problems (60 min)",
        "Day 3: Quiz + Review (30 min)",
        "Day 4: Prerequisite recap if needed",
        "Day 5: Timed practice set",
        "Day 6: Weak topic reinforcement",
        "Day 7: Weekly review & next topic"
    ]
    rec = {
        "next_topic": next_name,
        "daily_plan": daily_plan,
        "estimated_completion": "2.5 hours",
        "priority": "weak foundational concepts" if weak else "next in roadmap"
    }
    return jsonify({"recommendations": json.dumps(rec)})

def _fallback_rec():
    return {
        "next_topic": "Arrays",
        "daily_plan": ["Day 1: Arrays basics (45min)", "Day 2: Practice (60min)", "Day 3: Quiz (30min)"],
        "estimated_completion": "2.5 hours",
        "priority": "foundational concepts"
    }

# ----- Quiz submit (mastery from accuracy, time, confidence) -----
@app.route('/api/quiz', methods=['POST'])
def quiz_submit():
    try:
        data = request.get_json() or {}
        user_id = data.get('user_id') or 1
        if isinstance(user_id, str) and user_id.isdigit():
            user_id = int(user_id)
        raw_scores = data.get('scores', [50, 50, 50])
        confidence = int(data.get('confidence', 70))
        topic_id = data.get('topic_id')
        time_seconds = data.get('time_seconds')

        if isinstance(raw_scores, dict):
            scores = raw_scores.get('quiz', raw_scores.get('scores', [50, 50, 50]))
        else:
            scores = raw_scores
        if not scores:
            scores = [50, 50, 50]

        accuracy = sum(scores) / len(scores) if scores else 50
        mastery = (accuracy * 0.7) + (confidence * 0.3)

        if accuracy >= 70 and confidence < 50:
            status = "⚠ Low Confidence - Needs Encouragement"
        elif accuracy < 50 and confidence > 80:
            status = "⚠ Overconfident - Needs Practice"
        else:
            status = "✅ Balanced Understanding"

        if mastery < 60:
            roadmap = ["Revise Foundations", "Solve Basic Questions", "Take Reinforcement Quiz"]
        elif mastery < 80:
            roadmap = ["Solve Intermediate Questions", "Timed Practice", "Concept Strengthening"]
        else:
            roadmap = ["Advanced Problems", "Mini Project", "Weekly Mastery Review"]

        mastery_pct = round(mastery, 1)
        if topic_id and user_id:
            conn = get_conn()
            c = conn.cursor()
            c.execute("SELECT mastery_map FROM user WHERE id = ?", (user_id,))
            row = c.fetchone()
            if row:
                m = json.loads(row[0] or "{}")
                m[str(topic_id)] = mastery_pct
                c.execute("UPDATE user SET mastery_map = ? WHERE id = ?", (json.dumps(m), user_id))
                c.execute(
                    "INSERT INTO quiz_attempt (user_id, topic_id, score, time_seconds, confidence) VALUES (?,?,?,?,?)",
                    (user_id, topic_id, mastery_pct, time_seconds, confidence)
                )
                conn.commit()
            conn.close()

        return jsonify({
            "success": True,
            "user_id": user_id,
            "accuracy": round(accuracy, 1),
            "confidence": confidence,
            "mastery": mastery_pct,
            "mastery_percent": mastery_pct,
            "message": f"Mastery: {mastery_pct}% — {status}",
            "status": status,
            "roadmap": roadmap
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400

# ----- Leaderboard (gamified: tests, accuracy, consistency, projects) -----
@app.route('/api/leaderboard')
def leaderboard_api():
    conn = get_conn()
    c = conn.cursor()
    c.execute("SELECT id, name, xp, streak FROM user ORDER BY xp DESC LIMIT 50")
    rows = c.fetchall()
    conn.close()
    out = []
    for i, r in enumerate(rows, 1):
        out.append({"rank": i, "user_id": r[0], "name": r[1], "xp": r[2], "streak": r[3]})
    return jsonify(out)

# ----- Reminders -----
@app.route('/api/reminder/<int:user_id>', methods=['GET', 'POST'])
def reminder(user_id):
    conn = get_conn()
    c = conn.cursor()
    if request.method == 'GET':
        c.execute("SELECT daily_study_time, notify_browser, notify_email FROM reminder WHERE user_id = ?", (user_id,))
        row = c.fetchone()
        conn.close()
        if not row:
            return jsonify({"daily_study_time": None, "notify_browser": True, "notify_email": False})
        return jsonify({
            "daily_study_time": row[0],
            "notify_browser": bool(row[1]),
            "notify_email": bool(row[2])
        })
    data = request.get_json() or {}
    c.execute(
        """INSERT INTO reminder (user_id, daily_study_time, notify_browser, notify_email)
           VALUES (?, ?, ?, ?) ON CONFLICT(user_id) DO UPDATE SET
           daily_study_time=excluded.daily_study_time, notify_browser=excluded.notify_browser, notify_email=excluded.notify_email""",
        (user_id, data.get("daily_study_time"), 1 if data.get("notify_browser", True) else 0, 1 if data.get("notify_email") else 0)
    )
    conn.commit()
    conn.close()
    return jsonify({"success": True})

# ----- Rating -----
@app.route('/api/rating', methods=['POST'])
def rate():
    uid, _ = get_user_id()
    user_id = uid or 1
    data = request.get_json() or {}
    stars = int(data.get('stars', 5))
    if not 1 <= stars <= 5:
        return jsonify({"success": False, "error": "Stars 1-5"}), 400
    conn = get_conn()
    c = conn.cursor()
    c.execute("INSERT INTO rating (user_id, stars) VALUES (?, ?)", (user_id, stars))
    conn.commit()
    conn.close()
    return jsonify({"success": True})

# ----- Downloads (list) -----
@app.route('/api/downloads/<int:user_id>')
def downloads(user_id):
    conn = get_conn()
    c = conn.cursor()
    c.execute("SELECT resource_name, topic_id, created_at FROM download WHERE user_id = ? ORDER BY created_at DESC LIMIT 20", (user_id,))
    rows = c.fetchall()
    conn.close()
    return jsonify([{"resource_name": r[0], "topic_id": r[1], "created_at": r[2]} for r in rows])

# ----- Recent test scores -----
@app.route('/api/test-scores/<int:user_id>')
def test_scores(user_id):
    conn = get_conn()
    c = conn.cursor()
    c.execute("""
        SELECT qa.topic_id, t.name, qa.score, qa.created_at
        FROM quiz_attempt qa JOIN topic t ON qa.topic_id = t.id
        WHERE qa.user_id = ? ORDER BY qa.created_at DESC LIMIT 10
    """, (user_id,))
    rows = c.fetchall()
    conn.close()
    return jsonify([{"topic_id": r[0], "topic_name": r[1], "score": r[2], "created_at": r[3]} for r in rows])

# ----- Gap detection: weak topics + prerequisite recommendation -----
@app.route('/api/gaps/<int:user_id>')
def gaps(user_id):
    conn = get_conn()
    c = conn.cursor()
    c.execute("SELECT mastery_map FROM user WHERE id = ?", (user_id,))
    row = c.fetchone()
    if not row:
        conn.close()
        return jsonify({"weak": [], "recommendations": []})
    mastery = json.loads(row[0] or "{}")
    weak = []
    c.execute("SELECT id, name, prerequisites FROM topic")
    for tid, name, preq in c.fetchall():
        s = float(mastery.get(str(tid), 0))
        if s < 60:
            weak.append({"topic_id": tid, "topic_name": name, "mastery": s, "prerequisites": json.loads(preq or "[]")})
    weak.sort(key=lambda x: x["mastery"])
    rec = []
    for w in weak[:5]:
        rec.append(f"Revise {w['topic_name']} (current {w['mastery']:.0f}%). Prioritize prerequisite topics first.")
    conn.close()
    return jsonify({"weak": weak, "recommendations": rec})

# ----- Extra knowledge (where topic is used) -----
EXTRA_KNOWLEDGE = {
    "Arrays": ["Used in Google Interviews", "Used in Competitive Programming", "Used in Database indexing"],
    "Linked List": ["Used in LRU Cache", "Used in Browser History", "Used in Music Playlist"],
    "Trees": ["Used in File Systems", "Used in DOM", "Used in Decision Trees (ML)"],
    "Graphs": ["Used in Social Networks", "Used in Maps", "Used in Recommendation systems"],
    "Limits": ["Used in Derivatives", "Used in Physics", "Used in Continuity"],
    "Derivatives": ["Used in Optimization", "Used in Physics (velocity)", "Used in ML (gradients)"],
    "Integration": ["Used in Area under curve", "Used in Physics", "Used in Probability"],
}

@app.route('/api/extra-knowledge/<topic_name>')
def extra_knowledge(topic_name):
    name = topic_name.replace("%20", " ").strip()
    tips = EXTRA_KNOWLEDGE.get(name, ["Used in advanced topics", "Used in real-world applications"])
    return jsonify({"topic": name, "uses": tips})

if __name__ == '__main__':
    app.run(debug=True, port=5001, host='0.0.0.0')
