from dataclasses import dataclass, field


@dataclass
class Owner:
    name: str
    available_time: int
    preferences: list[str] = field(default_factory=list)
    pets: list["Pet"] = field(default_factory=list)

    def update_preferences(self, preferences: list[str]) -> None:
        raise NotImplementedError

    def get_available_time(self) -> int:
        raise NotImplementedError


@dataclass
class Pet:
    name: str
    species: str
    age: int
    special_needs: str = ""
    care_tasks: list["CareTask"] = field(default_factory=list)

    def get_profile_summary(self) -> str:
        raise NotImplementedError

    def get_care_needs(self) -> list[str]:
        raise NotImplementedError


@dataclass
class CareTask:
    title: str
    category: str
    duration: int
    priority: str
    frequency: str
    required: bool = False

    def fits_in_time(self, available_time: int) -> bool:
        raise NotImplementedError

    def update_task(
        self,
        title: str | None = None,
        category: str | None = None,
        duration: int | None = None,
        priority: str | None = None,
        frequency: str | None = None,
        required: bool | None = None,
    ) -> None:
        raise NotImplementedError

    def get_description(self) -> str:
        raise NotImplementedError


class Scheduler:
    def __init__(self, owner: Owner, pets: list[Pet], tasks: list[CareTask]) -> None:
        self.owner = owner
        self.pets = pets
        self.tasks = tasks

    def rank_tasks(self) -> list[CareTask]:
        raise NotImplementedError

    def filter_tasks(self) -> list[CareTask]:
        raise NotImplementedError

    def generate_daily_plan(self) -> list[CareTask]:
        raise NotImplementedError

    def explain_plan(self) -> str:
        raise NotImplementedError
