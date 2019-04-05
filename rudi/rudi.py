from __future__ import print_function
from geo import spatial_distance
from team import Meeting


class RunningDinner:
    """ Object representation of a RunningDinner event """

    def __init__(self):
        # list of participating teams
        self.teams = []
        # number of meetings
        self.nmeetings = 3
        # number of teams per meeting
        self.nteams_per_meeting = 3

    def addTeam(self, team):
        # Add a team to list of teams
        self.teams.append(team)
        team.setRudi(self)

    def loadcsv(self, csvfile):
        # load the event data from a csv file
        # TODO: implement
        pass

    def savecsv(self, csvfile):
        # save the event data to a csv file
        # TODO: implement
        with open("out.csv", "w+") as f:
            for team in self.teams:
                msg = "Team #"+str(team.id)
                msg += "\n"
                msg += "Route: "
                msg += ", ".join([(str(m.host.id) if m is not None else "N")
                                  for m in team.route])
                print(msg)

    def routeslength(self):
        # total length of routes to be walked (including constraint penalties)
        result = 0
        for team in self.teams:
            result += team.routelength()
        return result

    def optimize(self):
        # Find optimal routes for teams
        # first: generate Meetings and assign hosts
        self.generateMeetings()
        # second: generate routes for each team
        # self.generateRoutes()
        pass

    def generateMeetings(self):
        # assign meetings to teams
        for meal in range(self.nmeetings):
            for team in self.teams:
                # generate dictionary of meetings and distances
                meetings = {}
                for enemy in self.teams:
                    if enemy is not team:
                        meeting = enemy.route[meal]
                        # if meeting exists: skip
                        if meeting is None:
                            continue
                        # if the meeting would include teams that already met: skip
                        if any(t in meeting.teams for t in team.teamsMet):
                            continue
                        # if the meeting is full
                        if len(meeting.teams) >= self.nteams_per_meeting:
                            continue
                        # else: add to list of potential meetings
                        meetings[meeting] = spatial_distance(
                            team.coords, meeting.host.coords)
                # sort dictionary by distance
                meetings = sorted(meetings.items(), key=lambda kv: kv[1])
                # if there is meetings near me, go to the closest one!
                if len(meetings) > 0:
                    meeting = meetings[0][0]
                    # assign team to meeting
                    meeting.addTeam(team)
                    # put meeting into team's route
                    team.route[meal] = meeting
                elif not team.hasHosted:
                    # no close meeting was found, team has not yet hosted
                    # team should be host for new meeting!
                    team.route[meal] = Meeting()
                    team.route[meal].host = team
                    team.route[meal].addTeam(team)
                    team.hasHosted = True

    def generateRoutes(self):
        # find optimal route of meetings for each team
        # TODO: implement
        pass
