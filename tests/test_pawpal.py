"""Simple tests for the PawPal system."""

import sys
from datetime import date, time
from pathlib import Path

# Make pawpal_system.py (one directory up) importable when running from tests/.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from pawpal_system import Pet, Task


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
