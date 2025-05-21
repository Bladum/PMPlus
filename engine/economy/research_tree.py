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

    def add_entry(self, entry):
        # Randomize cost 50-150% of base cost when adding to tree
        if not hasattr(entry, '_cost_randomized'):
            base_cost = entry.cost
            entry.cost = int(base_cost * random.uniform(0.5, 1.5))
            entry._cost_randomized = True
        self.entries[entry.id] = entry
        if self._requirements_met(entry):
            self.available.add(entry.id)

    def start_research(self, tech_id):
        if tech_id in self.available and tech_id not in self.in_progress:
            self.in_progress[tech_id] = 0

    def progress_research(self, tech_id, points):
        if tech_id in self.in_progress:
            self.in_progress[tech_id] += points
            entry = self.entries[tech_id]
            if self.in_progress[tech_id] >= entry.cost:
                self.complete_research(tech_id)

    def complete_research(self, tech_id):
        if tech_id in self.in_progress:
            self.completed.add(tech_id)
            del self.in_progress[tech_id]
            self.available.discard(tech_id)
            self._unlock_new_techs(tech_id)

    def get_available_research(self):
        return [self.entries[tid] for tid in self.available if tid not in self.completed]

    def is_completed(self, tech_id):
        return tech_id in self.completed

    def _requirements_met(self, entry):
        return all(req in self.completed for req in entry.tech_needed)

    def _unlock_new_techs(self, completed_tech_id):
        for entry in self.entries.values():
            if entry.id not in self.completed and entry.id not in self.available:
                if self._requirements_met(entry):
                    self.available.add(entry.id)

    def get_entry(self, tech_id):
        return self.entries.get(tech_id)

    def reset(self):
        self.completed.clear()
        self.in_progress.clear()
        self.available = {tid for tid, entry in self.entries.items() if self._requirements_met(entry)}

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
        Example:
        A
          -> B
            -> C
        D
          -> C
        E
          -> B
            -> C
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

