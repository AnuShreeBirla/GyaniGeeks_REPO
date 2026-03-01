# Flask React Quiz App

This project is a web application that combines a Flask backend with a React frontend to create an interactive quiz platform. Users can take quizzes, submit their answers, and receive feedback on their performance.

## Project Structure

```
flask-react-quiz-app
├── backend
│   ├── app.py                # Flask application with API endpoints
│   ├── requirements.txt      # Python dependencies for the backend
│   ├── .env.example          # Template for environment variables
│   ├── templates             # HTML templates for rendering
│   │   ├── index.html        # Home page template
│   │   └── dashboard.html     # Dashboard page template
│   ├── static                # Static files (CSS, JS)
│   │   ├── css
│   │   │   └── styles.css    # CSS styles for the application
│   │   └── js
│   │       └── main.js       # JavaScript for client-side interactions
│   └── tests                 # Unit tests for the Flask application
│       └── test_app.py       # Tests for API and routes
├── frontend
│   ├── package.json          # Configuration for the React application
│   ├── public                # Public files for the React app
│   │   └── index.html        # Main HTML file for the React app
│   └── src                   # Source files for the React application
│       ├── index.js          # Entry point for the React application
│       ├── App.jsx           # Main App component
│       ├── components         # React components
│       │   ├── QuizForm.jsx  # Component for quiz input
│       │   └── Dashboard.jsx  # Component for displaying results
│       └── api               # API functions for backend communication
│           └── api.js        # Functions for making API calls
├── docker-compose.yml        # Docker configuration for running services
├── .gitignore                # Files to ignore in version control
├── LICENSE                   # Licensing information
└── README.md                 # Project documentation
```

## Getting Started

### Prerequisites

- Python 3.x
- Node.js and npm
- Docker (optional, for containerized setup)

### Backend Setup

1. Navigate to the `backend` directory:
   ```
   cd backend
   ```

2. Install the required Python packages:
   ```
   pip install -r requirements.txt
   ```

3. (Optional) Create a `.env` file based on `.env.example` to configure environment variables.

4. Run the Flask application:
   ```
   python app.py
   ```

### Frontend Setup

1. Navigate to the `frontend` directory:
   ```
   cd frontend
   ```

2. Install the required Node.js packages:
   ```
   npm install
   ```

3. Start the React application:
   ```
   npm start
   ```

### Running with Docker

1. Ensure Docker is running on your machine.

2. Run the following command in the root directory of the project:
   ```
   docker-compose up
   ```

## Usage

- Access the application at `http://localhost:5000` for the Flask backend.
- Access the React frontend at `http://localhost:3000`.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for details.