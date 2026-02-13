import csv
from datetime import date, timedelta
from astral import LocationInfo
from astral.sun import sun
from ortools.sat.python import cp_model

class OutdoorScheduler:
    def __init__(self, location_name="Amritsar", country="India",
                 slot_minutes=30, num_days=5):
        self.location = LocationInfo(location_name, country)
        self.slot_minutes = slot_minutes
        self.num_days = num_days
        self.groups = {"1-6": (50, 120), "7-12": (60, 90)}  # min,max outdoor mins
        self.slots_per_day = int(24*60 // slot_minutes)
        self.daylight = {}  # {d: (sunrise_slot, sunset_slot)}
        self.weather = {}   # {d: {slot: 0/1}}

    def compute_daylight(self, start_date):
        for d in range(self.num_days):
            dt = start_date + timedelta(days=d)
            s = sun(self.location.observer, date=dt)
            sunrise, sunset = s["sunrise"], s["sunset"]

            sr_slot = int((sunrise.hour*60 + sunrise.minute)//self.slot_minutes)
            ss_slot = int((sunset.hour*60 + sunset.minute)//self.slot_minutes)
            self.daylight[d] = (sr_slot, ss_slot)

    def load_weather_csv(self, path):
        """
        CSV format:
        day,slot,ok
        0,10,1
        0,11,0
        ...
        """
        self.weather = {d: {} for d in range(self.num_days)}

        with open("weather.csv", newline="") as f:   # same folder, no full path needed
          reader = csv.DictReader(f)
        for row in reader:
         d = int(row["day"])
        t = int(row["slot"])
        ok = int(row["ok"])
        self.weather[d][t] = ok


    def build_and_solve(self, time_limit_seconds=20, csv_out=True, out_path="schedule.csv"):
        model = cp_model.CpModel()
        X = {}  # decision: group g at slot t on day d
        for d in range(self.num_days):
            for g in self.groups:
                for t in range(self.slots_per_day):
                    X[(d,g,t)] = model.NewBoolVar(f"X_{d}_{g}_{t}")

        # Constraints
        for d in range(self.num_days):
            sr, ss = self.daylight[d]
            for g,(min_req,max_req) in self.groups.items():
                # outdoor time in minutes
                total = sum(self.slot_minutes * X[(d,g,t)]
                            for t in range(self.slots_per_day))
                model.Add(total >= min_req)
                model.Add(total <= max_req)

                for t in range(self.slots_per_day):
                    # forbid outside daylight
                    if not (sr <= t <= ss):
                        model.Add(X[(d,g,t)] == 0)
                    # forbid bad weather
                    if self.weather.get(d,{}).get(t,1) == 0:
                        model.Add(X[(d,g,t)] == 0)

        # Objective: spread outdoor time, minimize fragmentation
        obj = sum(X.values())
        model.Maximize(obj)

        solver = cp_model.CpSolver()
        solver.parameters.max_time_in_seconds = time_limit_seconds
        status = solver.Solve(model)

        if status not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
            print("No solution found")
            return None

        # Collect schedule
        schedule = []
        for d in range(self.num_days):
            for g in self.groups:
                for t in range(self.slots_per_day):
                    if solver.Value(X[(d,g,t)]) == 1:
                        schedule.append([d,g,t])

        if csv_out:
            with open(out_path,"w",newline="") as f:
                w = csv.writer(f)
                w.writerow(["day","group","slot"])
                w.writerows(schedule)
        return schedule


if __name__ == "__main__":
    sched = OutdoorScheduler(num_days=3, slot_minutes=30)
    sched.compute_daylight(start_date=date(2025,9,1))
    sched.load_weather_csv("weather.csv")
    sched.build_and_solve(time_limit_seconds=10)
