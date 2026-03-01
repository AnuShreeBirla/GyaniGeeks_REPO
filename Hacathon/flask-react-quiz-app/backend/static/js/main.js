const submitQuiz = async (quizData) => {
    try {
        const response = await fetch('/api/quiz', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(quizData),
        });

        if (!response.ok) {
            throw new Error('Network response was not ok');
        }

        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error submitting quiz:', error);
        return { success: false, error: error.message };
    }
};

document.addEventListener('DOMContentLoaded', () => {
    const quizForm = document.getElementById('quiz-form');

    if (quizForm) {
        quizForm.addEventListener('submit', async (event) => {
            event.preventDefault();

            const userId = document.getElementById('user-id').value;
            const scores = Array.from(document.querySelectorAll('input[name="score"]')).map(input => parseInt(input.value, 10));
            const confidence = parseInt(document.getElementById('confidence').value, 10);

            const quizData = { user_id: userId, scores, confidence };
            const result = await submitQuiz(quizData);

            if (result.success) {
                // Handle successful response (e.g., display results)
                console.log('Quiz submitted successfully:', result);
            } else {
                // Handle error response
                console.error('Error:', result.error);
            }
        });
    }
});