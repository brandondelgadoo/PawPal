from datetime import date, timedelta

from pawpal_system import CareTask, Owner, Pet, Scheduler


def test_mark_complete_changes_task_status() -> None:
    task = CareTask(
        title="Morning walk",
        category="exercise",
        duration=20,
        time="08:00",
        priority="high",
        frequency="daily",
        due_date=date.today(),
    )

    task.mark_complete()

    assert task.completed is True


def test_add_task_increases_pet_task_count() -> None:
    pet = Pet(name="Mochi", species="dog", age=4)
    task = CareTask(
        title="Dinner",
        category="feeding",
        duration=10,
        time="17:30",
        priority="medium",
        frequency="daily",
        due_date=date.today(),
    )

    pet.add_task(task)

    assert len(pet.care_tasks) == 1


def test_mark_task_complete_creates_next_daily_occurrence() -> None:
    pet = Pet(name="Mochi", species="dog", age=4)
    task = CareTask(
        title="Morning walk",
        category="exercise",
        duration=20,
        time="08:00",
        priority="high",
        frequency="daily",
        due_date=date.today(),
    )

    pet.add_task(task)
    next_task = pet.mark_task_complete("Morning walk")

    assert task.completed is True
    assert next_task is not None
    assert next_task.due_date == date.today() + timedelta(days=1)
    assert next_task.completed is False


def test_detect_conflicts_returns_warning_for_same_time_tasks() -> None:
    owner = Owner(name="Jordan", available_time=60)
    mochi = Pet(name="Mochi", species="dog", age=4)
    luna = Pet(name="Luna", species="cat", age=2)

    mochi.add_task(
        CareTask(
            title="Morning walk",
            category="exercise",
            duration=20,
            time="08:30",
            priority="high",
            frequency="daily",
            due_date=date.today(),
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

    owner.add_pet(mochi)
    owner.add_pet(luna)

    scheduler = Scheduler(owner)
    warnings = scheduler.detect_conflicts()

    assert len(warnings) == 1
    assert "conflicts with" in warnings[0]
