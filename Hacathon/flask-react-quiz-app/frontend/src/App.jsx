import React, { useState } from 'react';
import QuizForm from './components/QuizForm';
import Dashboard from './components/Dashboard';

const App = () => {
    const [quizData, setQuizData] = useState(null);

    const handleQuizSubmit = (data) => {
        setQuizData(data);
    };

    return (
        <div className="App">
            <h1>Quiz Application</h1>
            {!quizData ? (
                <QuizForm onSubmit={handleQuizSubmit} />
            ) : (
                <Dashboard data={quizData} />
            )}
        </div>
    );
};

export default App;