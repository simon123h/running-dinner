from .geo import adress2coords, spatial_distance


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
        self.route = [None]*rudi.nmeals

    def meet(self, team):
        # an enemy team was met: save to list of met teams
        if team not in self.teamsMet:
            self.teamsMet.append(team)
        if self not in team.teamsMet:
            team.teamsMet.append(self)

    def attendMeeting(self, meeting):
        # attend a meeting (as corresponding meal)
        # add meeting to route
        self.route[meeting.meal] = meeting
        # add team to meeting
        meeting.addTeam(self)

    def filterMeetings(self, meetings, reencounters=False, overcrowding=0, debug=False):
        # from a list of meetings, return the ones that match the criteria
        options = []
        for meeting in meetings:
            # is the meeting overcrowded? --> skip
            if len(meeting.teams) >= self.rudi.nteams_per_meeting + overcrowding:
                continue
            # have some teams met already? --> skip
            if any(t in meeting.teams for t in self.teamsMet) and not reencounters:
                continue
            # else: add the meeting to list of options
            options.append(meeting)
        # print debugging info
        if debug:
            print(self, "Options:\t", ", ".join(
                [str(o) for o in options]))
        return options

    def coordsAt(self, meal=-1):
        # returns the current position of the team for given meal
        if meal < 0:
            return self.coords
        elif self.route[meal] is None:
            return self.coordsAt(meal-1)
        else:
            return self.route[meal].host.coords

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

    def __init__(self, meal, host=None):
        self.teams = []
        self.meal = meal
        self.host = None
        if host is not None:
            self.addTeam(host)
            self.setHost(host)

    def addTeam(self, team):
        # save enemy teams to teamsMet list
        for enemy in self.teams:
            team.meet(enemy)
        # try to add team to list of teams if possible
        if team not in self.teams:
            self.teams.append(team)

    def setHost(self, team):
        self.host = team

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return "Meeting@"+str(self.host.id)+"<" + ", ".join(["#"+str(t.id) for t in self.teams]) + ">"
