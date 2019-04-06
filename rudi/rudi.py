from __future__ import print_function
from geo import spatial_distance
from tsp import tsp
from team import Meeting
import random
import numpy as np


class RunningDinner:
    """ Object representation of a RunningDinner event """

    def __init__(self):
        # list of participating teams
        self.teams = []
        # number of meetings
        self.nmeals = 3
        # number of teams per meeting
        self.nteams_per_meeting = 3
        self.strn = 99

    def addTeam(self, team):
        # Add a team to list of teams
        self.teams.append(team)
        team.setRudi(self)

    def loadcsv(self, csvfile):
        # load the event data from a csv file
        # TODO: implement
        pass

    def savecsv(self, csvfile="out.csv"):
        # save the event data to a csv file
        self.teams = sorted(self.teams, key=lambda t: t.id)
        with open("out.csv", "w+") as f:
            for team in self.teams:
                msg = "Team #"+str(team.id)
                msg += "\t"
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

    def organize(self):
        # organize the hosts, meetings and routes for the teams
        # with preferably minimal route lengths and no second encounters
        # Step 1: generate meetings & hosts for meals
        self.generateMeetings()
        # Step 2: generate routes for teams between meetings
        self.generateRoutes()
        # Step 3: try to optimize routes
        self.optimize()

    def generate_team_ids(self):
        # re-generate team ID so that they reflect spatial vicinity
        # using a traveling salesman algorithm
        N = len(self.teams)
        matrix = np.zeros((N, N))
        for i in range(N):
            for j in range(N):
                matrix[i, j] = spatial_distance(
                    self.teams[i].coords, self.teams[j].coords)

    def generateMeetings(self):
        # generate meetings & hosts for each meal
        for meal in range(self.nmeals):
            # create meeting at every nth team
            for team in self.teams:
                if (team.id-1) % self.nteams_per_meeting == meal:
                    # assign new meeting with team as host to team's route
                    team.route[meal] = Meeting(meal, team)

    def generateRoutes(self):
        # generate routes for teams between meetings for each meal
        for meal in range(self.nmeals):
            # generate a list of all meetings for this meal
            meetings = []
            for team in self.teams:
                if team.route[meal] is not None and team.route[meal] not in meetings:
                    meetings.append(team.route[meal])
            # repeat the following algorithm until all teams have a meeting for this meal
            ndone = 0
            nundecided = 0
            while ndone < len(self.teams):
                # reset counter
                ndone = 0
                # loop over teams, check out each team's options and handle accordingly
                for team in self.teams:
                    nundecided += 1
                    # if team already has a meet for this meal: count as assigned and skip
                    if team.route[meal] is not None:
                        ndone += 1
                        continue
                    # generate list of possible options (meetings) for the team
                    options = team.filterMeetings(meetings)
                    # handle according to the number of options
                    if len(options) == 0:
                        # zero options: allow reencounter with another team
                        options = team.filterMeetings(
                            meetings, reencounters=True)
                    if len(options) == 0:
                        # still no options: make up an own meeting!
                        team.attendMeeting(Meeting(meal, team))
                    elif len(options) == 1:
                        # single option: plug the meeting into team's route
                        team.attendMeeting(options[0])
                    else:
                        # multiple options:
                        # if not all teams are undecided yet, skip this one
                        if nundecided < len(self.teams):
                            continue
                        # else, all teams are undecided --> search optimal option
                        # sort the options by shortest distance to current position
                        distances = {}
                        for meeting in options:
                            distances[meeting] = spatial_distance(
                                team.coordsAt(meal-1), meeting.host.coords)
                        options = [x[0] for x in sorted(
                            distances.items(), key=lambda kv: kv[1])]
                        # pick the option with minimal walking distance
                        team.attendMeeting(options[0])
                    # routes may have changed, reset undecided counter
                    nundecided = 0

    # try to find errors and perform sane optimizations on the routes
    def optimize(self):
        # TODO: check for meetings with len(meeting.teams) == 1
        # TODO: check for optimization of routes by swapping teams
        pass
