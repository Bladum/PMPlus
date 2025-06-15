"""
engine/economy/research_tree.py

Defines the TResearchTree class, which manages the research tree structure, dependencies, progress, and visualization.

Classes:
    TResearchTree: Manages the research tree and research progress.

Last standardized: 2025-06-15
"""

"""
research_tree.py
---------------
TResearchTree: Manages the research tree and research progress.
Purpose: Handles research entries, progress, dependencies, and visualization in the XCOM/AlienFall economy system.

This module defines the TResearchTree class, which manages the research tree structure, dependencies, progress, and visualization. It supports randomization of costs, dependency unlocking, and research status tracking.

Attributes:
    entries (dict): tech_id -> TResearchEntry
    completed (set): Set of completed tech_ids
    in_progress (dict): tech_id -> progress (int)
    available (set): Set of available tech_ids
    locked (set): Set of permanently locked tech_ids

Usage:
    tree = TResearchTree()
    tree.add_entry(entry)
    tree.start_research(tech_id)
    tree.progress_research(tech_id, points)
    tree.complete_research(tech_id)
"""

import random

class TResearchTree:
    """
    Represents a research tree, it is a list of research entries.
    Manages research progress, dependencies, and visualization.
    See module docstring for attribute details.
    
    Methods:
        add_entry(entry): Add a research entry to the tree.
        start_research(tech_id): Start research on a tech.
        progress_research(tech_id, points): Advance progress on a tech.
        complete_research(tech_id): Mark a tech as completed.
        get_research_progress(tech_id): Get progress and percent for a tech.
        get_available_research(): List all available research entries.
        assign_scientists(tech_id, scientists): Assign scientists to a tech.
        progress_all_research(): Advance all in-progress research.
        daily_progress(): Advance all research by one day.
        is_completed(tech_id): Check if a tech is completed.
        lock_entry(tech_id), unlock_entry(tech_id): Lock/unlock a tech.
        _requirements_met(entry): Check if requirements are met for a tech.
        _unlock_new_techs(completed_tech_id): Unlock new techs after completion.
        get_entry(tech_id): Get a research entry by ID.
        reset(): Reset the tree state.
        visualize_dependencies(): Visualize dependencies.
        export_dependencies_to_file(filepath): Export dependencies to file.
        visualize_dependencies_tree(): Visualize dependency tree.
        export_dependencies_tree_to_file(filepath): Export dependency tree to file.
    """

    def __init__(self):
        self.entries = {}  # tech_id -> TResearchEntry
        self.completed = set()
        self.in_progress = {}  # tech_id -> progress (int)
        self.available = set()
        self.locked = set()  # tech_id set for permanently locked research

    def add_entry(self, entry):
        """
        Add a research entry to the tree, randomizing cost if needed.
        Args:
            entry (TResearchEntry): The research entry to add.
        """
        # Randomize cost 50-150% of base cost when adding to tree
        if not hasattr(entry, '_cost_randomized'):
            base_cost = entry.cost
            entry.cost = int(base_cost * random.uniform(0.5, 1.5))
            entry._cost_randomized = True
        self.entries[entry.id] = entry
        if self._requirements_met(entry) and entry.id not in self.locked:
            self.available.add(entry.id)

    def start_research(self, tech_id):
        """
        Start research on a technology if available and not locked.
        Args:
            tech_id (str): Technology ID to start.
        """
        if tech_id in self.available and tech_id not in self.in_progress and tech_id not in self.locked:
            self.in_progress[tech_id] = 0

    def progress_research(self, tech_id, points):
        """
        Advance progress on a technology by a given number of points.
        Args:
            tech_id (str): Technology ID.
            points (int): Progress points to add.
        """
        if tech_id in self.in_progress:
            self.in_progress[tech_id] += points
            entry = self.entries[tech_id]
            if self.in_progress[tech_id] >= entry.cost:
                self.complete_research(tech_id)

    def complete_research(self, tech_id):
        """
        Mark a technology as completed and unlock dependencies.
        Args:
            tech_id (str): Technology ID to complete.
        """
        if tech_id in self.in_progress and tech_id not in self.locked:
            self.completed.add(tech_id)
            del self.in_progress[tech_id]
            self.available.discard(tech_id)
            self._unlock_new_techs(tech_id)

    def get_research_progress(self, tech_id):
        """
        Returns the progress (0.0-1.0) and percentage (0-100) for a given research entry.
        Args:
            tech_id (str): Technology ID.
        Returns:
            tuple: (progress ratio, percent complete)
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
        Returns:
            list: List of available TResearchEntry objects.
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
        Assign a number of scientists to a technology.
        Args:
            tech_id (str): Technology ID.
            scientists (int): Number of scientists to assign.
        """
        if tech_id in self.in_progress:
            self.in_progress[tech_id] = self.in_progress.get(tech_id, 0)
            self.entries[tech_id].assigned_scientists = scientists

    def progress_all_research(self):
        """
        Advance all in-progress research by one day.
        """
        for tech_id in list(self.in_progress.keys()):
            entry = self.entries[tech_id]
            scientists = getattr(entry, 'assigned_scientists', 0)
            self.progress_research(tech_id, scientists)

    def daily_progress(self):
        """
        Advance all research by one day (alias for progress_all_research).
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
        """
        Check if a technology is completed.
        Args:
            tech_id (str): Technology ID.
        Returns:
            bool: True if completed, False otherwise.
        """
        return tech_id in self.completed

    def lock_entry(self, tech_id):
        """
        Permanently lock a technology entry.
        Args:
            tech_id (str): Technology ID.
        """
        self.locked.add(tech_id)
        self.available.discard(tech_id)
        self.in_progress.pop(tech_id, None)
        self.completed.discard(tech_id)

    def unlock_entry(self, tech_id):
        """
        Unlock a previously locked technology entry.
        Args:
            tech_id (str): Technology ID.
        """
        self.locked.discard(tech_id)

    def _requirements_met(self, entry):
        """
        Check if all requirements for a research entry are met.
        Args:
            entry (TResearchEntry): The research entry to check.
        Returns:
            bool: True if requirements are met.
        """
        return all(req in self.completed for req in entry.tech_needed)

    def _unlock_new_techs(self, completed_tech_id):
        """
        Unlock new technologies after completing a tech.
        Args:
            completed_tech_id (str): Completed technology ID.
        """
        for entry in self.entries.values():
            if entry.id not in self.completed and entry.id not in self.available and entry.id not in self.locked:
                if self._requirements_met(entry):
                    self.available.add(entry.id)

    def get_entry(self, tech_id):
        """
        Get a research entry by technology ID.
        Args:
            tech_id (str): Technology ID.
        Returns:
            TResearchEntry: The research entry object.
        """
        return self.entries.get(tech_id)

    def reset(self):
        """
        Reset the research tree state.
        """
        self.completed.clear()
        self.in_progress.clear()
        self.available = {tid for tid, entry in self.entries.items() if self._requirements_met(entry) and tid not in self.locked}
        self.locked.clear()

    def visualize_dependencies(self):
        """
        Visualize the research dependencies (implementation dependent).
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
        """
        Export the research dependencies to a file.
        Args:
            filepath (str): Path to the output file.
        """
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(self.visualize_dependencies())

    def visualize_dependencies_tree(self):
        """
        Visualize the research dependency tree (implementation dependent).
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
        """
        Export the research dependency tree to a file.
        Args:
            filepath (str): Path to the output file.
        """
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(self.visualize_dependencies_tree())
