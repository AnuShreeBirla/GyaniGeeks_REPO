import axios from 'axios';

const API_URL = 'http://localhost:5000/api/quiz';

export const submitQuiz = async (quizData) => {
    try {
        const response = await axios.post(API_URL, quizData);
        return response.data;
    } catch (error) {
        throw new Error('Error submitting quiz: ' + error.message);
    }
};