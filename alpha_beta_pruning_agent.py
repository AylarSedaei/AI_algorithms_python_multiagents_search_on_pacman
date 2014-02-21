class AlphaBetaAgent(MultiAgentSearchAgent):
    """
Your minimax agent with alpha-beta pruning (question 3)
"""

    def getAction(self, gameState):
      """
Returns the minimax action using self.depth and self.evaluationFunction
"""
      "*** YOUR CODE HERE ***"
      return self.value(gameState, 0, float("-inf"), float("inf"), self.depth-1)[1]

    def value(self, gameState, agentIndex, alpha, beta, depth):
      #terminate when it is a leaf node, i.e. when the game ends
      if gameState.isWin() or gameState.isLose():
        return (self.evaluationFunction(gameState), 'stop')
      #last ghost reached, time to decrease a depth
      elif agentIndex == gameState.getNumAgents():
        return self.value(gameState, 0, alpha, beta, depth - 1)
      elif agentIndex > 0: #agent is a ghost
        return self.minvalue(gameState,agentIndex, alpha, beta, depth)
      elif agentIndex == 0: #agent is pacman
        return self.maxvalue(gameState,agentIndex, alpha, beta, depth)
      else:
        print "ERROR"
        return 0

    def maxvalue(self, gameState, agentIndex, alpha, beta, depth):
      v = float("-inf")
      bestAction = 'stop'
      legalMoves = gameState.getLegalActions(agentIndex) # Collect legal moves and successor states
      for action in legalMoves:
        score = self.value(gameState.generateSuccessor(agentIndex, action), agentIndex+1, alpha, beta, depth)
        if score[0] > v:
          v = score[0]
          bestAction = action
          if v > beta:
            return (v, bestAction)
          alpha = max(v,alpha)
      return (v, bestAction)

    def minvalue(self, gameState, agentIndex, alpha, beta, depth):
      v = float("inf")
      bestAction = 'stop'
       #terminate when agent is the final ghost at depth 0
      if agentIndex == (gameState.getNumAgents() - 1) and depth == 0:
        legalMoves = gameState.getLegalActions(agentIndex) # Collect legal moves and successor states
        for action in legalMoves:
          score = (self.evaluationFunction(gameState.generateSuccessor(agentIndex, action)), action)
          if score[0] < v:
            bestAction = action
            v = score[0]
            if v < alpha:
              return (v, bestAction)
            beta = min(beta, v)
        return (v, bestAction)
      else: # keep on recursing
        legalMoves = gameState.getLegalActions(agentIndex) # Collect legal moves and successor states
        for action in legalMoves:
          score = self.value(gameState.generateSuccessor(agentIndex, action), agentIndex+1, alpha, beta, depth)
          if score[0] < v:
            v = score[0]
            bestAction = action
            if v < alpha:
              return (v, bestAction)
            beta = min(beta, v)
        return (v, bestAction)
