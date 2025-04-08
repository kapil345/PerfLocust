This project provides a scalable and modular framework for performance testing APIs, databases, UI interactions, and microservices using Locust.

⚙️ Setup Instructions
1️⃣ Install Dependencies
bash
Copy
Edit
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate      # Windows

pip install -r requirements.txt
🚀 Running Tests
🔹 Run Default Load Test

python runner/run_locust.py -f environments/load_test.yml


🔹 Run in Web UI Mode

python runner/run_locust.py -f environments/load_test.yml
Then open http://localhost:8089 to start the test.

🔹 Run Specific Performance Tests

Soak Test
python runner/run_locust.py -f environments/soak_test.yml


Spike Test
python runner/run_locust.py -f environments/spike_test.yml


Stress Test
python runner/run_locust.py -f environments/stress_test.yml
Concurrency Test


python runner/run_locust.py -f environments/concurrent_test.yml


🔄 Running Multiple Test Suites
If multiple test files are specified in YAML, all will run sequentially.


test_files:
  - "simulations/api_tests.py"
  - "simulations/db_tests.py"
  - "simulations/ui_tests.py"
Run:


python runner/run_locust.py -f environments/load_test.yml


⚡ Features

Supports headless and web UI modes

Runs API, UI, database, and microservice performance tests

Automated YAML-driven configuration

Supports multiple test files per execution

Easily integrated into CI/CD pipelines

