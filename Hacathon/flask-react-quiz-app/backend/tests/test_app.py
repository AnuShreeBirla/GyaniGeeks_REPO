from flask import Flask, jsonify
import json

def test_quiz_submit(client):
    response = client.post('/api/quiz', json={
        'user_id': 'TestUser',
        'scores': [80, 90, 70],
        'confidence': 75
    })
    data = json.loads(response.data)

    assert response.status_code == 200
    assert data['success'] is True
    assert data['user_id'] == 'TestUser'
    assert data['accuracy'] == 80.0
    assert data['confidence'] == 75
    assert data['mastery'] >= 0  # Check if mastery is calculated
    assert isinstance(data['roadmap'], list)  # Ensure roadmap is a list

def test_quiz_submit_invalid_data(client):
    response = client.post('/api/quiz', json={})
    data = json.loads(response.data)

    assert response.status_code == 400
    assert data['success'] is False
    assert 'error' in data  # Ensure error message is returned

def test_home_page(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'Welcome' in response.data  # Check for a welcome message or title

def test_dashboard_page(client):
    response = client.get('/dashboard')
    assert response.status_code == 200
    assert b'Dashboard' in response.data  # Check for dashboard title or content