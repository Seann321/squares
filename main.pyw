import pygame
from random import randint
import easygui

pygame.init()

# Setting up the display
backgroundColor = (50, 50, 50)
screenWidth, screenHeight = 1000, 1100
screen = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption('Squares Player 1\'s turn. First to 90 tokens wins')
screen.fill(backgroundColor)

# Enable Random AI
randomAI = True

# Time Vars
FPS = 60
clock = pygame.time.Clock()
deltaTime = clock.tick(FPS)

# Player 1 and 2 logic
currentPlayer = 0
playerColorOptions = [['#2081c3', '#63d2ff', '#78d5d7', '#bed8d4'],  # Blue
                ['#14BD58', '#058c42', '#04471c', '#0d2818'],  # Green
                ['#E3C567', '#d9ae61', '#c8963e', '#573d1c'],  # Yellow
                ['#AD2831', '#A7171E', '#640D14', '#38040E']]  # Red

playerColors = []
for i in range(int(easygui.choicebox('How many players?', 'Player count', [2, 3, 4], 0))):
    playerColors.append(playerColorOptions[i])


# Defines what a GridSpace is and does
class GridSpace:
    def __init__(self, bounds):
        self.bounds = bounds
        self.tokens = 0
        self.playerController = -1

    def render(self):
        circlePOS = [(self.bounds[0] + self.bounds[3] / 3, self.bounds[1] + self.bounds[3] / 3),
                     (self.bounds[0] + (self.bounds[3] / 3) * 2, self.bounds[1] + self.bounds[3] / 3),
                     (self.bounds[0] + self.bounds[3] / 3, self.bounds[1] + self.bounds[3] / 1.5),
                     (self.bounds[0] + self.bounds[3] / 3 + self.bounds[3] / 3, self.bounds[1] + self.bounds[3] / 1.5)]
        if self.tokens == 0:
            if screenGrid.index(self) % 2:
                pygame.draw.rect(screen, (100, 100, 100), self.bounds)
            else:
                pygame.draw.rect(screen, (0, 0, 0), self.bounds)
        elif self.tokens < 5:
            for i in range(self.tokens):
                pygame.draw.circle(screen, playerColors[currentPlayer][i], circlePOS[i], self.bounds[3] / 4, 100)
        pygame.display.update(self.bounds)


# Initial ScoreBoard Graphics
font = pygame.font.Font('slkscr.ttf', 32)


# Scoreboard and current turn UI
def updateScoreBoardAndCurrentTurn():
    text = font.render(f"    Player {currentPlayer + 1}'s turn with {tokenCount(currentPlayer)} tokens    ", True, playerColors[currentPlayer][1], backgroundColor)
    textRect = text.get_rect()
    textRect.center = (500, 1050)
    screen.blit(text, textRect)
    pygame.display.update(textRect)


# Finds neighboring boxes returns a list
def findNearBoxes(space):
    neighboringBoxChecks = [pygame.Rect(space.bounds[0], space.bounds[1] + space.bounds[3], 1, 1),  # UP
                            pygame.Rect(space.bounds[0], space.bounds[1] - space.bounds[3], 1, 1),  # DOWN
                            pygame.Rect(space.bounds[0] - space.bounds[2], space.bounds[1], 1, 1),  # LEFT
                            pygame.Rect(space.bounds[0] + space.bounds[2], space.bounds[1], 1, 1)]  # RIGHT
    nB = []
    for i in range(len(screenGrid)):
        for checkBox in range(len(neighboringBoxChecks)):
            if screenGrid[i].bounds.colliderect(neighboringBoxChecks[checkBox]):
                nB.append(screenGrid[i])
    return nB


# Creates a Grid across the screen, must be odd number
gridSize = 9
screenGrid = []
gridWidth = int(screenWidth / gridSize)
gridHeight = int((screenHeight - 100) / gridSize)
for x in range(gridSize):
    for y in range(gridSize):
        screenGrid.append(GridSpace(pygame.Rect([(x * gridWidth), y * gridHeight, gridWidth, gridHeight])))
for grid in screenGrid:
    if screenGrid.index(grid) % 2:
        pygame.draw.rect(screen, (100, 100, 100), grid.bounds)
    else:
        pygame.draw.rect(screen, (0, 0, 0), grid.bounds)
pygame.display.flip()


# Domino effect with boxes
def spreadDots():
    while checkForOverflow():
        for i in range(len(screenGrid)):
            if screenGrid[i].tokens >= 5:
                screenGrid[i].playerController = -1
                screenGrid[i].tokens = 0
                screenGrid[i].render()
                nearBoxes = findNearBoxes(screenGrid[i])
                for nB in range(len(nearBoxes)):
                    nearBoxes[nB].playerController = currentPlayer
                    nearBoxes[nB].tokens += 1
                    nearBoxes[nB].render()


# Checks for any grid objects with over 5 tokens, if so returns true to the while loop
def checkForOverflow():
    for i in range(len(screenGrid)):
        if screenGrid[i].tokens >= 5:
            return True
    return False


# Checks to see if a player controller has 90+ tokens
def checkWinCondition():
    updateScoreBoardAndCurrentTurn()
    playerCounts = []
    for i in range(len(playerColors)):
        playerCounts.append(0)
    victoryCount = gridSize * 10
    for i in range(len(screenGrid)):
        if screenGrid[i].playerController != -1:
            playerCounts[screenGrid[i].playerController] += screenGrid[i].tokens
    for i in range(2):
        if playerCounts[i] > victoryCount:
            text = font.render(f"    Player {currentPlayer + 1}'s wins with {tokenCount(currentPlayer)} tokens!    ", True,
                               playerColors[currentPlayer][1], backgroundColor)
            textRect = text.get_rect()
            textRect.center = (500, 1050)
            screen.blit(text, textRect)
            pygame.display.update(textRect)


def tokenCount(player):
    playerCounts = []
    for i in range(len(playerColors)):
        playerCounts.append(0)
    for i in range(len(screenGrid)):
        if screenGrid[i].playerController != -1:
            playerCounts[screenGrid[i].playerController] += screenGrid[i].tokens
    return playerCounts[player]


# Initial ScoreBoard
updateScoreBoardAndCurrentTurn()
# Game Loop
running = True
while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # Check for left click
        if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            # Add and render new tokens
            for i in range(len(screenGrid)):
                if screenGrid[i].bounds.collidepoint(pos):
                    # Check if player can interact with space, if not return
                    if screenGrid[i].playerController == -1 or screenGrid[i].playerController == currentPlayer:
                        screenGrid[i].playerController = currentPlayer
                        screenGrid[i].tokens += 1
                        if screenGrid[i].tokens == 5:
                            spreadDots()
                        screenGrid[i].render()
                        # Switch to other player
                        if currentPlayer == len(playerColors)-1:
                            currentPlayer = 0
                        else:
                            currentPlayer += 1
                        pygame.display.set_caption(
                            f"Squares. Player {currentPlayer + 1}'s turn. First to 90 tokens wins")
                        checkWinCondition()
    # Enable Random AI
    if randomAI:
        if currentPlayer != 0:
            validMoves = []
            for i in range(len(screenGrid)):
                if screenGrid[i].playerController == -1 or screenGrid[i].playerController == currentPlayer:
                    validMoves.append(screenGrid[i])
            randomTile = validMoves[randint(0, len(validMoves) - 1)]
            randomTile.playerController = currentPlayer
            randomTile.tokens += 1
            if randomTile.tokens == 5:
                spreadDots()
            randomTile.render()
            if currentPlayer == len(playerColors) - 1:
                currentPlayer = 0
            else:
                currentPlayer += 1
            pygame.display.set_caption(
                f"Squares. Player {currentPlayer + 1}'s turn. First to 90 tokens wins")
            checkWinCondition()
