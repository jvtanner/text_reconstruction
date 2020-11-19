import shell
import util
import wordsegUtil

############################################################
# Problem 1b: Solve the segmentation problem under a unigram model

class SegmentationProblem(util.SearchProblem):
    def __init__(self, query, unigramCost):
        self.query = query
        self.unigramCost = unigramCost

    def startState(self):
        # BEGIN_YOUR_CODE (our solution is 1 line of code, but don't worry if you deviate from this)
        return self.query
        # END_YOUR_CODE

    def isEnd(self, state):
        # BEGIN_YOUR_CODE (our solution is 2 lines of code, but don't worry if you deviate from this)
        if state == '':
            return True
        # END_YOUR_CODE

    def succAndCost(self, state):
        # BEGIN_YOUR_CODE (our solution is 7 lines of code, but don't worry if you deviate from this)
        prediction = []
        succ_state_pos = len(state) + 1
        for x in range(succ_state_pos):
            former = state[:x]
            latter = state[x:]
            cost = self.unigramCost(state[0:x])
            prediction.append((former, latter, cost))
        return prediction
        # END_YOUR_CODE

def segmentWords(query, unigramCost):
    if len(query) == 0:
        return ''

    ucs = util.UniformCostSearch(verbose=0)
    ucs.solve(SegmentationProblem(query, unigramCost))

    # BEGIN_YOUR_CODE (our solution is 3 lines of code, but don't worry if you deviate from this)
    if len(ucs.actions) > 0:
        return ' '.join(ucs.actions)
    else:
        return ''
    # END_YOUR_CODE

############################################################
# Problem 2b: Solve the vowel insertion problem under a bigram cost

class VowelInsertionProblem(util.SearchProblem):
    def __init__(self, queryWords, bigramCost, possibleFills):
        self.queryWords = queryWords
        self.bigramCost = bigramCost
        self.possibleFills = possibleFills

    def startState(self):
        # BEGIN_YOUR_CODE (our solution is 1 line of code, but don't worry if you deviate from this)
        return 0, wordsegUtil.SENTENCE_BEGIN
        # END_YOUR_CODE

    def isEnd(self, state):
        # BEGIN_YOUR_CODE (our solution is 2 lines of code, but don't worry if you deviate from this)
        if state[0] == len(self.queryWords):
            return True
        # END_YOUR_CODE

    def succAndCost(self, state):
        # BEGIN_YOUR_CODE (our solution is 8 lines of code, but don't worry if you deviate from this)
        prediction = []
        start = self.queryWords[state[0]]
        future = self.possibleFills(start)
        if len(future) == 0:
            future.add(start)

        prediction += [(word, (state[0] + 1, word), self.bigramCost(state[1], word)) for word in future if state[0] < len(self.queryWords)]

        return prediction
        # END_YOUR_CODE

def insertVowels(queryWords, bigramCost, possibleFills):
    # BEGIN_YOUR_CODE (our solution is 3 lines of code, but don't worry if you deviate from this)
    # Same as previously
    if len(queryWords) == 0:
        return ''

    ucs = util.UniformCostSearch(verbose=0)
    ucs.solve(VowelInsertionProblem(queryWords, bigramCost, possibleFills))
    if len(ucs.actions) > 0:
        return ' '.join(ucs.actions)
    else:
        return ''
    # END_YOUR_CODE

############################################################
# Problem 3b: Solve the joint segmentation-and-insertion problem

class JointSegmentationInsertionProblem(util.SearchProblem):
    def __init__(self, query, bigramCost, possibleFills):
        self.query = query
        self.bigramCost = bigramCost
        self.possibleFills = possibleFills

    def startState(self):
        # BEGIN_YOUR_CODE (our solution is 1 line of code, but don't worry if you deviate from this)
        return 0, wordsegUtil.SENTENCE_BEGIN
        # END_YOUR_CODE

    def isEnd(self, state):
        # BEGIN_YOUR_CODE (our solution is 2 lines of code, but don't worry if you deviate from this)
        if state[0] == len(self.query):
            return True
        # END_YOUR_CODE

    def succAndCost(self, state):
        # BEGIN_YOUR_CODE (our solution is 14 lines of code, but don't worry if you deviate from this)
        prediction = []
        first = state[1]

        for x in range(state[0], len(self.query) + 1):
            next_words = self.possibleFills(self.query[state[0]:x])
            prediction += [(word, (x, word), self.bigramCost(first, word)) for word in next_words]

        return prediction
        # END_YOUR_CODE

def segmentAndInsert(query, bigramCost, possibleFills):
    if len(query) == 0:
        return ''

    # BEGIN_YOUR_CODE (our solution is 4 lines of code, but don't worry if you deviate from this)
    ucs = util.UniformCostSearch(verbose=0)
    ucs.solve(JointSegmentationInsertionProblem(query, bigramCost, possibleFills))

    if len(ucs.actions) > 0:
        # print 'Problem 3-b: ', ' '.join(ucs.actions)
        return ' '.join(ucs.actions)
    else:
        return ''
    # END_YOUR_CODE

############################################################

if __name__ == '__main__':
    shell.main()
