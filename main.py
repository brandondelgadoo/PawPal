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
            priority="high",
            frequency="daily",
            required=True,
        )
    )
    mochi.add_task(
        CareTask(
            title="Medication",
            category="health",
            duration=10,
            priority="high",
            frequency="daily",
            required=True,
        )
    )
    luna.add_task(
        CareTask(
            title="Play session",
            category="enrichment",
            duration=15,
            priority="medium",
            frequency="daily",
        )
    )
    luna.add_task(
        CareTask(
            title="Brush fur",
            category="grooming",
            duration=25,
            priority="low",
            frequency="weekly",
        )
    )

    owner.add_pet(mochi)
    owner.add_pet(luna)

    scheduler = Scheduler(owner)
    schedule = scheduler.generate_daily_plan()

    print("Today's Schedule")
    print("=" * 16)

    if not schedule:
        print("No tasks fit within the available time today.")
        return

    total_time = 0
    for index, task in enumerate(schedule, start=1):
        print(
            f"{index}. {task.title} [{task.category}] - "
            f"{task.duration} minutes, {task.priority} priority"
        )
        total_time += task.duration

    print(f"\nTotal scheduled time: {total_time} minutes")
    print("\nWhy these tasks were chosen:")
    print(scheduler.explain_plan())


if __name__ == "__main__":
    main()
