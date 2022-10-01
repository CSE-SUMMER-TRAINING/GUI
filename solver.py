from college import Branch
from groups_input import group
from arabic_reshaper import reshape

mem, OO = dict(), int(1e18)
wrongForBuild, wrongForFloor, wrongForHall = int(1e6), int(1e3), 1
toPrint = []
uniqueGroups = set()

def dp(idx, msk, g, h)->int:
    if (idx == len(h)):
        if msk != ((1 << len(g)) - 1): return OO
        else: return 0
    
    if (idx, msk) in mem: return mem[(idx, msk)]

    mem[(idx, msk)] = OO

    for i in range(len(g)):
        if msk & (1 << i): continue
        sm, j, weight = h[idx].volume, idx + 1, 0
        while j < len(h) and sm < group[g[i]].volume:
            sm += h[j].volume
            if h[j].buildNum != h[j - 1].buildNum:
                weight += wrongForBuild
                j += 1
                continue
            if h[j].floorNum != h[j - 1].floorNum:
                weight += wrongForFloor
                j += 1
                continue
            weight += wrongForHall
            j += 1
        if sm < group[g[i]].volume: continue
        mem[(idx, msk)] = min(mem[(idx, msk)], weight + dp(j, msk | (1 << i), g, h), OO)
    
    mem[(idx, msk)] = min(mem[(idx, msk)], dp(idx + 1, msk, g, h), OO)
    
    return mem[(idx, msk)]


def buildDp(idx, msk, g, h)->None:
    if idx == len(h):
        for hall, gro, _from, to in toPrint:
            print(f"{reshape(hall)[::-1]}    {reshape(gro)[::-1]}    {_from}    {to}")
        print("\n\n==========================================================\n\n")
        return
    
    optimal = dp(idx, msk, g, h)

    for i in range(len(g)):
        if msk & (1 << i): continue
        sm, j, weight = h[idx].volume, idx + 1, 0
        while j < len(h) and sm < group[g[i]].volume:
            sm += h[j].volume
            if h[j].buildNum != h[j - 1].buildNum:
                weight += wrongForBuild
                j += 1
                continue
            if h[j].floorNum != h[j - 1].floorNum:
                weight += wrongForFloor
                j += 1
                continue
            weight += wrongForHall
            j += 1
        if sm < group[g[i]].volume: continue
        if (weight + dp(j, msk | (1 << i), g, h) == optimal):
            sm, j, initial = 0, idx, group[g[i]]._from
            while j < len(h) and sm < group[g[i]].volume:
                toPrint.append((h[j].name, group[g[i]].name, initial, min(initial + h[j].volume - 1, group[g[i]].to)))
                sm += h[j].volume
                initial += h[j].volume
                j += 1
            buildDp(j, msk | (1 << i), g, h)
            return
    
    toPrint.append((h[idx].name, 'فارغه', '       ---', '---'))
    buildDp(idx + 1, msk, g, h)
    return

def solve(branch :Branch)->None:
    
    groups = branch.groupsInBranch

    for i in range(1 << len(groups)):  
        iHave, g1, cnt = [], [], 0
        for j in range(len(groups)):
            iHave.append(j)
        for j in range(len(groups)):
            if i & (1 << j):
                g1.append(iHave[j - cnt])
                iHave.pop(j - cnt)
                cnt += 1
        
        for ii in range(1 << len(iHave)):
            g2, g3 = [], []
            for j in range(len(iHave)):
                if ii & (1 << j):
                    g2.append(iHave[j])
                else:
                    g3.append(iHave[j])
            
            mem.clear()
            if dp(0, 0, g1, branch.hallsInBranch) == OO: continue
            mem.clear()
            if dp(0, 0, g2, branch.hallsInBranch) == OO: continue
            mem.clear()
            if dp(0, 0, g3, branch.hallsInBranch) == OO: continue
            # mem.clear()
            # buildDp(0, 0, g1, branch.hallsInBranch)
            # mem.clear()
            # buildDp(0, 0, g2, branch.hallsInBranch)
            # mem.clear()
            # buildDp(0, 0, g3, branch.hallsInBranch)
            uniqueGroups.add(tuple(sorted([tuple(g1), tuple(g2), tuple(g3)])))

    # print(uniqueGroups)

