# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.

    My initial UML design used four classes to represent the main parts of the PawPal+ pet care app: `Owner`, `Pet`, `CareTask`, and `Scheduler`. I chose these classes because they map directly to the problem the app is solving. The `Owner` class represents the person using the app and stores their available time and preferences. The `Pet` class represents the animal receiving care and stores profile information like species, age, and special needs. The `CareTask` class represents each activity that might need to be scheduled, such as a walk, feeding, medication, or grooming, along with details like duration, priority, and frequency. The `Scheduler` class is responsible for the planning logic, using the owner, pets, and tasks to decide what should go into the daily plan.

- What classes did you include, and what responsibilities did you assign to each?

    I am designing a pet care app with four core classes: `Owner`, `Pet`, `CareTask`, and `Scheduler`.

    `Owner` holds attributes like name, available time, and care preferences. Its methods might include updating preferences or providing the total time available for planning.

    `Pet` holds attributes like name, species, age, and any special needs or notes. Its methods might include returning a summary of the pet's profile or listing care needs that affect scheduling.

    `CareTask` holds attributes like title, category, duration, priority, frequency, and whether the task is required. Its methods might include checking whether the task fits in the available time, updating task details, or returning a readable description for the schedule.

    `Scheduler` holds the scheduling rules or references to the owner, pet, and available tasks. Its methods might include ranking tasks, filtering tasks based on constraints, generating the day's plan, and explaining the reasoning behind the final schedule.

    I reviewed the diagram to keep the relationships simple and logical. For example, an `Owner` can have one or more `Pet` objects, each `Pet` can have multiple `CareTask` objects, and the `Scheduler` uses that information to build the day's plan. I left out extra classes for now so the design stays focused on the core scheduling system and does not become more complex than the project needs.

**b. Design changes**

- Did your design change during implementation?

    Not significantly. My initial design stayed mostly the same as I moved from the UML diagram to the Python class skeleton.

- If yes, describe at least one change and why you made it.

    I did not make any major design changes during implementation. The main adjustment was making the class relationships more explicit in code so the skeleton matched the UML more clearly.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.

    One tradeoff my scheduler makes is that its conflict detection only checks for exact matching dates and times instead of calculating whether two task durations overlap. For example, it will warn me if two tasks are both scheduled at 8:30 AM, but it will not yet detect that a task from 8:00 to 8:30 could overlap with a task starting at 8:15.

- Why is that tradeoff reasonable for this scenario?

    That tradeoff is reasonable for this version of the project because it keeps the logic lightweight and easy to understand while still catching the most obvious scheduling mistakes. Since this is an early pet care planner and not a full calendar system, exact-time conflict warnings provide useful feedback without adding too much complexity to the code.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?

    I used VS Code Copilot throughout the project for design brainstorming, creating class skeletons, refining methods, and checking how to connect my backend logic to the Streamlit UI. Copilot was especially helpful when I was turning the UML into dataclasses and when I was adding new scheduler behaviors like sorting, filtering, recurrence, and conflict detection. I also used it to help think through how session state should work in Streamlit and how to organize my tests.

- What kinds of prompts or questions were most helpful?

    The most helpful prompts were specific and tied to the codebase. For example, prompts like "Based on my skeletons in #file:pawpal_system.py, how should the Scheduler retrieve all tasks from the Owner's pets?" or "What are the most important edge cases to test for a pet scheduler with sorting and recurring tasks?" gave better results than general prompts. Asking focused questions about one feature at a time made the AI much more useful.

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.

    One moment where I did not accept an AI suggestion as-is was when the design risked becoming more complicated than the project needed. I chose to keep the system centered on four main classes instead of adding extra objects just because they were technically possible. I also kept conflict detection lightweight by only checking exact matching times instead of building a more advanced overlap engine.

- How did you evaluate or verify what the AI suggested?

    I evaluated AI suggestions by comparing them to the project requirements, checking whether they still matched my UML design, and testing whether the code stayed readable. If a suggestion felt more "Pythonic" but made the system harder to understand, I preferred the simpler version. I also verified suggestions by running the demo script, checking Streamlit behavior, and running pytest tests after important changes.

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?

    I tested several core behaviors in the backend logic. My tests verify that marking a task complete changes its status, adding a task to a pet increases that pet's task count, sorting returns tasks in chronological order, completing a daily task creates a new task for the following day, and conflict detection returns a warning when two tasks are scheduled for the same time.

- Why were these tests important?

    These tests were important because they covered the scheduler features that most directly affect whether the app is useful and trustworthy. If task completion, recurrence, sorting, or conflict warnings fail, the daily plan could become confusing or inaccurate for the pet owner.

**b. Confidence**

- How confident are you that your scheduler works correctly?

    I am fairly confident that my scheduler works correctly for the main scenarios I implemented. The core features all passed automated tests, and I also checked the behavior through the demo script and Streamlit interface. I would rate my confidence as 4 out of 5 because the main workflow is working, but there are still some simplifications in the logic.

- What edge cases would you test next if you had more time?

    If I had more time, I would test edge cases such as an owner with no pets, a pet with no tasks, non-recurring tasks that should not generate a follow-up task, multiple overlapping tasks with different durations, and invalid time input formats. I would also test more cases where future recurring tasks should be hidden from today's plan until their due date arrives.

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

    I am most satisfied with how the system stayed organized as it grew. Starting with the UML and then building a matching logic layer made it much easier to add features like sorting, filtering, recurring tasks, and conflict detection without losing track of the overall design.

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

    If I had another iteration, I would improve the scheduler so it could detect overlapping task durations instead of only exact matching times. I would also improve persistence so the app could save data across full browser refreshes or app restarts instead of only storing it in Streamlit session state.

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?

    One important thing I learned is that using AI effectively still requires me to act as the lead architect. Copilot was very helpful for generating code, suggesting tests, and explaining patterns, but I had to decide what belonged in the design, what was too complex, and which suggestions actually fit the project goals. Using separate chat sessions for different phases also helped me stay organized because each session had a clearer purpose, such as design, implementation, testing, or reflection, instead of mixing everything together.
