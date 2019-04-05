from __future__ import print_function
from rudi import RunningDinner, Team


# rudi = None
rudi = RunningDinner()


def main():
    # Main routine of program
    print("Hello World!")
    # create the event
    # load the teams from a file
    # rudi.loadcsv("in.csv")
    # create some teams
    # rudi.addTeam(Team())
    # rudi.teams[-1].coords = (0, 0)
    # rudi.addTeam(Team())
    # rudi.teams[-1].coords = (1, 0)
    # rudi.addTeam(Team())
    # rudi.teams[-1].coords = (0, 1)

    # rudi.addTeam(Team())
    # rudi.teams[-1].coords = (-1, 0)
    # rudi.addTeam(Team())
    # rudi.teams[-1].coords = (0, -1)
    # rudi.addTeam(Team())
    # rudi.teams[-1].coords = (1, 1)

    for i in range(9):
        rudi.addTeam(Team())
        rudi.teams[-1].coords = (0, i)

    # find optimal routes
    rudi.optimize()
    # save the routes to file
    rudi.savecsv("out.csv")


# If called directly: invoke main routine
if __name__ == "__main__":
    main()
