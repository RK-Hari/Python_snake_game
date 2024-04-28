import random
import tkinter
from tkinter import *

#Constants that we'll be using furthur in the project
HIGH_SCORE=0
WIDTH=690
HEIGHT=690
SNAKE_SIZE=3
SPEED=60
OBJECT_SIZE=30
SNAKE_COLOR="#CC0066"
FOOD_COLOR="#339999"
BACKGROUND="#FFFFCC"

#Structure of the snake
class Snake:
    def __init__(self):
        self.body_size=SNAKE_SIZE
        self.circles=[]
        self.coordinates=[]

        #Appending the coordinates of all the circles in the body of the snake into coordinates list
        for i in range(SNAKE_SIZE):
            self.coordinates.append([0,0])

        #Appending all the cirles in the body of the snake into the circle list
        for x,y in self.coordinates:
            circle = canvas.create_oval(x , y , x+OBJECT_SIZE , y+OBJECT_SIZE , fill=SNAKE_COLOR , tag="snake")
            self.circles.append(circle)


#Defining how the food object should be displayed
class Food:
    def __init__(self):

        #To generate random coordinates of x and y among the game window
        x = random.randint(0, int(WIDTH / OBJECT_SIZE) - 1) * OBJECT_SIZE
        y = random.randint(0, int(HEIGHT / OBJECT_SIZE) - 1) * OBJECT_SIZE

        #Assigning it to contructor
        self.coordinates=[x,y]

        #To create a rectange in the game window at the desired coordinates
        canvas.create_oval(x , y, x+OBJECT_SIZE, y+OBJECT_SIZE , fill=FOOD_COLOR , tag="food")


#This function the actions to be performed for the movement of the snake
def next_turn(snake , food):
    #Extracting the head of the snake
    x,y = snake.coordinates[0]

    #To determine the direction of movement
    if(direction == "up"):
        y-=OBJECT_SIZE
    elif(direction == "down"):
        y+=OBJECT_SIZE
    elif (direction == "right"):
        x += OBJECT_SIZE
    elif (direction == "left"):
        x -= OBJECT_SIZE

    #Inserting the coordinates of the newly created circle at the head
    snake.coordinates.insert(0,(x,y))

    #Inserting a new circle at the head if the snake during the movement
    circle = canvas.create_oval(x , y , x+OBJECT_SIZE , y+OBJECT_SIZE , fill=SNAKE_COLOR )
    snake.circles.insert(0,circle)

    #We'll keep the newly created circle if , the head collides with food
    if (x == food.coordinates[0] and y == food.coordinates[1]):
        #Updating the scores
        global score,HIGH_SCORE
        score+=1
        if(score>=HIGH_SCORE):
            HIGH_SCORE=max(HIGH_SCORE,score)
        #Displaying the newly updates score
        label.config(text="Score:{}".format(score))
        label2.config(text="High Score:{}".format(HIGH_SCORE))

        #Deleting the existing food
        canvas.delete("food")
        #Creating a new food
        food=Food()

    #Else we'll delete the newly created circle
    else:
        # Deleting the tail from the coordinates list,body of the snake and also from the game screen
        del snake.coordinates[-1]
        canvas.delete(snake.circles[-1])
        del snake.circles[-1]

    #If collisions occur , gameover() function is called
    if(check_collisions(snake)):
        gameover()
    else:
        #Setting the speed at which the actions has to performed
        window.after(SPEED, next_turn, snake, food)

def change_direction(new_direction):
    #Calling the global variable
    global direction

    #Checking the directions to change the direction of the moving snake
    if(new_direction=="left"):
        #This is included to avoid a 180 degree rotation.
        if(direction!="right"):
            direction=new_direction
    elif (new_direction == "right"):
        if (direction != "left"):
            direction = new_direction
    elif (new_direction == "up"):
        if (direction != "down"):
            direction = new_direction
    elif (new_direction == "down"):
        if (direction != "up"):
            direction = new_direction

#Check for collisions
def check_collisions(snake):
    #Head of the snake
    x,y=snake.coordinates[0]

    #If x or y reaches the end of the screen, then true is returned
    if(x<0 or x>=WIDTH):
        return True
    elif(y<0 or y>=HEIGHT):
        return True

    #Checking for collision with body itself
    for obj in snake.coordinates[1:]:
        if(x==obj[0] and y==obj[1]):
            return True

    #If there are no collisions . Then false is returned
    return False

#A function to handle the game over functionality
def gameover():
    #If there are collisions then , the is ended by deleting all components created
    canvas.delete(ALL)
    #Postioning and placing the GAME OVER text
    canvas.create_text(canvas.winfo_width()/2,canvas.winfo_height()/2,text="GAME OVER",font=('Palatino',80),fill="#800000",tag="gameover")
    #Creating a restart button
    restart_button = Button(window, text="Restart", command=restart_game)
    #Placing the button at the center
    restart_button.place(relx=0.5, rely=0.637, anchor=CENTER)
    #Redesigning the button layout design
    restart_button.configure(font=('Arial', 14), bg='green', fg='white')
    #Assiging the button to a window variable
    window.restart_button=restart_button

#A function to handle to restart functionality
def restart_game():
    #Deleting the GAME OVER text
    canvas.delete(ALL)
    #Destroying the restart button
    window.restart_button.destroy()
    
    #Resetting all the variables
    global snake,food,score,direction,HIGH_SCORE
    HIGH_SCORE=max(HIGH_SCORE,score)
    snake=Snake()
    food=Food()
    score=0
    direction="down"
    label.config(text="Score : {}".format(score))
    label2.config(text="High Score : {}".format(HIGH_SCORE))
    next_turn(snake,food)

#Create a new window
window=Tk()
#To avoid th resizing of the game window
window.resizable(False,False)
#Title to be set for the game window
window.title("Snake Game")

#Initial score and intial direction
score=0
direction = "down"

#Add label to the project, which displays the score
label = Label(window,text="Score : {}".format(score),font= ('Impact', 20))
label.pack()
label2 = Label(window,text="High Score : {}".format(HIGH_SCORE),font= ('Impact', 20))
label2.pack()

#Set the height,width and color of the game window
canvas = Canvas(window, bg=BACKGROUND, height=HEIGHT, width=WIDTH)
canvas.pack()

#Update the changes to the window
window.update()

#To calculate center the game window that displays
window_height = window.winfo_height()
window_width = window.winfo_width()
screen_height = window.winfo_screenheight()
screen_width = window.winfo_screenwidth()

x = int((screen_width/2)-(window_width/2))
y = int((screen_height/2)-(window_height/2))

#Setting the window position
window.geometry(f"{window_width}x{window_height}+{x}+{y}")

#Setting the keys to determine the movement of the snake
window.bind('<Left>', lambda event: change_direction("left"))
window.bind('<Right>', lambda event: change_direction("right"))
window.bind('<Up>', lambda event: change_direction("up"))
window.bind('<Down>', lambda event: change_direction("down"))

#Intialising the objects
snake=Snake()
food=Food()
next_turn(snake,food)

#To keep the window running constantly , and look for interactions done by the user
window.mainloop()