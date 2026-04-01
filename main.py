from datetime import date

from pawpal_system import CareTask, Owner, Pet, Scheduler


def main() -> None:
    owner = Owner(
        name="Jordan",
        available_time=60,
        preferences=["short walks on weekdays", "prioritize medication"],
    )

    mochi = Pet(name="Mochi", species="dog", age=4, special_needs="Needs daily exercise")
    luna = Pet(name="Luna", species="cat", age=2, special_needs="Prefers evening play")

    mochi.add_task(
        CareTask(
            title="Morning walk",
            category="exercise",
            duration=20,
            time="08:30",
            priority="high",
            frequency="daily",
            due_date=date.today(),
            required=True,
        )
    )
    mochi.add_task(
        CareTask(
            title="Medication",
            category="health",
            duration=10,
            time="07:15",
            priority="high",
            frequency="daily",
            due_date=date.today(),
            required=True,
        )
    )
    luna.add_task(
        CareTask(
            title="Play session",
            category="enrichment",
            duration=15,
            time="08:30",
            priority="medium",
            frequency="daily",
            due_date=date.today(),
        )
    )
    luna.add_task(
        CareTask(
            title="Brush fur",
            category="grooming",
            duration=25,
            time="12:45",
            priority="low",
            frequency="weekly",
            due_date=date.today(),
        )
    )

    owner.add_pet(mochi)
    owner.add_pet(luna)

    scheduler = Scheduler(owner)
    next_brush_fur = scheduler.mark_task_complete("Luna", "Brush fur")
    schedule = scheduler.generate_daily_plan()

    print("Tasks Sorted By Time")
    print("=" * 20)
    for task in scheduler.sort_by_time(owner.get_all_tasks_including_completed()):
        print(f"{task.time} - {task.title} ({'done' if task.completed else 'pending'})")

    print("\nMochi's Tasks")
    print("=" * 13)
    for task in scheduler.filter_tasks(pet_name="Mochi"):
        print(f"{task.time} - {task.title}")

    print("\nCompleted Tasks")
    print("=" * 15)
    for task in scheduler.filter_tasks(completed=True):
        print(f"{task.time} - {task.title}")

    if next_brush_fur is not None:
        print("\nRecurring Task Created")
        print("=" * 22)
        print(next_brush_fur.get_description())

    print()

    print("Conflict Warnings")
    print("=" * 17)
    conflict_warnings = scheduler.detect_conflicts()
    if conflict_warnings:
        for warning in conflict_warnings:
            print(warning)
    else:
        print("No conflicts detected.")

    print()

    print("Today's Schedule")
    print("=" * 16)

    if not schedule:
        print("No tasks fit within the available time today.")
        return

    total_time = 0
    for index, task in enumerate(schedule, start=1):
        print(
            f"{index}. {task.time} - {task.title} [{task.category}] - "
            f"{task.duration} minutes, {task.priority} priority"
        )
        total_time += task.duration

    print(f"\nTotal scheduled time: {total_time} minutes")
    print("\nWhy these tasks were chosen:")
    print(scheduler.explain_plan())


if __name__ == "__main__":
    main()
