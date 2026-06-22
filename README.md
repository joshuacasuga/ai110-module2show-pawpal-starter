# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## 🖥️ Sample Output

Paste a sample of your app's CLI or Streamlit output here so a reader can see what a generated plan looks like:

Today's Schedule — Monday, June 22, 2026
========================================
  07:30 AM  Morning walk
  08:15 AM  Feed breakfast
  12:00 PM  Litter cleanup
  06:00 PM  Dinner
========================================

## 🧪 Testing PawPal+

```bash
# Run the full test suite:
pytest

# Run with coverage:
pytest --cov
```

Sample test output:

```
# Paste your pytest output here
```

## 📐 Smarter Scheduling

PawPal+ adds several scheduling behaviors on top of the basic data model. Each
feature and the method that implements it (all in `pawpal_system.py` unless
noted) is documented below.

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting | `Scheduler.sort_by_time()` | Orders tasks chronologically (earliest first) |
| Filtering by completion status | `Scheduler.filter_by_status()` | Returns pending-only or completed-only tasks |
| Filtering by pet | `Scheduler.filter_by_pet()` | Returns a single pet's tasks (case-insensitive name) |
| Filtering by date | `Scheduler.filter_tasks()` + `Task.is_due()` | Keeps only tasks due on a given date |
| Conflict detection | `Scheduler.conflict_warnings()` / `Scheduler.detect_conflicts()` | Flags same-time clashes as non-crashing warnings |
| Recurring tasks | `Task.next_occurrence()` + `Pet.mark_task_complete()` | Auto-spawns the next daily/weekly instance on completion |

### Sorting behavior — `Scheduler.sort_by_time()`

Uses Python's `sorted()` with a `key=lambda t: t.time` so tasks come back
ordered by time of day, earliest first. Because `Task.time` is a
`datetime.time`, it compares chronologically directly — the same result you'd
get sorting zero-padded `"HH:MM"` strings, which sort lexicographically in
order. `generate_daily_plan()` and `build_schedule()` both rely on it.

### Filtering behavior

- **`Scheduler.filter_by_status(tasks, is_complete=False)`** — keeps only tasks
  whose `is_complete` matches the argument. Defaults to pending tasks (what the
  owner still has left to do).
- **`Scheduler.filter_by_pet(pet_name)`** — returns all tasks for one pet,
  looked up case-insensitively through the owner; returns an empty list if no
  pet matches.
- **`Scheduler.filter_tasks(tasks, on_date)`** — keeps only tasks due on a given
  date, delegating the recurrence rules to `Task.is_due()`.

### Conflict detection — `Scheduler.conflict_warnings()`

A lightweight strategy that **warns rather than crashes**. It groups all
gathered tasks (same pet *or* different pets) by start time and returns one
human-readable warning string per clashing slot, e.g.
`[!] Conflict at 12:00 PM: 2 tasks overlap - Lunch, Litter cleanup`. It returns
an empty list when there are no conflicts, so callers can simply check
`if warnings:`. The lower-level `detect_conflicts()` returns the colliding
`Task` objects themselves (used by the Streamlit UI in `app.py`). Current
limitation: only exact start-time matches are detected, not overlapping
durations — see `reflection.md` §2b.

### Recurring task logic — `Task.next_occurrence()` + `Pet.mark_task_complete()`

When a recurring task is completed, the next instance is created automatically:

- **`Task.next_occurrence()`** computes a fresh, incomplete `Task` for the next
  date using `timedelta` — `+1 day` for `"daily"`, `+7 days` for `"weekly"`.
  `timedelta` rolls over month/year boundaries accurately (e.g. Dec 31 + 1 day
  → Jan 1). Non-recurring frequencies (`"monthly"`, `"once"`) return `None`.
- **`Pet.mark_task_complete(task)`** marks the task done and, if
  `next_occurrence()` produced one, attaches it to the pet's task list and
  returns it. The recurrence lives on `Pet` because that's where the task list
  lives — a `Task` has no back-reference to its pet.

## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:

1. <!-- Describe this step -->
2. <!-- Describe this step -->
3. <!-- Describe this step -->
4. <!-- Describe this step -->
5. <!-- Add more steps as needed -->

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
