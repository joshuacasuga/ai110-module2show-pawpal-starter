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

====================================================================================================== test session starts ======================================================================================================
platform win32 -- Python 3.14.2, pytest-9.0.3, pluggy-1.6.0
rootdir: E:\CodePath AI Weekly Tasks\Module 2\Week 4\ai110-module2show-pawpal-starter\tests
plugins: anyio-4.13.0
collected 18 items                                                                                                                                                                                                               

test_pawpal.py ..................                                                                                                                                                                                          [100%]

====================================================================================================== 18 passed in 0.04s =======================================================================================================

Confidence Level: 5

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

This section walks through PawPal+ end to end so a reader can follow along without watching a video.

### Main UI features (Streamlit — `app.py`)

The app is a single scrolling page. From top to bottom, a user can:

- **Set the owner name** — a text input keeps the persisted `Owner` in sync.
- **Add a pet** — enter a name, pick a species (`dog` / `cat` / `other`), and set an
  age, then click **Add pet**. Duplicate names (case-insensitive) are rejected with
  an info message.
- **Schedule a task** — choose which pet it's for, give it a title, pick a time, and
  select a frequency (`daily` / `weekly` / `monthly` / `once`), then click **Add task**.
- **Review current tasks** — every pet renders as a table (Time / Task / Frequency /
  Status) already sorted chronologically via `Scheduler.sort_by_time()`.
- **Generate today's schedule** — click **Generate schedule** to build, filter, and
  sort the day's plan, see a pending-vs-total summary, and get one warning per
  time conflict.

### Example workflow

1. Open the app and confirm the owner name (defaults to **Jordan**).
2. **Add a pet**: name `Mochi`, species `cat`, age `2` → success message confirms it.
3. **Schedule a task**: for `Mochi`, title `Feed breakfast`, time `08:15 AM`,
   frequency `daily` → it appears in Mochi's task table.
4. Add a second pet (`Rex`) and a few more tasks, including two at the **same time**
   to demonstrate conflict handling.
5. Click **Generate schedule** to view today's plan as a clean table, with a
   `st.success` summary of how many tasks are still pending and a `st.warning` for
   each clashing time slot.

### Key Scheduler behaviors shown

- **Sorting** — tasks are entered out of order but always display earliest-first
  (`Scheduler.sort_by_time()`), in both the per-pet tables and the daily plan.
- **Date filtering** — only tasks due on the chosen day appear in the plan
  (`Scheduler.filter_tasks()` + `Task.is_due()`), respecting each task's frequency.
- **Status filtering** — completed tasks are separated from pending ones
  (`Scheduler.filter_by_status()`); the UI shows a pending-vs-total count.
- **Conflict warnings** — same-time tasks (even across different pets) are flagged
  as non-crashing warnings (`Scheduler.conflict_warnings()`).
- **Recurrence** — completing a recurring task auto-spawns its next instance
  (`Pet.mark_task_complete()` + `Task.next_occurrence()`).

### Sample CLI output (`python main.py`)

The CLI demo in `main.py` builds an owner with two pets, adds tasks deliberately out
of order (including a 12:00 PM clash across two pets), completes one task to trigger
recurrence, then exercises each Scheduler behavior:

```text
Auto-recurrence (mark_task_complete):
  Completed: Feed breakfast on 2026-06-22
  Next instance auto-created for: 2026-06-23

Raw task order (as added):
  06:00 PM  Dinner
  07:30 AM  Morning walk
  12:00 PM  Lunch
  12:00 PM  Litter cleanup
  08:15 AM  Feed breakfast
  08:15 AM  Feed breakfast

Sorted by time (sort_by_time):
  07:30 AM  Morning walk
  08:15 AM  Feed breakfast
  08:15 AM  Feed breakfast
  12:00 PM  Lunch
  12:00 PM  Litter cleanup
  06:00 PM  Dinner

Pending tasks only (filter_by_status):
  07:30 AM  Morning walk
  08:15 AM  Feed breakfast
  12:00 PM  Lunch
  12:00 PM  Litter cleanup
  06:00 PM  Dinner

Completed tasks only:
  08:15 AM  Feed breakfast

Rex's tasks only (filter_by_pet), sorted by time:
  07:30 AM  Morning walk
  12:00 PM  Lunch
  06:00 PM  Dinner

Today's Schedule - Monday, June 22, 2026
========================================
  07:30 AM  Morning walk
  08:15 AM  Feed breakfast
  12:00 PM  Lunch
  12:00 PM  Litter cleanup
  06:00 PM  Dinner
========================================

Schedule warnings:
  [!] Conflict at 12:00 PM: 2 tasks overlap - Lunch, Litter cleanup
```

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
