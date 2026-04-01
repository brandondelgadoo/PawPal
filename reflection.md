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
- Why is that tradeoff reasonable for this scenario?

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
