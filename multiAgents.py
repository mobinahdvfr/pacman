# multiAgents.py
# --------------
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
from math import inf

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
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices)  # Pick randomly among the best

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

        "*** YOUR CODE HERE ***"

        for ghost in successorGameState.getGhostPositions():
            if (manhattanDistance(newPos, ghost) < 2):
                return -inf
        closestFoodDist = inf
        for food in newFood.asList():
            closestFoodDist = min(closestFoodDist, manhattanDistance(newPos, food))
        if (closestFoodDist == inf):
            closestFoodDist = 0.5;
        scaredTimes = 0
        for scaredTime in newScaredTimes:
            scaredTimes += scaredTime
        return (successorGameState.getScore() - currentGameState.getScore()) + 1.0 / closestFoodDist + scaredTimes


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

    def __init__(self, evalFn='scoreEvaluationFunction', depth='2'):
        self.index = 0  # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)


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

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"

        def max_value(gameState,depth):
            Actions=gameState.getLegalActions(0)
            if len(Actions)==0 or depth==self.depth or gameState.isWin() or gameState.isLose():         #end state or we've done with the last depth
                return(self.evaluationFunction(gameState),None)
            v=-inf
            Act = None
            for action in Actions:
                sValue=min_value(gameState.generateSuccessor(0,action),1,depth)[0]
                if(sValue>v):
                    v,Act=sValue,action
            return(v,Act)

        def min_value(gameState,ghostNum,depth):
            Actions=gameState.getLegalActions(ghostNum)
            if len(Actions) == 0:                                #end of game
                return(self.evaluationFunction(gameState),None)
            v=inf
            Act = None
            for action in Actions:
                if(ghostNum==gameState.getNumAgents() -1):        #pacman's turn
                    sValue=max_value(gameState.generateSuccessor(ghostNum,action),depth + 1)[0]
                else:                                            #next ghost's turn
                    sValue=min_value(gameState.generateSuccessor(ghostNum,action),ghostNum+1,depth)[0]
                if(sValue<v):
                    v,Act=sValue,action
            return(v,Act)

        return max_value(gameState,0)[1]


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"

        def max_value(gameState, depth, a, b):
            Actions = gameState.getLegalActions(0)
            if len(Actions) == 0 or gameState.isWin() or gameState.isLose() or depth == self.depth:
                return (self.evaluationFunction(gameState), None)
            v = -inf
            for action in Actions:
                sValue = min_value(gameState.generateSuccessor(0, action), 1, depth, a, b)[0]
                if v < sValue:
                    v, Act = sValue, action
                if v > b:
                    return (v, Act)
                a = max(a, v)
            return (v, Act)

        def min_value(gameState, ghostNum, depth, a, b):
            Actions = gameState.getLegalActions(ghostNum)
            if len(Actions) == 0:
                return (self.evaluationFunction(gameState), None)
            v = inf
            for action in Actions:
                if (ghostNum == gameState.getNumAgents() - 1):
                    sValue = max_value(gameState.generateSuccessor(ghostNum, action), depth + 1, a, b)[0]
                else:
                    sValue = min_value(gameState.generateSuccessor(ghostNum, action), ghostNum + 1, depth, a, b)[0]
                if (sValue < v):
                    v, Act = sValue, action
                if (v < a):
                    return (v, Act)
                b = min(b, v)
            return (v, Act)

        return max_value(gameState, 0, -inf, inf)[1]


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

        def max_value(gameState, depth):
            Actions = gameState.getLegalActions(0)
            if len(Actions) == 0 or gameState.isWin() or gameState.isLose() or depth == self.depth:
                return (self.evaluationFunction(gameState), None)
            v = -inf
            Act = None
            for action in Actions:
                sValue = exp_value(gameState.generateSuccessor(0, action), 1, depth)[0]
                if (v < sValue):
                    v, Act = sValue, action
            return (v, Act)

        def exp_value(gameState, ghostNum, depth):
            Actions = gameState.getLegalActions(ghostNum)
            if len(Actions) == 0:
                return (self.evaluationFunction(gameState), None)
            v = 0
            for action in Actions:
                if (ghostNum == gameState.getNumAgents() - 1):
                    sValue = max_value(gameState.generateSuccessor(ghostNum, action), depth + 1)[0]
                else:
                    sValue = exp_value(gameState.generateSuccessor(ghostNum, action), ghostNum + 1, depth)[0]
                v += sValue / len(Actions)
            return (v, None)

        return max_value(gameState, 0)[1]


def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    position = currentGameState.getPacmanPosition()
    foods = currentGameState.getFood().asList()
    closestFoodDist = inf
    for food in foods:
        closestFoodDist = min(manhattanDistance(position, food), closestFoodDist)
    if (closestFoodDist == inf):
        closestFoodDist = 0.5
    score = currentGameState.getScore()

    return 1.0 / closestFoodDist + score

# Abbreviation
better = betterEvaluationFunction
