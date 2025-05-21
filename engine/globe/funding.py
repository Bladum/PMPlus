class TFunding:
    """
    Class to manage funding of XCOM based on score in each country and make monthly report
    This is from country perspective
    """
    def __init__(self, countries):
        self.countries = countries  # List or dict of TCountry
        self.month_scores = {country.id: 0 for country in countries}

    def add_tile_score(self, country_id, score):
        if country_id in self.month_scores:
            self.month_scores[country_id] += score

    def monthly_report(self):
        """
        Update all countries' funding and relation based on their monthly score.
        Returns a summary report as a dict.
        """
        report = {}
        for country in self.countries:
            score = self.month_scores.get(country.id, 0)
            country.monthly_update(score)
            report[country.name] = {
                'relation': country.relation,
                'funding': country.funding,
                'active': country.active,
                'score': score
            }
            self.month_scores[country.id] = 0  # Reset for next month
        return report

