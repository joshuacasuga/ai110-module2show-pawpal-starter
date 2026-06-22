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

    # Add tasks deliberately OUT OF ORDER so we can see sort_by_time() work.
    # "daily" tasks are due every day.
    today = date.today()
    rex.add_task(Task("Dinner", time(18, 0), today, "daily"))
    rex.add_task(Task("Morning walk", time(7, 30), today, "daily"))
    mochi.add_task(Task("Litter cleanup", time(12, 0), today, "daily"))
    mochi.add_task(Task("Feed breakfast", time(8, 15), today, "daily"))
    # Deliberate clash: Rex's lunch also at 12:00 PM — same time as Mochi's
    # litter cleanup, across two different pets, to exercise conflict detection.
    rex.add_task(Task("Lunch", time(12, 0), today, "daily"))

    # Mark one task done so the status filter has something to separate out.
    # mark_task_complete() also auto-spawns the next occurrence for recurring
    # ("daily"/"weekly") tasks.
    feed_breakfast = mochi.get_tasks()[1]  # "Feed breakfast" (daily)
    next_feed = mochi.mark_task_complete(feed_breakfast)
    print("Auto-recurrence (mark_task_complete):")
    print(f"  Completed: {feed_breakfast.description} on {feed_breakfast.date}")
    if next_feed is not None:
        print(f"  Next instance auto-created for: {next_feed.date}\n")

    scheduler = Scheduler(owner)

    # 1) SORTING — feed the raw (unsorted) tasks through sort_by_time().
    raw_tasks = scheduler.gather_tasks()
    print("Raw task order (as added):")
    for task in raw_tasks:
        print(f"  {task.time:%I:%M %p}  {task.description}")

    print("\nSorted by time (sort_by_time):")
    for task in scheduler.sort_by_time(raw_tasks):
        print(f"  {task.time:%I:%M %p}  {task.description}")

    # 2) FILTERING by completion status.
    print("\nPending tasks only (filter_by_status):")
    for task in scheduler.sort_by_time(scheduler.filter_by_status(raw_tasks)):
        print(f"  {task.time:%I:%M %p}  {task.description}")

    print("\nCompleted tasks only:")
    for task in scheduler.filter_by_status(raw_tasks, is_complete=True):
        print(f"  {task.time:%I:%M %p}  {task.description}")

    # 3) FILTERING by pet.
    print("\nRex's tasks only (filter_by_pet), sorted by time:")
    for task in scheduler.sort_by_time(scheduler.filter_by_pet("Rex")):
        print(f"  {task.time:%I:%M %p}  {task.description}")

    # 4) The full daily plan (filter due-today + sort) as before.
    plan = scheduler.generate_daily_plan(today)
    print(f"\nToday's Schedule - {today:%A, %B %d, %Y}")
    print("=" * 40)
    if not plan:
        print("Nothing scheduled today.")
    else:
        for task in plan:
            print(f"  {task.time:%I:%M %p}  {task.description}")
    print("=" * 40)

    # 5) CONFLICT DETECTION — warn (don't crash) on same-time tasks.
    warnings = scheduler.conflict_warnings(plan)
    if warnings:
        print("\nSchedule warnings:")
        for message in warnings:
            print(f"  {message}")
    else:
        print("\nNo scheduling conflicts.")


if __name__ == "__main__":
    main()
