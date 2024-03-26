try:
    import tkinter as tk
except ImportError:
    import Tkinter as tk
from math import sqrt

def U(N,P):
    return (N/(N+(1.96**2)))*(P+(1.96**2/(2*N))+1.96*sqrt(((P*(1-P))/N)+(1.96**2/(4*N**2)))) #Upper limit for 95% CI

def L(N,P):
    return (N/(N+(1.96**2)))*(P+(1.96**2/(2*N))-1.96*sqrt(((P*(1-P))/N)+(1.96**2/(4*N**2)))) #Lower limit for 95% CI

def P_agree(A,B,C): #Pass agreement
    N = A+B+C
    P = 2*A/(2*A+B+C)
    final = ("P_agree: {} \n95% CI: {} to {}").format(round(P,4),round(L(N,P),4),round(U(N,P),4)) 
    return final
    
def F_agree(A,B,C): #Fail agreement
    N = A+B+C
    P = 2*A/(2*A+B+C)
    final = ("F_agree: {} \n95% CI: {} to {}").format(round(P,4),round(L(N,P),4),round(U(N,P),4))
    return final


def PreP(A,B): #Predictive Pass
    N = A+B
    P = A/N
    final = ("PreP: {} \n95% CI: {} to {}").format(round(P,4),round(L(N,P),4),round(U(N,P),4))
    return final
    
def PreF(C,D): #Predictive Fail
    N = C+D
    P = D/N
    final = ("PreF: {} \n95% CI: {} to {}").format(round(P,4),round(L(N,P),4),round(U(N,P),4))
    return final

def sen(B,D): #Sensitivity
    N = B+D
    P = D/N
    final = ("Sensitivity: {} \n95% CI: {} to {}").format(round(P,4),round(L(N,P),4),round(U(N,P),4))
    return final

def spec(A,C): #Specificity
    N = A+C
    P = A/N
    final = ("Specificity: {} \n95% CI: {} to {}").format(round(P,4),round(L(N,P),4),round(U(N,P),4))
    return final


root = tk.Tk()
root.geometry("300x350")

P1 = tk.Label(root, text="P")#Labels category (P, F)
F1 = tk.Label(root, text="F")
P2 = tk.Label(root, text="P")
F2 = tk.Label(root, text="F")

a = tk.Entry(root, width = 3) #Generates each entry
b = tk.Entry(root, width = 3)
c = tk.Entry(root, width = 3)
d = tk.Entry(root, width = 3)


a.place(in_=root,x=15,y=15)
b.place(in_=root,x=45,y=15)
c.place(in_=root,x=15,y=45)
d.place(in_=root,x=45,y=45)
a.focus_set() #Places typing focus on the first cell
P1.place(in_=a,x=-15,y=-2)
F1.place(in_=c,x=-15,y=-2)
P2.place(in_=a,x=2,y=-20)
F2.place(in_=b,x=2,y=-20)

Out = tk.Text(root,height = 20, width = 25,font = ("arial",10)) #Output text box
Out.place(in_=root,x=80,y=10)


def enter_button():
    a2 = float(a.get())
    b2 = float(b.get())
    c2 = float(c.get())
    d2 = float(d.get()) #Takes all the input values
    Out.config(state="normal")
    Out.delete("1.0",tk.END)
    Out.insert(tk.END,P_agree(a2,b2,c2))   #Outputs each calculation
    Out.insert(tk.END,"\n\n")
    Out.insert(tk.END,F_agree(d2,b2,c2))
    Out.insert(tk.END,"\n\n")
    Out.insert(tk.END,PreP(a2,b2))
    Out.insert(tk.END,"\n\n")
    Out.insert(tk.END, PreF(c2,d2))
    Out.insert(tk.END,"\n\n")
    Out.insert(tk.END,sen(b2,d2))
    Out.insert(tk.END,"\n\n")
    Out.insert(tk.END,spec(a2,c2))
    Out.config(state="disabled")

def enter(event):
    enter_button()
    
    
    
button = tk.Button(root,text = "Go",command=enter_button, width = 6)
button.place(in_=c,x=-2,y=30)
root.bind("<Return>",enter)

root.mainloop()
