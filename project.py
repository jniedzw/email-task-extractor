"""Scans email files and extracts action items and deadlines into a sorted to do list."""
from email import policy
from email.parser import BytesParser
import re
from datetime import timedelta
import sys
import argparse
import glob

def main():
    parser = argparse.ArgumentParser(description="Extract tasks from .eml files")
    parser.add_argument("folder", help="Folder with .eml files")
    args = parser.parse_args()  
    paths = glob.glob(f"{args.folder}/*.eml")
    if not paths:
        sys.exit(f"No .eml files found in {args.folder}")
    all_tasks = []

    for path in paths:
        data = parse_email(path)
        tasks = extract_tasks(data["body"])
        
        for text in tasks:    
            all_tasks.append({
                "text": text,
                "deadline": extract_deadline(text, data["date"]),
                "from": data["from"],
                "subject": data["subject"],
                "sent": data["date"],
            })
    
    for task in rank_tasks(all_tasks):
        sent = task["sent"].strftime("%a %d %b")
        if task["deadline"] is None:
            when = "—"
        else:
            when = task["deadline"].strftime("%a %d %b")    
        print(f"{when:12}{task['text']}")
        print(f"            {task['from']} - {task['subject']} (sent {sent})")
        print()

def parse_email(path):
    with open(path, "rb") as f:
        msg = BytesParser(policy=policy.default).parse(f)
    body = msg.get_body(preferencelist=("plain",))
    
    return {
    "from": msg["from"], "subject": msg["subject"],
    "date": msg["date"].datetime, "body": body.get_content()
    }
def extract_tasks(body):
    
    tasks = []
    for line in body.splitlines():
        if re.search(r"^([-*]|\d+\.)", line):
            tasks.append(line)

        elif re.search(r"please|can you|could you|need to|needs to|make sure|important", line, re.IGNORECASE):
            tasks.append(line)
    return tasks
                    


def extract_deadline(text, received_date):
    """Return a datetime for the deadline mentioned in text or None."""
    if re.search(r"\btomorrow\b", text, re.IGNORECASE):
        return received_date + timedelta(days=1)
    if re.search(r"\btoday\b", text, re.IGNORECASE):
        return received_date

   
    match = re.search(r"\b(by|before|due|on|until)\s+(monday|tuesday|wednesday|thursday|friday|saturday|sunday)\b", text, re.IGNORECASE)
    if not match:
        return None
    day = match.group(2).lower()
    weekdays = {
        "monday": 0,
        "tuesday": 1,
        "wednesday": 2,
        "thursday": 3,
        "friday": 4,
        "saturday": 5,
        "sunday": 6,
    }
    target = weekdays[day]
    days_ahead = (target - received_date.weekday()) % 7
    if days_ahead == 0:
        days_ahead = 7
    return received_date + timedelta(days=days_ahead)
      

def rank_tasks(tasks):
    """Return tasks sorted by deadline with undated tasks last."""
    dated = []
    undated = []
    for task in tasks:
        if task["deadline"] is None:
            undated.append(task)
        else:
            dated.append(task)
    dated.sort(key=lambda t: t["deadline"])
    return dated + undated

if __name__ == "__main__":
    main()
