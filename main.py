from __future__ import print_function
import matplotlib
matplotlib.use("Agg")
from rudi import RunningDinner, Team
from numpy.random import normal
from subprocess import Popen
rudi = RunningDinner()


def main():
    # Main routine of program
    Popen("rm -rf out; mkdir -p out", shell=True).communicate()
    # create the event
    # load the teams from a file
    # rudi.loadcsv("in.csv")
    # create some teams
    N = 18
    for _ in range(N):
        t = Team()
        t.coords = (normal(), normal())
        rudi.addTeam(t)

    # find optimal routes
    rudi.organize()
    # save the routes to file
    rudi.savecsv("out.csv")
    print("Routelength:", rudi.routeslength())
    rudi.plot()

# If called directly: invoke main routine
if __name__ == "__main__":
    main()
