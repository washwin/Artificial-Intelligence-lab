import random
import util

class QLearningAgent():
    def init(self, alpha=0.5, epsilon=0.1, gamma=0.9):
        self.alpha = alpha  # learning rate
        self.epsilon = epsilon  # exploration rate
        self.gamma = gamma  # discount factor
        self.QValues = util.Counter()  # dictionary to store Q-values

    def getQValue(self, state, action):
        return self.QValues[(state, action)]

    def computeValueFromQValues(self, state):
        actions = self.getLegalActions(state)
        if not actions:
            return 0.0
        return max([self.getQValue(state, action) for action in actions])

    def computeActionFromQValues(self, state):
        actions = self.getLegalActions(state)
        if not actions:
            return None
        maxQ = max([self.getQValue(state, action) for action in actions])
        bestActions = [action for action in actions if self.getQValue(state, action) == maxQ]
        return random.choice(bestActions)

    def getLegalActions(self, state):
        return self.actionFn(state)

    def update(self, state, action, nextState, reward):
        sample = reward + self.gamma * self.computeValueFromQValues(nextState)
        self.QValues[(state, action)] = (1 - self.alpha) * self.getQValue(state, action) + self.alpha * sample