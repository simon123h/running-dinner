from __future__ import print_function
from geo import spatial_distance
from team import Meeting
import random


class RunningDinner:
    """ Object representation of a RunningDinner event """

    def __init__(self):
        # list of participating teams
        self.teams = []
        # number of meetings
        self.nmeetings = 3
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

    def optimize(self):
        # Find optimal routes for teams
        self.generateMeetings(maxDistance=25)
        # self.generateMeetings(maxDistance=25)
        # self.generateMeetings(maxDistance=25)
        self.savecsv()

    def generateMeetings(self, maxDistance=100):
        # random.shuffle(self.teams)
        penalty_remeet = 100
        penalty_overfill = 9999
        penalty_rehost = 9999
        for meal in range(self.nmeetings):
            for _ in range(self.nteams_per_meeting):
                for team in self.teams:
                    # if team already has a Meeting for this meal: skip
                    if team.route[meal] is not None:
                        continue
                    # generate dictionary of possible meetings and distances
                    meetings = {}
                    for enemy in self.teams:
                        if enemy is not team and enemy.route[meal] is not None:
                            meeting = enemy.route[meal]
                            penalty = 0
                            # if the meeting would include teams that already met: penalize
                            if any(t in meeting.teams for t in team.teamsMet):
                                penalty += penalty_remeet
                            # if the meeting is full: penalize
                            if len(meeting.teams) >= self.nteams_per_meeting:
                                penalty += penalty_overfill
                            # else: add to list of potential meetings
                            meetings[meeting] = spatial_distance(
                                team.coords, meeting.host.coords) + penalty
                    # add possibility of hosting a meeting
                    ownmeeting = Meeting()
                    ownmeeting.setHost(team)
                    if not team.hasHosted and len(meetings) == 0:
                        meetings[ownmeeting] = 0
                    elif not team.hasHosted:
                        meetings[ownmeeting] = 10
                    elif meal > 0 and team.route[meal-1] is not None and team.route[meal-1].host is team:
                        meetings[ownmeeting] = penalty_rehost
                    # sort dictionary by distance
                    meetings = sorted(meetings.items(), key=lambda kv: kv[1])
                    # print(team, meetings)
                    # if there is meetings near me, go to the closest one!
                    if len(meetings) > 0 and meetings[0][1] < maxDistance:
                        meeting = meetings[0][0]
                        # assign team to meeting
                        meeting.addTeam(team)
                        # put meeting into team's route
                        team.route[meal] = meeting
                        # if the meeting is self hosted, adjust boolean
                        if meeting.host is team:
                            team.hasHosted = True
                    # else: do nothing, maybe a suitable meeting is found later on!
