from __future__ import print_function
from rudi import RunningDinner, Team


def main():
    # Main routine of program
    print("Hello World!")
    # create the event
    rudi = RunningDinner()
    # load the teams from a file
    # rudi.loadcsv("in.csv")
    # create some teams
    rudi.addTeam(Team())
    rudi.addTeam(Team())
    rudi.addTeam(Team())
    # find optimal routes
    rudi.solve()
    # save the routes to file
    rudi.savecsv("out.csv")


# If called directly: invoke main routine
if __name__ == "__main__":
    main()
