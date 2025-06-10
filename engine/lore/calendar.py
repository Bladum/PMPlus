"""
TCalendar: In-game calendar and campaign scheduling manager.
Purpose: Handles date progression, campaign generation, and event checks for each day, week, month, quarter, and year.
Last update: 2025-06-10
"""
from engine.lore.campaign_step import TCampaignStep


class TCalendar:
    """
    TCalendar manages the in-game calendar, campaign scheduling, and event checks.
    It advances time, triggers campaign and event logic, and provides date utilities.

    Attributes:
        year (int): Current year in the game.
        month (int): Current month (1-12).
        day (int): Current day (1-30).
        total_days (int): Total days elapsed since start.
        campaign_months (dict): Campaign rules for each month.
    """
    def __init__(self, data=None):
        """
        Initialize the calendar with campaign data.
        Args:
            data (dict): Campaign step data per month (e.g., {"m01": {...}, ...}).
        """
        self.year = 2000
        self.month = 1
        self.day = 1
        self.total_days = 0
        self.campaign_months = {}
        if data is None:
            data = {}
        # Parse campaign steps for each month
        for month_key, month_info in data.items():
            if not isinstance(month_info, dict):
                continue
            try:
                month_num = int(month_key[1:])
                entry = TCampaignStep(month_num, month_info)
                self.campaign_months[month_num] = entry
            except (ValueError, IndexError):
                continue
        # Fill up to 120 months (10 years)
        complete_months = {}
        last_month_data = None
        for i in range(120):
            if i in self.campaign_months:
                complete_months[i] = self.campaign_months[i]
                last_month_data = self.campaign_months[i]
            else:
                complete_months[i] = last_month_data
        self.campaign_months = complete_months

    def set_start_date(self, year, month, day):
        """
        Set the starting date for the calendar.
        Args:
            year (int): Start year.
            month (int): Start month (1-12).
            day (int): Start day (1-30).
        """
        self.year = year
        self.month = month
        self.day = day
        self.total_days = 0

    def get_date(self):
        """
        Get the current date.
        Returns:
            tuple: (year, month, day)
        """
        return self.year, self.month, self.day

    def advance_days(self, n, *args, **kwargs):
        """
        Advance the game by n days, performing all checks (daily, weekly, monthly, quarterly, yearly).
        Args:
            n (int): Number of days to advance.
        """
        for _ in range(n):
            self._advance_one_day(*args, **kwargs)

    def _advance_one_day(self, *args, **kwargs):
        """
        Advance the calendar by one day and trigger event checks.
        """
        self.day += 1
        self.total_days += 1
        if self.day > 30:
            self.day = 1
            self.month += 1
            if self.month > 12:
                self.month = 1
                self.year += 1
        self.on_day(*args, **kwargs)
        if (self.total_days % 7) == 1:
            self.on_week(*args, **kwargs)
        if self.day == 1:
            self.on_month(*args, **kwargs)
        if self.day == 1 and self.month in (1, 4, 7, 10):
            self.on_quarter(*args, **kwargs)
        if self.day == 1 and self.month == 1:
            self.on_year(*args, **kwargs)

    def on_day(self, *args, **kwargs):
        """Placeholder for daily logic."""
        pass

    def on_week(self, *args, **kwargs):
        """Placeholder for weekly logic."""
        pass

    def on_month(self, *args, **kwargs):
        """Placeholder for monthly logic."""
        pass

    def on_quarter(self, *args, **kwargs):
        """Placeholder for quarterly logic."""
        pass

    def on_year(self, *args, **kwargs):
        """Placeholder for yearly logic."""
        pass

    def generate_monthly_campaigns(self, month, research_status, all_campaigns, all_factions, worldmap):
        """
        Generate campaigns for the given month based on campaign_months data.
        Args:
            month (int): Month number.
            research_status (callable): Function or set to check if tech is researched.
            all_campaigns (list): List of TCampaign.
            all_factions (list): List of TFaction.
            worldmap: Reference to world map for region/tile selection.
        Returns:
            list: Campaign instances to start this month.
        """
        month_data = self.campaign_months.get(month)
        if not month_data:
            return []
        import random
        weights = month_data.weights or {}
        factions_pool = list(weights.keys())
        qty = random.randint(month_data.qty_min, month_data.qty_max)
        selected_factions = random.choices(factions_pool, weights=[weights[f] for f in factions_pool], k=qty)
        campaigns_to_start = []
        for faction_name in selected_factions:
            faction = next((f for f in all_factions if f.name == faction_name), None)
            if not faction:
                continue
            if faction.tech_start and not all(research_status(t) for t in faction.tech_start):
                continue
            if faction.tech_end and any(research_status(t) for t in faction.tech_end):
                continue
            valid_campaigns = []
            for camp in all_campaigns:
                if camp.faction != faction_name:
                    continue
                if camp.tech_start and not all(research_status(t) for t in camp.tech_start):
                    continue
                if camp.tech_end and any(research_status(t) for t in camp.tech_end):
                    continue
                valid_campaigns.append(camp)
            if not valid_campaigns:
                continue
            campaign = random.choice(valid_campaigns)
            regions = campaign.regions or {r.name: 1 for r in worldmap.regions}
            region_names = list(regions.keys())
            region_weights = [regions[r] for r in region_names]
            selected_region = random.choices(region_names, weights=region_weights, k=1)[0]
            campaign_instance = {
                'campaign': campaign,
                'faction': faction,
                'region': selected_region,
                'missions': [],
                'start_day': None,
                'active_missions': []
            }
            for mission in campaign.missions:
                if mission.tech_start and not all(research_status(t) for t in mission.tech_start):
                    continue
                if mission.tech_end and any(research_status(t) for t in mission.tech_end):
                    continue
                for _ in range(mission.count):
                    if random.random() > mission.chance:
                        continue
                    campaign_instance['missions'].append({
                        'mission': mission,
                        'timer': mission.timer,
                        'scheduled_day': None,
                        'region': selected_region
                    })
            campaigns_to_start.append(campaign_instance)
        return campaigns_to_start

    def daily_campaign_check(self, current_day, active_campaigns, worldmap):
        """
        Check all active campaigns and their missions, create locations if timer/date fits.
        Args:
            current_day (int): Current day in the calendar.
            active_campaigns (list): Campaign instances generated by generate_monthly_campaigns.
            worldmap: Reference to world map for location creation.
        """
        for camp in active_campaigns:
            for mission_entry in camp['missions']:
                if mission_entry['scheduled_day'] == current_day:
                    region = mission_entry['region']
                    tile = worldmap.get_random_tile_in_region(region)
                    # Placeholder: worldmap.create_location(mission_entry['mission'], camp['faction'], tile)
                    camp['active_missions'].append(mission_entry)
                    # Optionally, remove from missions if one-time
