class StatsTracker:
    def __init__(self):
        self.records = []

    def log(self, patient, stage, duration):
        self.records.append({
            "patient": patient,
            "stage": stage,
            "duration": duration
        })

    def average_time(self):
        if not self.records:
            return 0
        return sum(r["duration"] for r in self.records) / len(self.records)

