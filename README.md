# Email Task Extractor and Organiser
#### Video Demo: <URL HERE>
#### Description:

# Email Task Extractor and Organiser

#### Video Demo: <URL HERE>

#### Description:

This project is an Email Task Extractor. The code in project.py reads .eml files from a folder named on the command line. These .eml files hold buried deadlines within the emails which need to be extracted and sorted for easy reading. The tasks that are extracted are requests and action items that the sender is asking you to complete. Then each task from the emails is sorted into its deadlines by date with the closest date being first in the list. The last pieces of text will be the ones with no deadline or date within the email.

## Usage
Run python project.py emails

```
Wed 26 Aug  Legal came back overnight. Could you look at the redlines today? It is
            Nadia Haddad <nadia.haddad@example.com> - contract review (sent Wed 26 Aug)

Fri 28 Aug  - Rotate the staging credentials due Friday
            Tomasz Lewandowski <tomasz@example.org> - handover notes (sent Tue 25 Aug)

—           - Archive the old dashboards, no particular rush
            Tomasz Lewandowski <tomasz@example.org> - handover notes (sent Tue 25 Aug)
```

## Files

**project.py** — Functions

parse_email - Reads one .eml file and returns a dict with sender, subject, date and body.

extract_tasks - Returns a list by using request phrases like please or can you and also returns lines starting with bullet points or numbers.

extract_deadline - Return a datetime for the deadline mentioned in text or None.

rank_tasks - Return tasks sorted by deadline with the undated tasks last.

**test_project.py** — [what's covered, and why these three functions are
the testable ones]

I did not test the first function parse_email because it needs a file whereas the other functions can be tested using made up values.

1. test_extract_tasks 
    This tests that the function correctly extracts the text from anywhere in the body. Also that it ignores anything else on other lines.

2. test_extract_deadline
    The test firstly calculates the correct deadline date from when the email arrived. Then the function will also return None if no date or day is within the text.

3. test_rank_tasks
    This passes three tasks into a random order and then checks that they come back in the correct order which is earliest first and undated last.

**emails/** — 
The emails are test files and are not real. They cover different scenarios and edge cases to test the code properly. As an example there is a multi part email, one newsletter with no task at all.

**requirements.txt** — Lists pytest. The project uses the standard library nothing else required.

## How tasks are identified

They are identified using two rules. First one that spots bullet points or numbers eg. '- Ping Marcus about VPN access'. Second a rule that finds request phrases eg. 'Also please double-check the headcount tab'. These rules also miss out and ignore Read online: and Unsubscribe: from sample 03 because they're not addressed to a person.

## How deadlines are resolved

Deadlines are calculated relative to the date on the email. They are handled using today, tomorrow and a weekday that has key words before. Sam's email arrived Friday 21 August saying "tomorrow morning" so the deadline is Saturday 22 August and still would if you ran it next year.

## Design decisions

Some of the decisions that were made was to create an allowlist because a blocklist would allow false positives to slip through. The original version would have allowed 'it's been red since Tuesday' and turned it into a deadline. Whereas with an allowlist allowing words such as by, before, due, on ect it removed any false positives such as 'we shipped it Tuesday'. Overall false positives cost more than misses for a to do list. extract_tasks returns plain strings so all three functions are testable without constructing an email.

## Known limitations

Date formats are not included only days of the week and today or tomorrow are.
The deadlines have to be within the same sentence otherwise they're not picked up eg. if the deadline is three sentences away.
Tasks that are addressed to someone else get included eg. '2. Someone should look at the failing nightly job'.
One gap within this code is that real inboxes would produce false positives. Real inboxes are filled with please and can you so an example that would land in the to do list is eg. 'Please do not reply to this message'.