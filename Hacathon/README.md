# AI-Powered Personalized Learning Intelligence System

Full-stack adaptive learning platform: concept-level tracking, gap detection, dynamic roadmap, personalized recommendations.  
**Tech:** HTML, CSS, JS (frontend); Python Flask + SQLite (backend).  
**Target users:** College students (Engineering, Medical, Competitive Exams).

## Run the app

1. **Start the backend** (from project root):
   ```bash
   cd Hacathon
   ./learning_env/bin/python backend/app.py
   ```
   Or: `python3 backend/app.py` if Flask is installed.  
   Server: **http://localhost:5001**

2. **Open in browser**
   - Home: http://localhost:5001/
   - Dashboard: http://localhost:5001/dashboard
   - Leaderboard: http://localhost:5001/leaderboard
   - Subjects: http://localhost:5001/subjects
   - Subject detail: http://localhost:5001/subject/1
   - Profile: http://localhost:5001/profile
   - Login/Register: http://localhost:5001/login
   - Maths (quiz): http://localhost:5001/maths
   - Courses: http://localhost:5001/course

## Features

- **Home:** AI-based recommended subjects, continue learning, rotating quotes, today’s focus
- **Dashboard:** Progress graph, enrolled courses, streak, weak topics, badges, downloads, recent test scores
- **Profile:** Personal info, dark/light mode, reminders (daily study time, browser/email), downloads, share, 5-star rating
- **Leaderboard:** Rank, XP, streak, “ahead of X%”, comparison chart
- **Subjects:** Subject cards with week-wise roadmap, completion %, link to topic quizzes
- **Subject detail:** Topics list, time per topic, completion %, week roadmap, “where this topic is used”
- **AI layer:** Concept mastery (quiz + confidence), gap detection (score &lt; 60%), adaptive recommendations, 7-day roadmap
- **Auth:** Login/Register (JWT-style token), optional for demo (default user id=1)
- **DB:** SQLite (User, Subject, Topic, Quiz, QuizAttempt, Reminder, Rating, Download)
