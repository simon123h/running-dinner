
class RunningDinner:
    """ Object representation of a RunningDinner event """

    def __init__(self):
        self.teams = []

    def addTeam(self, team):
        # Add a team to list of teams
        self.teams.append(team)

    def solve(self):
        # Find optimal routes for teams
        # TODO: implement
        pass

    def loadcsv(self, csvfile):
        # load the event data from a csv file
        # TODO: implement
        pass

    def savecsv(self, csvfile):
        # save the event data to a csv file
        # TODO: implement
        pass
