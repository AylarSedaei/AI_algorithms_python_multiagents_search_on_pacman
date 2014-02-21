# multiAgents.py
# --------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
  """
	A reflex agent chooses an action at each choice point by examining
	its alternatives via a state evaluation function.

	The code below is provided as a guide.  You are welcome to change
	it in any way you see fit, so long as you don't touch our method
	headers.
  """


  def getAction(self, gameState):
	"""
	You do not need to change this method, but you're welcome to.

	getAction chooses among the best options according to the evaluation function.

	Just like in the previous project, getAction takes a GameState and returns
	some Directions.X for some X in the set {North, South, West, East, Stop}
	"""
	# Collect legal moves and successor states
	legalMoves = gameState.getLegalActions()

	# Choose one of the best actions
	scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
	bestScore = max(scores)
	bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
	chosenIndex = random.choice(bestIndices) # Pick randomly among the best

	"Add more of your code here if you want to"

	return legalMoves[chosenIndex]

  def evaluationFunction(self, currentGameState, action):
	"""
	Design a better evaluation function here.

	The evaluation function takes in the current and proposed successor
	GameStates (pacman.py) and returns a number, where higher numbers are better.

	The code below extracts some useful information from the state, like the
	remaining food (newFood) and Pacman position after moving (newPos).
	newScaredTimes holds the number of moves that each ghost will remain
	scared because of Pacman having eaten a power pellet.

	Print out these variables to see what you're getting, then combine them
	to create a masterful evaluation function.
	"""
	# Useful information you can extract from a GameState (pacman.py)
	successorGameState = currentGameState.generatePacmanSuccessor(action)
	newPos = successorGameState.getPacmanPosition()
	newFood = successorGameState.getFood()
	newGhostStates = successorGameState.getGhostStates()
	newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

	foodDist = float('inf')
	for food in newFood.asList():
		dist = manhattanDistance(food, newPos)
		if(dist < foodDist):
			foodDist = dist
		
	ghostScore = 0
	for state in newGhostStates:
		dist = manhattanDistance(newPos, state.getPosition())
		if dist == 0 and state.scaredTimer > 0:
			ghostScore += 100000000000
		elif state.scaredTimer > 0 and dist < state.scaredTimer:
			ghostScore += (1 / (1 + dist))
		elif dist < 3:
			ghostScore -= dist / 100;
	
	score = 3.0 / (1 + len(newFood.asList())) + ghostScore + 1.0 / (100 + foodDist)
	
	return score;

def scoreEvaluationFunction(currentGameState):
  """
	This default evaluation function just returns the score of the state.
	The score is the same one displayed in the Pacman GUI.

	This evaluation function is meant for use with adversarial search agents
	(not reflex agents).
  """
  return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
  """
	This class provides some common elements to all of your
	multi-agent searchers.  Any methods defined here will be available
	to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

	You *do not* need to make any changes here, but you can if you want to
	add functionality to all your adversarial search agents.  Please do not
	remove anything, however.

	Note: this is an abstract class: one that should not be instantiated.  It's
	only partially specified, and designed to be extended.  Agent (game.py)
	is another abstract class.
  """

  def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
	self.index = 0 # Pacman is always agent index 0
	self.evaluationFunction = util.lookup(evalFn, globals())
	self.depth = int(depth)
	self.moves = 0
	self.tf = False

class MinimaxAgent(MultiAgentSearchAgent):
  """
	Your minimax agent (question 2)
  """

  def getAction(self, gameState):
	"""
	  Returns the minimax action from the current gameState using self.depth
	  and self.evaluationFunction.

	  Here are some method calls that might be useful when implementing minimax.

	  gameState.getLegalActions(agentIndex):
		Returns a list of legal actions for an agent
		agentIndex=0 means Pacman, ghosts are >= 1

	  Directions.STOP:
		The stop direction, which is always legal

	  gameState.generateSuccessor(agentIndex, action):
		Returns the successor game state after an agent takes an action

	  gameState.getNumAgents():
		Returns the total number of agents in the game
	"""
	"*** YOUR CODE HERE ***"
	v = float('-inf')
	nextAction = Directions.STOP
	for action in gameState.getLegalActions(0):
		temp = self.minValue(0, 1, gameState.generateSuccessor(0, action))
		if temp > v and action != Directions.STOP:
			v = temp
			nextAction = action

	return nextAction
		

  def maxValue(self, depth, agent, state):
		if depth == self.depth:
			return self.evaluationFunction(state)
		else:
			actions = state.getLegalActions(agent)
			if len(actions) > 0:
				v = float('-inf')
			else:
				v = self.evaluationFunction(state)
			for action in actions:
				s = self.minValue(depth, agent+1, state.generateSuccessor(agent, action))
				if s > v:
					v = s
			return v

  def minValue(self, depth, agent, state):
		if depth == self.depth:
			return self.evaluationFunction(state)
		else:
			actions = state.getLegalActions(agent)
			if len(actions) > 0:
				v = float('inf')
			else:
				v = self.evaluationFunction(state)

			for action in actions:
				if agent == state.getNumAgents() - 1:
					s = self.maxValue(depth+1, 0, state.generateSuccessor(agent, action))
					if s < v:
						v = s
				else:
					s = self.minValue(depth, agent+1, state.generateSuccessor(agent, action))
					if s < v:
						v = s
			return v
		

class AlphaBetaAgent(MultiAgentSearchAgent):
  """
	Your minimax agent with alpha-beta pruning (question 3)
  """

  def getAction(self, gameState):
	"""
	  Returns the minimax action using self.depth and self.evaluationFunction
	"""
	"*** YOUR CODE HERE ***"
	v = float('-inf')
	nextAction = Directions.STOP
	for action in gameState.getLegalActions(0):
		temp = self.minValue(0, 1, gameState.generateSuccessor(0, action), float('-inf'), float('inf'))
		if temp > v and action != Directions.STOP:
			v = temp
			nextAction = action
	
	return nextAction
		

  def maxValue(self, depth, agent, state, alpha, beta):
		if depth == self.depth:
			return self.evaluationFunction(state)
		else:
			actions = state.getLegalActions(agent)
			if len(actions) > 0:
				v = float('-inf')
			else:
				v = self.evaluationFunction(state)
			
			for action in actions:
				v = max(v, self.minValue(depth, agent+1, state.generateSuccessor(agent, action), alpha, beta))
				if v >= beta:
					return v
				alpha = max(v, alpha)
			return v

  def minValue(self, depth, agent, state, alpha, beta):
		if depth == self.depth:
			return self.evaluationFunction(state)
		else:
			actions = state.getLegalActions(agent)
			if len(actions) > 0:
				v = float('inf')
			else:
				v = self.evaluationFunction(state)
				
			for action in actions:
				if agent == state.getNumAgents() - 1:
					v = min(v, self.maxValue(depth+1, 0, state.generateSuccessor(agent, action), alpha, beta))
					if v <= alpha:
						return v
					beta = min(v, beta)
				else:
					v = min(v, self.minValue(depth, agent+1, state.generateSuccessor(agent, action), alpha, beta))
					if v <= alpha:
						return v
					beta = min(v, beta)
			return v

class ExpectimaxAgent(MultiAgentSearchAgent):
  """
	Your expectimax agent (question 4)
  """

  def getAction(self, gameState):
	"""
	  Returns the expectimax action using self.depth and self.evaluationFunction

	  All ghosts should be modeled as choosing uniformly at random from their
	  legal moves.
	"""
	"*** YOUR CODE HERE ***"
	v = float('-inf')
	nextAction = Directions.STOP
	for action in gameState.getLegalActions(0):
		temp = self.expValue(0, 1, gameState.generateSuccessor(0, action))
		if temp > v and action != Directions.STOP:
			v = temp
			nextAction = action
	
	return nextAction
		

  def maxValue(self, depth, agent, state):
		if depth == self.depth:
			return self.evaluationFunction(state)
		else:
			actions = state.getLegalActions(agent)
			if len(actions) > 0:
				v = float('-inf')
			else:
				v = self.evaluationFunction(state)
			for action in state.getLegalActions(agent):
				v = max(v, self.expValue(depth, agent+1, state.generateSuccessor(agent, action)))
					
			return v

  def expValue(self, depth, agent, state):
		if depth == self.depth:
			return self.evaluationFunction(state)
		else:
			v = 0;
			actions = state.getLegalActions(agent)
			for action in actions:
				if agent == state.getNumAgents() - 1:
					v += self.maxValue(depth+1, 0, state.generateSuccessor(agent, action))
				else:
					v += self.expValue(depth, agent+1, state.generateSuccessor(agent, action))
			if len(actions) != 0:
				return v / len(actions)
			else:
				return self.evaluationFunction(state)

def betterEvaluationFunction(currentGameState):
 	"""
	Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
	evaluation function (question 5).

	DESCRIPTION: <write something here so we know what you did>
  	"""
  	"*** YOUR CODE HERE ***"
	newPos = currentGameState.getPacmanPosition()
	newFood = currentGameState.getFood()
	newGhostStates = currentGameState.getGhostStates()
	newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

	foodDist = 0
	for food in newFood.asList():
		dist = manhattanDistance(food, newPos)
		#print ('dist', dist)
		foodDist += dist
	
	score = 0
	if len(newFood.asList()) == 0:
		score = 1000000000
	
	ghostScore = 0
	if newScaredTimes[0] > 0:
			 ghostScore += 100.0
	for state in newGhostStates:
		dist = manhattanDistance(newPos, state.getPosition())
		if state.scaredTimer == 0 and dist < 3:
			ghostScore -= 1.0 / (3.0 - dist);
		elif state.scaredTimer < dist:
			ghostScore += 1.0 / (dist)
	
	score += 1.0 / (1 + len(newFood.asList())) + 1.0 / (1 + foodDist) + ghostScore + currentGameState.getScore()
	
	return score;

# Abbreviation
better = betterEvaluationFunction
