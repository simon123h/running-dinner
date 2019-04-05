from geo import adress2coords, spatial_distance


class Team:
    """ Object representation of a Team """
    # total number of teams
    teamcount = 0

    def __init__(self):
        # initialize Team object
        # member names
        self.members = []
        # adress and corresponding coordinates
        self.adress = None
        self.coords = None
        # list of Meetings, that the team will attend
        self.route = []
        # the instance of the RuDi event in which the team participates
        self.rudi = None
        # generate ID of the team by total team count
        self.id = Team.teamcount
        Team.teamcount += 1
        # has the team yet been a host for a meeting?
        self.hasHosted = False
        # list of teams that were already met
        self.teamsMet = []

    def setAdress(self, adress):
        # set the adress and geocode coordinates
        self.adress = adress
        self.coords = adress2coords(adress)

    def setRudi(self, rudi):
        # set the RuDi event in which the team participates
        self.rudi = rudi
        # create empty route
        self.route = [None]*rudi.nmeetings

    def met(self, team):
        # an enemy team was met: save to list of met teams
        if team not in self.teamsMet:
            self.teamsMet.append(team)

    def routelength(self):
        # calculate total route length
        result = 0
        startCoords = self.coords
        for meeting in self.route:
            result += spatial_distance(startCoords, meeting.host.coords)
            startCoords = meeting.host.coords
        return result

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return "Team#" + str(self.id)


class Meeting:
    """ Object representation of a Meeting: encounter of Teams """

    def __init__(self):
        self.teams = []
        self.host = None

    def addTeam(self, team):
        # save enemy teams to teamsMet list
        for enemy in self.teams:
            team.met(enemy)
            enemy.met(team)
        # try to add team to list of teams if possible
        if team not in self.teams:
            self.teams.append(team)
            # return True if successful
            return True
        # return False if not successful
        return False

    def setHost(self, team):
        self.host = team

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return "Meeting@"+str(self.host.id)+"<" + ", ".join(["#"+str(t.id) for t in self.teams]) + ">"
