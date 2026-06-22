"""PawPal pet care system — core implementation.

Generated from diagrams/uml_draft.mmd. Implements four classes:
Task, Pet, Owner, and Scheduler.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, time


@dataclass
class Task:
    """A specific pet care activity (feeding, walking, grooming, etc.)."""

    description: str
    time: time
    date: date
    frequency: str
    is_complete: bool = False

    def mark_complete(self) -> None:
        """Mark this task as done."""
        self.is_complete = True

    def mark_incomplete(self) -> None:
        """Mark this task as not yet done."""
        self.is_complete = False

    def reschedule(self, new_date: date, new_time: time) -> None:
        """Move this task to a new date and time."""
        self.date = new_date
        self.time = new_time

    def is_due(self, on_date: date) -> bool:
        """Return True if this task should occur on the given date."""
        if on_date < self.date:
            return False

        freq = self.frequency.strip().lower()
        if freq in ("daily", "every day"):
            return True
        if freq in ("weekly", "every week"):
            return on_date.weekday() == self.date.weekday()
        if freq in ("monthly", "every month"):
            return on_date.day == self.date.day
        # "once" / "one-time" / anything unrecognized: only its exact date.
        return on_date == self.date


@dataclass
class Pet:
    """An individual pet and the care tasks associated with it."""

    name: str
    species: str
    age: int
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Attach a care task to this pet."""
        self.tasks.append(task)

    def remove_task(self, task: Task) -> None:
        """Detach a care task from this pet (no-op if not present)."""
        if task in self.tasks:
            self.tasks.remove(task)

    def get_tasks(self) -> list[Task]:
        """Return all care tasks for this pet."""
        return self.tasks

    def get_info(self) -> str:
        """Return a human-readable summary of this pet."""
        return f"{self.name} ({self.species}, age {self.age}) — {len(self.tasks)} task(s)"


@dataclass
class Owner:
    """The pet owner — manages pets and retrieves tasks across all of them."""

    name: str
    pets: list[Pet] = field(default_factory=list)
    preferences: dict[str, str] = field(default_factory=dict)

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to this owner."""
        self.pets.append(pet)

    def remove_pet(self, pet: Pet) -> None:
        """Remove a pet from this owner (no-op if not present)."""
        if pet in self.pets:
            self.pets.remove(pet)

    def get_pet(self, name: str) -> Pet | None:
        """Look up a pet by name (case-insensitive), or None if not found."""
        for pet in self.pets:
            if pet.name.lower() == name.lower():
                return pet
        return None

    def get_all_pets(self) -> list[Pet]:
        """Return every pet belonging to this owner."""
        return self.pets

    def get_all_tasks(self) -> list[Task]:
        """Return tasks gathered from every pet."""
        tasks: list[Task] = []
        for pet in self.pets:
            tasks.extend(pet.get_tasks())
        return tasks

    def set_preference(self, key: str, value: str) -> None:
        """Set an owner preference."""
        self.preferences[key] = value

    def get_preference(self, key: str) -> str | None:
        """Read an owner preference, or None if unset."""
        return self.preferences.get(key)


class Scheduler:
    """Generates a daily care plan from an owner's pets and tasks."""

    def __init__(self, owner: Owner) -> None:
        self.owner = owner

    def generate_daily_plan(self, on_date: date) -> list[Task]:
        """Build the ordered list of tasks due on the given date."""
        due_today = self.filter_tasks(self.gather_tasks(), on_date)
        return self.sort_tasks(due_today)

    def gather_tasks(self) -> list[Task]:
        """Collect tasks across all of the owner's pets (single source of truth)."""
        return self.owner.get_all_tasks()

    def sort_tasks(self, tasks: list[Task]) -> list[Task]:
        """Return tasks ordered by time of day."""
        return sorted(tasks, key=lambda t: t.time)

    def filter_tasks(self, tasks: list[Task], on_date: date) -> list[Task]:
        """Keep only tasks due on the given date."""
        return [task for task in tasks if task.is_due(on_date)]

    def detect_conflicts(self, tasks: list[Task]) -> list[Task]:
        """Return tasks that share a start time with at least one other task."""
        seen: dict[time, list[Task]] = {}
        for task in tasks:
            seen.setdefault(task.time, []).append(task)

        conflicts: list[Task] = []
        for grouped in seen.values():
            if len(grouped) > 1:
                conflicts.extend(grouped)
        return conflicts

    def build_schedule(self) -> dict[time, Task]:
        """Organize all gathered tasks into a time-keyed schedule."""
        # NOTE: one Task per time slot — simultaneous tasks collide (last wins);
        # use detect_conflicts() to surface those first.
        schedule: dict[time, Task] = {}
        for task in self.sort_tasks(self.gather_tasks()):
            schedule[task.time] = task
        return schedule
