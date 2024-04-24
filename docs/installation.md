# Installation

To install and run the FeedbackAI Tool Backend, follow these steps:

## Clone the Repository

```bash
git clone https://github.com/AlecVangilbergen/FeedbackAI-Tool-Backend.git
```

## Create a Local Database

Make sure you have PostgreSQL installed. Then, create a local database named `feedbacktool`.

```bash
createdb feedbacktool
```

## Install Dependencies

Navigate to the project directory and install the required dependencies using `pip` and the `requirements.txt` file.

```bash
pip install -r requirements.txt
```

## Run the Application

You can run the application using `uvicorn`.

```bash
uvicorn app.main:app --reload
```

This command will start the FastAPI server, and you'll be able to access the API at `http://localhost:8000`.

```bash
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

Open your web browser and navigate to `http://localhost:8001` to view the API documentation.