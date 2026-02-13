
# app.py
import streamlit as st
import pandas as pd
import calendar
import random
from school_scheduler import SchoolScheduler

st.set_page_config(page_title="NoGlasses Scheduler", layout="wide")

def parse_grades(input_str: str):
    grades = []
    for part in input_str.split(","):
        part = part.strip()
        if not part:
            continue
        if "-" in part:
            start, end = part.split("-")
            grades.extend(range(int(start), int(end) + 1))
        else:
            grades.append(int(part))
    # de-dup and sort
    return sorted(set(grades))

def schedule_to_df(schedule: dict, classes_per_day: int) -> pd.DataFrame:
    rows = []
    for day, grades in schedule.items():
        for grade, sections in grades.items():
            for section, classes in sections.items():
                row = {"Day": day, "Grade": grade, "Section": section}
                for idx, val in enumerate(classes, 1):
                    row[f"Class {idx}"] = val
                rows.append(row)
    return pd.DataFrame(rows)

st.title("📚 NoGlasses Class Scheduler")
st.markdown("Generate automated indoor/outdoor timetables for schools.")

with st.form("inputs"):
    col1, col2, col3 = st.columns(3)
    with col1:
        city = st.text_input("City", value="Amritsar")
        classes_per_day = st.number_input("Classes per day", min_value=1, max_value=12, value=6)
        class_length = st.number_input("Class length (minutes)", min_value=10, max_value=120, value=40)
    with col2:
        country = st.text_input("Country", value="India")
        max_outdoor_together = st.number_input("Max consecutive outdoor classes", min_value=1, max_value=6, value=2)
        seed = st.text_input("Random seed (optional)", value="")
    with col3:
        timezone = st.text_input("Timezone", value="Asia/Kolkata")
        month = st.selectbox("Month", options=list(range(1, 13)), format_func=lambda m: calendar.month_name[m])
        schedule_type = st.radio("Schedule for", ["Day", "Week (5 days)", "Week (6 days)"])

    grades_input = st.text_input("Grades (e.g., 1-5, 8, 10-12)", value="1-5")
    grades = parse_grades(grades_input)

    st.markdown("### Sections per Grade")
    sec_cols = st.columns(min(4, len(grades)) if grades else 1)
    sections = {}
    for i, grade in enumerate(grades):
        with sec_cols[i % max(1, len(sec_cols))]:
            sections[grade] = st.number_input(f"Grade {grade}", min_value=1, max_value=10, value=2, key=f"sec_{grade}")

    submitted = st.form_submit_button("Generate Timetable 🚀")

if submitted:
    if seed.strip():
        try:
            random.seed(int(seed.strip()))
        except ValueError:
            random.seed(seed.strip())

    num_days = 1 if schedule_type.startswith("Day") else (5 if "5" in schedule_type else 6)

    scheduler = SchoolScheduler(
        city=city,
        country=country,
        timezone=timezone,
        month=int(month),
        grades=grades,
        classes_per_day=int(classes_per_day),
        sections=sections,
        class_length=int(class_length),
        max_outdoor_together=int(max_outdoor_together),
    )

    schedule = scheduler.generate_schedule(num_days=num_days)
    avg_daylight = scheduler.daylight_hours

    st.success("Timetable generated!")
    st.metric("Average daylight (hrs)", f"{avg_daylight:.2f}")

    df = schedule_to_df(schedule, classes_per_day=int(classes_per_day))
    st.dataframe(df, use_container_width=True)

    csv_bytes = df.to_csv(index=False).encode("utf-8")
    st.download_button("📥 Download CSV", data=csv_bytes, file_name=f"schedule_{calendar.month_name[int(month)]}.csv", mime="text/csv")

    # Optional: Show nested view
    with st.expander("View nested schedule JSON"):
        st.json(schedule)
