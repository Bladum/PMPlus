from engine.lore.campaign_month import TCampaignMonth


class TCalendar:
    """
    Represents a calendar in game, it is used to manage campaigns
    Every month new campaign for specific faction is created in specific region
    manage all date related methods
    manage all events
    """
    def __init__(self, data=None):

        self.year = 2000
        self.month = 1
        self.day = 1
        self.total_days = 0

        # Campaign and arc entries
        self.campaign_months = {}

        for month_key, month_info in data.items():
            if not isinstance(month_info, dict):
                continue

            # Parse month number from key (e.g., "m03" -> 3)
            try:
                month_num = int(month_key[1:])
                entry = TCampaignMonth(month_num, month_info)
                self.campaign_months[month_num] = entry
            except (ValueError, IndexError):
                # Skip invalid month keys
                continue

        complete_months = {}
        last_month_data = None
        for i in range(120):  # Fill up to month 120 = 10 years of gameplay
            if i in self.campaign_months:
                # If this month has data, use it
                complete_months[i] = self.campaign_months[i]
                last_month_data = self.campaign_months[i]
            else:
                complete_months[i] = last_month_data

        # Replace the sparse months with the complete set
        self.campaign_months = complete_months

    def set_start_date(self, year, month, day):
        self.year = year
        self.month = month
        self.day = day
        self.total_days = 0

    def get_date(self):
        return self.year, self.month, self.day

    def advance_days(self, n, *args, **kwargs):
        """
        Advance the game by n days, performing all checks (daily, weekly, monthly, quarterly, yearly).
        """
        for _ in range(n):
            self._advance_one_day(*args, **kwargs)

    def _advance_one_day(self, *args, **kwargs):
        # Advance day
        self.day += 1
        self.total_days += 1
        if self.day > 30:
            self.day = 1
            self.month += 1
            if self.month > 12:
                self.month = 1
                self.year += 1
        # Daily check
        self.on_day(*args, **kwargs)
        # Weekly check (Monday: every 7th day, assuming start is Monday)
        if (self.total_days % 7) == 1:
            self.on_week(*args, **kwargs)
        # Monthly check (first day of month)
        if self.day == 1:
            self.on_month(*args, **kwargs)
        # Quarterly check (first day of quarter)
        if self.day == 1 and self.month in (1, 4, 7, 10):
            self.on_quarter(*args, **kwargs)
        # Yearly check (first day of year)
        if self.day == 1 and self.month == 1:
            self.on_year(*args, **kwargs)

    def on_day(self, *args, **kwargs):
        # Placeholder for daily logic
        pass

    def on_week(self, *args, **kwargs):
        # Placeholder for weekly logic
        pass

    def on_month(self, *args, **kwargs):
        # Placeholder for monthly logic
        pass

    def on_quarter(self, *args, **kwargs):
        # Placeholder for quarterly logic
        pass

    def on_year(self, *args, **kwargs):
        # Placeholder for yearly logic
        pass

    def generate_monthly_campaigns(self, month, research_status, all_campaigns, all_factions, worldmap):
        """
        Generate campaigns for the given month based on campaign_months data.
        research_status: function or set to check if tech is researched
        all_campaigns: list of TCampaign (all possible campaigns)
        all_factions: list of TFaction (all possible factions)
        worldmap: reference to world map for region/tile selection
        """
        month_data = self.campaign_months.get(month)
        if not month_data:
            return []

        # 1. Select factions for this month using weights and qty_min/qty_max
        import random
        weights = month_data.weights or {}
        factions_pool = list(weights.keys())
        qty = random.randint(month_data.qty_min, month_data.qty_max)
        selected_factions = random.choices(factions_pool, weights=[weights[f] for f in factions_pool], k=qty)

        campaigns_to_start = []
        for faction_name in selected_factions:
            # 2. Find the faction object
            faction = next((f for f in all_factions if f.name == faction_name), None)
            if not faction:
                continue
            # 3. Check tech requirements for faction
            if faction.tech_start and not all(research_status(t) for t in faction.tech_start):
                continue
            if faction.tech_end and any(research_status(t) for t in faction.tech_end):
                continue
            # 4. Find campaigns for this faction and check their tech requirements
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
            # 5. Select a campaign randomly
            campaign = random.choice(valid_campaigns)
            # 6. Select region using campaign regions weights or all regions equally
            regions = campaign.regions or {r.name: 1 for r in worldmap.regions}
            region_names = list(regions.keys())
            region_weights = [regions[r] for r in region_names]
            selected_region = random.choices(region_names, weights=region_weights, k=1)[0]
            # 7. Prepare campaign instance for this month
            campaign_instance = {
                'campaign': campaign,
                'faction': faction,
                'region': selected_region,
                'missions': [],
                'start_day': None,  # to be set by calendar
                'active_missions': []  # missions scheduled for this campaign
            }
            # 8. For each mission in campaign, check tech and schedule missions
            for mission in campaign.missions:
                if mission.tech_start and not all(research_status(t) for t in mission.tech_start):
                    continue
                if mission.tech_end and any(research_status(t) for t in mission.tech_end):
                    continue
                for _ in range(mission.count):
                    if random.random() > mission.chance:
                        continue
                    # Schedule mission with timer (delay)
                    campaign_instance['missions'].append({
                        'mission': mission,
                        'timer': mission.timer,
                        'scheduled_day': None,  # to be set when campaign starts
                        'region': selected_region
                    })
            campaigns_to_start.append(campaign_instance)
        return campaigns_to_start

    def daily_campaign_check(self, current_day, active_campaigns, worldmap):
        """
        Check all active campaigns and their missions, create locations if timer/date fits.
        active_campaigns: list of campaign instances generated by generate_monthly_campaigns
        worldmap: reference to world map for location creation
        """
        for camp in active_campaigns:
            for mission_entry in camp['missions']:
                # If mission is scheduled for today
                if mission_entry['scheduled_day'] == current_day:
                    # Select random tile in region
                    region = mission_entry['region']
                    tile = worldmap.get_random_tile_in_region(region)
                    # Create location (ufo/site/base) on world map
                    # Placeholder: worldmap.create_location(mission_entry['mission'], camp['faction'], tile)
                    camp['active_missions'].append(mission_entry)
                    # Optionally, remove from missions if one-time

