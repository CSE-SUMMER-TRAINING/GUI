from data_input import *

class Hall:
    def __init__(self, brn, bn, fn, v, s):
        self.branchNum = brn
        self.buildNum = bn
        self.floorNum = fn
        self.volume = v
        self.name = s

class Floor:
    def __init__(self, brn, bn, fn, noh):
        self.branchNum = brn
        self.buildNum = bn
        self.floorNum = fn
        self.numOfHalls = noh
        self.hallsInFloor = []
        self.getHalls()
        self.volume = sum(hall.volume for hall in self.hallsInFloor)

    def getHalls(self):
        for hall in name_and_volume_of_halls[self.branchNum][self.buildNum][self.floorNum]:
            self.hallsInFloor.append(Hall(self.branchNum, self.buildNum, self.floorNum, hall[1], hall[0]))

class Build:
    def __init__(self, brn, bn, nof):
        self.branchNum = brn
        self.buildNum = bn
        self.numOfFloors = nof
        self.floorsInBuild = []
        self.getFloors()
        self.volume = sum(floor.volume for floor in self.floorsInBuild)

    def getFloors(self):
        for i in range(self.numOfFloors): 
            self.floorsInBuild.append(Floor(self.branchNum, self.buildNum, i, len(name_and_volume_of_halls[self.branchNum][self.buildNum][i])))

class Branch:
    def __init__(self, s, brn, nob):
        self.name = s
        self.branchNum = brn
        self.numOfBuilds = nob
        self.buildsInBranch :list[Build]= []
        self.hallsInBranch = []
        self.groupsInBranch = []
        self.getBuilds()
        self.volume = sum(build.volume for build in self.buildsInBranch)

    def getBuilds(self):
        for i in range(self.numOfBuilds):
            self.buildsInBranch.append(Build(self.branchNum, i, num_of_floors[self.branchNum][i]))
            for floor in self.buildsInBranch[-1].floorsInBuild:
                for hall in floor.hallsInFloor:
                    self.hallsInBranch.append(hall)