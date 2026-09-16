# Analysis of Matt Pocock's Teaching Philosophy

Based on Matt Pocock's demonstration and explanation of his "Teach" skill, his teaching philosophy is built around the transition from static, one-off interactions to persistent, adaptive learning environments. This analysis explores the core pillars of his approach.

## 1. Stateless vs. Stateful Skills

Pocock distinguishes between two fundamental types of AI skill architectures:

| Feature | Stateless Skills | Stateful Skills |
| :--- | :--- | :--- |
| **Persistence** | No memory of previous runs or actions. | Retains state and context across multiple sessions. |
| **Storage** | Does not save anything to the file system or databases. | Saves data (ADRs, notes, records) to the local file system or MCP servers. |
| **Continuity** | Starts "fresh" every time; requires the user to re-provide context. | Picks up exactly where the last session left off. |
| **Example** | `grill-me`: Quizzes the user on a topic without building a long-term profile. | `teach`: Tracks a student's journey from novice to mastery over weeks. |

## 2. Why Teaching Must Be Stateful

Pocock argues that effective teaching is inherently a stateful process. A "stateless" teacher would simply provide a list of resources or a one-time explanation, which is insufficient for complex skill acquisition. Teaching must be stateful because:

*   **Memory of Progress:** A teacher must know what the student has already mastered to avoid redundant instruction.
*   **Contextual Pathing:** Learning isn't linear. A stateful teacher knows the "next step" based on previous successes and failures.
*   **Zone of Proximal Development (ZPD):** This is the core of Pocock’s philosophy. ZPD is the area where a student is perfectly challenged—not bored by simplicity, but not overwhelmed by complexity. Maintaining a student in this zone requires constant tracking of their current capabilities.
*   **Dynamic Resource Management:** A stateful agent can curate and recall specific high-trust resources used in previous lessons, building a coherent curriculum over time.

## 3. How a Stateful Agent Tracks Learning Progress

Pocock’s "Teach" skill uses a structured file-system-based approach to track and manage the learning journey:

### The Mission (`mission.md`)
The agent begins by defining the *why*. It records the student's specific goals (e.g., "solve a Rubik's cube unaided," not necessarily for speed). This aligns the agent’s instructional strategy with the student's personal mission.

### Learning Records
When a student completes a lesson or reports progress, the agent creates a **learning record**. These are simple data entries that allow the agent to diagnose the student's current state (e.g., "Concept solid, but lacking muscle memory for the corner cycle").

### The Glossary and Reference Material
As new jargon or concepts are introduced, they are added to a **glossary** or **cheat sheets**. This allows future lessons to be more concise, as the agent can refer back to established terms rather than re-explaining them.

### Internal Notes (`notes.md`)
The agent maintains a private scratchpad to record student preferences, "watch outs," and instructional strategies. This mimics the internal "teacher’s notes" used to tailor future sessions.

### Interactive Lessons (HTML)
By using HTML instead of Markdown for lessons, the agent creates a rich feedback loop. HTML allows for:
*   **Interactivity:** Guided modes and interactive diagrams (e.g., a virtual Rubik's cube).
*   **Visual Clarity:** Better call-outs, quizzes, and structured explainers.
*   **Persistence:** Each numbered lesson (e.g., `001-notation.html`) remains on disk as a permanent record of the curriculum.

## Conclusion
Pocock’s philosophy shifts the role of AI from a "search engine with a chat interface" to a "long-term mentor." By utilizing a stateful architecture, the agent can respect the student's Zone of Proximal Development, ensuring that every session is a meaningful step toward the defined mission.
