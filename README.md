# AI-Driven Patient Intake & Appointment Reminder System

This project is an AI-driven patient intake system designed to optimize scheduling, reduce no-shows, and ensure all necessary documents are completed before a patient's visit.

## Getting Started

Follow these instructions to get the project up and running on your local machine.

### Prerequisites

- Python 3.12+
- [uv](https://github.com/astral-sh/uv) (a fast Python package installer and resolver)

### Installation

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd autointake
    ```

2.  **Install the dependencies:**
    Use `uv` to install the required packages from `pyproject.toml`.
    ```bash
    uv pip install -e .
    ```

## Running the Application

You will need two separate terminals to run the application and the simulation script.

**Terminal 1: Start the Web Server**

This command starts the FastAPI server. The `--reload` flag will automatically restart the server when you make changes to the code.

```bash
uv run start
```
or directly:
```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

**Terminal 2: Run the Intake Simulation**

This script sends a test webhook to the running application to simulate a new patient intake.

```bash
uv run test
```
or directly:
```bash
python test_intake.py
```

You should see output in the first terminal indicating that the webhook was received successfully.
