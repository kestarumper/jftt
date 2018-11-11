def finiteAutomatonMatcher(T, delta, pattern):
    occurences = []
    n = len(T)
    m = len(pattern)
    q = 0
    for i in range(n):
        symbol = T[i]
        q = delta[q][symbol]
        if(q == m):
            shift = i + 1 - m
            occurences.append(shift)
    return occurences

def computeTransitionFunction(P, sigma):
    m = len(P)
    delta = {}
    for q in range(m+1):
        delta[q] = {}
        for symbol in sigma:
            k = min(m, q+1)
            patternPq = P[:q]
            patternPq += symbol
            while(not patternPq.endswith(P[:k])):
                k = k - 1
            delta[q][symbol] = k
    return delta

def stringToAlphabet(str):
    return set(list(str))

def printOccurences(pattern, occs):
    print("Wzorzec {} występuje z przesunięciami: {}".format(pattern, occs))

ciag = "ąćąćąćąśśśćąćąćąćąćśśśćąćś"
slow = ['ć', 'ą', 'ś', '&']
testCases = [
    (ciag, "&", slow, []),
    (ciag, "&ś", slow, []),
    (ciag, "ąć", slow, []),
    (ciag, "ś", slow, []),
    (ciag, "śś", slow, []),
    (ciag, "ćąć", slow, []),
]

for case in testCases:
    (text, pattern, alphabet, expected) = case
    occurences = finiteAutomatonMatcher(text, computeTransitionFunction(pattern, alphabet), pattern)
    printOccurences(pattern, occurences)
    # assert occurences == expected, "given: {} != {}: expected".format(occurences, expected)

