# valueIterationAgents.py
# -----------------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


import mdp, util

from learningAgents import ValueEstimationAgent

class ValueIterationAgent(ValueEstimationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A ValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100):
        """
          Your value iteration agent should take an mdp on
          construction, run the indicated number of iterations
          and then act according to the resulting policy.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state, action, nextState)
              mdp.isTerminal(state)
        """
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        self.values = util.Counter() # A Counter is a dict with default 0
        self.Value_Iteration()
        # Write value iteration code here
        "*** YOUR CODE HERE ***"

    
    def Value_Iteration(self):
        x = 0
        y = self.iterations
        
        while x < y:
            
            Value = util.Counter()
            
            for i in self.mdp.getStates():
        
                if self.mdp.isTerminal(i):
                    Value[i] = 0
                    
                else:
                
                    actions = self.mdp.getPossibleActions(i)
                    max_Value = -220203
                    
                    for j in actions:
                        
                        value = 0
                        trans_state_prob = self.mdp.getTransitionStatesAndProbs(i, j)
                        
                        for state_Prob in trans_state_prob:
                            c = state_Prob[0]
                            b = state_Prob[1]
                            value = value + b * (self.mdp.getReward(i, j, b) + self.discount * self.values[c])
                            
                        max_Value = max(max_Value, value)
                        
                    if max_Value != -220203:
                        Value[i] = max_Value
            self.values = Value
            x = x + 1
            
            
            
            
            
            

    def getValue(self, state):
        """
          Return the value of the state (computed in __init__).
        """
        return self.values[state]
    
    
    
    
    
    
    


    def computeQValueFromValues(self, state, action):
        """
          Compute the Q-value of action in state from the
          value function stored in self.values.
        """
        "*** YOUR CODE HERE ***"
        q_Value = 0
        
        for state_Prob in self.mdp.getTransitionStatesAndProbs(state, action):
            a = state_Prob[0]
            b = state_Prob[1]
            c = self.mdp.getReward(state, action, b)
            q_Value = q_Value + b * (c + self.discount * self.values[a])
            
        return q_Value
    
    
    
    
    

    def computeActionFromValues(self, state):
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.

          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
        "*** YOUR CODE HERE ***"
        if self.mdp.isTerminal(state):
            return None

        Actions = dict()
        actions = self.mdp.getPossibleActions(state)
        for action in actions:
            Actions[action] = self.computeQValueFromValues(state, action)

        return max(Actions, key=Actions.get)
    
    
    
    
    
    

    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)
