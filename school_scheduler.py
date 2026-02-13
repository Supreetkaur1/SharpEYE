
# school_scheduler.py
from datetime import date
import calendar
from astral import LocationInfo
from astral.sun import sun
import pytz
import random
from typing import Dict, List

class SchoolScheduler:
    def __init__(self, city: str, country: str, timezone: str, month: int,
                 grades: list, classes_per_day: int, sections: dict,
                 class_length: int, max_outdoor_together: int):
        self.city = city
        self.country = country
        self.timezone = timezone
        self.month = month
        self.grades = grades
        self.classes_per_day = classes_per_day
        self.sections = sections  # keys should be ints matching grade numbers
        self.class_length = class_length
        self.max_outdoor_together = max_outdoor_together

        self.daylight_hours = self.get_average_daylight_hours()

    def get_average_daylight_hours(self, year: int = 2025) -> float:
        """Calculate average daylight hours for given month."""
        loc = LocationInfo(self.city, self.country, self.timezone)
        days_in_month = calendar.monthrange(year, self.month)[1]
        daylight_hours = []
        tz = pytz.timezone(self.timezone)

        for day in range(1, days_in_month + 1):
            current_date = date(year, self.month, day)
            s = sun(loc.observer, date=current_date, tzinfo=tz)
            sunrise, sunset = s["sunrise"], s["sunset"]
            duration = sunset - sunrise  # FIX: removed erroneous +18 hours
            daylight_hours.append(duration.total_seconds() / 3600)

        return sum(daylight_hours) / len(daylight_hours) if daylight_hours else 0.0

    def generate_schedule(self, num_days: int) -> Dict[str, Dict[str, Dict[str, List[str]]]]:
        """Generate the timetable without printing; returns a nested dict."""
        schedule = {}

        for day in range(1, num_days + 1):
            schedule[f"Day {day}"] = {}
            for grade in self.grades:
                num_sections = int(self.sections.get(grade, 1))

                # Compute outdoor slot bounds in class *slots*
                if 1 <= int(grade) <= 6:
                    min_slots = max(1, 60 // self.class_length)
                    max_slots = max(min_slots, 120 // self.class_length)
                else:
                    min_slots = max(1, 40 // self.class_length)
                    max_slots = max(min_slots, 90 // self.class_length)

                outdoor_slots = random.randint(min_slots, max_slots)
                outdoor_slots = min(outdoor_slots, self.classes_per_day)  # clamp

                schedule[f"Day {day}"][f"Grade {grade}"] = {}

                for section in range(1, num_sections + 1):
                    # Choose candidate outdoor slots
                    chosen_slots = sorted(random.sample(range(1, self.classes_per_day + 1), outdoor_slots))

                    # Enforce max consecutive outdoor rule
                    final_slots = []
                    count = 0
                    for slot in chosen_slots:
                        if final_slots and slot == final_slots[-1] + 1:
                            count += 1
                            if count >= self.max_outdoor_together:
                                continue
                        else:
                            count = 1
                        final_slots.append(slot)

                    entries = ["Outdoor" if i in final_slots else "Indoor"
                               for i in range(1, self.classes_per_day + 1)]
                    schedule[f"Day {day}"][f"Grade {grade}"][f"Section {section}"] = entries

        return schedule
