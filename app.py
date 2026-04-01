import streamlit as st

from pawpal_system import CareTask, Owner, Pet, Scheduler


def initialize_session_state() -> None:
    """Create persistent session objects the first time the app runs."""
    if "owner" not in st.session_state:
        st.session_state.owner = Owner(name="Jordan", available_time=60, preferences=[])
    if "generated_plan" not in st.session_state:
        st.session_state.generated_plan = []
    if "plan_explanation" not in st.session_state:
        st.session_state.plan_explanation = ""
    if "owner_name_input" not in st.session_state:
        st.session_state.owner_name_input = st.session_state.owner.name
    if "available_time_input" not in st.session_state:
        st.session_state.available_time_input = st.session_state.owner.available_time
    if "pet_name_input" not in st.session_state:
        st.session_state.pet_name_input = "Mochi"
    if "pet_age_input" not in st.session_state:
        st.session_state.pet_age_input = 4
    if "pet_species_input" not in st.session_state:
        st.session_state.pet_species_input = "dog"
    if "special_needs_input" not in st.session_state:
        st.session_state.special_needs_input = ""
    if "task_title_input" not in st.session_state:
        st.session_state.task_title_input = "Morning walk"
    if "task_category_input" not in st.session_state:
        st.session_state.task_category_input = "exercise"
    if "task_duration_input" not in st.session_state:
        st.session_state.task_duration_input = 20
    if "task_time_input" not in st.session_state:
        st.session_state.task_time_input = "08:00"
    if "task_priority_input" not in st.session_state:
        st.session_state.task_priority_input = "high"
    if "task_frequency_input" not in st.session_state:
        st.session_state.task_frequency_input = "daily"
    if "task_required_input" not in st.session_state:
        st.session_state.task_required_input = False


initialize_session_state()
owner = st.session_state.owner
scheduler = Scheduler(owner)

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

st.subheader("Owner")
owner_name = st.text_input("Owner name", key="owner_name_input")
available_time = st.number_input(
    "Available time today (minutes)",
    min_value=1,
    max_value=240,
    key="available_time_input",
)

owner.name = owner_name
owner.available_time = int(available_time)

st.subheader("Add a Pet")
pet_name = st.text_input("Pet name", key="pet_name_input")
species = st.selectbox("Species", ["dog", "cat", "other"], key="pet_species_input")
pet_age = st.number_input("Pet age", min_value=0, max_value=30, key="pet_age_input")
special_needs = st.text_input("Special needs", key="special_needs_input")

if st.button("Add pet"):
    if pet_name.strip():
        owner.add_pet(
            Pet(
                name=pet_name.strip(),
                species=species,
                age=int(pet_age),
                special_needs=special_needs.strip(),
            )
        )
        st.success(f"Added pet: {pet_name.strip()}")
    else:
        st.error("Please enter a pet name before adding a pet.")

if owner.pets:
    st.write("Current pets:")
    st.table(
        [
            {
                "name": pet.name,
                "species": pet.species,
                "age": pet.age,
                "special_needs": pet.special_needs,
            }
            for pet in owner.pets
        ]
    )
else:
    st.info("No pets added yet.")

st.divider()

st.subheader("Add a Task")
st.caption("Tasks are stored on each pet and persist while this session is open.")

pet_options = [pet.name for pet in owner.pets]

if pet_options:
    selected_pet_name = st.selectbox("Choose a pet", pet_options)
    task_title = st.text_input("Task title", key="task_title_input")
    task_category = st.text_input("Category", key="task_category_input")
    duration = st.number_input(
        "Duration (minutes)",
        min_value=1,
        max_value=240,
        key="task_duration_input",
    )
    task_time = st.text_input("Time (HH:MM)", key="task_time_input")
    priority = st.selectbox(
        "Priority",
        ["low", "medium", "high"],
        key="task_priority_input",
    )
    frequency = st.text_input("Frequency", key="task_frequency_input")
    required = st.checkbox("Required task", key="task_required_input")

    if st.button("Add task"):
        selected_pet = next(pet for pet in owner.pets if pet.name == selected_pet_name)
        selected_pet.add_task(
            CareTask(
                title=task_title.strip(),
                category=task_category.strip(),
                duration=int(duration),
                time=task_time.strip(),
                priority=priority,
                frequency=frequency.strip(),
                required=required,
            )
        )
        st.success(f"Added task to {selected_pet_name}: {task_title.strip()}")
else:
    st.info("Add a pet before adding tasks.")

all_tasks = [
    {
        "pet": owner.get_pet_name_for_task(task),
        "title": task.title,
        "category": task.category,
        "duration": task.duration,
        "time": task.time,
        "due_date": task.due_date.isoformat(),
        "priority": task.priority,
        "frequency": task.frequency,
        "required": task.required,
        "completed": task.completed,
    }
    for task in scheduler.sort_by_time(owner.get_all_tasks_including_completed())
]

if all_tasks:
    st.write("All tasks, sorted by time:")
    st.table(all_tasks)

    st.markdown("### Filtered task view")
    filter_pet_options = ["All pets"] + pet_options
    selected_filter_pet = st.selectbox("Filter by pet", filter_pet_options)
    status_filter = st.selectbox("Filter by status", ["All", "Pending", "Completed"])

    filtered_tasks = scheduler.filter_tasks(
        pet_name=None if selected_filter_pet == "All pets" else selected_filter_pet,
        completed=(
            None
            if status_filter == "All"
            else status_filter == "Completed"
        ),
    )

    filtered_task_rows = [
        {
            "pet": owner.get_pet_name_for_task(task),
            "title": task.title,
            "time": task.time,
            "due_date": task.due_date.isoformat(),
            "priority": task.priority,
            "completed": task.completed,
        }
        for task in scheduler.sort_by_time(filtered_tasks)
    ]

    if filtered_task_rows:
        st.table(filtered_task_rows)
    else:
        st.info("No tasks match the current filters.")

    conflict_warnings = scheduler.detect_conflicts()
    if conflict_warnings:
        st.markdown("### Schedule warnings")
        for warning in conflict_warnings:
            st.warning(warning)
    else:
        st.success("No task conflicts detected for today's pending tasks.")

st.divider()

st.subheader("Build Schedule")
st.caption("This uses the objects stored in session state instead of resetting on every rerun.")

if st.button("Generate schedule"):
    st.session_state.generated_plan = scheduler.generate_daily_plan()
    st.session_state.plan_explanation = scheduler.explain_plan()

if st.session_state.generated_plan:
    st.write("Today's schedule:")
    st.table(
        [
            {
                "title": task.title,
                "category": task.category,
                "duration": task.duration,
                "time": task.time,
                "due_date": task.due_date.isoformat(),
                "priority": task.priority,
                "frequency": task.frequency,
                "required": task.required,
            }
            for task in st.session_state.generated_plan
        ]
    )
    st.markdown("### Why this plan was chosen")
    st.text(st.session_state.plan_explanation)
