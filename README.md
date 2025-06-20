# AI-Driven Patient Intake & Appointment Reminder System

This project is an AI-driven patient intake system designed to optimize scheduling, reduce no-shows, and ensure all necessary documents are completed before a patient's visit.

## Getting Started

Follow these instructions to get the project up and running on your local machine.

### Prerequisites

- Python 3.12+
- [uv](https://github.com/astral-sh/uv) (a fast Python package installer and resolver)

### Installation & Setup

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd autointake
    ```

2.  **Create a virtual environment:**
    It's recommended to use a virtual environment to manage dependencies.
    ```bash
    python -m venv venv
    source venv/bin/activate
    ```

3.  **Install dependencies:**
    Use `uv` to install the required packages from `pyproject.toml`.
    ```bash
    uv pip install -e .
    ```

4.  **Set up environment variables:**
    Create a `.env` file in the root directory. This file will contain secrets like database connection strings and API keys. You can start by copying the example if one exists, or create a new one.

    ```bash
    # Create an empty .env file
    touch .env
    ```
    Then, edit the `.env` file with your actual credentials.

## Available Commands

### Run the Application

This command starts the FastAPI server using uvicorn. The `--reload` flag will automatically restart the server when you make changes to the code.

```bash
uvicorn autointake.main:app --reload
```

### Run the Celery Worker

This command starts a Celery worker that will listen for and execute the asynchronous tasks, such as sending an SMS.

```bash
celery -A autointake.app.celery_app worker --loglevel=INFO
```

### Run the Celery Beat Scheduler

This command starts the Celery scheduler, which is responsible for triggering the periodic tasks, like checking for reminders. It should be run as a separate service.

```bash
celery -A autointake.app.celery_app beat --loglevel=INFO
```

### Run Tests

To run the tests, use the following command (assuming tests are set up with pytest):

```bash
python evals/main_eval.py
```
