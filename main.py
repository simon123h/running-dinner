from __future__ import print_function
from rudi import RunningDinner, Team


# rudi = None
rudi = RunningDinner()


def main():
    # Main routine of program
    # create the event
    # load the teams from a file
    # rudi.loadcsv("in.csv")
    # create some teams
    for i in range((9*8)-6):
        t = Team()
        t.coords = (0, i)
        rudi.addTeam(t)

    # find optimal routes
    rudi.organize()
    # save the routes to file
    rudi.savecsv("out.csv")


# If called directly: invoke main routine
if __name__ == "__main__":
    main()
