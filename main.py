"""PawPal demo — build an owner with pets and tasks, then print today's plan."""

from datetime import date, time

from pawpal_system import Owner, Pet, Scheduler, Task


def main() -> None:
    # Create an owner and two pets.
    owner = Owner(name="Josh")

    rex = Pet(name="Rex", species="Dog", age=4)
    mochi = Pet(name="Mochi", species="Cat", age=2)
    owner.add_pet(rex)
    owner.add_pet(mochi)

    # Add tasks at different times of day. "daily" tasks are due every day.
    today = date.today()
    rex.add_task(Task("Morning walk", time(7, 30), today, "daily"))
    rex.add_task(Task("Dinner", time(18, 0), today, "daily"))
    mochi.add_task(Task("Feed breakfast", time(8, 15), today, "daily"))
    mochi.add_task(Task("Litter cleanup", time(12, 0), today, "daily"))

    # Build today's plan through the scheduler.
    scheduler = Scheduler(owner)
    plan = scheduler.generate_daily_plan(today)

    # Print "Today's Schedule".
    print(f"Today's Schedule — {today:%A, %B %d, %Y}")
    print("=" * 40)
    if not plan:
        print("Nothing scheduled today.")
    else:
        for task in plan:
            print(f"  {task.time:%I:%M %p}  {task.description}")
    print("=" * 40)


if __name__ == "__main__":
    main()
