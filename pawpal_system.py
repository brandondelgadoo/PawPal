from __future__ import annotations

from dataclasses import dataclass, field


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
    priority: str
    frequency: str
    required: bool = False
    completed: bool = False

    def fits_in_time(self, available_time: int) -> bool:
        """Return whether the task can fit within the available time."""
        return self.duration <= available_time

    def mark_complete(self) -> None:
        """Mark the task as completed."""
        self.completed = True

    def update_task(
        self,
        title: str | None = None,
        category: str | None = None,
        duration: int | None = None,
        priority: str | None = None,
        frequency: str | None = None,
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
        if priority is not None:
            self.priority = priority
        if frequency is not None:
            self.frequency = frequency
        if required is not None:
            self.required = required
        if completed is not None:
            self.completed = completed

    def get_description(self) -> str:
        """Return a readable summary of the task."""
        status = "completed" if self.completed else "pending"
        return (
            f"{self.title} ({self.category}) - {self.duration} min, "
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
        return [task for task in self.care_tasks if not task.completed]


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


class Scheduler:
    def __init__(self, owner: Owner) -> None:
        """Create a scheduler for a specific owner."""
        self.owner = owner
        self.tasks: list[CareTask] = []

    def refresh_tasks(self) -> list[CareTask]:
        """Refresh the scheduler's task list from the owner's pets."""
        self.tasks = self.owner.get_all_tasks()
        return self.tasks

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

    def filter_tasks(self) -> list[CareTask]:
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
        return self.filter_tasks()

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

        return "\n".join(lines)
