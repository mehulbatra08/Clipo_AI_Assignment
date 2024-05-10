# Video Project API

This is a simple RESTful API for managing video projects, including CRUD operations and user authentication.

- **CRUD Operations**: Create, read, update, and delete video projects.
- **User Authentication**: Token-based authentication with JWT.
- **Testing**: Unit tests for CRUD operations.
## Setup Instructions
To set up the project locally, follow these steps:

1. Clone the repository: `git clone <repo-url>`
2. Navigate to the project directory: `cd video_project_api`
3. Create a virtual environment: `python3 -m venv venv`
4. Activate the virtual environment:
   - **Linux/macOS**: `source venv/bin/activate`
   - **Windows**: `venv\Scripts\activate`
5. Install the required dependencies: `pip install -r requirements.txt`
6. Initialize the database (if applicable):
   - Apply migrations: `flask db upgrade`
  
7. ## Running the Application
To start the Flask server, ensure you've set up the virtual environment and installed the dependencies:

1. Start the Flask server: `flask run`
2. Access the API at `http://localhost:5000`
