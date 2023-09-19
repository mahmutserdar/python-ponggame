from graphics import *

import random

WIDTH = 300
HEIGHT = 600

MARGIN = 10
MOVEINCREMENT = 15
BOUNCE_WAIT = 1200

BALLRADIUS = 15
BALL_COUNT = 1
BALL_SPEED_MAX = 20
BALL_SPEED_MIN = 2

LIVES = 2


class ColliderBox:
    def __init__(self, x, y, width, height):
        self.x = int(x)
        self.y = int(y)
        self.width = width
        self.height = height

    def collided(self, collider):
        if self.x < collider.x + collider.width and\
                self.x + self.width > collider.x and\
                self.y < collider.y + collider.height and\
                self.y + self.height > collider.y:
            return True
        return False


class Timer:
    def __init__(self):
        self.value = 0


class Paddle:
    def __init__(self, color, width, height, coordx, screen):
        self.color = color
        self.width = width
        self.height = height
        self.shape = Rectangle(Point(coordx - int(self.width / 2), screen.getHeight() - MARGIN - self.height),
                               Point(coordx + int(self.width / 2), screen.getHeight() - MARGIN))
        self.coordx = coordx
        self.x = self.shape.p1.x
        self.y = self.shape.p1.y
        self.shape.setFill(self.color)
        self.shape.draw(screen)
        self.collider = ColliderBox(self.x, self.y, self.width, self.height)


    def update_collider(self):
        self.collider = ColliderBox(self.x, self.y, self.width, self.height)


    def move_left(self):
        if self.x > 0:
            self.x -= MOVEINCREMENT
            self.shape.move(-MOVEINCREMENT, 0)


    def move_right(self):
        if self.x < WIDTH-self.width:
            self.x += MOVEINCREMENT
            self.shape.move(MOVEINCREMENT, 0)


class Bubbles:
    def __init__(self, screen, x_index, y_index):
        self.screen = screen
        self.radius = 30

        self.x_index = x_index
        self.y_index = y_index
        self.x = self.radius*2*self.x_index+self.radius
        self.y = self.radius*2*self.y_index+self.radius

        self.color = ["Purple", "Blue", "Pink"]


    def draw_bubble(self):
        self.shape = Circle(Point(self.x, self.y), self.radius)
        self.shape.setFill(self.color[self.y_index])
        self.shape.draw(self.screen)
        self.collider_x = self.shape.p1.x
        self.collider_y = self.shape.p1.y
        self.collider = ColliderBox(self.collider_x, self.collider_y, self.radius*2, self.radius*2)


class Ball:
    def __init__(self, coordx, coordy, color, radius, x_direction, speed, screen):
        self.shape = Circle(Point(coordx, coordy), radius)
        self.coordx = coordx
        self.coordy = coordy
        self.x = coordx
        self.y = coordy
        self.xMovement = 0
        self.yMovement = 0
        self.color = color
        self.screendow = screen
        self.shape.setFill(self.color)
        self.shape.draw(self.screendow)
        self.radius = radius
        self.timer = 0
        self.x_direction = x_direction
        self.speed = speed
        self.collider = ColliderBox(self.x, self.y, self.radius*2, self.radius*2)

    def is_moving(self):
        return True if self.xMovement != 0 and self.yMovement != 0 else False

    def is_edge(self):
        if self.x <= 0:
            return "Left"
        if self.x >= WIDTH-self.radius*2:
            return "Right"
        if self.y <= 0:
            return "Up"

    def bounce(self, gameTimer, minX, maxX, maxY, paddle, bubbles):
        global LIVES

        if gameTimer >= self.timer + BOUNCE_WAIT:
            self.timer = gameTimer

            self.x = self.shape.p1.x
            self.y = self.shape.p1.y

            self.collider = ColliderBox(self.x, self.y, self.radius*2, self.radius*2)
            paddle.update_collider()

            if self.collider.collided(paddle.collider):
                self.yMovement = -1

            for y in bubbles:
                for bubble in y:
                    if bubble != 0:
                        if self.collider.collided(bubble.collider):
                            return bubble

            if self.is_edge() == "Left":
                self.xMovement = 1
            if self.is_edge() == "Right":
                self.xMovement = -1
            if self.is_edge() == "Up":
                self.yMovement = 1

            if self.y > maxY:
                if LIVES > 1:
                    LIVES -= 1
                    return "Restart"
                elif LIVES == 1:
                    return True

            if self.xMovement == 1:
                self.x += self.speed
            elif self.xMovement == -1:
                self.x -= self.speed
            self.shape.move(self.xMovement * self.speed, self.yMovement * self.speed)

            return False


class Game:
    def __init__(self):
        self.screen = GraphWin("19291049 Pong Game", WIDTH, HEIGHT)
        self.screen.setBackground("Black")

        self.myPaddle = Paddle("White", 100, 15, 150, self.screen)
        self.ColorsList = ["Cyan", "Red", "Green", "Yellow"]

        self.BallList = list()
        self.BubbleList = list()

        for i in range(BALL_COUNT):
            self.rand_speed = random.randint(5, 20)
            self.rand_direction = random.randint(0, 1)
            self.ball = Ball(self.myPaddle.coordx - int(self.myPaddle.width/2) + i*30, self.screen.getHeight() - MARGIN - self.myPaddle.height - BALLRADIUS,self.ColorsList[i%4] , BALLRADIUS,self.rand_direction,self.rand_speed, self.screen)
            self.BallList.append(self.ball)

            self.livesCounter = Text(Point(self.screen.getWidth() - int(self.screen.getWidth() / 5), 250), f'Lives -- {LIVES}')
            self.livesCounter.setTextColor("Cyan")
            self.livesCounter.setSize(15)
            self.livesCounter.draw(self.screen)
            self.gameTimer = Timer()


        for y in range(3):
            self.BubbleList.append([])
            for x in range(5):
                bubble = Bubbles(self.screen, x, y)
                bubble.draw_bubble()
                self.BubbleList[y].append(bubble)

        self.main()

    def restart(self):
        self.screen.delete("all")

        self.myPaddle = Paddle("White", 100, 15, 150, self.screen)
        self.ColorsList = ["Cyan", "Red", "Green", "Yellow"]
        self.BallList = list()
        BubbleListCopy = self.BubbleList

        for i in range(BALL_COUNT):
            self.rand_speed = random.randint(5, 20)
            self.rand_direction = random.randint(0, 1)

            self.ball = Ball(self.myPaddle.coordx - int(self.myPaddle.width/2) + i*30, self.screen.getHeight() - MARGIN - self.myPaddle.height - BALLRADIUS, self.ColorsList[i % 4], BALLRADIUS, self.rand_direction, self.rand_speed, self.screen)

            self.BallList.append(self.ball)

            self.livesCounter = Text(Point(self.screen.getWidth() - int(self.screen.getWidth() / 5), 250), f'Lives -- {LIVES}')
            self.livesCounter.setTextColor("Cyan")
            self.livesCounter.setSize(15)
            self.livesCounter.draw(self.screen)
            self.gameTimer = Timer()


        for y in BubbleListCopy:
            for b in y:
                if b != 0:
                    b.draw_bubble()

        self.main()


    def check_win(self):
        for y in self.BubbleList:
            for b in y:
                if b != 0:
                    return False
        return True


    def main(self):
        while LIVES > 0:
            try:
                keyPress = self.screen.checkKey()
                if keyPress == 'a':
                    self.myPaddle.move_left()

                if keyPress == 'd':
                    self.myPaddle.move_right()

                if keyPress == 'i':
                    for item in self.BallList:
                        if item.speed <= BALL_SPEED_MAX:
                            item.speed += 1

                if keyPress == 'k':
                    for item in self.BallList:
                        if item.speed >= BALL_SPEED_MIN:
                            item.speed -= 1

                if keyPress == 's':
                    for item in self.BallList:
                        if not item.is_moving():
                            if item.x_direction == 1:
                                item.xMovement = 1
                            else:
                                item.xMovement = -1
                            item.yMovement = -1

                for item in self.BallList:
                    gameOver = item.bounce(self.gameTimer.value, (self.myPaddle.coordx-int(self.myPaddle.width/2)), (self.myPaddle.coordx+int(self.myPaddle.width/2)), self.screen.getHeight() - MARGIN - self.myPaddle.height, self.myPaddle, self.BubbleList)

                    if gameOver != None:
                        if gameOver == "Restart":
                            self.restart()
                            break
                        elif type(gameOver).__name__ == "Bubbles":
                            self.BubbleList[gameOver.y_index][gameOver.x_index].shape.undraw()
                            self.BubbleList[gameOver.y_index][gameOver.x_index] = 0
                        elif gameOver:
                            self.endscreen("LOST")
                            break

                if self.check_win():
                    self.endscreen("WIN")
                    break

                self.gameTimer.value += 1
            except GraphicsError:
                self.screen.close()
                break


    def endscreen(self, status):
        self.screen.delete("all")
        while self.screen.checkKey() == "":
            try:
                self.livesCounter = Text(Point(self.screen.getWidth() - int(self.screen.getWidth() / 5), 250), f'Lives--{LIVES - 1}')
                self.livesCounter.setTextColor("Cyan")
                self.livesCounter.setSize(15)
                self.livesCounter.draw(self.screen)

                GameOverText = Text(Point(150, 345), f"GAME OVER\n\nYOU {status}!\n\nPress Any Key to Quit")
                GameOverText.setTextColor("Red")
                GameOverText.setSize(18)
                GameOverText.draw(self.screen)

                if self.screen.checkKey() != "":
                    self.screen.close()
            except GraphicsError:
                self.screen.close()
                break



Game()
