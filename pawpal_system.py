from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, timedelta


PRIORITY_ORDER = {
    "high": 0,
    "medium": 1,
    "low": 2,
}


@dataclass
class CareTask:
    title: str
    category: str
    duration: int
    time: str
    priority: str
    frequency: str
    due_date: date = field(default_factory=date.today)
    required: bool = False
    completed: bool = False

    def fits_in_time(self, available_time: int) -> bool:
        """Return whether the task can fit within the available time."""
        return self.duration <= available_time

    def mark_complete(self) -> None:
        """Mark the task as completed."""
        self.completed = True

    def create_next_occurrence(self) -> CareTask | None:
        """Create the next dated instance for recurring tasks."""
        frequency_key = self.frequency.lower()
        if frequency_key == "daily":
            next_due_date = self.due_date + timedelta(days=1)
        elif frequency_key == "weekly":
            next_due_date = self.due_date + timedelta(weeks=1)
        else:
            return None

        return CareTask(
            title=self.title,
            category=self.category,
            duration=self.duration,
            time=self.time,
            priority=self.priority,
            frequency=self.frequency,
            due_date=next_due_date,
            required=self.required,
        )

    def update_task(
        self,
        title: str | None = None,
        category: str | None = None,
        duration: int | None = None,
        time: str | None = None,
        priority: str | None = None,
        frequency: str | None = None,
        due_date: date | None = None,
        required: bool | None = None,
        completed: bool | None = None,
    ) -> None:
        """Update one or more task attributes in place."""
        if title is not None:
            self.title = title
        if category is not None:
            self.category = category
        if duration is not None:
            self.duration = duration
        if time is not None:
            self.time = time
        if priority is not None:
            self.priority = priority
        if frequency is not None:
            self.frequency = frequency
        if due_date is not None:
            self.due_date = due_date
        if required is not None:
            self.required = required
        if completed is not None:
            self.completed = completed

    def get_description(self) -> str:
        """Return a readable summary of the task."""
        status = "completed" if self.completed else "pending"
        return (
            f"{self.title} on {self.due_date.isoformat()} at {self.time} "
            f"({self.category}) - {self.duration} min, "
            f"{self.priority} priority, {self.frequency}, {status}"
        )


@dataclass
class Pet:
    name: str
    species: str
    age: int
    special_needs: str = ""
    care_tasks: list[CareTask] = field(default_factory=list)

    def add_task(self, task: CareTask) -> None:
        """Add a care task to this pet."""
        self.care_tasks.append(task)

    def get_profile_summary(self) -> str:
        """Return a short summary of the pet's profile."""
        needs = f" Special needs: {self.special_needs}." if self.special_needs else ""
        return f"{self.name} is a {self.age}-year-old {self.species}.{needs}"

    def get_care_needs(self) -> list[str]:
        """Return the titles of this pet's care tasks."""
        return [task.title for task in self.care_tasks]

    def get_pending_tasks(self) -> list[CareTask]:
        """Return tasks that have not been completed yet."""
        today = date.today()
        return [
            task
            for task in self.care_tasks
            if not task.completed and task.due_date <= today
        ]

    def get_tasks_by_status(self, completed: bool) -> list[CareTask]:
        """Return tasks filtered by completion status."""
        return [task for task in self.care_tasks if task.completed is completed]

    def mark_task_complete(self, task_title: str) -> CareTask | None:
        """Mark a task complete and create the next occurrence if it recurs."""
        for task in self.care_tasks:
            if task.title == task_title and not task.completed:
                task.mark_complete()
                next_task = task.create_next_occurrence()
                if next_task is not None:
                    self.add_task(next_task)
                return next_task
        return None


@dataclass
class Owner:
    name: str
    available_time: int
    preferences: list[str] = field(default_factory=list)
    pets: list[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to this owner's list of pets."""
        self.pets.append(pet)

    def update_preferences(self, preferences: list[str]) -> None:
        """Replace the owner's current preferences."""
        self.preferences = preferences

    def get_available_time(self) -> int:
        """Return how many minutes the owner has available today."""
        return self.available_time

    def get_all_tasks(self) -> list[CareTask]:
        """Collect all pending tasks across the owner's pets."""
        tasks: list[CareTask] = []
        for pet in self.pets:
            tasks.extend(pet.get_pending_tasks())
        return tasks

    def get_all_tasks_including_completed(self) -> list[CareTask]:
        """Collect all tasks across the owner's pets."""
        tasks: list[CareTask] = []
        for pet in self.pets:
            tasks.extend(pet.care_tasks)
        return tasks

    def get_pet_name_for_task(self, target_task: CareTask) -> str | None:
        """Return the pet name that owns a given task."""
        for pet in self.pets:
            for task in pet.care_tasks:
                if task is target_task:
                    return pet.name
        return None


class Scheduler:
    def __init__(self, owner: Owner) -> None:
        """Create a scheduler for a specific owner."""
        self.owner = owner
        self.tasks: list[CareTask] = []

    def refresh_tasks(self) -> list[CareTask]:
        """Refresh the scheduler's task list from the owner's pets."""
        self.tasks = self.owner.get_all_tasks()
        return self.tasks

    def mark_task_complete(self, pet_name: str, task_title: str) -> CareTask | None:
        """Complete a task for a pet and generate its next occurrence if needed."""
        for pet in self.owner.pets:
            if pet.name == pet_name:
                return pet.mark_task_complete(task_title)
        return None

    def rank_tasks(self) -> list[CareTask]:
        """Sort tasks by required status, priority, and duration."""
        tasks = self.refresh_tasks()
        return sorted(
            tasks,
            key=lambda task: (
                not task.required,
                PRIORITY_ORDER.get(task.priority.lower(), 99),
                task.duration,
            ),
        )

    def sort_by_time(self, tasks: list[CareTask] | None = None) -> list[CareTask]:
        """Sort tasks by their HH:MM time value."""
        tasks_to_sort = self.refresh_tasks() if tasks is None else tasks
        return sorted(tasks_to_sort, key=lambda task: task.time)

    def filter_tasks(
        self,
        pet_name: str | None = None,
        completed: bool | None = None,
    ) -> list[CareTask]:
        """Filter tasks by pet name and/or completion status."""
        filtered_tasks: list[CareTask] = []

        for pet in self.owner.pets:
            if pet_name is not None and pet.name != pet_name:
                continue

            pet_tasks = (
                pet.care_tasks
                if completed is None
                else pet.get_tasks_by_status(completed)
            )
            filtered_tasks.extend(pet_tasks)

        return filtered_tasks

    def select_tasks_for_day(self) -> list[CareTask]:
        """Select tasks that fit within the owner's available time."""
        ranked_tasks = self.rank_tasks()
        available_time = self.owner.get_available_time()
        selected_tasks: list[CareTask] = []
        used_time = 0

        for task in ranked_tasks:
            if used_time + task.duration <= available_time:
                selected_tasks.append(task)
                used_time += task.duration

        return selected_tasks

    def generate_daily_plan(self) -> list[CareTask]:
        """Build the final list of tasks for today's schedule."""
        return self.select_tasks_for_day()

    def detect_conflicts(self) -> list[str]:
        """Return warning messages for tasks scheduled at the same date and time."""
        pending_tasks = self.sort_by_time(self.refresh_tasks())
        warnings: list[str] = []

        for index, current_task in enumerate(pending_tasks):
            for next_task in pending_tasks[index + 1 :]:
                if (
                    current_task.due_date == next_task.due_date
                    and current_task.time == next_task.time
                ):
                    current_pet = self.owner.get_pet_name_for_task(current_task) or "Unknown pet"
                    next_pet = self.owner.get_pet_name_for_task(next_task) or "Unknown pet"
                    warnings.append(
                        "Warning: "
                        f"{current_task.title} for {current_pet} conflicts with "
                        f"{next_task.title} for {next_pet} at "
                        f"{current_task.time} on {current_task.due_date.isoformat()}."
                    )

        return warnings

    def explain_plan(self) -> str:
        """Explain why the chosen tasks were included in the plan."""
        plan = self.generate_daily_plan()
        if not plan:
            return "No tasks fit within the available time today."

        total_time = sum(task.duration for task in plan)
        lines = [
            f"Planned {len(plan)} task(s) in {total_time} minutes "
            f"for {self.owner.name}."
        ]

        for task in plan:
            reason = "required" if task.required else f"{task.priority} priority"
            lines.append(f"- {task.title}: selected because it is {reason}.")

        conflicts = self.detect_conflicts()
        if conflicts:
            lines.append("Conflict warnings:")
            lines.extend(conflicts)

        return "\n".join(lines)
