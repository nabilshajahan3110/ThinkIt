class UserProgress:
    def __init__(self):
        self.entries = []

    def add_entry(self, entry: dict):
        self.entries.append(entry)

    def get_summary(self):
        total = len(self.entries)
        correct = sum(1 for e in self.entries if e["correct"])
        return {"total": total, "correct": correct}