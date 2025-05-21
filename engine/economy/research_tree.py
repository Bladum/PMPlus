import random

class TResearchTree:
    """
    Represents a research tree, it is a list of research entries
    """

    def __init__(self):
        self.entries = {}  # tech_id -> TResearchEntry
        self.completed = set()
        self.in_progress = {}  # tech_id -> progress (int)
        self.available = set()
        self.locked = set()  # tech_id set for permanently locked research

    def add_entry(self, entry):
        # Randomize cost 50-150% of base cost when adding to tree
        if not hasattr(entry, '_cost_randomized'):
            base_cost = entry.cost
            entry.cost = int(base_cost * random.uniform(0.5, 1.5))
            entry._cost_randomized = True
        self.entries[entry.id] = entry
        if self._requirements_met(entry) and entry.id not in self.locked:
            self.available.add(entry.id)

    def start_research(self, tech_id):
        if tech_id in self.available and tech_id not in self.in_progress and tech_id not in self.locked:
            self.in_progress[tech_id] = 0

    def progress_research(self, tech_id, points):
        if tech_id in self.in_progress:
            self.in_progress[tech_id] += points
            entry = self.entries[tech_id]
            if self.in_progress[tech_id] >= entry.cost:
                self.complete_research(tech_id)

    def complete_research(self, tech_id):
        if tech_id in self.in_progress and tech_id not in self.locked:
            self.completed.add(tech_id)
            del self.in_progress[tech_id]
            self.available.discard(tech_id)
            self._unlock_new_techs(tech_id)

    def get_research_progress(self, tech_id):
        """
        Returns the progress (0.0-1.0) and percentage (0-100) for a given research entry.
        If not started, returns 0.0, 0.
        """
        entry = self.entries.get(tech_id)
        if not entry:
            return 0.0, 0
        progress = self.in_progress.get(tech_id, 0)
        percent = int(100 * progress / entry.cost) if entry.cost > 0 else 0
        return min(progress / entry.cost, 1.0), min(percent, 100)

    def get_available_research(self):
        """
        Returns a list of research entries that can be started (all prerequisites met, not completed, not in progress, not locked).
        """
        available = []
        for entry in self.entries.values():
            if entry.id in self.completed:
                continue
            if entry.id in self.in_progress:
                continue
            if entry.id in self.locked:
                continue
            if self._requirements_met(entry):
                available.append(entry)
        return available

    def assign_scientists(self, tech_id, scientists):
        """
        Assigns a number of scientists to a research project. Stores the number for progress calculation.
        """
        if tech_id in self.in_progress:
            self.in_progress[tech_id] = self.in_progress.get(tech_id, 0)
            self.entries[tech_id].assigned_scientists = scientists

    def progress_all_research(self):
        """
        Progresses all in-progress research by their assigned scientists per day.
        """
        for tech_id in list(self.in_progress.keys()):
            entry = self.entries[tech_id]
            scientists = getattr(entry, 'assigned_scientists', 0)
            self.progress_research(tech_id, scientists)

    def daily_progress(self):
        """
        Progress all in-progress research by their assigned scientists per day.
        If a research is completed, it is marked as completed and scientists are freed.
        This should be called once per day by the calendar.
        """
        completed_today = []
        for tech_id in list(self.in_progress.keys()):
            entry = self.entries[tech_id]
            scientists = getattr(entry, 'assigned_scientists', 0)
            self.in_progress[tech_id] += scientists
            if self.in_progress[tech_id] >= entry.cost:
                self.complete_research(tech_id)
                # Free scientists
                entry.assigned_scientists = 0
                completed_today.append(tech_id)
        return completed_today

    def is_completed(self, tech_id):
        return tech_id in self.completed

    def lock_entry(self, tech_id):
        """
        Permanently lock a research entry so it can never be available or completed.
        """
        self.locked.add(tech_id)
        self.available.discard(tech_id)
        self.in_progress.pop(tech_id, None)
        self.completed.discard(tech_id)

    def unlock_entry(self, tech_id):
        """
        Remove a research entry from the locked list.
        """
        self.locked.discard(tech_id)

    def _requirements_met(self, entry):
        return all(req in self.completed for req in entry.tech_needed)

    def _unlock_new_techs(self, completed_tech_id):
        for entry in self.entries.values():
            if entry.id not in self.completed and entry.id not in self.available and entry.id not in self.locked:
                if self._requirements_met(entry):
                    self.available.add(entry.id)

    def get_entry(self, tech_id):
        return self.entries.get(tech_id)

    def reset(self):
        self.completed.clear()
        self.in_progress.clear()
        self.available = {tid for tid, entry in self.entries.items() if self._requirements_met(entry) and tid not in self.locked}
        self.locked.clear()

    def visualize_dependencies(self):
        """
        Returns a string visualizing the research tree dependencies in a readable text format.
        Example:
        TechA
          -> TechB
          -> TechC
        TechB
          -> TechD
        ...
        """
        lines = []
        for entry in self.entries.values():
            line = f"{entry.id} ({entry.name})"
            if entry.tech_needed:
                reqs = ', '.join(entry.tech_needed)
                line += f"  [requires: {reqs}]"
            lines.append(line)
            # Show what this entry unlocks
            unlocks = [e.id for e in self.entries.values() if entry.id in e.tech_needed]
            for unlock in unlocks:
                lines.append(f"  -> {unlock}")
        return '\n'.join(lines)

    def export_dependencies_to_file(self, filepath):
        """Exports the research dependencies visualization to a text file."""
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(self.visualize_dependencies())

    def visualize_dependencies_tree(self):
        """
        Returns a string visualizing the research tree as a dependency tree, showing all paths from roots to leaves.
        """
        def visit(node_id, prefix, visited, lines):
            if node_id in visited:
                lines.append(f"{prefix}-> {node_id} (cycle)")
                return
            visited.add(node_id)
            entry = self.entries[node_id]
            lines.append(f"{prefix}{node_id} ({entry.name})")
            unlocks = [e.id for e in self.entries.values() if node_id in e.tech_needed]
            for unlock in unlocks:
                visit(unlock, prefix + "  -> ", visited.copy(), lines)

        # Find roots (entries with no prerequisites)
        roots = [e.id for e in self.entries.values() if not e.tech_needed]
        lines = []
        for root in roots:
            visit(root, '', set(), lines)
        # Also show disconnected nodes (not reachable from any root)
        all_ids = set(self.entries.keys())
        shown = set(l.split()[0] for l in lines if l)
        for node_id in all_ids - shown:
            visit(node_id, '', set(), lines)
        return '\n'.join(lines)

    def export_dependencies_tree_to_file(self, filepath):
        """Exports the research dependency tree visualization to a text file."""
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(self.visualize_dependencies_tree())

