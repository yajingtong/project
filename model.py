import matplotlib
matplotlib.use('TkAgg')
import random
import operator
import numpy as np
import matplotlib.pyplot
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import agentframework
import w
import requests
import bs4
import matplotlib.animation as animation
import tkinter

#initialise the pramiters
num_of_agents = 10 #initialise the number of agents
num_of_wolves = 3
num_of_iterations = 50   #initialise the number of iterations
agents = [] #make a empty list of agents
wolves = [] #male a empty list of agents "wolf"
neighbourhood = 20# #initialise the number of neighbourhood

#read in environment data
f = open("in.txt")
environment=[]	#make a empty list of environment
for row in f:
    parsed_row = str.split(row,",") #split the string data depending on ","
    rowlist = []  #make a new list 
    for value in parsed_row:
        rowlist.append(float(value)) #convert string to float and append to the new list
    environment.append(rowlist) #append rowlist to the list of environment
f.close() #close file

#initialise the agents data
r = requests.get('http://www.geog.leeds.ac.uk/courses/computing/practicals/python/agent-framework/part9/data.html')
#use the function of request to get the data of webpage
content = r.text #pass in the text and store it in context
soup = bs4.BeautifulSoup(content, 'html.parser')#use the function of bs4 
td_ys = soup.find_all(attrs={"class" : "y"})
td_xs = soup.find_all(attrs={"class" : "x"})
#print(td_ys)
#print(td_xs) 
r.close

# create fig and ax the animation function based on
fig = matplotlib.pyplot.figure(figsize=(7, 7))
ax = fig.add_axes([0, 0, 1, 1]) 

carry_on=True



# Make the agents fro object Sheep.
for i in range(num_of_agents):#use the for-loop to create agents in each iterations
    y = int(td_ys[i].text) #assign x,y coordinates  values to agents
    x = int(td_xs[i].text)
    agents.append(agentframework.Sheep(x, y, environment,agents, neighbourhood))

#Make the wolf agents.
for j in range(num_of_wolves):
    wolves.append(w.wolf(x,y, wolves))    



#the function animation based on  
def update(frame_number):
    
    fig.clear()   
    global carry_on
    
    for j in range(num_of_wolves): 
        wolves[j].random_move()
        
    for i in range(num_of_agents): 
        agents[i].eat()
        agents[i].move()
        agents[i].share_with_neighbours(neighbourhood)
        agents[i].hungry()
        agents[i].eaten()
    
    #draw a catterplot of agents and show the environment
    for i in range(num_of_agents):
        matplotlib.pyplot.xlim(0, 300)
        matplotlib.pyplot.ylim(0, 300)
        matplotlib.pyplot.imshow(environment) 
        matplotlib.pyplot.scatter(agents[i].y,agents[i].x,color="white")
        #print(agents[i].x,agents[i].y) 
     
    for j in range(num_of_wolves): 
        matplotlib.pyplot.xlim(0, 300)
        matplotlib.pyplot.ylim(0, 300)
        matplotlib.pyplot.imshow(environment) 
        matplotlib.pyplot.scatter(wolves[j].y,wolves[j].x,color="black")
         
#def gen_function stop condition
def gen_function(b = [0]):
    a = 0
    global carry_on
    while (a < num_of_iterations) & (carry_on) :
        yield a			# Returns control and waits next call.
        a = a + 1
    
        
def run():# the function runs model
    animation = matplotlib.animation.FuncAnimation(fig, update, frames=gen_function, repeat=False)
    canvas.draw()    
    


root = tkinter.Tk()
root.wm_title("Model")
canvas = matplotlib.backends.backend_tkagg.FigureCanvasTkAgg(fig, master=root)
canvas._tkcanvas.pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=True)
menu_bar = tkinter.Menu(root)
root.config(menu=menu_bar)
model_menu = tkinter.Menu(menu_bar)
menu_bar.add_cascade(label="Model", menu=model_menu)
model_menu.add_command(label="Run model", command=run)
tkinter.mainloop()
