import React, { useEffect, useState } from 'react';
import { fetchQuizResults } from '../api/api';

const Dashboard = () => {
    const [results, setResults] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const userId = 'Student'; // Replace with actual user ID if available
        fetchQuizResults(userId)
            .then(data => {
                setResults(data);
                setLoading(false);
            })
            .catch(err => {
                setError(err);
                setLoading(false);
            });
    }, []);

    if (loading) {
        return <div>Loading...</div>;
    }

    if (error) {
        return <div>Error: {error.message}</div>;
    }

    return (
        <div>
            <h1>Dashboard</h1>
            <h2>User ID: {results.user_id}</h2>
            <p>Accuracy: {results.accuracy}%</p>
            <p>Confidence: {results.confidence}%</p>
            <p>Mastery: {results.mastery}%</p>
            <p>Status: {results.status}</p>
            <h3>Roadmap:</h3>
            <ul>
                {results.roadmap.map((item, index) => (
                    <li key={index}>{item}</li>
                ))}
            </ul>
        </div>
    );
};

export default Dashboard;