"""
Danny F., 2017

Hey, so I relize that this code is probably an absolute mess and could be
greatly optimized/generally better written (eg. less global variables), but
it works, and that's really all I was going for. But feel free to improve on
the code.
"""


try:
    import tkinter as tk #Python 3.x
except ImportError:
    import Tkinter as tk #Python 2.x
    
from numpy import zeros, sqrt, dot

root = tk.Tk()

#Most of these globals were made so the window could be cleared when changing between grid dimention settings

global entries 
entries = {} #Contains each entry cell, can later be used to retrieve user-entered data
global Out
Out = tk.Text(root,height = 0, width = 0) #Defines the text box that contains the output data
global rounding 
rounding = tk.Spinbox() #Defines a spinbox to allow for the user to select how many digits to round to

labels = {1:"A", 2:"B", 3:"C",4:"D",5:"E",6:"F",7:"G",8:"H",9:"I",10:"J",11:"K",12:"L",13:"M",14:"N",
          15:"O",16:"P",17:"Q",18:"R",19:"S",20:"T",21:"U",22:"V",23:"W",24:"X",25:"Y",26:"Z"} #Labels for each category
global category_x   
global category_y
category_x = {}
category_y = {}

def make_chart(event): #generates the kxk grid of entries
    global entries
    global Out
    global rounding
    global category_x      
    global category_y
 
    Go = tk.Button(root, text = "GO",width = 5, height = 1, command = Run) #Runs the coefficient calculations
    Go.place(x = 55, y = 2)
    
    rnd = tk.Label(root, text = "Rounding: ")
    rnd.place(x=0,y=40)
    digits = tk.StringVar()
    digits.set("4")
    rounding = tk.Spinbox(root,from_=1,to=16, width = 8, textvariable = digits) #Allows user to select how many digits to round numbers to
    rounding.place(x=2,y=65)
    
    dim = num.get()

    
    chart = zeros((dim,dim),dtype="O") #contais the x,y coordinates of each entry cell
    for y in range(int(sqrt(len(entries)))):
        for x in range(int(sqrt(len(entries)))):
            entries[("ent{}{}".format(x,y))].destroy() #deletes all present cells
            
    for i in range(int(sqrt(len(entries)))): #deletes all present category labels
        category_x[i].destroy()
        category_y[i].destroy()

    entries = {} #empties the Entries dictionary
    for y in range(0,dim):
        for x in range(0,dim): #populates the program with the necessary number of cells
            chart[y][x] = [90+30*x,60+30*y]
            entries[("ent{}{}".format(x,y))] = tk.Entry(root,width = 3)
            entries[("ent{}{}".format(x,y))].place(in_=root, x=chart[y][x][0],y = chart[y][x][1]) #Associates each entry with a text box
            
    category_x = {}
    category_y = {}
    for i in range(dim): #labels each category with a letter
        category_x[i] = tk.Label(root, text = labels[i+1])
        category_y[i] = tk.Label(root, text = labels[i+1])
        category_x[i].place(x=95+30*i, y = 38)
        category_y[i].place(x=75,y=58+30*i)
        
    entries["ent00"].focus_set() #set's typing focus on the first cell
    
    Out.destroy() #deletes the output text box
    Out = tk.Text(root,height = 10, width = 25,font = ("arial",10)) #regenerates the output text box
    Out.place(in_=entries[("ent{}{}".format(dim-1,0))],x=50,y=0) #places text box relative to the top-rightmost cell
    
    if str(dim) == "": #Control for window size
        pass
    else:
        if dim < 7:
            root.geometry("{}x250".format(chart[0][dim-1][0]+250))
        else:
            root.geometry("{}x{}".format(310+30*dim,80+30*dim))
    return chart

    
num = tk.IntVar() #Defines the number selected from the dropbox
menu = tk.OptionMenu(root,num,2,3,4,5,6,7,8,9,10,11,12,
                     13,14,15,16,17,18,19,20, command = make_chart) #generates the drop box that allows user to select how many categories in the agreement chart

  
def Kappa(): #calculates Kappa coefficient, Standard Error, and 95% CI
    dim = num.get()
    values = zeros((dim,dim))
    N = 0
    P_0 = 0
    P_e = 0
    row_totes = zeros((dim,1))
    col_totes = zeros((1,dim))
    rnd = int(rounding.get())
    
    #Cohen's Kappa
    for y in range(0,dim):
        for x in range(0,dim):
            values[y][x] = float(entries["ent{}{}".format(x,y)].get())
            N += values[y][x] #Total number of subjects

    
    for y in range(dim):
        for x in range(dim):
            if x == y: #Only count along the diagonal of the agreement chart
                P_0 += values[y][x]/N #Observed Agreement

    for y in range(dim):
        for x in range(dim):
            row_totes[y,0] += values[y][x] #Column vector of the totals for each row
    for x in range(dim):
         for y in range(dim):
             col_totes[0,x] += values[y][x] #Row vector of the totals for each column

    P_e = float((dot(col_totes,row_totes))/(N**2)) #Chance Agreement

    k = (P_0-P_e)/(1-P_e) #Cohen's Kappa

    #Standard Error
    a = 0
    b = 0
    c = (k-P_e*(1-k))**2
    for i in range(dim):
        for j in range(dim):
            if i!=j: #Counts along all non-diagonal elements
                b += ((1-k)**2)*(values[i][j]/N)*((col_totes[0,i]/N)+(row_totes[j,0]/N))**2

    for i in range(dim):
        a += (values[i][i]/N)*(1-((row_totes[i,0]/N)+(col_totes[0,i]/N))*(1-k))**2

    SE = sqrt((a+b-c)/N)/(1-P_e)
    
    
    #95% CI
    u95 = k + 1.98*SE
    l95 = k - 1.98*SE

    Out.config(state="normal") #Allows program to write to the output text box
    Out.delete("1.0",tk.END)
    Out.insert(tk.END,("κ = {}").format(round(k,rnd)))
    Out.insert(tk.END,"\n")                                         #Displays Cohen's Kappa, SE, and 95% CI in the output text box
    Out.insert(tk.END,("SE = {}").format(round(SE,rnd)))
    Out.insert(tk.END,"\n")
    Out.insert(tk.END,("95% CI = {} ~ {}").format(round(l95,rnd),round(u95,rnd)))
    Out.insert(tk.END,"\n\n")


def AC1(): #Calculates Gwet's AC1 coefficient of agreement, standard error, and 95% CI
    dim = num.get()
    values = zeros((dim,dim))
    pi_k = zeros(dim)
    N = 0
    P_0 = 0
    P_e = 0
    rnd = int(rounding.get())
    
    #AC1
    for y in range(0,dim):
        for x in range(0,dim):
            values[y][x] = float(entries["ent{}{}".format(x,y)].get())
            N += values[y][x] #Total number of subjects
     
    for y in range(dim):
        for x in range(dim):
            if x == y: #Only counts along the diagonal
                P_0 += values[y][x]/N #Observed Agreement
    
    for i in range(dim): #Adds the number of subjects who were in each category for both raters, double-counting the agreement cell (eg. PP, FF)
        for y in range(dim): 
            pi_k[i] += values[y][i]/2/N
        for x in range(dim):
            pi_k[i] += values[i][x]/2/N
    
    for i in pi_k:
        P_e += i*(1-i)/(dim-1) #Chance Agreement

    AC1 = ((P_0-P_e)/(1-P_e)) #Gwet's AC1

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

    var = (P_0*(1-P_0) - 4*(1-AC1)*sum1 + 4*((1-AC1)**2)*sum2)/(N*(1-P_e)**2)

    SE = sqrt(var)

    #95% CI
    u95 = AC1 + 1.98*SE
    l95 = AC1 - 1.98*SE
       
    Out.insert(tk.END,("AC1 = {}").format(round(AC1,rnd)))
    Out.insert(tk.END,"\n")
    Out.insert(tk.END,("SE = {}").format(round(SE,rnd)))
    Out.insert(tk.END,"\n")
    Out.insert(tk.END,("95% CI = {} ~ {} ").format(round(l95,rnd),round(u95,rnd)))
    Out.insert(tk.END,"\n")
    Out.config(state="disabled")


def Run(): #Calls the coefficient calculations
    try:
        Kappa()
        AC1()
    except ValueError: #If the user left any entries empty, the output will ask them to fill the empty cells
        i = 0
        x1 = 0
        y1 = 0
        dim = int(num.get())
        for y in range(0,dim):
            for x in range(0,dim):
                if entries["ent{}{}".format(x,y)].get() == "":
                    i+=1
                    x1 = x+1
                    y1 = y+1
        if i==1:
            Out.config(state="normal")
            Out.delete("1.0",tk.END)
            Out.insert(tk.END, ("Enter data for cell ({},{})").format(labels[x1],labels[y1])) #Tells user to fill a speified cell, if only one cell is blank
            i=0
        if i > 1:
            Out.config(state="normal")
            Out.delete("1.0",tk.END)
            Out.insert(tk.END, ("Enter data for all cells.")) #If more than one cell is blank, asks user to fill all cells.
            i=0


def Run_key(event): #Calls the coefficient calculateions on a key-press
    Run()
    
root.bind("<Return>",Run_key)
menu.grid()

root.mainloop()
