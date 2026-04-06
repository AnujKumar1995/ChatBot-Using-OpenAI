"""
OpenAI Fine-Tuning Script for Customer Support Chatbot
=====================================================
This script helps you fine-tune an OpenAI model with your custom
customer support training data.

Usage:
    python fine_tune.py upload     # Upload training file
    python fine_tune.py train      # Start fine-tuning job
    python fine_tune.py status     # Check job status
    python fine_tune.py list       # List all fine-tuning jobs
"""

import sys
import json
from openai import OpenAI
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()

TRAINING_FILE = Path(__file__).parent / "training_data" / "customer_support_training.jsonl"


def validate_training_data():
    """Validate JSONL training data format."""
    errors = []
    with open(TRAINING_FILE) as f:
        for i, line in enumerate(f, 1):
            try:
                data = json.loads(line)
                if "messages" not in data:
                    errors.append(f"Line {i}: missing 'messages' key")
                    continue
                roles = [m["role"] for m in data["messages"]]
                if roles[0] != "system":
                    errors.append(f"Line {i}: first message should be 'system'")
                if "user" not in roles:
                    errors.append(f"Line {i}: missing 'user' message")
                if "assistant" not in roles:
                    errors.append(f"Line {i}: missing 'assistant' message")
            except json.JSONDecodeError:
                errors.append(f"Line {i}: invalid JSON")

    if errors:
        print("Validation FAILED:")
        for e in errors:
            print(f"  - {e}")
        return False

    print(f"Validation PASSED: {i} training examples found.")
    return True


def upload_file():
    """Upload training file to OpenAI."""
    if not validate_training_data():
        return None

    print(f"Uploading {TRAINING_FILE}...")
    result = client.files.create(file=open(TRAINING_FILE, "rb"), purpose="fine-tune")
    print(f"File uploaded! ID: {result.id}")
    return result.id


def start_training(file_id=None):
    """Start a fine-tuning job."""
    if file_id is None:
        file_id = upload_file()
        if file_id is None:
            return

    print(f"Starting fine-tuning job with file {file_id}...")
    job = client.fine_tuning.jobs.create(
        training_file=file_id,
        model="gpt-4o-mini-2024-07-18",
        hyperparameters={"n_epochs": 3},
    )
    print(f"Fine-tuning job created!")
    print(f"  Job ID: {job.id}")
    print(f"  Status: {job.status}")
    print(f"\nRun 'python fine_tune.py status' to check progress.")
    print(f"Once complete, add the model ID to your .env as OPENAI_FINE_TUNED_MODEL")


def check_status():
    """Check status of all fine-tuning jobs."""
    jobs = client.fine_tuning.jobs.list(limit=10)
    if not jobs.data:
        print("No fine-tuning jobs found.")
        return

    for job in jobs.data:
        print(f"\nJob: {job.id}")
        print(f"  Model: {job.model}")
        print(f"  Status: {job.status}")
        if job.fine_tuned_model:
            print(f"  Fine-tuned model: {job.fine_tuned_model}")
            print(f"  -> Add to .env: OPENAI_FINE_TUNED_MODEL={job.fine_tuned_model}")
        if job.error and job.error.message:
            print(f"  Error: {job.error.message}")


def list_jobs():
    """List recent fine-tuning jobs."""
    check_status()


if __name__ == "__main__":
    commands = {
        "upload": upload_file,
        "train": start_training,
        "status": check_status,
        "list": list_jobs,
        "validate": validate_training_data,
    }

    if len(sys.argv) < 2 or sys.argv[1] not in commands:
        print("Usage: python fine_tune.py <command>")
        print(f"Commands: {', '.join(commands.keys())}")
        sys.exit(1)

    commands[sys.argv[1]]()
