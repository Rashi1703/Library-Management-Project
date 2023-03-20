                                                #Standard calculator
from tkinter import *
import math
from tkinter import messagebox
operator=''

#-------------------------------------------------------------------------------
#COMMANDS
def Exit():
    Exit=messagebox.askyesno("CALCULATOR","Confirm if you want to exit")
    if Exit > 0:
        my_window.destroy()

def btnclick(numbers):
    global operator
    operator=operator+str(numbers)
    text_input.set(operator)

def btnAC():
    text_input.set("")

def btnresult():
    global operator
    try:
        result=str(eval(operator))
        text_input.set(result)
        operator=''
    except:
        text_input.set("")
        operator=''
        messagebox.showinfo("Error","Enter valid equation")
        
def btnback():
    global operator
    operator=operator[0:-1]
    text_input.set(operator)
def standard():
    global text_input,my_window
    my_window=Tk()
    my_window.title("STANDARD CALCULATOR")
    my_window.configure(bg="grey",width=500,height=500)
    my_window.resizable(width=False, height=False)
    text_input=StringVar()
    label_1=Label(my_window,text="Solve your difficult problems in a second",bg="Black",fg="white",font="Arial 20 bold italic underline",bd=10,relief="sunken",padx=3,pady=3)
    label_1.grid(row=0,columnspan=5)

    space_label_1=Label(my_window,text='',bg="grey")
    space_label_1.grid(row=1)

    #Buttons
    label_2=Label(my_window,textvariable=text_input,width=45,height=3,bg="white",fg="black",font="Arial 14 bold",bd=5,relief="groove",padx=3,pady=3,justify="right")
    label_2.grid(row=3,columnspan=5)

    space_label_2=Label(my_window,text="",bg="grey")
    space_label_2.grid(row=4)

    button_k1=Button(my_window,text="AC",bg="Black",fg="white",font="Arial 15 bold ",bd=10,relief="raised",padx=3,pady=3,command=btnAC)
    button_k1.grid(row=5,column=0)

    button_k2=Button(my_window,text="9",bg="Black",fg="white",font="Arial 15 bold ",bd=10,relief="raised",padx=3,pady=3,command=lambda:btnclick(9))
    button_k2.grid(row=5,column=1)

    button_k3=Button(my_window,text="8",bg="Black",fg="white",font="Arial 15 bold ",bd=10,relief="raised",padx=3,pady=3,command=lambda:btnclick(8))
    button_k3.grid(row=5,column=2)

    button_k4=Button(my_window,text="7",bg="Black",fg="white",font="Arial 15 bold ",bd=10,relief="raised",padx=3,pady=3,command=lambda:btnclick(7))
    button_k4.grid(row=5,column=3)

    button_k5=Button(my_window,text="Backspace",bg="Black",fg="white",font="Arial 12 bold ",bd=10,relief="raised",padx=3,pady=3,command=btnback)
    button_k5.grid(row=5,column=4)

    button_k6=Button(my_window,text="%",bg="Black",fg="white",font="Arial 15 bold ",bd=10,relief="raised",padx=3,pady=3,command=lambda:btnclick("%"))
    button_k6.grid(row=6,column=0)

    button_k7=Button(my_window,text="6",bg="Black",fg="white",font="Arial 15 bold ",bd=10,relief="raised",padx=3,pady=3,command=lambda:btnclick(6))
    button_k7.grid(row=6,column=1)

    button_k8=Button(my_window,text="5",bg="Black",fg="white",font="Arial 15 bold ",bd=10,relief="raised",padx=3,pady=3,command=lambda:btnclick(5))
    button_k8.grid(row=6,column=2)

    button_k9=Button(my_window,text="4",bg="Black",fg="white",font="Arial 15 bold ",bd=10,relief="raised",padx=3,pady=3,command=lambda:btnclick(4))
    button_k9.grid(row=6,column=3)

    button_k10=Button(my_window,text="*",bg="Black",fg="white",font="Arial 15 bold ",bd=10,relief="raised",padx=3,pady=3,command=lambda:btnclick("*"))
    button_k10.grid(row=6,column=4)

    button_k11=Button(my_window,text="(",bg="Black",fg="white",font="Arial 15 bold ",bd=10,relief="raised",padx=3,pady=3,command=lambda:btnclick("("))
    button_k11.grid(row=7,column=0)

    button_k12=Button(my_window,text="3",bg="Black",fg="white",font="Arial 15 bold ",bd=10,relief="raised",padx=3,pady=3,command=lambda:btnclick(3))
    button_k12.grid(row=7,column=1)

    button_k13=Button(my_window,text="2",bg="Black",fg="white",font="Arial 15 bold ",bd=10,relief="raised",padx=3,pady=3,command=lambda:btnclick(2))
    button_k13.grid(row=7,column=2)

    button_k14=Button(my_window,text="1",bg="Black",fg="white",font="Arial 15 bold ",bd=10,relief="raised",padx=3,pady=3,command=lambda:btnclick(1))
    button_k14.grid(row=7,column=3)

    button_k15=Button(my_window,text="+",bg="Black",fg="white",font="Arial 15 bold ",bd=10,relief="raised",padx=3,pady=3,command=lambda:btnclick("+"))
    button_k15.grid(row=7,column=4)

    button_k16=Button(my_window,text=")",bg="Black",fg="white",font="Arial 15 bold ",bd=10,relief="raised",padx=3,pady=3,command=lambda:btnclick(")"))
    button_k16.grid(row=8,column=0)

    button_k17=Button(my_window,text=".",bg="Black",fg="white",font="Arial 15 bold ",bd=10,relief="raised",padx=3,pady=3,command=lambda:btnclick("."))
    button_k17.grid(row=8,column=1)

    button_k18=Button(my_window,text="0",bg="Black",fg="white",font="Arial 15 bold ",bd=10,relief="raised",padx=3,pady=3,command=lambda:btnclick(0))
    button_k18.grid(row=8,column=2)

    button_k19=Button(my_window,text="/",bg="Black",fg="white",font="Arial 15 bold ",bd=10,relief="raised",padx=3,pady=3,command=lambda:btnclick("/"))
    button_k19.grid(row=8,column=3)

    button_k20=Button(my_window,text="-",bg="Black",fg="white",font="Arial 15 bold ",bd=10,relief="raised",padx=3,pady=3,command=lambda:btnclick("-"))
    button_k20.grid(row=8,column=4)

    space_label_3=Label(my_window,text="",bg="grey")
    space_label_3.grid(row=9)

    button_kR=Button(my_window,text="Get result",bg="Black",fg="white",font="Arial 15 bold ",bd=10,relief="raised",padx=3,pady=3,command=btnresult)
    button_kR.grid(row=10,column=2)
    menubar=Menu(my_window)
    menubar.add_command(label="Scientific Calculator",command=lambda:[my_window.destroy(),scientific()])
    menubar.add_command(label="Standard Calculator",command=lambda:[my_window.destroy(),standard()])
    menubar.add_command(label="Exit",command=Exit)
    my_window.config(menu=menubar)
    my_window.mainloop()
#------------------------------------------------------------------------------------------------------

def scientific():
    global text_input,my_window
    my_window=Tk()
    my_window.title("STANDARD CALCULATOR")
    my_window.configure(bg="grey",width=500,height=500)
    my_window.resizable(width=False, height=False)
    text_input=StringVar()
    label_1=Label(my_window,text="Solve your difficult problems in a second",bg="Black",fg="white",font="Arial 20 bold italic underline",bd=10,relief="sunken",padx=3,pady=3)
    label_1.grid(row=0,columnspan=5)

    space_label_1=Label(my_window,text='',bg="grey")
    space_label_1.grid(row=1)

    #Buttons
    label_2=Label(my_window,textvariable=text_input,width=45,height=3,bg="white",fg="black",font="Arial 14 bold",bd=5,relief="groove",padx=3,pady=3,justify="right")
    label_2.grid(row=3,columnspan=5)

    space_label_2=Label(my_window,text="",bg="grey")
    space_label_2.grid(row=4)
    #Buttons
    label_2=Label(my_window,textvariable=text_input,width=45,height=3,bg="white",fg="black",font="Arial 14 bold",bd=5,relief="groove",padx=3,pady=3,justify="right")
    label_2.grid(row=3,columnspan=5)

    space_label_2=Label(my_window,text="",bg="grey")
    space_label_2.grid(row=4)



    space_label_3=Label(my_window,text="",bg="grey")
    space_label_3.grid(row=9)

    button_kR=Button(my_window,text="Get result",bg="Black",fg="white",font="Arial 15 bold ",bd=10,relief="raised",padx=3,pady=3,command=btnresult)
    button_kR.grid(row=10,column=2)
    menubar=Menu(my_window)
    menubar.add_command(label="Scientific Calculator",command=lambda:[my_window.destroy(),scientific()])
    menubar.add_command(label="Standard Calculator",command=lambda:[my_window.destroy(),standard()])
    menubar.add_command(label="Exit",command=Exit)
    my_window.config(menu=menubar)
    my_window.mainloop()
    
standard()
#Menu

