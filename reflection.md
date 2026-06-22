# PawPal+ Project Reflection

## 1. System Design
User should be able to add pets, schedule tasks for pets, see all tasks for each pet that day.

**a. Initial design**

My design has four classes. The Owner holds the user's pets and their preferences, and is in charge of adding or removing pets and pulling together tasks from all of them. Each Pet stores its own basic info like name, species, and age, along with the list of care tasks that belong to it. A Task represents one care activity such as feeding or walking, and it keeps track of its description, time, date, how often it repeats, and whether it's done yet. The Scheduler is the piece that actually builds the daily plan. It gathers the tasks from all the pets, sorts and filters them, checks for simple conflicts, and lays everything out into a schedule the owner can follow.

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

My scheduler detects conflicts only by **exact start-time matches**, not by
overlapping durations. `detect_conflicts`/`conflict_warnings` bucket tasks by
their `time` value and warn when two or more land in the same slot. This means
a 7:30 AM walk that realistically takes 45 minutes and an 8:00 AM feeding are
*not* flagged, even though one human can't do both — because their start times
differ. To catch that, a `Task` would need a `duration` and the check would
compare `[start, start + duration)` ranges for overlap.

This tradeoff is reasonable for the current scenario because tasks don't yet
store a duration, exact-match detection is simple and fast (one pass, O(n)),
and it already catches the most common and most obvious mistake — booking two
care tasks at the literally identical time. It keeps the warning logic easy to
read and verify now, while leaving a clear path to upgrade to duration-aware
overlap detection later.

A second, related tradeoff: conflicts are reported as **non-blocking warnings**
rather than errors. The schedule still prints in full; the owner is simply told
which slots clash and decides what to do. This favors the owner's judgment over
having the program refuse to build a plan.

---

## 3. AI Collaboration

**a. How you used AI**

I used AI in a few different ways. Early on it helped me brainstorm the class layout and turn my UML into Python stubs. Later I leaned on it more for the routine work, like drafting the test suite, cleaning up the Streamlit display so it used my Scheduler methods, and writing the README walkthrough. The prompts that worked best were the specific ones where I pointed it at an actual file and asked a narrow question, like "what edge cases should I test for a scheduler with sorting and recurring tasks." Vague questions gave me vague answers.

**b. Judgment and verification**

One thing I didn't take as-is was around conflict detection. The suggestion treated it as fully handled, but I noticed it only catches tasks at the exact same start time, not ones that overlap because of how long they take. I kept the simple version for now but wrote down the limitation instead of pretending it was solved. I verified suggestions mostly by running main.py and watching the output, and by running the test suite. If the tests passed and the printed schedule matched what I expected, I trusted it. A couple of times the output didn't line up and I had to go back and fix things.

---

## 4. Testing and Verification

**a. What you tested**

I focused on the behaviors that make the scheduler actually a scheduler: sorting tasks into chronological order, the recurrence logic that spawns the next instance when you complete a daily or weekly task, and conflict detection flagging two tasks at the same time. I also tested the due-date filtering for each frequency and a couple of edge cases, like a pet with no tasks and two tasks at the exact same time. These mattered because they're the parts most likely to break quietly and the parts the whole daily plan depends on.

**b. Confidence**

Pretty confident. There are 18 tests and they all pass, and the ones that matter most cover the core logic rather than trivial getters. If I had more time I'd test duration-based overlaps once tasks have a length, monthly tasks on a day like the 31st that not every month has, and behavior around the build_schedule method, which currently drops one task when two share a time slot.

---

## 5. Reflection

**a. What went well**

I'm most satisfied with how cleanly the responsibilities split across the classes. The Owner holds pets, the Pet holds its tasks, the Task knows its own recurrence rules, and the Scheduler just reads from the owner and arranges things. Because of that, adding features like filtering by pet or status was easy and didn't tangle anything up.

**b. What you would improve**

The big one is giving tasks a duration so the scheduler can detect real overlaps instead of only exact start-time clashes. I'd also fix build_schedule so it doesn't silently drop a task when two share a time, and probably add task priority so the plan can reflect what matters most when the day is full.

**c. Key takeaway**

Designing the classes first, before writing logic, made the whole build smoother because I already knew where each piece lived. And working with AI, the lesson was that it's only as good as how specific I am and how carefully I check the output, treating it as a fast first draft rather than a final answer.
