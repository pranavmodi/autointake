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
    Use `uv` to install the required packages.
    ```bash
    uv pip install -r requirements.txt
    ```

4.  **Set up environment variables:**
    Create a `.env` file in the `autointake` directory by copying the example file. This file contains the database connection string and other secrets.
    ```bash
    cp .env.example .env
    ```
    Then, edit the `.env` file with your actual database credentials.

## Running the Application

This command starts the FastAPI server. The `--reload` flag will automatically restart the server when you make changes to the code.

```bash
python autointake/main.py
```

## Running Tests

To run the tests, use the following command:

```bash
pytest
```
