from datetime import date, time

import streamlit as st

from pawpal_system import Owner, Pet, Scheduler, Task

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

st.subheader("Quick Demo Inputs")

# The Owner lives in the session "vault" so it (and its pets/tasks)
# survives Streamlit's reruns. Create it once, then reuse it.
if "owner" not in st.session_state:
    st.session_state.owner = Owner(name="Jordan")
owner = st.session_state.owner

owner_name = st.text_input("Owner name", value=owner.name)
owner.name = owner_name  # keep the persisted owner in sync with the input

st.markdown("### Add a Pet")
col_a, col_b, col_c = st.columns(3)
with col_a:
    pet_name = st.text_input("Pet name", value="Mochi")
with col_b:
    species = st.selectbox("Species", ["dog", "cat", "other"])
with col_c:
    age = st.number_input("Age", min_value=0, max_value=50, value=2)

if st.button("Add pet"):
    if owner.get_pet(pet_name) is None:
        owner.add_pet(Pet(name=pet_name, species=species, age=int(age)))
        st.success(f"Added {pet_name} to {owner.name}'s pets.")
    else:
        st.info(f"{pet_name} is already in the list.")

st.markdown("### Schedule a Task")
st.caption("Tasks are attached to a pet and fed into the scheduler.")

pets = owner.get_all_pets()
if not pets:
    st.info("Add a pet first, then you can schedule tasks for it.")
else:
    target_name = st.selectbox("For which pet?", [p.name for p in pets])
    col1, col2, col3 = st.columns(3)
    with col1:
        task_title = st.text_input("Task title", value="Morning walk")
    with col2:
        task_time = st.time_input("Time", value=time(7, 30))
    with col3:
        frequency = st.selectbox("Frequency", ["daily", "weekly", "monthly", "once"])

    if st.button("Add task"):
        pet = owner.get_pet(target_name)
        pet.add_task(Task(task_title, task_time, date.today(), frequency))
        st.success(f"Added '{task_title}' for {pet.name}.")

# Show every pet's current tasks straight from the model.
if pets:
    st.write("Current pets and tasks:")
    for pet in pets:
        st.markdown(f"**{pet.get_info()}**")
        if pet.get_tasks():
            for t in pet.get_tasks():
                status = "done" if t.is_complete else "pending"
                st.write(f"- {t.time:%I:%M %p} — {t.description} ({t.frequency}, {status})")
        else:
            st.caption("No tasks yet.")

st.divider()

st.subheader("Build Schedule")
st.caption("Calls Scheduler.generate_daily_plan() for today.")

if st.button("Generate schedule"):
    scheduler = Scheduler(owner)
    today = date.today()
    plan = scheduler.generate_daily_plan(today)

    st.markdown(f"#### Today's Schedule — {today:%A, %B %d, %Y}")
    if not plan:
        st.info("Nothing scheduled today. Add some tasks above.")
    else:
        for t in plan:
            st.write(f"{t.time:%I:%M %p} — {t.description}")

    conflicts = scheduler.detect_conflicts(plan)
    if conflicts:
        st.warning(
            "Time conflicts detected: "
            + ", ".join(f"{t.description} @ {t.time:%I:%M %p}" for t in conflicts)
        )
