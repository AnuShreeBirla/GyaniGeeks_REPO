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
  Tracks topic-wise mastery
  Detects weak concepts early
  Adapts study roadmap automatically
  Provides structured subject flow
  Uses performance data to recommend next steps

# 3. Proposed Solution

Solution Overview - A web-based personalized learning platform that:
  Monitors mastery (0–100%) for each topic
  Identifies weak topics
  Suggests revision of prerequisites
  Generates weekly study plans
  Gamifies learning through streaks & leaderboard

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
User → Frontend → Backend → Model → Database → Response

Architecture Description
Architecture Diagram
(Add system architecture diagram image here)

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
Frontend
Backend
ML/AI
Database
Deployment
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

Design and implement APIs using Python

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

Build UI using React + Tailwind

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
16. Known Limitations
17. Impact
