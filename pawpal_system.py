"""PawPal pet care system — class skeleton.

Generated from diagrams/uml_draft.mmd. Method bodies are stubs to be
implemented; signatures and type hints reflect the UML draft.
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
        ...

    def mark_incomplete(self) -> None:
        """Mark this task as not yet done."""
        ...

    def reschedule(self, new_date: date, new_time: time) -> None:
        """Move this task to a new date and time."""
        ...

    def is_due(self, on_date: date) -> bool:
        """Return True if this task is due on the given date."""
        ...


@dataclass
class Pet:
    """An individual pet and the care tasks associated with it."""

    name: str
    species: str
    age: int
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Attach a care task to this pet."""
        ...

    def remove_task(self, task: Task) -> None:
        """Detach a care task from this pet."""
        ...

    def get_tasks(self) -> list[Task]:
        """Return all care tasks for this pet."""
        ...

    def get_info(self) -> str:
        """Return a human-readable summary of this pet."""
        ...


@dataclass
class Owner:
    """The pet owner — manages pets and retrieves tasks across all of them."""

    name: str
    pets: list[Pet] = field(default_factory=list)
    preferences: dict[str, str] = field(default_factory=dict)

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to this owner."""
        ...

    def remove_pet(self, pet: Pet) -> None:
        """Remove a pet from this owner."""
        ...

    def get_pet(self, name: str) -> Pet | None:
        """Look up a pet by name."""
        ...

    def get_all_pets(self) -> list[Pet]:
        """Return every pet belonging to this owner."""
        ...

    def get_all_tasks(self) -> list[Task]:
        """Return tasks gathered from every pet."""
        ...

    def set_preference(self, key: str, value: str) -> None:
        """Set an owner preference."""
        ...

    def get_preference(self, key: str) -> str | None:
        """Read an owner preference."""
        ...


class Scheduler:
    """Generates a daily care plan from an owner's pets and tasks."""

    def __init__(self, owner: Owner) -> None:
        self.owner = owner

    def generate_daily_plan(self, on_date: date) -> list[Task]:
        """Build the ordered list of tasks due on the given date."""
        ...

    def gather_tasks(self) -> list[Task]:
        """Collect tasks across all of the owner's pets."""
        ...

    def sort_tasks(self, tasks: list[Task]) -> list[Task]:
        """Sort tasks (e.g. by time)."""
        ...

    def filter_tasks(self, tasks: list[Task], on_date: date) -> list[Task]:
        """Keep only tasks due on the given date."""
        ...

    def detect_conflicts(self, tasks: list[Task]) -> list[Task]:
        """Return tasks that overlap or conflict in the schedule."""
        ...

    def build_schedule(self) -> dict[time, Task]:
        """Organize tasks into a time-keyed schedule for the owner."""
        ...
