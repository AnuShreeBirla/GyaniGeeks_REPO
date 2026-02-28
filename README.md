# Project Title - The Silent Academic Dropout Crisis

An Adaptive learning system that detects real-time conceptual gaps and confidence mismatches to prevent invisible academic failure before it happens.

# 1. Problem Statement

Problem Title - The Silent Academic Dropout Crisis

Problem Description - India produces over 15 million graduates annually. Yet a significant proportion enter higher education without mastering foundational concepts from previous years. The traditional classroom model assumes that all students learn at the same pace and achieve similar understanding under uniform instruction. In reality, students absorb knowledge differently. Some struggle silently while others move ahead. With large classrooms of 60–80 students, teachers cannot realistically track individual comprehension in real time. Although online resources are abundant, they are passive and do not adapt to a student’s unique learning gaps. Students progress without mastering foundational knowledge. Learning gaps compound over time and teachers lack visibility into individual comprehension. So, by the time the gap appears in exam results, months of learning have already been built on weak foundations. Which leads to loss of academic confidence, gradual disengagement from studies, increased dropout rates, underperformance despite available content and widening learning inequality.

Target Users - Undergraduate students (Engineering, Medical, Science), { Fututre Scope - Faculty handling large classrooms (60–80 students) and Educational institutions }

Existing Gaps - 1> Student's understanding of individual concepts are not tracked properly.
  2> There is no system to identify where and when a student misunderstands something.
  3> Teachers cannot see how well each student truly understands the topic.
  4> There is no way to check how confident students are about their answers.
  5> Small learning mistakes keep building up quietly over time.
  
# 2. Problem Understanding & Approach

Root Cause Analysis - 1> Education tracks marks, not understanding.
  2> Foundational knowledge dependencies are ignored.
  3> Students often feel “confident but wrong.”
  4> Assessment occurs too late (end-semester).
  5> Large classrooms prevent individual tracking.
  6> Core Insight: Academic failure often begins months before it becomes visible.
  
Solution Strategy - We designed a full-stack intelligent platform that:
  1> Tracks topic-wise mastery
  2> Detects weak concepts early
  3> Adapts study roadmap automatically
  4> Provides structured subject flow
  5> Uses performance data to recommend next steps

# 3. Proposed Solution

Solution Overview - A web-based personalized learning platform that:
  1> Monitors mastery (0–100%) for each topic
  2> Identifies weak topics
  3> Suggests revision of prerequisites
  4> Generates weekly study plans
  5> Gamifies learning through streaks & leaderboard

Core Idea - Instead of measuring how much content a student covers, we measure how well they understand each concept and advance through the subject accordingly.

Key Features - 1>Concept Mastery Mapping. Each topic has a mastery score calculated from:
    Quiz accuracy
    Reattempt count
    Confidence rating
  2> Gap Detection Algorithm 
    If: Score < 70% OR Repeated mistakes occur
    Then: Topic marked as Weak and prerequisite revision recommended
  3> Adaptive Learning Path
    If student is weak in: “Integration”
    System recommends: Limits revision , Derivatives recap and Practice sets
  4> Personalized Dashboard. 
    Includes:
      Subject Progress and Strength
      Overall Mastery %
      Weak topic alerts
      Study streak & XP level
      Daily focus goal
      Badges & achievements
  5> Gamification
    XP system
    Leaderboard
    Badges: {Beginner , Foundation Built , Concept Mastered , Streak Champion , etc...}
  6> Smart Reminder System:
    User-set study time
    Streak-based notifications
    Email reminders
    Smart push reminders if activity drops

# 4. System Architecture

High-Level Flow
User → React Frontend → Python Backend → SQL Database → Intelligence Layer → Backend → Frontend → User

Architecture Description - The user interacts with the React frontend, which communicates with our Python backend via RESTful APIs. The backend retrieves and stores data in a SQL database and processes it through our intelligence layer built using Pandas and NumPy. The computed mastery scores and adaptive roadmap are then returned to the frontend for visualization.

Architecture Diagram(Add system architecture diagram image here)-

                                        ┌──────────────┐
                    │     User     │
                    └───────┬──────┘
                            │
                            ▼
                ┌────────────────────┐
                │   React Frontend   │
                │ (UI + Tailwind)    │
                └────────┬───────────┘
                         │ API Calls
                         ▼
                ┌────────────────────┐
                │   Python Backend   │
                │  (RESTful APIs)    │
                └───────┬────────────┘
                        │
        ┌───────────────┼────────────────┐
        ▼                               ▼
┌──────────────────┐           ┌─────────────────────┐
│   SQL Database   │           │  Intelligence Layer │
│ (Users, Scores,  │           │ (Pandas, NumPy)     │
│  Progress Data)  │           │ Mastery + Gap Logic │
└────────┬─────────┘           └──────────┬──────────┘
         │                                  │
         └───────────────┬──────────────────┘
                         ▼
                ┌────────────────────┐
                │  Backend Response  │
                └────────┬───────────┘
                         ▼
                ┌────────────────────┐
                │  Frontend Display  │
                │ (Charts - Matplot) │
                └────────┬───────────┘
                         ▼
                    ┌──────────────┐
                    │     User     │
                    └──────────────┘

# 5. Database Design
ER Diagram
(Add ER diagram image here)

ER Diagram Description
# 6. Dataset Selected
Dataset Name
Source
Data Type
Selection Reason
Preprocessing Steps
# 7. Model Selected
Model Name
Selection Reasoning
Alternatives Considered
Evaluation Metrics
# 8. Technology Stack
🧩 Technology Stack
🎨 Frontend

React
Tailwind CSS
HTML5
CSS3

Purpose:

Build responsive and interactive UI

Capture user input

Display mastery scores and adaptive roadmap

Communicate with backend via APIs

🧠 Backend

Python
JavaScript

Purpose:

Design and implement RESTful APIs

Handle authentication securely

Execute mastery scoring and gap detection logic

Connect frontend with database

🤖 Intelligence Layer

Pandas
NumPy
Matplotlib

Purpose:

Process user performance data

Calculate mastery scores

Detect learning gaps

Generate adaptive roadmaps

Visualize learning progress

🗄 Database

MySQL (or any SQL-based database)

Purpose:

Store user data securely

Track scores and progress

Maintain roadmap data

🚀 Deployment

Cloud-based hosting platform

Deployment-ready architecture

Scalable backend and database design


# 9. API Documentation & Testing
API Endpoints List
Endpoint 1:
Endpoint 2:
Endpoint 3:
API Testing Screenshots
(Add Postman / Thunder Client screenshots here)

# 10. Module-wise Development & Deliverables
Checkpoint 1: Research & Planning
Deliverables:
Checkpoint 2: Backend Development
Deliverables:
Checkpoint 3: Frontend Development
Deliverables:
Checkpoint 4: Model Training
Deliverables:
Checkpoint 5: Model Integration
Deliverables:
Checkpoint 6: Deployment
Deliverables:
# 11. End-to-End Workflow
# 12. Demo & Video
Live Demo Link:
Demo Video Link:
GitHub Repository:
# 13. Hackathon Deliverables Summary
# 14. Team Roles & Responsibilities

🧩 Aastha Musale  – Product & Operations Lead

(Strategy, Coordination & Quality Control)

Responsibilities:
📌 Product Planning

Define overall product vision

Finalize core features for MVP

Prioritize what to build (and what to skip)

🗂 Project Management

Divide tasks efficiently

Track development progress

Ensure deadlines are met within 24 hrs

🏗 System Coordination

Ensure frontend and backend integration is smooth

🎤 Presentation & Documentation

Prepare pitch deck

Write problem statement

Explain architecture to judges

Lead demo presentation

🧩 Anu Shree Birla – Backend & Intelligence Engineer
Responsibilities:

Design and implement RESTful APIs using Python

Manage structured data using SQL databases

Process and analyze user performance data using Pandas and NumPy

Develop and implement:

  Mastery score calculation logic

  Gap detection algorithm

  Adaptive roadmap generation logic

Generate learning insights and visualizations using Matplotlib

Ensure secure authentication and protected user access

Integrate backend services with the frontend using JavaScript

🧩 Amrisha Ashish – Frontend & Experience Engineer
Responsibilities:

Build UI using HTML + React + Tailwind

Design:

  Dashboard

  Subject Page

  Leaderboard

  Profile Page

Implement charts and visualization

Ensure responsive and clean UI

Integrate APIs

Improve user experience flow

   
# 15. Future Scope & Scalability
Short-Term
Long-Term

# 16. Known Limitations

1> The system currently relies on rule-based logic and does not use advanced predictive models.

2> Concept gap detection depends on quiz performance and may not fully capture deeper misunderstandings.

3> Real-time analysis may slow down with a very large number of users.

4> Confidence tracking is self-reported and may not always reflect true understanding.

5> Integration with institutional LMS platforms is not yet implemented.

# 17. Impact
Failure doesn’t happen suddenly — it builds silently. But we will change that, our system monitors concept-level understanding and student confidence in real time. It identifies learning gaps early and provides adaptive guidance before small misunderstandings turn into major academic setbacks.
