
# Stock Trading Agent with Flask, Celery, and Redis

This project is a Python-based stock trading agent powered by Flask for the API, Celery for task management, and Redis for task queuing and result backend. The agent leverages advanced tools and models to handle trading-related queries, perform market data analysis, and execute trades programmatically.

---

## Features

- **Dynamic Stock Agent**: Supports web-based searches and trading operations using a combination of custom tools.
- **Asynchronous Task Execution**: Powered by Celery and Redis, enabling non-blocking API calls.
- **RESTful API**: Exposes endpoints for running the agent and checking task status.
- **Configurable Models**: Dynamically adjusts the agent's behavior based on configuration (e.g., debug mode, model selection).
- **Dockerized**: Includes Docker support for easy deployment with Flask, Celery, and Redis.

---

## Project Structure

```
project_root/
├── app/
│   ├── __init__.py          # Flask app initialization
│   ├── routes/
│   │   ├── __init__.py      # Blueprint initialization
│   │   ├── agent_routes.py  # Routes for StockAgent API
│   ├── tasks/
│   │   ├── __init__.py      # Celery task registration
│   │   └── stock_tasks.py   # Celery tasks for the StockAgent
│   ├── agents/
│   │   ├── __init__.py      # Initialization for agents
│   │   └── stock_agent.py   # StockAgent implementation
│   ├── tools/
│   │   ├── __init__.py      # Helper tools initialization
│   │   └── helpers.py       # General utility/helper functions
│   ├── config.py            # Flask and Celery configuration
├── tests/                   # Unit and integration tests
├── customagents/            # Custom libraries and tools
├── .dockerignore            # Files to exclude from Docker image
├── .env                     # Environment variables (Flask, Redis, etc.)
├── docker-compose.yml       # Docker Compose configuration
├── Dockerfile               # Dockerfile for Flask and Celery
├── requirements.txt         # Python dependencies
└── README.md                # Project documentation
```

---

## Setup and Installation

### 1. Clone the Repository

```bash
git clone https://github.com/igu1/automated-stock-market
cd automated-stock-market
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure the Environment

Create a `.env` file in the project root:

```env
DEBUG=True
SECRET_KEY=your_secret_key
MAX_ITERATIONS=10
CELERY_BROKER_URL=redis://127.0.0.1:6379/0
CELERY_RESULT_BACKEND=redis://127.0.0.1:6379/0

GEMINI_API_KEY=your_gemini_api_key
DEEPSEEK_API_KEY=your_deepseek_api_key
ALPACA_API_KEY=your_alpaca_api_key
ALPACA_SECRET_KEY=your_alpaca_secret_key
```

### 5. Start Redis

Make sure Redis is running:

```bash
redis-server
```

Alternatively, use Docker to run Redis:

```bash
docker run -d -p 6379:6379 redis
```

### 6. Start the Flask App

```bash
flask --app app run
```

### 7. Start the Celery Worker

```bash
celery -A app.tasks.stock_task.celery worker --pool=threads --loglevel=info --concurrency=4
```
---

## Usage

### Run the Agent

Send a POST request to `/agent/run`:

```bash
curl -X POST http://127.0.0.1:5000/agent/run -H "Content-Type: application/json" -d '{"query": "give me all my history trades", "debug": false}'
```

### Check Task Status

Retrieve the task status using the task ID:

```bash
curl http://127.0.0.1:5000/agent/status/<task_id>
```

---

## Running with Docker

### Build and Start the Application

```bash
docker-compose up --build
```

- **Flask API**: Accessible at `http://localhost:5000`.
- **Celery Worker**: Connected to Redis automatically.
- **Redis**: Managed by Docker Compose.

---

## Testing

Run unit and integration tests:

```bash
pytest tests/
```

---

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request for review.

---

## License

This project is licensed under the [Apache License 2.0](LICENSE).

---

## Contact

For questions or suggestions, feel free to reach out:

- **GitHub**: [igu1](https://github.com/igu1)
- **Email**: eesaard@gmail.com
