import arabic_reshaper
from data_input import  branch_index, branch

group = []

class Group:
    def __init__(self, d, v, f, t, brn, s):
        self.id = d
        self.volume = v
        self._from = f
        self.to = t
        self.branchNum = brn
        self.name = s
def read_sheet(excelSheet, num_of_branches):
    global sheet
    sheet = excelSheet.parse(excelSheet.sheet_names[num_of_branches])

def get_and_store_groups():
    for index, rows in sheet.iterrows():
            g = rows.values.tolist()
            g[2] = int(g[2])
            g[3] = int(g[3])
            g[4] = int(g[4])
            # g[0] = arabic_reshaper.reshape(g[0])[::-1]
            g[1] = arabic_reshaper.reshape(g[1])[::-1]
            brn = branch_index[g[1]]
            branch[brn].groupsInBranch.append(len(group))
            group.append(Group(len(group), g[2], g[3], g[4], brn, g[0]))