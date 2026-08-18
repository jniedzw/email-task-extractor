"""Scans email files and extracts action items and deadlines into a sorted to-do list."""


def main():
    ...


def parse_email(path):
    """Read an .eml file and return a dict with from, subject, date, body."""
    ...


def extract_tasks(body):
    """Return a list of action-item strings found in an email body."""
    ...


def extract_deadline(text, received_date):
    """Return a datetime for the deadline mentioned in text, or None."""
    ...


def rank_tasks(tasks):
    """Return tasks sorted by deadline, then urgency."""
    ...


if __name__ == "__main__":
    main()
