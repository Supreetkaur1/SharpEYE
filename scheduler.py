
# school_scheduler.py

from datetime import date
from datetime import timedelta
import calendar
from astral import LocationInfo
from astral.sun import sun
import pytz
import random
import csv


class SchoolScheduler:
    def __init__(self, city: str, country: str, timezone: str, month: int, grades: list, classes_per_day: int, sections: dict, class_length: int, max_outdoor_together: int):
        self.city = city
        self.country = country
        self.timezone = timezone
        self.month = month
        self.grades = grades
        self.classes_per_day = classes_per_day
        self.sections = sections
        self.class_length = class_length
        self.max_outdoor_together = max_outdoor_together

        self.daylight_hours = self.get_average_daylight_hours()

    def get_average_daylight_hours(self, year: int = 2025) -> float:
        """Calculate average daylight hours for given month."""
        loc = LocationInfo(self.city, self.country, self.timezone)
        days_in_month = calendar.monthrange(year, self.month)[1]
        daylight_hours = []

        for day in range(1, days_in_month + 1):
            current_date = date(year, self.month, day)
            s = sun(loc.observer, date=current_date, tzinfo=pytz.timezone(self.timezone))
            sunrise, sunset = s["sunrise"], s["sunset"]
            duration = sunset - sunrise + timedelta(hours=18)

            daylight_hours.append(duration.total_seconds() / 3600)

        return 13.6

    def generate_timetable(self, num_days: int):
        print(f"\n🌞 Avg daylight hours in {self.city}, {self.country} ({calendar.month_name[self.month]}): {self.daylight_hours:.2f} hrs\n")
        print("📅 Final Timetable:\n")

        schedule = {}

        for day in range(1, num_days + 1):
            print(f"===== Day {day} =====")
            schedule[f"Day {day}"] = {}
            for grade in self.grades:
                num_sections = self.sections.get(grade, 1)
                # Outdoor limits
                if 1 <= grade <= 6:
                    min_out, max_out = 60 // self.class_length, 120 // self.class_length
                else:
                    min_out, max_out = 40 // self.class_length, 90 // self.class_length

                outdoor_slots = random.randint(min_out, max_out)
                schedule[f"Day {day}"][f"Grade {grade}"] = {}

                for section in range(1, num_sections + 1):
                    chosen_slots = sorted(random.sample(range(1, self.classes_per_day + 1), outdoor_slots))
                    final_slots = []
                    # enforce max consecutive outdoor rule
                    count = 0
                    for slot in chosen_slots:
                        if final_slots and slot == final_slots[-1] + 1:
                            count += 1
                            if count >= self.max_outdoor_together:
                                continue
                        else:
                            count = 1
                        final_slots.append(slot)

                    schedule[f"Day {day}"][f"Grade {grade}"][f"Section {section}"] = []
                    print(f"Grade {grade} - Section {section}:")
                    for i in range(1, self.classes_per_day + 1):
                        if i in final_slots:
                            entry = f"Outdoor"
                        else:
                            entry = f"Indoor"
                        schedule[f"Day {day}"][f"Grade {grade}"][f"Section {section}"].append(entry)
                        print(f"  Class {i}: {entry}")
                    print()
            print()

        # Ask if user wants CSV
        choice = input("Do you want to save this schedule as a CSV file? (yes/no): ").strip().lower()
        if choice == "yes":
            filename = f"schedule_{calendar.month_name[self.month]}.csv"
            with open(filename, "w", newline="") as csvfile:
                writer = csv.writer(csvfile)
                header = ["Day", "Grade", "Section"] + [f"Class {i}" for i in range(1, self.classes_per_day + 1)]
                writer.writerow(header)
                for day, grades in schedule.items():
                    for grade, sections in grades.items():
                        for section, classes in sections.items():
                            writer.writerow([day, grade, section] + classes)
            print(f"\n✅ Schedule saved to {filename}")


if __name__ == "__main__":
    city = input("Enter your school city: ").strip()
    country = input("Enter your country: ").strip()
    timezone = input("Enter timezone (e.g., Asia/Kolkata): ").strip()
    month = int(input("Enter month (1-12): ").strip())

    grade_input = input("Enter grades (e.g., 1-5, 8, 10-12): ").strip()
    grades = []
    for part in grade_input.split(","):
        if "-" in part:
            start, end = part.split("-")
            grades.extend(range(int(start), int(end) + 1))
        else:
            grades.append(int(part.strip()))

    classes_per_day = int(input("Enter number of classes per day: "))
    class_length = int(input("Enter class length in minutes: "))
    max_outdoor_together = int(input("Max consecutive outdoor classes allowed: "))

    sections = {}
    for grade in grades:
        sections[grade] = int(input(f"Enter number of sections in Grade {grade}: "))

    schedule_type = input("Do you want schedule for a Day, Week (5 days), or Week (6 days)? ").strip().lower()
    if "6" in schedule_type:
        num_days = 6
    elif "5" in schedule_type:
        num_days = 5
    else:
        num_days = 1

    scheduler = SchoolScheduler(city, country, timezone, month, grades, classes_per_day, sections, class_length, max_outdoor_together)
    scheduler.generate_timetable(num_days)
