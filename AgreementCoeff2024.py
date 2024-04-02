"""
Danny F., 2024

Run the script, select a number of categories, and enter your data into the array of cells that appear. 
Press Enter or click GO to recieve two sets of inter-rater agreement statistics, rounded to the nearest decimal of your choice:
- Cohen's Kappa (κ), its standard error (σ), and 95% confidece interval (https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3900052/)
- Gwet's AC1, its standard error (σ), and 95% confidence interval (https://www.ncbi.nlm.nih.gov/books/NBK82266/)

This is a refactored version of a tool I made in Winter 2017 while working as an undergrad research assistant 
with the Optometry department. Also fixed a bug that misplaced GUI elements when using more than 11 categories.

We were originally using an inter-rater agreement statistic calculator that was made in
Excel and that made it INCREDIBLY slow to work worth. I got sick of dealing with it so I decided to 
look up the math behind it and make my own (much faster) calculator in Python. It also gave me something to do
besides rote data entry all day. 

Note: We only used this for 2x2 and 3x3 sets of data. Even though this program allows for general NxN datasets, data entry may get tedious when using larger N.  
This was also my first time making anything with a GUI outside of HTML, so its not very pretty.
"""
try:
    import tkinter as tk #Python 3.x
except ImportError:
    import Tkinter as tk #Python 2.x
    
from numpy import zeros, sqrt, dot

#############
# FUNCTIONS #
#############

def ClearArray(entries): #Clears the current array of textboxes
    for y in range(int(sqrt(len(entries)))):
        for x in range(int(sqrt(len(entries)))):
            entries[("ent{}_{}".format(x,y))].destroy() #deletes all present cells    

    Out.config(state="normal") #Allows program to write to the output text box
    Out.delete("1.0",tk.END) #clears the text in the textbox
    Out.config(state="disabled") #re-lock the textbox
    Out.destroy() #deletes the output text box
    
    for i in range(int(sqrt(len(entries)))): #deletes all present category labels
        categoryLabels_x[i].destroy()
        categoryLabels_y[i].destroy()

    categoryLabels_x.clear()
    categoryLabels_y.clear()
    entries.clear() #empties the Entries and categoryLabels dictionaries

def PopulateArray(dim,grid): #Creates the new array of textboxes, and output textbox
    global Out
    for y in range(0,dim):
        for x in range(0,dim): #populates the program with the necessary number of textboxes
            grid[y][x] = [90+30*x,60+30*y] #fills in grid coordinates
            
            entries[("ent{}_{}".format(x,y))] = tk.Entry(root,width = 3) #Associates each entry with a text box
            entries[("ent{}_{}".format(x,y))].place(in_=root, x=grid[y][x][0],y = grid[y][x][1]) 
    
    for i in range(dim): #labels each category with a letter
        categoryLabels_x[i] = tk.Label(root, text = labels[i+1])
        categoryLabels_y[i] = tk.Label(root, text = labels[i+1])
        categoryLabels_x[i].place(x=95+30*i, y = 38)
        categoryLabels_y[i].place(x=75,y=58+30*i)

    Out = tk.Text(root, height = 10, width = 30, font = ("arial",10)) #regenerates the output text box
    Out.place(in_=entries[("ent{}_{}".format(dim-1,0))],x=50,y=0) #places text box relative to the top-rightmost cell
    
def RecreateArray(event): #Upon selecting dim, deletes current array of text boxes and creates a new one with the chosen dimensions (and resizes window when dim >= 7)
    
    ClearArray(entries) #deletes current array

    dim = num.get() #number of observers
    grid = zeros((dim,dim),dtype="O") #stores the x,y coordinates of each entry cell. Datatype "O" (Object) since something like Vector2 or "A" (array) are not valid Python datatypes

    PopulateArray(dim,grid) #makes the new array of textboxes and fills grid with coordinates
    
    entries["ent0_0"].focus_set() #sets typing focus on the first cell
    
    if str(dim) == "": #Control for window size -- makes it large enough to fit all the cells
        pass
    else:
        if dim < 7:
            root.geometry("{}x250".format(grid[0][dim-1][0]+290))
        else:
            root.geometry("{}x{}".format(350+30*dim,80+30*dim))

def Kappa(dim, entries): #calculates Cohen's Kappa coefficient and Standard Error (https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3900052/)
    values = zeros((dim,dim))
    N = 0 #total number of observations
    P_0 = 0 #relative observed agreement among raters
    P_e = 0 #hypothetical probability of chance agreement
    row_totes = zeros((dim)) #Column vector of the totals for each row
    col_totes = zeros((dim)) #Row vector of the totals for each column
    
    #Cohen's Kappa calculation
    for y in range(0,dim):
        for x in range(0,dim):
            values[y][x] = float(entries["ent{}_{}".format(x,y)].get()) #get the user-entered data from the array
            N += values[y][x]
            row_totes[y] += values[y][x] 
            col_totes[x] += values[y][x] 

    for i in range(dim):
        P_0 += values[i][i]/N #Observed Agreement is the sum of the diagonal elements

    P_e = float((dot(col_totes,row_totes))/(N**2)) #Chance Agreement

    k = (P_0-P_e)/(1-P_e) #Cohen's Kappa

    #Standard Error
    a = 0
    b = 0
    c = (k-P_e*(1-k))**2
    for i in range(dim):
        a += (values[i][i]/N)*(1-((row_totes[i]/N)+(col_totes[i]/N))*(1-k))**2
        for j in range(dim):
            if i!=j: #Counts along all non-diagonal elements
                b += ((1-k)**2)*(values[i][j]/N)*((col_totes[i]/N)+(row_totes[j]/N))**2

    SE = sqrt((a+b-c)/N)/(1-P_e)
    
    return k,SE

def AC1(dim, entries): #calculates Gwet's AC1 coefficient and Standard Error (https://www.ncbi.nlm.nih.gov/books/NBK82266/)
    values = zeros((dim,dim))
    N = 0 #total number of observations
    P_0 = 0 #relative observed agreement among raters
    P_e = 0 #hypothetical probability of chance agreement
    pi_k = zeros(dim)
    
    for y in range(0,dim):
        for x in range(0,dim):
            values[y][x] = float(entries["ent{}_{}".format(x,y)].get())
            N += values[y][x]
     
    for y in range(dim):
        for x in range(dim):
            pi_k[y] += values[x][y]/2/N
            pi_k[y] += values[y][x]/2/N
            if x == y: #Only counts along the diagonal
                P_0 += values[y][x]/N #Observed Agreement
    
    for i in pi_k:
        P_e += i*(1-i)/(dim-1) #Chance Agreement

    AC = ((P_0-P_e)/(1-P_e)) #Gwet's AC1

    #Standard Error
    sum1 = 0
    sum2 = 0
    for i in range(dim):
        sum1 += ((values[i][i]/N)*(1-pi_k[i]))/(dim - 1)
    sum1 -= P_0*P_e
    
    for i in range(dim):
        for j in range(dim):
            sum2 += (values[i][j]/N)*((1-(pi_k[i]+pi_k[j])/2)**2)/(dim-1)/(dim-1)
    sum2 -= P_e*P_e

    var = (P_0*(1-P_0) - 4*(1-AC)*sum1 + 4*((1-AC)**2)*sum2)/(N*(1-P_e)**2)

    acSE = sqrt(var)
    
    return AC,acSE

def KappaOutput(k, SE, rounding): #Writes Kappa, SE, and 95% Confidence interval to the Out textbok
    u95 = k + 1.98*SE
    l95 = k - 1.98*SE
    
    Out.insert(tk.END,("κ = {}").format(round(k,rounding)))
    Out.insert(tk.END,"\n")                                         
    Out.insert(tk.END,("σ = {}").format(round(SE,rounding)))
    Out.insert(tk.END,"\n")
    Out.insert(tk.END,("95% CI = {} ~ {}").format(round(l95,rounding),round(u95,rounding)))
    Out.insert(tk.END,"\n\n")   

def AC1Output(AC,acSE,rounding):
    u95 = AC + 1.98*acSE
    l95 = AC - 1.98*acSE

    Out.insert(tk.END,("AC1 = {}").format(round(AC,rounding)))
    Out.insert(tk.END,"\n")
    Out.insert(tk.END,("σ = {}").format(round(acSE,rounding)))
    Out.insert(tk.END,"\n")
    Out.insert(tk.END,("95% CI = {} ~ {} ").format(round(l95,rounding),round(u95,rounding)))
    Out.insert(tk.END,"\n")

def WriteOutputs(k,SE,ac,acSE,round):
    Out.config(state="normal") #Allows program to write to the output text box
    Out.delete("1.0",tk.END) #clear any text currently in the textbox

    KappaOutput(k, SE, round) #write Kappa outputs
    AC1Output(ac,acSE,round) #write AC1 outputs

    Out.config(state="disabled") #lock the textbox

def Run(): #Calls the coefficient calculations
    categories = num.get()
    roundto = int(digits.get())
    try:
        k,kSE = Kappa(categories, entries)
        ac, acSE = AC1(categories, entries)
        WriteOutputs(k,kSE,ac,acSE,roundto)
    except ValueError: #If the user inputs something non-numeric, the output will ask them to correct the offending cells
        i = 0 #counter: how many cells are not properly filled
        x1 = 0  #(if i=1) horizontal position of cell  
        y1 = 0  #(if i=1) vertical position of cell
        dim = int(num.get())

        #Go through each cell, if it has a non-number character then float(entries) should fail, increasing the counter and noting which cell the error was in
        for y in range(0,dim):
            for x in range(0,dim):
                try:
                    float(entries["ent{}_{}".format(x,y)].get())
                except ValueError:
                    i+=1
                    x1 = x+1
                    y1 = y+1
        if i==1:
            Out.config(state="normal")
            Out.delete("1.0",tk.END)
            Out.insert(tk.END, ("Enter number data for cell ({},{})").format(labels[x1],labels[y1])) #Tells user to check a speified cell, if only one cell is off
            i=0
        if i > 1:
            Out.config(state="normal")
            Out.delete("1.0",tk.END)
            Out.insert(tk.END, ("Enter number data for all cells.")) #If more than one cell is off, asks user to check all cells. (should probably make this list out the offendeing cells)
            i=0

def Run_key(event): #Lets us bind a key, so that we can run the coefficient calculations on a key-press
    Run()

###################
# INITIALIZATIONS #
###################
    
#Initialize GUI#
root = tk.Tk() #Main window
root.geometry("250x250")
global Out
Out = tk.Text(root,height = 0, width = 0) #Defines the text box that contains the output data
Go = tk.Button(root, text = "GO", width = 5, height = 1, command = Run) #Runs the coefficient calculations on click
Go.place(x = 55, y = 2)

#Rounding#
digits = tk.StringVar() #stores the value selected from the rounding spinbox
digits.set("4") #Default rounding
rounding = tk.Spinbox(root,from_=1,to=16, width = 8, textvariable = digits) #Defines a spinbox to allow for the user to select how many digits to round to
rounding.place(x=2,y=65)
roundingLabel = tk.Label(root, text = "Rounding: ")
roundingLabel.place(x=0,y=40)

#Number of categories#
num = tk.IntVar() #Number of cateories. Stores the number selected from the dropbox
menu = tk.OptionMenu(root,num,2,3,4,5,6,7,8,9,10,11,12,
                     13,14,15,16,17,18,19,20, command = RecreateArray) #Generates the drop box that allows user to select how many categories in the agreement chart. Upon selection, generate the chart
                                                                        #currently only set to go up to 20, but in principle you can have as many categories as you want

#Category labels#
labels = {1:"A", 2:"B", 3:"C",4:"D",5:"E",6:"F",7:"G",8:"H",9:"I",10:"J",11:"K",12:"L",13:"M",14:"N",
          15:"O",16:"P",17:"Q",18:"R",19:"S",20:"T",21:"U",22:"V",23:"W",24:"X",25:"Y",26:"Z"} #Labels for each category. Prepared for up to 26 categories, but can be changed according to need
categoryLabels_x = {} #contains the lables along the horizontal direction (i.e. for the columns)
categoryLabels_y = {} #contains labels along the vertical direction (i.e. for the rows)

#User-entered data#
entries = {} #Dictionary with keys "entX_Y", and values being user-entered data. Contains each entry cell, used to retrieve user-entered data.

root.bind("<Return>",Run_key) #bind "Run" to the Enter key

menu.grid() #puts GUI elements on a grid

root.mainloop()
