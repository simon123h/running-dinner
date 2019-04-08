from __future__ import print_function
from subprocess import Popen
import matplotlib
matplotlib.use("Agg")


def main():
    # Main routine of program

    # recreate the output folder
    Popen("rm -rf out; mkdir -p out; mkdir -p out/mails", shell=True).communicate()

    # create the event
    from rudi import RunningDinner, Team, Person
    rudi = RunningDinner()

    # # load the teams from a file
    # import csv
    # with open("in.tsv") as csv_file:
    #     csv_reader = csv.reader(csv_file, delimiter='\t')
    #     for row in csv_reader:
    #         if row[4] != "":
    #             p = Person(row[1])
    #             p.email = row[2]
    #             t = Team()
    #             t.addMember(p)
    #             # try to geocode adress and add team to event if successfull
    #             if t.setAdress(row[4] + ", Muenster"):
    #                 rudi.addTeam(t)

    # create some random teams
    from numpy.random import normal
    for _ in range(81):
        t = Team()
        t.coords = (normal(), normal())
        rudi.addTeam(t)

    # find optimal routes
    rudi.organize()
    # save the routes to file
    rudi.savecsv("out.csv")
    print("Routelength:", rudi.routeslength())
    print("RMS:", rudi.rms_routes())
    rudi.plot()

    for team in rudi.teams:
        rudi.plot(teams=[team])


# If called directly: invoke main routine
if __name__ == "__main__":
    main()
