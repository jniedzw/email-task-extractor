from project import parse_email, extract_tasks, extract_deadline, rank_tasks
from datetime import datetime


def test_extract_tasks():
    body = "Hi there\nPlease send the report\nThanks"
    assert extract_tasks(body) == ["Please send the report"]

    body = "Good morning james,\nCan you finish and update the project before friday"
    assert extract_tasks(body) == [
        "Can you finish and update the project before friday"
    ]


def test_extract_deadline():
    monday = datetime(2026, 8, 17)
    assert extract_deadline("tomorrow", monday) == datetime(2026, 8, 18)
    assert extract_deadline("sometime", monday) is None


def test_rank_tasks():
    later = {"text": "later", "deadline": datetime(2026, 8, 21)}
    sooner = {"text": "sooner", "deadline": datetime(2026, 8, 15)}
    undated = {"text": "undated", "deadline": None}

    assert rank_tasks([later, undated, sooner]) == [sooner, later, undated]
