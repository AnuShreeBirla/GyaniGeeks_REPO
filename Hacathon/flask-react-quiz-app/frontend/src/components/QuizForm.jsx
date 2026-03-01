import React, { useState } from 'react';
import { submitQuiz } from '../api/api';

const QuizForm = () => {
    const [userId, setUserId] = useState('');
    const [scores, setScores] = useState([50, 50, 50]);
    const [confidence, setConfidence] = useState(70);
    const [result, setResult] = useState(null);

    const handleScoreChange = (index, value) => {
        const newScores = [...scores];
        newScores[index] = value;
        setScores(newScores);
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        const response = await submitQuiz({ user_id: userId, scores, confidence });
        setResult(response);
    };

    return (
        <div>
            <h2>Quiz Submission</h2>
            <form onSubmit={handleSubmit}>
                <div>
                    <label>User ID:</label>
                    <input type="text" value={userId} onChange={(e) => setUserId(e.target.value)} />
                </div>
                {scores.map((score, index) => (
                    <div key={index}>
                        <label>Score {index + 1}:</label>
                        <input
                            type="number"
                            value={score}
                            onChange={(e) => handleScoreChange(index, parseInt(e.target.value))}
                        />
                    </div>
                ))}
                <div>
                    <label>Confidence Level (0-100):</label>
                    <input
                        type="number"
                        value={confidence}
                        onChange={(e) => setConfidence(parseInt(e.target.value))}
                    />
                </div>
                <button type="submit">Submit</button>
            </form>
            {result && (
                <div>
                    <h3>Results:</h3>
                    <p>User ID: {result.user_id}</p>
                    <p>Accuracy: {result.accuracy}</p>
                    <p>Confidence: {result.confidence}</p>
                    <p>Mastery: {result.mastery}</p>
                    <p>Status: {result.status}</p>
                    <h4>Roadmap:</h4>
                    <ul>
                        {result.roadmap.map((item, index) => (
                            <li key={index}>{item}</li>
                        ))}
                    </ul>
                </div>
            )}
        </div>
    );
};

export default QuizForm;