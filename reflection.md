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
