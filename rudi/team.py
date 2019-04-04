class Team:
    """ Object representation of a Team """
    # total number of teams
    teamcount = 0

    def __init__(self):
        self.route = []
        self.members = []
        self.adress = None
        self.coords = None
        self.id = Team.teamcount
        Team.teamcount += 1

    def setAdress(self, adress):
        self.adress = adress
        self.coords = adress2coords(adress)
