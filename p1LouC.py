#!/Library/Frameworks/Python.framework/Versions/3.6/bin/python3.6


import sys
import random

# iterative deepening by 8 in late game
# with legal moves, return stuff that need to be flipped
class Strategy():
    def best_strategy(self, board, player, best_move, still_running):
        # depth = 1
        constraints = createConstraints()
        if player == "@":
            enemy = "o"
            player = "x"
        else: enemy = "x"
        board = "".join(board).replace("?","").replace("@","x")
        poss = findPlaces(board, constraints, enemy, player)
        best_move.value = self.my_search_strategy(board, player, enemy, poss, constraints, True)
        best_move.value = self.my_search_strategy(board, player, enemy, poss, constraints, False)

    def my_search_strategy(self, board, player, enemy, poss, constraints, isHer):
        if isHer:
            pick = pickMove(board, poss, constraints, player,
                            {0: {1, 8, 9}, 7: {6, 14, 15}, 56: {48, 49, 57}, 63: {54, 55, 62}},
                            {*range(8), *range(0, 57, 8), *range(7, 64, 8), *range(56, 64)})
        else:
            improvable, hardBound = -64, 64
            pick = negamaxTerminal(board, player, enemy, constraints, improvable, hardBound)
        return 11 + (pick // 8) * 10 + (pick % 8)


def printBoard(board):
    print("\n".join([board[i: i + 8] for i in range(0, len(board), 8)]))


def createConstraints():
    constraints = {spot: [] for spot in range(64)}
    for row in range(0, 64, 8):
        sr = [i for i in range(row, row + 8)]
        for ir in range(row, row + 8):
            constraints[ir].append(sr)
    for col in range(8):
        sc = [j for j in range(col, col + 64, 8)]
        for ic in range(col, col + 64, 8):
            constraints[ic].append(sc)
    for s1 in range(8):
        s1s = [abs(i - s1) * 8 + i for i in range(s1 + 1)]
        for i1d in s1s:
            constraints[i1d].append(s1s)
    for sub1 in range(8, 15):
        sub1s = [(sub1 - i) * 8 + i for i in range(sub1 - 7, 8)]
        for isub1 in sub1s:
            constraints[isub1].append(sub1s)
    for s2 in range(7, -1, -1):
        s2s = [(j - s2) * 8 + j for j in range(s2, 8)]
        for is2s in s2s:
            constraints[is2s].append(s2s)
    for sub2 in range(1, 8):
        sub2s = [(k + sub2) * 8 + k for k in range(8 - sub2)]
        for isub2 in sub2s:
            constraints[isub2].append(sub2s)
    return constraints


def testIndexEdge(board, index, constraints, char):
    allCons = list()
    for con in constraints[index]:
        f = con.index(index)
        l = list()
        l.append(con[:f][::-1])
        l.append(con[f + 1:])
        for c in l:
            aSet = set()
            first = ""
            for i in range(len(c)):
                if board[c[i]] != ".":
                    if first == "": first = board[c[i]]
                    aSet.add(board[c[i]])
                if board[c[i]] == "." or i == len(c) - 1:
                    if len(aSet) == 2:
                        if first.lower() != char.lower():
                            allCons.append(c[:i + 1])
                            break
                    break
    return allCons


def findPlaces(board, constraints, findChar, char):
    poss = set()
    for p in range(len(board)):
        if board[p].lower() == findChar.lower():
            if p <= 55: poss.add(p + 8)
            if p >= 8: poss.add(p - 8)
            if p < 63: poss.add(p + 1)
            if p > 0: poss.add(p - 1)
            if p >= 9: poss.add(p - 8 - 1)
            if p < 55: poss.add(p + 8 + 1)
            if p >= 7: poss.add(p - 8 + 1)
            if p < 57: poss.add(p + 8 - 1)
    # newPoss = set()
    # for ele in poss:
    #     if board[ele] == ".": newPoss.add(ele)
    # poss = set()
    # for index in newPoss:
    #     file = testIndex(board, index, constraints, char)
    #     if file: poss.add(index)
    newPoss = dict()
    for ele in poss:
        if board[ele] == ".":
            file = testIndex(board, ele, constraints, char)
            if file: newPoss[ele] = file
    return newPoss


def testIndex(board, index, constraints, char):
    allCons = list()
    for con in constraints[index]:
        f = con.index(index)
        l = list()
        l.append(con[:f][::-1])
        l.append(con[f + 1:])
        for c in l:
            aSet, count, first = set(), 0, ""
            for i in c:
                if board[i] != ".":
                    if first == "": first = board[i]
                    aSet.add(board[i])
                if len(aSet) == 2:
                    if first.lower() != char.lower():
                        allCons.append(c[:count])
                        break
                if board[i] == ".": break
                count += 1
    return allCons


def findChar(board):
    l = [1 for char in board if char == "."]
    if len(l) % 2 == 0:
        if "x" in board: return "x"
        else: return "X"
    else:
        if "o" in board: return "o"
        else: return "O"


def pickMove(board, poss, constraints, char, cx, edgecon):
    A, B, C, D = True, True, True, True
    if A == True:
        cor = findCorners(poss)
        if cor: return random.choice([*cor])
    if B == True:
        p = playEdge(board, poss, char, constraints, edgecon)
        if p: return random.choice([*p])
    if C == True:
        cposs = noCX(board, poss, char, cx)
        if D == True:
            nposs = noEdge(cposs)
            if nposs: return random.choice([*nposs])
        if cposs: return random.choice([*cposs])
    if D == True:
        nposs = noEdge(poss)
        if nposs: return random.choice([*nposs])
    return random.choice([*poss])


def findCorners(poss):
    cor = set()
    for i in poss:
        if i in [0, 7, 56, 63]: cor.add(i)
    return cor


def playEdge(board, p, char, constraints, edgecon):
    edges = set()
    for i in p:
        if i in edgecon:
            l = testIndexEdge(board, i, constraints, char)
            for c in [0, 7, 56, 63]:
                if board[c] == char:
                    for al in l:
                        if c in al: edges.add(i)
    return edges



def noCX(board, poss, char, cx):
    good = set(poss)
    for cor in cx:
        if board[cor] == char: continue
        for i in poss:
            if i in cx[cor]: good.remove(i)
    return good


def noEdge(poss):
    good = set(poss)
    for i in poss:
        if i in {0, 1, 2, 3, 4, 5, 6, 7, 8, 16, 24, 32, 40, 48, 56, 15, 23, 31, 39, 47, 55, 63, 57, 58, 59, 60, 61, 62}: good.remove(i)
    return good


def createNewPoss(bad, poss):
    newPoss = set()
    for i in poss:
        if i not in bad: newPoss.add(i)
    return newPoss


def createEdges():
    return {0: {[*range(1, 8)], [range(8, 57, 8)]}, 7: {[*range(1, 7)], [*range(15, 64, 8)]}, 56: {[*range(8, 56, 8)], [*range(57, 64)]}, 63: {[*range(57, 63)], [*range(15, 63, 8)]}}


def fillPlace(board, place, constrs, theChar):
    board = board[:place] + theChar + board[place + 1:]
    for l in constrs:
        for i in l:
            if i == theChar: break
            else: board = board[:i] + theChar + board[i + 1:]
    return board


def evalBoard(board, token, enemytoken):
    return len([1 for c in board if c == token]) - len([1 for c in board if c == enemytoken])


def negamaxTerminal(board, token, enemytoken, constraints, improvable, hardBound):
    lm = findPlaces(board, constraints, enemytoken, token)
    if not lm:
        elm = findPlaces(board, constraints, token, enemytoken)
        if not elm: return [evalBoard(board, token, enemytoken)]
        nm = negamaxTerminal(board, enemytoken, token, constraints, -hardBound, -improvable) + [-1]
        return [-nm[0]] + nm[1:]
    best = []
    newHB = -improvable
    for mv in lm:
        nm = negamaxTerminal(fillPlace(board, mv, lm[mv], token), enemytoken, token, constraints, -hardBound, newHB) + [mv]
        if not best or nm[0] < newHB:
            best = nm
            if nm[0] < newHB:
                newHB = nm[0]
                if -newHB >= hardBound: return [-best[0]] + best[1:]
    return [-best[0]] + best[1:]


def main():
    board, player = sys.argv[1:3]
    printBoard(board)
    print("board:", board, "char:", player, "\n")
    constraints = createConstraints()
    if player.lower() == "x":
        if "o" in board:
            enemy = "o"
            player = "x"
        else:
            player = "X"
            enemy = "O"
    else:
        if "x" in board:
            player = "o"
            enemy = "x"
        else:
            player = "O"
            enemy = "X"
    poss = findPlaces(board, constraints, enemy, player)
    print("Possible Moves:", poss.keys())
    if poss:
        pick = pickMove(board, poss, constraints, player,
                        {0: {1, 8, 9}, 7: {6, 14, 15}, 56: {48, 49, 57}, 63: {54, 55, 62}},
                        {*range(8), *range(0, 57, 8), *range(7, 64, 8), *range(56, 64)})
        print("My heuristic choice is {}".format(pick))
    else: print("No possible moves")
    improvable, hardBound = -64, 64
    pick = negamaxTerminal(board, player, enemy, constraints, improvable, hardBound)
    print("Negamax Score: {} and Sequence (with final move as first move): {}".format(pick[0], pick))


if __name__ == "__main__":
    main()