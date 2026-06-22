"""Simple tests for the PawPal system."""

import sys
from datetime import date, time, timedelta
from pathlib import Path

# Make pawpal_system.py (one directory up) importable when running from tests/.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from pawpal_system import Owner, Pet, Scheduler, Task


def test_task_completion():
    """Calling mark_complete() changes the task's status to done."""
    task = Task("Morning walk", time(7, 30), date.today(), "daily")
    assert task.is_complete is False

    task.mark_complete()

    assert task.is_complete is True


def test_task_addition():
    """Adding a task to a Pet increases that pet's task count."""
    pet = Pet(name="Rex", species="Dog", age=4)
    assert len(pet.get_tasks()) == 0

    pet.add_task(Task("Dinner", time(18, 0), date.today(), "daily"))

    assert len(pet.get_tasks()) == 1


# --- Sorting correctness ---------------------------------------------------


def test_sort_by_time_orders_chronologically():
    """sort_by_time() returns tasks earliest-first regardless of input order."""
    owner = Owner(name="Josh")
    pet = Pet(name="Rex", species="Dog", age=4)
    owner.add_pet(pet)

    # Added deliberately out of chronological order.
    pet.add_task(Task("Dinner", time(18, 0), date.today(), "daily"))
    pet.add_task(Task("Morning walk", time(7, 30), date.today(), "daily"))
    pet.add_task(Task("Lunch", time(12, 0), date.today(), "daily"))

    scheduler = Scheduler(owner)
    ordered = scheduler.sort_by_time(scheduler.gather_tasks())

    times = [t.time for t in ordered]
    assert times == [time(7, 30), time(12, 0), time(18, 0)]
    assert times == sorted(times)


def test_sort_by_time_empty_list():
    """Sorting an empty task list returns an empty list (no crash)."""
    owner = Owner(name="Josh")
    scheduler = Scheduler(owner)

    assert scheduler.sort_by_time([]) == []


# --- Recurrence logic ------------------------------------------------------


def test_daily_completion_spawns_next_day_task():
    """Completing a daily task auto-creates a fresh task for the next day."""
    pet = Pet(name="Mochi", species="Cat", age=2)
    start = date(2026, 6, 22)
    task = Task("Feed breakfast", time(8, 15), start, "daily")
    pet.add_task(task)

    next_task = pet.mark_task_complete(task)

    # Original is now done; a new incomplete instance was attached.
    assert task.is_complete is True
    assert next_task is not None
    assert next_task.date == start + timedelta(days=1)
    assert next_task.is_complete is False
    assert next_task in pet.get_tasks()
    assert len(pet.get_tasks()) == 2


def test_weekly_completion_spawns_next_week_task():
    """Completing a weekly task schedules the next occurrence 7 days out."""
    pet = Pet(name="Rex", species="Dog", age=4)
    start = date(2026, 6, 22)
    task = Task("Grooming", time(9, 0), start, "weekly")
    pet.add_task(task)

    next_task = pet.mark_task_complete(task)

    assert next_task is not None
    assert next_task.date == start + timedelta(days=7)


def test_once_completion_does_not_recur():
    """A non-recurring task spawns nothing when completed."""
    pet = Pet(name="Rex", species="Dog", age=4)
    task = Task("Vet visit", time(15, 0), date.today(), "once")
    pet.add_task(task)

    next_task = pet.mark_task_complete(task)

    assert next_task is None
    assert len(pet.get_tasks()) == 1


def test_next_occurrence_rolls_over_year_boundary():
    """next_occurrence() uses real date math across month/year boundaries."""
    task = Task("Dinner", time(18, 0), date(2026, 12, 31), "daily")

    nxt = task.next_occurrence()

    assert nxt is not None
    assert nxt.date == date(2027, 1, 1)


# --- Conflict detection ----------------------------------------------------


def test_detect_conflicts_flags_duplicate_times():
    """Tasks sharing a start time (even across pets) are flagged as conflicts."""
    owner = Owner(name="Josh")
    rex = Pet(name="Rex", species="Dog", age=4)
    mochi = Pet(name="Mochi", species="Cat", age=2)
    owner.add_pet(rex)
    owner.add_pet(mochi)

    # Same time, different pets -> conflict.
    rex.add_task(Task("Lunch", time(12, 0), date.today(), "daily"))
    mochi.add_task(Task("Litter cleanup", time(12, 0), date.today(), "daily"))
    # A non-colliding task that must NOT appear in the conflict list.
    rex.add_task(Task("Morning walk", time(7, 30), date.today(), "daily"))

    scheduler = Scheduler(owner)
    conflicts = scheduler.detect_conflicts(scheduler.gather_tasks())

    descriptions = {t.description for t in conflicts}
    assert descriptions == {"Lunch", "Litter cleanup"}
    assert "Morning walk" not in descriptions


def test_no_conflicts_when_times_differ():
    """Distinct times produce no conflicts and no warnings."""
    owner = Owner(name="Josh")
    pet = Pet(name="Rex", species="Dog", age=4)
    owner.add_pet(pet)
    pet.add_task(Task("Morning walk", time(7, 30), date.today(), "daily"))
    pet.add_task(Task("Dinner", time(18, 0), date.today(), "daily"))

    scheduler = Scheduler(owner)
    tasks = scheduler.gather_tasks()

    assert scheduler.detect_conflicts(tasks) == []
    assert scheduler.conflict_warnings(tasks) == []


def test_conflict_warnings_are_human_readable():
    """conflict_warnings() returns one message per clashing time slot."""
    owner = Owner(name="Josh")
    pet = Pet(name="Rex", species="Dog", age=4)
    owner.add_pet(pet)
    pet.add_task(Task("Lunch", time(12, 0), date.today(), "daily"))
    pet.add_task(Task("Playtime", time(12, 0), date.today(), "daily"))

    scheduler = Scheduler(owner)
    warnings = scheduler.conflict_warnings(scheduler.gather_tasks())

    assert len(warnings) == 1
    assert "Conflict" in warnings[0]
    assert "Lunch" in warnings[0] and "Playtime" in warnings[0]


# --- Due-date filtering ----------------------------------------------------


def test_daily_task_due_on_and_after_start():
    """A daily task is due on its start date and every day after."""
    start = date(2026, 6, 22)
    task = Task("Feed", time(8, 0), start, "daily")

    assert task.is_due(start) is True
    assert task.is_due(start + timedelta(days=5)) is True
    assert task.is_due(start - timedelta(days=1)) is False


def test_weekly_task_due_only_on_matching_weekday():
    """A weekly task is due only on the same weekday as its start date."""
    start = date(2026, 6, 22)  # a Monday
    task = Task("Grooming", time(9, 0), start, "weekly")

    assert task.is_due(start) is True
    assert task.is_due(start + timedelta(days=7)) is True
    assert task.is_due(start + timedelta(days=1)) is False  # Tuesday


def test_once_task_due_only_on_exact_date():
    """A one-time task is due only on its exact date."""
    start = date(2026, 6, 22)
    task = Task("Vet visit", time(15, 0), start, "once")

    assert task.is_due(start) is True
    assert task.is_due(start + timedelta(days=1)) is False


# --- Filtering by pet / status ---------------------------------------------


def test_filter_by_pet_is_case_insensitive():
    """filter_by_pet() matches names case-insensitively, [] for unknown pets."""
    owner = Owner(name="Josh")
    rex = Pet(name="Rex", species="Dog", age=4)
    owner.add_pet(rex)
    rex.add_task(Task("Morning walk", time(7, 30), date.today(), "daily"))

    scheduler = Scheduler(owner)

    assert len(scheduler.filter_by_pet("rex")) == 1
    assert scheduler.filter_by_pet("Nobody") == []


def test_filter_by_status_separates_pending_and_done():
    """filter_by_status() splits tasks by completion state (defaults to pending)."""
    owner = Owner(name="Josh")
    pet = Pet(name="Rex", species="Dog", age=4)
    owner.add_pet(pet)
    done = Task("Morning walk", time(7, 30), date.today(), "daily")
    pending = Task("Dinner", time(18, 0), date.today(), "daily")
    pet.add_task(done)
    pet.add_task(pending)
    done.mark_complete()

    scheduler = Scheduler(owner)
    tasks = scheduler.gather_tasks()

    assert scheduler.filter_by_status(tasks) == [pending]
    assert scheduler.filter_by_status(tasks, is_complete=True) == [done]


# --- Edge cases ------------------------------------------------------------


def test_daily_plan_empty_for_pet_with_no_tasks():
    """A pet with no tasks yields an empty daily plan (no crash)."""
    owner = Owner(name="Josh")
    owner.add_pet(Pet(name="Rex", species="Dog", age=4))

    scheduler = Scheduler(owner)

    assert scheduler.generate_daily_plan(date.today()) == []


def test_generate_daily_plan_filters_and_sorts():
    """generate_daily_plan() returns only due tasks, ordered by time."""
    owner = Owner(name="Josh")
    pet = Pet(name="Rex", species="Dog", age=4)
    owner.add_pet(pet)
    today = date(2026, 6, 22)
    pet.add_task(Task("Dinner", time(18, 0), today, "daily"))
    pet.add_task(Task("Morning walk", time(7, 30), today, "daily"))
    # Not due today: a one-time task dated tomorrow.
    pet.add_task(Task("Vet visit", time(9, 0), today + timedelta(days=1), "once"))

    scheduler = Scheduler(owner)
    plan = scheduler.generate_daily_plan(today)

    assert [t.description for t in plan] == ["Morning walk", "Dinner"]
