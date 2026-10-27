"""Member 1: OOP classes for the Cricket Sports Analytics project."""



class Player:
    def __init__(self, name, team="Unknown", role="Player"):
        self.__name = str(name)
        self.__team = str(team)
        self.__role = str(role)

    def get_name(self):
        return self.__name

    def get_team(self):
        return self.__team

    def get_role(self):
        return self.__role

    def set_team(self, team):
        self.__team = str(team)

    def calculate_performance(self):
        """Base implementation; subclasses override this method."""
        return 0.0

    def __str__(self):
        return f"{self.__name} ({self.__role})"



class Batter(Player):
    def __init__(self, name, runs, balls_faced):
        super().__init__(name, role="Batter")
        self.__runs = int(runs)
        self.__balls_faced = int(balls_faced)

    def get_runs(self):
        return self.__runs

    def get_balls_faced(self):
        return self.__balls_faced

    def calculate_performance(self):
        """Return batting strike rate."""
        if self.__balls_faced == 0:
            return 0.0
        return round(self.__runs / self.__balls_faced * 100, 2)


class Bowler(Player):
    def __init__(self, name, team="Unknown", runs_conceded=0, wickets=0,
                 legal_balls=0):
        super().__init__(name, team=team, role="Bowler")
        self.__runs_conceded = float(runs_conceded)
        self.__wickets = int(wickets)
        self.__legal_balls = int(legal_balls)

    def get_runs_conceded(self):
        return self.__runs_conceded

    def get_wickets(self):
        return self.__wickets

    def get_legal_balls(self):
        return self.__legal_balls

    def calculate_performance(self):
        """Return bowling economy rate (runs per six legal balls)."""
        if self.__legal_balls == 0:
            return 0.0
        return round(self.__runs_conceded / (self.__legal_balls / 6), 2)


class Team:
    def __init__(self, name, total_runs=0, wickets=0, legal_balls=0):
        self.__name = str(name)
        self.__total_runs = int(total_runs)
        self.__wickets = int(wickets)
        self.__legal_balls = int(legal_balls)

    def get_name(self):
        return self.__name

    def get_total_runs(self):
        return self.__total_runs

    def calculate_performance(self):
        """Return average runs per legal ball."""
        if self.__legal_balls == 0:
            return 0.0
        return round(self.__total_runs / self.__legal_balls, 3)

    def __str__(self):
        return f"{self.__name}: {self.__total_runs} runs"
