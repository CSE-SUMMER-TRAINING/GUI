import pandas as pd
from arabic_reshaper import *

branch_name = dict()
branch_index = dict()
branch = []
name_and_volume_of_halls = []
num_of_floors = []
num_of_builds = []


def read_inputt(filename):

    excelSheet = pd.ExcelFile(filename)
    allBranches = excelSheet.sheet_names
    allBranches.pop()

    for i in range(len(allBranches)):

        if (not (allBranches[i][0] >= 'A' and allBranches[i][0] <= 'z')):
            allBranches[i] = reshape(allBranches[i])[::-1]
        branch_name[i] = allBranches[i]
        branch_index[allBranches[i]] = i

    num_of_branches = len(allBranches)

    for i in range(num_of_branches):
        name_and_volume_of_halls.append([])
        num_of_floors.append([])
        num_of_builds.append(0)
        sheet = excelSheet.parse(excelSheet.sheet_names[i])
        for index, rows in sheet.iterrows():
            hall = rows.values.tolist()
            hall[1] = int(hall[1])
            hall[2] = int(hall[2])
            hall[3] = int(hall[3])
            while len(name_and_volume_of_halls[i]) <= hall[2]:
                name_and_volume_of_halls[i].append([])
                num_of_floors[i].append(0)
            while len(name_and_volume_of_halls[i][hall[2]]) <= hall[3]:
                name_and_volume_of_halls[i][hall[2]].append([])
            name_and_volume_of_halls[i][hall[2]
                                        ][hall[3]].append((hall[0], hall[1]))
            num_of_builds[i] = max(num_of_builds[i], hall[2] + 1)
            num_of_floors[i][hall[2]] = max(
                num_of_floors[i][hall[2]], hall[3] + 1)
    return (excelSheet, num_of_branches, allBranches)
