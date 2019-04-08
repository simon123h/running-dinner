from __future__ import print_function
from .geo import spatial_distance
from .team import Meeting
import random
import sys
import math
try:
    import tspy
except ImportError:
    raise ImportError(
        'Module \'tspy\' required.\nPlease install it via \'pip3 install --user tspy\'')
except SyntaxError:
    raise Exception("Module \'tspy\' requires Python 3")
try:
    import numpy as np
except ImportError:
    raise ImportError(
        'Module \'numpy\' required.\nPlease install it via \'pip3 install --user numpy\'')
try:
    import matplotlib.pyplot as plt
except ImportError:
    raise ImportError(
        'Module \'matplotlib\' required.\nPlease install it via \'pip3 install --user matplotlib\'')


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
        self.plotID = 0

    def addTeam(self, team):
        # Add a team to list of teams
        self.teams.append(team)
        team.setRudi(self)

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
                if csvfile == "":
                    print(msg)
                else:
                    print(msg, file=f)

    def routeslength(self):
        # total length of routes to be walked
        result = 0
        for team in self.teams:
            result += team.routelength()
        return result

    def rms_routes(self):
        # root mean square of routes to be walked
        result = 0
        for team in self.teams:
            result += math.pow(team.routelength(), 2)
        return math.sqrt(result / len(self.teams))

    def organize(self):
        # organize the hosts, meetings and routes for the teams
        # with preferably minimal route lengths and no second encounters

        # Step 0: re-generate team ID so that they reflect spatial vicinity
        print("Find single route through graph")
        self.generateTeamIDs(shuffle=True)
        # Step 1: generate meetings & hosts for meals
        print("Generate Meetings")
        self.generateMeetings()
        # Step 2: generate routes for teams between meetings
        print("Generate Routes")
        self.generateRoutes()
        # Step 3: try to optimize routes
        print("Optimize solution")
        self.optimize()

    def generateTeamIDs(self, shuffle=False):
        # re-generate team ID so that they reflect spatial vicinity
        # using a traveling salesman algorithm
        # shuffle teams
        if shuffle:
            random.shuffle(self.teams)
        # generate distance matrix
        N = len(self.teams)
        matrix = np.zeros((N, N))
        for i in range(N):
            for j in range(N):
                matrix[i, j] = spatial_distance(
                    self.teams[i].coords, self.teams[j].coords)
        # solve the traveling salesman problem using the package tspy
        tsp = tspy.TSP()
        tsp.read_mat(matrix)
        solver = tspy.solvers.TwoOpt_solver(
            initial_tour='NN', iter_num=10000)
        save_stdout = sys.stdout
        sys.stdout = open('/dev/null', 'w')  # no stdout for the following call
        solution = tsp.get_approx_solution(solver)
        sys.stdout = save_stdout
        xs = [self.teams[s].coords[0] for s in solution]
        ys = [self.teams[s].coords[1] for s in solution]
        plt.plot(xs, ys, linestyle="-", marker="o")
        plt.savefig("out/tsp.png")
        plt.cla()
        # set new team IDs according to solution
        for t in range(len(self.teams)):
            self.teams[t].id = solution[t]
        self.teams = sorted(self.teams, key=lambda t: t.id)

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
            # TODO: sort teams, so the ones furthest from center are served first
            # sort teams, so the ones that have a long route already are served first
            teams = sorted(
                self.teams, key=lambda t: t.routelength(), reverse=True)
            # repeat the following algorithm until all teams have a meeting for this meal
            ndone = 0
            nundecided = 0
            while ndone < len(self.teams):
                # reset counter
                ndone = 0
                # loop over teams, check out each team's options and handle accordingly
                for team in teams:
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
                        self.plot()
                    elif len(options) == 1:
                        # single option: plug the meeting into team's route
                        team.attendMeeting(options[0])
                        self.plot()
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
                        self.plot()
                    # routes may have changed, reset undecided counter
                    nundecided = 0

    # try to find errors and perform sane optimizations on the routes
    def optimize(self):
        # check for meetings with len(meeting.teams) == 1
        for meal in range(self.nmeals):
            # generate a list of all meetings for this meal
            meetings = []
            for team in self.teams:
                if team.route[meal] is not None and team.route[meal] not in meetings:
                    meetings.append(team.route[meal])
            for meeting in meetings:
                if len(meeting.teams) < 2:
                    print("Warning: meeting at", meeting.host, "has only",
                          len(meeting.teams), "members")
                    # TODO: try to swap teams to fix this

        # TODO: check for reencounters of teams
        # TODO: check for optimization of routes by swapping teams

    def plot(self, meals=None, teams=None):
        if teams is None:
            teams = self.teams
        if meals is None:
            meals = range(-1, self.nmeals)
        for team in self.teams:
            xs = [team.coordsAt(meal)[0] for meal in meals]
            ys = [team.coordsAt(meal)[1] for meal in meals]
            plt.plot(xs, ys, marker="o", color="grey", linestyle="")
        for team in teams:
            xs = [team.coordsAt(meal)[0] for meal in meals]
            ys = [team.coordsAt(meal)[1] for meal in meals]
            plt.plot(xs, ys, linestyle="-")
        plt.savefig("out/routes{:05d}.png".format(self.plotID))
        self.plotID += 1
        plt.cla()
