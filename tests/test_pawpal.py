from pawpal_system import CareTask, Pet


def test_mark_complete_changes_task_status() -> None:
    task = CareTask(
        title="Morning walk",
        category="exercise",
        duration=20,
        priority="high",
        frequency="daily",
    )

    task.mark_complete()

    assert task.completed is True


def test_add_task_increases_pet_task_count() -> None:
    pet = Pet(name="Mochi", species="dog", age=4)
    task = CareTask(
        title="Dinner",
        category="feeding",
        duration=10,
        priority="medium",
        frequency="daily",
    )

    pet.add_task(task)

    assert len(pet.care_tasks) == 1
