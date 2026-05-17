# CLI Expense Tracker

Command-line tool to track daily expenses. Built on Day 4 of my 84-day AI Engineer roadmap.

## Stack
- `argparse` — subcommand CLI interface  
- `json` + `pathlib` — file persistence  
- OOP — `ExpenseTracker` class with type hints

## Commands

```bash
python expense_tracker.py add -d "Lunch" -a 250 -c food
python expense_tracker.py list
python expense_tracker.py list -c food
python expense_tracker.py summary --month 2026-05
python expense_tracker.py remove --id 2
```

## What I learned
- argparse subparsers and type coercion
- JSON persistence with pathlib read_text/write_text
- OOP design for CLI tools
- Full Git branch → PR → merge workflow