#import module
from tkinter import *
from tkinter import ttk
from PIL import ImageTk,Image
from tkinter import messagebox
import mysql.connector
import datetime
from datetime import datetime
import smtplib
import winsound
import ssl
from email.message import EmailMessage

#Database connection
try:
    import mysql.connector as mys
    mydb1=mys.connect(host="localhost",user="root",passwd="1710")
    mycursor=mydb1.cursor()
    mycursor.execute("Create database if not exists library")
    mydb1.commit()
    import mysql.connector
    mydb=mysql.connector.connect(host="localhost",user="root",passwd="1710",database="library")
    mycursor=mydb.cursor()
    #Table book_issue
    mycursor.execute("Create table book_issue(Student_Id int(7),Student_name char(20),Book_name char(50),Issue_date timestamp default current_timestamp,fine int(5) default 0,paid int(3) default 0)")
    mydb.commit()
    #Table book_issue_teach
    mycursor.execute("Create table book_issue_teach(Teacher_Id varchar(6) NOT NULL,Teacher_name char(30),Book_name char(50),Issue_date timestamp default current_timestamp,fine int(5) default 0,paid int(3) default 0)")
    mydb.commit()
    #Table book_in_order
    mycursor.execute("Create table book_in_order(S_No int auto_increment primary key,Book_name char(50),Author_name char(30),Quantity int(3) Default 0)")
    mydb.commit()
    #Table book_return
    mycursor.execute("Create table book_return(Student_Id int(7),Student_name char(20),Book_name char(50),Return_date timestamp default current_timestamp)")
    mydb.commit()
    #Table book_return_teach
    mycursor.execute("Create table book_return_teach(Teacher_Id varchar(6),Teacher_name char(30),Book_name char(50),Return_date timestamp default current_timestamp)")
    mydb.commit()
    #Table booklist
    mycursor.execute("Create table booklist(S_No int auto_increment primary key,Book_name char(50),Author_name char(30),Quantity int(3) Default 0)")
    mydb.commit()
    #Table studentname
    mycursor.execute("Create table studentname(Stu_Id int(6) primary key auto_increment,Student_name char(30),Class varchar(8),Gmail varchar(35))")
    mydb.commit()
    #Table teachername
    mycursor.execute("Create table teachername(Teacher_Id varchar(6) primary key ,Teacher_name char(30),Gmail varchar(35))")
    mydb.commit()
    #Table login_id
    mycursor.execute("Create table login_id(login_id int(4) primary key ,user_name char(30))")
    mydb.commit()
except:
    flag=1
#Sound
def sound():
    filename='voice.wav'
    winsound.PlaySound(filename,winsound.SND_FILENAME)

#date-time
def time():
    now=datetime.now()
    string = now.strftime("%Y-%m-%d %H:%M:%S %p")
    label_1.config(text="Date and time \n"+string)
    label_1.after(1000, time)

#mysql-connection
mydb=mysql.connector.connect(host="localhost",user="root",passwd="1710",database="library")
mycursor=mydb.cursor(buffered=True)

def update_teach():
    q="Select Teacher_Id from book_issue_teach"
    mycursor.execute(q)
    c=mycursor.fetchall()
    for i in c:
        p="Select Issue_date from book_issue_teach where Teacher_Id='%s'"%i
        mycursor.execute(p)
        d=mycursor.fetchone()[0]
        datetime_from_db = datetime.strptime(str(d), '%Y-%m-%d %H:%M:%S')
        current_datetime = datetime.now()
        delta = current_datetime - datetime_from_db
        days_diff = delta.days
        if days_diff>7:
            m="select paid from book_issue_teach where Teacher_Id='%s'"%(i[0])
            mycursor.execute(m)
            d=mycursor.fetchone()[0]
            price =((days_diff-7)*5)-int(d)
            qu="Update book_issue_teach set fine=%s where Teacher_Id='%s'"%(price,i[0]) 
            mycursor.execute(qu)
            mydb.commit()

def update():
    q="Select Student_Id from book_issue"
    mycursor.execute(q)
    c=mycursor.fetchall()
    for i in c:
        p="Select Issue_date from book_issue where Student_Id='%s'"%i
        mycursor.execute(p)
        d=mycursor.fetchone()[0]
        datetime_from_db = datetime.strptime(str(d), '%Y-%m-%d %H:%M:%S')
        current_datetime = datetime.now()
        delta = current_datetime - datetime_from_db
        days_diff = delta.days
        if days_diff>7:
            m="select paid from book_issue where Student_Id='%s'"%(i[0])
            mycursor.execute(m)
            d=mycursor.fetchone()[0]
            price =(days_diff-7)*5-int(d)
            qu="Update book_issue set fine=%s where Student_Id='%s'"%(price,i[0]) 
            mycursor.execute(qu)
            mydb.commit()

def view_book_list():
    root = Tk()
    root.title("Library Management System")
    root.configure(bg="#b7413e")
    root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(),root.winfo_screenheight()))
    root.overrideredirect(True)
    e=Label(root,width=40,text='List of Books Available',borderwidth=5, relief='ridge',anchor='center',bg='black',fg='white',font=('Courier New Baltic',25)).pack(side="top",fill='x')
    
    btn13 = Button(root,text="Exit...",bg='black', fg='white',padx=50,width=30,font=('Courier New Baltic',18),command=root.destroy).pack(side="bottom",pady=10,padx=50)
    
    btn02 = Button(root,text="Delete Book",bg='black', fg='white',padx=50,width=30,font=('Courier New Baltic',18),command=lambda: [root.destroy(),del_book()]).pack(side="bottom",pady=10,padx=50)
    
    btn2 = Button(root,text="Add Books",bg='black', fg='white',padx=50,width=30,font=('Courier New Baltic',18),command=lambda: [root.destroy(),add_book()]).pack(side="bottom",pady=10,padx=50)
    
    tree=ttk.Treeview(root,height=100)
    tree["columns"]=("Serial Number","Book name","Author","Number of books available")
    tree["show"]="headings"
    s = ttk.Style(root)
    s.theme_use('clam')
    s.configure('Treeview.Heading', background="black",foreground="white",font=['Times',22,'normal'])
    s.configure('Treeview', background="#b7ffff", fieldbackground="#b7ffff",foreground="black",font=['Courier New Baltic',12],rowheight=29)

    tree.column("Serial Number",width=200,anchor=CENTER)
    tree.column("Book name",width=350,anchor=CENTER)
    tree.column("Author",width=350,anchor=CENTER)
    tree.column("Number of books available",width=350,anchor=CENTER)
    tree.heading("Serial Number",text="Serial Number",anchor=CENTER)
    tree.heading("Book name",text="Book name",anchor=CENTER)
    tree.heading("Author",text="Author",anchor=CENTER)
    tree.heading("Number of books available",text="Number of books available",anchor=CENTER)

    mycursor.execute('select * from booklist')
    i=0
    for booklist in mycursor:
        tree.insert('',i,text="",values=(booklist[0],booklist[1],booklist[2],booklist[3]))
        i=i+1
    hsb=ttk.Scrollbar(root,orient="vertical")
    hsb.configure(command=tree.yview)
    tree.configure(yscrollcommand=hsb.set)
    hsb.pack(fill=Y,side=RIGHT)
    tree.pack()
    root.mainloop()

def callback(event):
    global t
    t=event.widget.get()

def add_book_base():
    s_no = bookInfo1.get()
    title = bookInfo2.get()
    author = bookInfo3.get()
    number_available = bookInfo4.get()
    
    insertBooks = "insert into "+bookTable+" values ('"+s_no+"','"+title+"','"+author+"','"+number_available+"')"
    try:
        mycursor.execute(insertBooks)
        mydb.commit()
        messagebox.showinfo('Success',"Book added successfully")
    except:
        messagebox.showinfo("Error","Can't add data into Database")
    my_wind.destroy()
    
def add_book():
    global bookInfo1 ,bookInfo2, bookInfo3, bookInfo4, Canvas1, mycursor,mydb, bookTable, my_wind
    my_wind=Tk()
    my_wind.title("Library Management System")
    my_wind.geometry("{0}x{1}+0+0".format(my_wind.winfo_screenwidth(),my_wind.winfo_screenheight()))
    my_wind.overrideredirect(True)
    
    bookTable = "booklist"
    Canvas1 = Canvas(my_wind) 
    Canvas1.config(bg="#ff6e40")
    Canvas1.pack(expand=True,fill=BOTH)   
    headingFrame1 = Frame(my_wind,bg="#FFBB00",bd=5)
    headingFrame1.place(relx=0.25,rely=0.1,relwidth=0.5,relheight=0.13)
    headingLabel = Label(headingFrame1, text="Add Books", bg='black', fg='white', font=('Courier New Baltic',22))
    headingLabel.place(relx=0,rely=0, relwidth=1, relheight=1)
    labelFrame = Frame(my_wind,bg='black')
    labelFrame.place(relx=0.1,rely=0.4,relwidth=0.8,relheight=0.4)
        
    # Book ID
    lb1 = Label(labelFrame,text="Book ID : ", bg='black', fg='white', font=('Courier New Baltic',15))
    lb1.place(relx=0.05,rely=0.2, relheight=0.08)
    bookInfo1 = Entry(labelFrame)
    bookInfo1.place(relx=0.3,rely=0.2, relwidth=0.62, relheight=0.08)
        
    # Title
    lb2 = Label(labelFrame,text="Title : ", bg='black', fg='white', font=('Courier New Baltic',15))
    lb2.place(relx=0.05,rely=0.35, relheight=0.08)
    bookInfo2 = Entry(labelFrame)
    bookInfo2.place(relx=0.3,rely=0.35, relwidth=0.62, relheight=0.08)
        
    # Book Author
    lb3 = Label(labelFrame,text="Author : ", bg='black', fg='white', font=('Courier New Baltic',15))
    lb3.place(relx=0.05,rely=0.50, relheight=0.08)   
    bookInfo3 = Entry(labelFrame)
    bookInfo3.place(relx=0.3,rely=0.50, relwidth=0.62, relheight=0.08)
        
    # Book Status
    lb4 = Label(labelFrame,text="Number of books available : ", bg='black', fg='white', font=('Courier New Baltic',15))
    lb4.place(relx=0.05,rely=0.65, relheight=0.08)
    bookInfo4 = Entry(labelFrame)
    bookInfo4.place(relx=0.3,rely=0.65, relwidth=0.62, relheight=0.08)
        
    #Submit Button
    SubmitBtn = Button(my_wind,text="SUBMIT",bg='#d1ccc0', fg='black', font=('Courier New Baltic',15),command=add_book_base)
    SubmitBtn.place(relx=0.28,rely=0.9, relwidth=0.18,relheight=0.08)

    #Quit Button
    quitBtn = Button(my_wind,text="Quit",bg='#f7f1e3', fg='black', font=('Courier New Baltic',15),command=my_wind.destroy)
    quitBtn.place(relx=0.53,rely=0.9, relwidth=0.18,relheight=0.08)
    
    my_wind.mainloop()

def del_book_base():
    book_id_1 = book_id.get()
    
    delete = "delete from booklist where S_No=('%s')"%(book_id_1)
    q="SELECT COUNT(*) FROM booklist WHERE S_No=('%s')"%(book_id_1)
    mycursor.execute(q)
    c=mycursor.fetchall()
    try:
        if (c[-1][-1])==1:
            mycursor.execute(delete)
            mydb.commit()
            messagebox.showinfo('Success',"Book details deleted successfully")
        else:
            messagebox.showinfo("Error","Can't delete data")
    except:
        messagebox.showinfo("Error","Can't delete data")
    my_wind.destroy()
def del_book():
    global book_id,Canvas1, mycursor,mydb,my_wind
    my_wind=Tk()
    my_wind.title("Library Management System")
    my_wind.geometry("{0}x{1}+0+0".format(my_wind.winfo_screenwidth(),my_wind.winfo_screenheight()))
    my_wind.overrideredirect(True)
    
    Canvas1 = Canvas(my_wind) 
    Canvas1.config(bg="#ff4633")
    Canvas1.pack(expand=True,fill=BOTH)   
    headingFrame1 = Frame(my_wind,bg="#FFBB00",bd=5)
    headingFrame1.place(relx=0.25,rely=0.1,relwidth=0.5,relheight=0.13)
    headingLabel = Label(headingFrame1, text="Book Detail", bg='black', fg='white', font=('Courier New Baltic',20))
    headingLabel.place(relx=0,rely=0, relwidth=1, relheight=1)
    labelFrame = Frame(my_wind,bg='black')
    labelFrame.place(relx=0.1,rely=0.4,relwidth=0.8,relheight=0.3)

    def selected(event):
        book_name.delete(0,END)
        p=book_id.get()
        q="Select Book_name from  booklist where S_No='"+p+"'"
        mycursor.execute(q)
        c=mycursor.fetchone()[0]
        s1=c.replace("{","")
        s=s1.replace("}","")
        book_name.insert(END,s)
    q="Select S_No from booklist"
    mycursor.execute(q)
    c=mycursor.fetchall()
        
    n = StringVar()
    def search(event):
        value=event.widget.get()
        if value=='':
            book_id['values']=c
        else:
            data=[]
            for item in c:
                if value in item:
                    data.append(item)
            book_id['values']=data

    #Book Id
    lb1 = Label(labelFrame,text="Book Id : ", bg='black', fg='white',font=('Courier New Baltic',15))
    lb1.place(relx=0.05,rely=0.26, relheight=0.08)
    book_id = ttk.Combobox(my_wind, width = 27, textvariable = n)
    book_id['values']=[r for r in c]
    book_id.bind('<<KeyRelease>>',search)
    book_id.bind('<<ComboboxSelected>>',selected)
    book_id.place(relx=0.35,rely=0.47, relwidth=0.53, relheight=0.03)

    # Book Name    
    lb2 = Label(labelFrame,text="Book Name : ", bg='black', fg='white', font=('Courier New Baltic',15))
    lb2.place(relx=0.05,rely=0.58, relheight=0.08)
    book_name= Entry(labelFrame)
    book_name.place(relx=0.31,rely=0.58, relwidth=0.665, relheight=0.1)
            
    #Delete Button
    SubmitBtn = Button(my_wind,text="Delete",bg='#d1ccc0', fg='black', font=('Courier New Baltic',15),command=del_book_base)
    SubmitBtn.place(relx=0.28,rely=0.9, relwidth=0.18,relheight=0.08)

    #Quit Button    
    quitBtn = Button(my_wind,text="Quit",bg='#f7f1e3', fg='black', font=('Courier New Baltic',15),command=my_wind.destroy)
    quitBtn.place(relx=0.53,rely=0.9, relwidth=0.18,relheight=0.08)
    
    my_wind.mainloop() 

def add_teacher_base():
    tech_id_1 = tech_id.get()
    tech_name_1 = tech_name.get()
    gmail_1=gmail.get()
    insert_tech = "insert into "+teacher_table+" values ('"+tech_id_1+"','"+tech_name_1+"','"+gmail_1+"')"
    try:
        mycursor.execute(insert_tech)
        mydb.commit()
        messagebox.showinfo('Success',"Teacher's details added successfully")
    except:
        messagebox.showinfo("Error","Can't add data into Database")
    my_wind.destroy()
def add_teacher():
    global tech_id,tech_name, Canvas1, mycursor,mydb, teacher_table, my_wind,gmail
    my_wind=Tk()
    my_wind.title("Library Management System")
    my_wind.geometry("{0}x{1}+0+0".format(my_wind.winfo_screenwidth(),my_wind.winfo_screenheight()))
    my_wind.overrideredirect(True)
    
    teacher_table = "teachername"
    Canvas1 = Canvas(my_wind) 
    Canvas1.config(bg="#ff4633")
    Canvas1.pack(expand=True,fill=BOTH)   
    headingFrame1 = Frame(my_wind,bg="#FFBB00",bd=5)
    headingFrame1.place(relx=0.25,rely=0.1,relwidth=0.5,relheight=0.13)
    headingLabel = Label(headingFrame1, text="Add Teacher Details", bg='black', fg='white', font=('Courier New Baltic',20))
    headingLabel.place(relx=0,rely=0, relwidth=1, relheight=1)
    labelFrame = Frame(my_wind,bg='black')
    labelFrame.place(relx=0.1,rely=0.4,relwidth=0.8,relheight=0.3)
        
    # Teacher ID
    lb1 = Label(labelFrame,text="Teacher ID : ", bg='black', fg='white',font=('Courier New Baltic',15))
    lb1.place(relx=0.05,rely=0.35, relheight=0.08)
    tech_id = Entry(labelFrame)
    tech_id.place(relx=0.3,rely=0.35, relwidth=0.62, relheight=0.08)
        
    # Teacher name
    lb2 = Label(labelFrame,text="Teacher Name : ", bg='black', fg='white', font=('Courier New Baltic',15))
    lb2.place(relx=0.05,rely=0.55, relheight=0.08)
    tech_name = Entry(labelFrame)
    tech_name.place(relx=0.3,rely=0.55, relwidth=0.62, relheight=0.08)

    #Gmail ID
    lb2 = Label(labelFrame,text="Gmail Id : ", bg='black', fg='white', font=('Courier New Baltic',15))
    lb2.place(relx=0.05,rely=0.75, relheight=0.08)
    gmail = Entry(labelFrame)
    gmail.place(relx=0.3,rely=0.75, relwidth=0.62, relheight=0.08)
        
    #Submit Button
    SubmitBtn = Button(my_wind,text="SUBMIT",bg='#d1ccc0', fg='black', font=('Courier New Baltic',15),command=add_teacher_base)
    SubmitBtn.place(relx=0.28,rely=0.9, relwidth=0.18,relheight=0.08)

    #Quit Button
    quitBtn = Button(my_wind,text="Quit",bg='#f7f1e3', fg='black', font=('Courier New Baltic',15),command=my_wind.destroy)
    quitBtn.place(relx=0.53,rely=0.9, relwidth=0.18,relheight=0.08)
    
    my_wind.mainloop()

def add_student_base():
    Stu_id_1= Stu_id.get()
    Stu_name_1 = Stu_name.get()
    Stu_class_1=Stu_class.get()
    gmail_1=gmail.get()
    insert_Stu = "insert into "+stu_table+" values ('"+Stu_id_1+"','"+Stu_name_1+"','"+Stu_class_1+"','"+gmail_1+"')"
    try:
        mycursor.execute(insert_Stu)
        mydb.commit()
        messagebox.showinfo('Success',"Student's details added successfully")
    except:
        messagebox.showinfo("Error","Can't add data into Database")
    my_wind.destroy()
def add_student():
    global Stu_id,Stu_name,Stu_class, Canvas1, mycursor,mydb, stu_table, my_wind,gmail
    my_wind=Tk()
    my_wind.title("Library Management System")
    my_wind.geometry("{0}x{1}+0+0".format(my_wind.winfo_screenwidth(),my_wind.winfo_screenheight()))
    my_wind.overrideredirect(True)
    
    stu_table = "studentname"
    Canvas1 = Canvas(my_wind) 
    Canvas1.config(bg="#b7413e")
    Canvas1.pack(expand=True,fill=BOTH)   
    headingFrame1 = Frame(my_wind,bg="#FFBB00",bd=5)
    headingFrame1.place(relx=0.25,rely=0.1,relwidth=0.5,relheight=0.13)
    headingLabel = Label(headingFrame1, text="Add Student Details", bg='black', fg='white', font=('Courier New Baltic',20))
    headingLabel.place(relx=0,rely=0, relwidth=1, relheight=1)
    labelFrame = Frame(my_wind,bg='black')
    labelFrame.place(relx=0.1,rely=0.4,relwidth=0.8,relheight=0.3)
        
    # Student ID
    lb1 = Label(labelFrame,text="Student ID : ", bg='black', fg='white',font=('Courier New Baltic',15))
    lb1.place(relx=0.05,rely=0.25, relheight=0.08)
    Stu_id = Entry(labelFrame)
    Stu_id.place(relx=0.3,rely=0.25, relwidth=0.62, relheight=0.08)
        
    # Student name
    lb2 = Label(labelFrame,text="Student Name : ", bg='black', fg='white', font=('Courier New Baltic',15))
    lb2.place(relx=0.05,rely=0.45, relheight=0.08)
    Stu_name = Entry(labelFrame)
    Stu_name.place(relx=0.3,rely=0.45, relwidth=0.62, relheight=0.08)

    # Student class
    lb2 = Label(labelFrame,text="Student class : ", bg='black', fg='white', font=('Courier New Baltic',15))
    lb2.place(relx=0.05,rely=0.65, relheight=0.08)
    Stu_class = Entry(labelFrame)
    Stu_class.place(relx=0.3,rely=0.65, relwidth=0.62, relheight=0.08)

    #Gmail Id
    lb2 = Label(labelFrame,text="Gmail Id : ", bg='black', fg='white', font=('Courier New Baltic',15))
    lb2.place(relx=0.05,rely=0.85, relheight=0.08)
    gmail = Entry(labelFrame)
    gmail.place(relx=0.3,rely=0.85, relwidth=0.62, relheight=0.08)
        
    #Submit Button
    SubmitBtn = Button(my_wind,text="SUBMIT",bg='#d1ccc0', fg='black', font=('Courier New Baltic',15),command=add_student_base)
    SubmitBtn.place(relx=0.28,rely=0.9, relwidth=0.18,relheight=0.08)

    #Quit Button
    quitBtn = Button(my_wind,text="Quit",bg='#f7f1e3', fg='black', font=('Courier New Baltic',15),command=my_wind.destroy)
    quitBtn.place(relx=0.53,rely=0.9, relwidth=0.18,relheight=0.08)
    
    my_wind.mainloop()

def issue_tech_base():
    tech_id_issue_1 = tech_id_issue.get()
    book_name_issue_1=book_name_issue.get()
    now = datetime.now()
    a=str(now.strftime("%Y-%m-%d %H:%M:%S"))
    c=0
    mycursor.execute("SELECT * FROM teachername")
    myresult = mycursor.fetchall()
    for x in myresult:
        if x[0]==tech_id_issue_1:
            c+=1
        if c==1:
            query="SELECT Teacher_name FROM teachername where Teacher_Id='%s'"%(tech_id_issue_1)
            mycursor.execute(query)
            myresult = mycursor.fetchone()
            for y in myresult:
                tech_name_issue_1=y
                c+=1
                if c==2:
                    mycursor.execute("SELECT * FROM booklist")
                    myresult = mycursor.fetchall()
                    for z in myresult:
                        if z[1]==book_name_issue_1:
                            a="SELECT Quantity from booklist where Book_name='%s'"%(book_name_issue_1)
                            mycursor.execute(a)
                            myresult = mycursor.fetchone()
                            if myresult[0]>0:
                                c+=1
                                b="update booklist set Quantity=Quantity-1 where Book_name='%s'"%(book_name_issue_1)
                                mycursor.execute(b)
    if c==3:
        insert_tech_base = "INSERT INTO book_issue_teach(Teacher_Id,Teacher_name,Book_name) VALUES ('%s','%s','%s')"%(tech_id_issue_1,tech_name_issue_1,book_name_issue_1)
        p="select Gmail from teachername where Teacher_Id='%s'"%(tech_id_issue_1)
        mycursor.execute(p)
        gml=mycursor.fetchone()
        try:
            mycursor.execute(insert_tech_base)
            mydb.commit()
            email_sender = 'rashijain1710@gmail.com'
            email_password = 'vgadxfsxgjksnvnf'
            email_receiver = gml
            subject = 'Library Management System'
            body ='Issued book '+book_name_issue_1
            em = EmailMessage()
            em['From'] = email_sender
            em['To'] = email_receiver
            em['Subject'] = subject
            em.set_content(body)
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
                smtp.login(email_sender, email_password)
                smtp.sendmail(email_sender, email_receiver, em.as_string())
            messagebox.showinfo('Success',"Details added successfully")
        except:
            messagebox.showinfo("Error","Can't send mail but data added")
    if c==0 or c==1 or c==2:
        messagebox.showinfo("Error","Can't add data into Database")
    my_wind.destroy()

def issue_tech():
    global tech_id_issue,book_name_issue, Canvas1, mycursor,mydb,issue_tech_table, my_wind
    my_wind=Tk()
    my_wind.title("Library Management System")
    my_wind.geometry("{0}x{1}+0+0".format(my_wind.winfo_screenwidth(),my_wind.winfo_screenheight()))
    my_wind.overrideredirect(True)
    
    issue_tech_table= "book_issue_teach"
    Canvas1 = Canvas(my_wind) 
    Canvas1.config(bg="#b7413e")
    Canvas1.pack(expand=True,fill=BOTH)   
    headingFrame1 = Frame(my_wind,bg="#FFBB00",bd=5)
    headingFrame1.place(relx=0.25,rely=0.1,relwidth=0.5,relheight=0.13)
    headingLabel = Label(headingFrame1, text="Issue Books to Teacher", bg='black', fg='white', font=('Courier New Baltic',20))
    headingLabel.place(relx=0,rely=0, relwidth=1, relheight=1)
    labelFrame = Frame(my_wind,bg='black')
    labelFrame.place(relx=0.1,rely=0.4,relwidth=0.8,relheight=0.3)
    
    # Teacher ID
    q="Select Teacher_Id from teachername"
    mycursor.execute(q)
    c=[]
    for i in mycursor.fetchall():
        c.append(i[0])
    n = StringVar()
    lb1 = Label(labelFrame,text="Teacher ID : ", bg='black', fg='white',font=('Courier New Baltic',15))
    lb1.place(relx=0.05,rely=0.26, relheight=0.08)
    tech_id_issue = ttk.Combobox(my_wind, width = 27,values=c ,textvariable = n)

    tech_id_issue.place(relx=0.35,rely=0.47, relwidth=0.53, relheight=0.03)
    tech_id_issue.current()
    
    # Book Name
    q="Select Book_name from booklist"
    mycursor.execute(q)
    c=[]
    for i in mycursor.fetchall():
        s1=i[0].replace("{","")
        s=s1.replace("}","")
        c.append(s)
    n = StringVar()
    def search(event):
        value=event.widget.get()
        if value=='':
            book_name_issue['values']=c
        else:
            data=[]
            for item in c:
                if value.lower() in item.lower():
                    data.append(item)
            book_name_issue['values']=data
    lb2 = Label(labelFrame,text="Book Name : ", bg='black', fg='white', font=('Courier New Baltic',15))
    lb2.place(relx=0.05,rely=0.58, relheight=0.08)
    book_name_issue = ttk.Combobox(my_wind, width = 27,values=c ,textvariable = n)
    book_name_issue.place(relx=0.35,rely=0.57, relwidth=0.53, relheight=0.03)
    book_name_issue.bind('<KeyRelease>',search)
    book_name_issue.current()
    # Date
    now=datetime.now()
    a= str(now.strftime("%Y-%m-%d %H:%M:%S "))
    lb2 = Label(labelFrame,text="Datetime Entered(Default): ", bg='black', fg='white', font=('Courier New Baltic',15))
    lb2.place(relx=0.05,rely=0.85, relheight=0.08)
    lb3 = Label(labelFrame,text=a, bg='black', fg='white', font=('Courier New Baltic',15))
    lb3.place(relx=0.3,rely=0.85, relwidth=0.62, relheight=0.08)
        
    #Issue Button
    SubmitBtn = Button(my_wind,text="Issue",bg='#d1ccc0', fg='black', font=('Courier New Baltic',15),command=issue_tech_base)
    SubmitBtn.place(relx=0.28,rely=0.85, relwidth=0.18,relheight=0.08)

    #Quit Button
    quitBtn = Button(my_wind,text="Quit",bg='#f7f1e3', fg='black', font=('Courier New Baltic',15),command=my_wind.destroy)
    quitBtn.place(relx=0.53,rely=0.85, relwidth=0.18,relheight=0.08)
    
    my_wind.mainloop()
    
def issue_stu_base():
    stu_id_issue_1 = stu_id_issue.get()
    book_name_issue_1=book_name_issue.get()
    now = datetime.now()
    a=str(now.strftime("%Y-%m-%d %H:%M:%S"))
    c=0
    mycursor.execute("SELECT * FROM studentname")
    myresult = mycursor.fetchall()
    for x in myresult:
        if str(x[0])==stu_id_issue_1:
            c+=1
        if c==1:
            query="SELECT Student_name FROM studentname where Stu_Id='%s'"%(stu_id_issue_1)
            mycursor.execute(query)
            myresult = mycursor.fetchone()
            for y in myresult:
                stu_name_issue_1=y
                c+=1
                if c==2:
                    mycursor.execute("SELECT * FROM booklist")
                    myresult = mycursor.fetchall()
                    for z in myresult:
                        if z[1]==book_name_issue_1:
                            a="SELECT Quantity from booklist where Book_name='%s'"%(book_name_issue_1)
                            mycursor.execute(a)
                            myresult = mycursor.fetchone()
                            if myresult[0]>0:
                                c+=1
                                b="update booklist set Quantity=Quantity-1 where Book_name='%s'"%(book_name_issue_1)
                                mycursor.execute(b)
    if c==3:
        insert_stu_base = "INSERT INTO book_issue(Student_Id,Student_name,Book_name) VALUES ('%s','%s','%s')"%(stu_id_issue_1,stu_name_issue_1,book_name_issue_1)
        p="select Gmail from studentname where Stu_Id='%s'"%(stu_id_issue_1)
        mycursor.execute(p)
        gml=mycursor.fetchone()
        try:
            mycursor.execute(insert_stu_base)
            mydb.commit()
            email_sender = 'rashijain1710@gmail.com'
            email_password = 'vgadxfsxgjksnvnf'
            email_receiver = gml
            subject = 'Library Management System'
            body ='Issued book '+book_name_issue_1
            em = EmailMessage()
            em['From'] = email_sender
            em['To'] = email_receiver
            em['Subject'] = subject
            em.set_content(body)
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
                smtp.login(email_sender, email_password)
                smtp.sendmail(email_sender, email_receiver, em.as_string())
            messagebox.showinfo('Success',"Details added successfully")
        except:
            messagebox.showinfo("Error","Can't send mail but data added")
    if c==0:
        messagebox.showinfo("Error","Student ID invalid! Can't add data into Database")
    if c==1:
        messagebox.showinfo("Error","Student Name invalid! Can't add data into Database")
    if c==2:
        messagebox.showinfo("Error","Book name invalid! Can't add data into Database")
    my_wind.destroy()
def issue_stu():
    global stu_id_issue, stu_name_issue, book_name_issue, Canvas1, mycursor,mydb,issue_stu_table, my_wind
    my_wind=Tk()
    my_wind.title("Library Management System")
    my_wind.geometry("{0}x{1}+0+0".format(my_wind.winfo_screenwidth(),my_wind.winfo_screenheight()))
    my_wind.overrideredirect(True)
    
    issue_tech_table= "book_issue"
    Canvas1 = Canvas(my_wind) 
    Canvas1.config(bg="#b7413e")
    Canvas1.pack(expand=True,fill=BOTH)   
    headingFrame1 = Frame(my_wind,bg="#FFBB00",bd=5)
    headingFrame1.place(relx=0.25,rely=0.1,relwidth=0.5,relheight=0.13)
    headingLabel = Label(headingFrame1, text="Issue Books to Student", bg='black', fg='white', font=('Courier New Baltic',20))
    headingLabel.place(relx=0,rely=0, relwidth=1, relheight=1)
    labelFrame = Frame(my_wind,bg='black')
    labelFrame.place(relx=0.1,rely=0.4,relwidth=0.8,relheight=0.3)
        
    # Student ID
    q="Select Stu_Id from studentname"
    mycursor.execute(q)
    c=[]
    for i in mycursor.fetchall():
        c.append(i[0])
    n = StringVar()
    lb1 = Label(labelFrame,text="Student ID : ", bg='black', fg='white',font=('Courier New Baltic',15))
    lb1.place(relx=0.05,rely=0.26, relheight=0.08)
    stu_id_issue = ttk.Combobox(my_wind, width = 27,values=c ,textvariable = n)
    stu_id_issue.place(relx=0.35,rely=0.47, relwidth=0.53, relheight=0.03)
    stu_id_issue.current()    
    # Book Name
    q="Select Book_name from booklist"
    mycursor.execute(q)
    c=[]
    for i in mycursor.fetchall():
        s1=i[0].replace("{","")

        s=s1.replace("}","")
        c.append(s)
    n = StringVar()
    def search(event):
        value=event.widget.get()
        if value=='':
            book_name_issue['values']=c
        else:
            data=[]
            for item in c:
                if value.lower() in item.lower():
                    data.append(item)
            book_name_issue['values']=data
    lb2 = Label(labelFrame,text="Book Name : ", bg='black', fg='white', font=('Courier New Baltic',15))
    lb2.place(relx=0.05,rely=0.58, relheight=0.08)
    book_name_issue = ttk.Combobox(my_wind, width = 27,values=c ,textvariable = n)
    book_name_issue.place(relx=0.35,rely=0.57, relwidth=0.53, relheight=0.03)
    book_name_issue.bind('<KeyRelease>',search)
    book_name_issue.current()
    # Date
    now=datetime.now()
    a= str(now.strftime("%Y-%m-%d %H:%M:%S "))
    lb2 = Label(labelFrame,text="Datetime Entered(Default): ", bg='black', fg='white', font=('Courier New Baltic',15))
    lb2.place(relx=0.05,rely=0.85, relheight=0.08)
    lb3 = Label(labelFrame,text=a, bg='black', fg='white', font=('Courier New Baltic',15))
    lb3.place(relx=0.3,rely=0.85, relwidth=0.62, relheight=0.08)
        
    #Submit Button
    SubmitBtn = Button(my_wind,text="Issue",bg='#d1ccc0', fg='black', font=('Courier New Baltic',15),command=issue_stu_base)
    SubmitBtn.place(relx=0.28,rely=0.85, relwidth=0.18,relheight=0.08)

    #Quit Button
    quitBtn = Button(my_wind,text="Quit",bg='#f7f1e3', fg='black', font=('Courier New Baltic',15),command=my_wind.destroy)
    quitBtn.place(relx=0.53,rely=0.85, relwidth=0.18,relheight=0.08)
    
    my_wind.mainloop()

def return_tech_base():
    tech_id_return_1 = tech_id_return.get()
    book_name_return_1=book_name_return.get()
    now = datetime.now()
    a=str(now.strftime("%Y-%m-%d %H:%M:%S"))


    c=0
    p="select fine from book_issue_teach where Teacher_Id='%s'"%(tech_id_return_1)
    mycursor.execute(p)
    r =mycursor.fetchone()
    if r[0]==0:
        mycursor.execute("SELECT * FROM book_issue_teach")
        myresult = mycursor.fetchall()
        for x in myresult:
            if x[0]==tech_id_return_1:
                c+=1
            if c==1:
                query="SELECT Teacher_name FROM book_issue_teach where Teacher_Id='%s'"%(tech_id_return_1)
                mycursor.execute(query)
                myresult = mycursor.fetchall()
                for y in myresult:
                    tech_name_return_1=y[0]
                    c+=1
                    if c==2:
                        query="SELECT Book_name FROM book_issue_teach where Teacher_Id='%s'"%(tech_id_return_1)
                        mycursor.execute(query)
                        myresult = mycursor.fetchone()[0]
                        if myresult==book_name_return_1:
                            c+=1
                            b="update booklist set Quantity=Quantity+1 where Book_name='%s'"%(book_name_return_1)
                            mycursor.execute(b)

                    
            if c==3:
                insert_tech_base = "INSERT INTO book_return_teach(Teacher_Id,Teacher_name,Book_name) VALUES ('%s','%s','%s')"%(tech_id_return_1,tech_name_return_1,book_name_return_1)
                p="select Gmail from teachername where Teacher_Id='%s'"%(tech_id_return_1)
                mycursor.execute(p)
                gml=mycursor.fetchone()
                mycursor.execute(insert_tech_base)
                mycursor.execute("Delete from book_issue_teach where Teacher_Id='%s'"%(tech_id_return_1))
                mydb.commit()
                try:
                
                    email_sender = 'rashijain1710@gmail.com'
                    email_password = 'vgadxfsxgjksnvnf'
                    email_receiver = gml
                    subject = 'Library Management System'
                    body ='Returned book '+book_name_return_1
                    em = EmailMessage()
                    em['From'] = email_sender
                    em['To'] = email_receiver
                    em['Subject'] = subject
                    em.set_content(body)
                    context = ssl.create_default_context()
                    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
                        smtp.login(email_sender, email_password)
                        smtp.sendmail(email_sender, email_receiver, em.as_string())
                    messagebox.showinfo('Success',"Details added successfully")
                except:
                    messagebox.showinfo("Error","Can't send mail but data added")
        if c==0:
            messagebox.showinfo("Error","Teacher ID invalid! Can't add data into Database")
        if c==1:
            messagebox.showinfo("Error","Teacher Name invalid! Can't add data into Database")
        if c==2:
            messagebox.showinfo("Error","Book name invalid! Can't add data into Database")
    else:
        messagebox.showinfo("Error","Fine not cleared")
    my_wind.destroy()

def return_tech():
    global tech_id_return,book_name_return, Canvas1, mycursor,mydb,return_tech_table, my_wind
    my_wind=Tk()
    my_wind.title("Library Management System")
    my_wind.geometry("{0}x{1}+0+0".format(my_wind.winfo_screenwidth(),my_wind.winfo_screenheight()))
    my_wind.overrideredirect(True)
    
    return_tech_table= "book_return_teach"
    Canvas1 = Canvas(my_wind) 
    Canvas1.config(bg="#b7413e")
    Canvas1.pack(expand=True,fill=BOTH)   
    headingFrame1 = Frame(my_wind,bg="#FFBB00",bd=5)
    headingFrame1.place(relx=0.25,rely=0.1,relwidth=0.5,relheight=0.13)
    headingLabel = Label(headingFrame1, text="Return Books-Teacher", bg='black', fg='white', font=('Courier New Baltic',20))
    headingLabel.place(relx=0,rely=0, relwidth=1, relheight=1)
    labelFrame = Frame(my_wind,bg='black')
    labelFrame.place(relx=0.1,rely=0.4,relwidth=0.8,relheight=0.3)
    def selected(event):
        book_name_return.delete(0,END)
        p=tech_id_return.get()
        q="Select Book_name from  book_issue_teach where Teacher_Id='"+p+"'"
        mycursor.execute(q)
        c=mycursor.fetchone()[0]
        s1=c.replace("{","")
        s=s1.replace("}","")
        book_name_return.insert(END,s)
    # Teacher ID
    q="Select DISTINCT Teacher_Id from book_issue_teach"
    mycursor.execute(q)
    c=[]
    for i in mycursor.fetchall():
        c.append(i[0])
    n = StringVar()
    lb1 = Label(labelFrame,text="Teacher ID : ", bg='black', fg='white',font=('Courier New Baltic',15))
    lb1.place(relx=0.05,rely=0.26, relheight=0.08)
    tech_id_return =ttk.Combobox(my_wind, width = 27,values=c ,textvariable = n)
    tech_id_return.bind('<<ComboboxSelected>>',selected)
    tech_id_return.place(relx=0.35,rely=0.47, relwidth=0.53, relheight=0.03)

    # Book Name    
    lb2 = Label(labelFrame,text="Book Name : ", bg='black', fg='white', font=('Courier New Baltic',15))
    lb2.place(relx=0.05,rely=0.58, relheight=0.08)
    book_name_return = Entry(labelFrame)
    book_name_return.place(relx=0.31,rely=0.58, relwidth=0.665, relheight=0.1)
    
    # Date
    now=datetime.now()
    a= str(now.strftime("%Y-%m-%d %H:%M:%S "))
    lb2 = Label(labelFrame,text="Datetime Entered(Default): ", bg='black', fg='white', font=('Courier New Baltic',15))
    lb2.place(relx=0.05,rely=0.85, relheight=0.08)
    lb3 = Label(labelFrame,text=a, bg='black', fg='white', font=('Courier New Baltic',15))
    lb3.place(relx=0.3,rely=0.85, relwidth=0.62, relheight=0.08)
        
    #Return Button
    SubmitBtn = Button(my_wind,text="Return",bg='#d1ccc0', fg='black', font=('Courier New Baltic',15),command=return_tech_base)
    SubmitBtn.place(relx=0.28,rely=0.85, relwidth=0.18,relheight=0.08)

    #Quit Button
    quitBtn = Button(my_wind,text="Quit",bg='#f7f1e3', fg='black', font=('Courier New Baltic',15),command=my_wind.destroy)
    quitBtn.place(relx=0.53,rely=0.85, relwidth=0.18,relheight=0.08)
    
    my_wind.mainloop()

def return_stu_base():
    stu_id_return_1 = stu_id_return.get()
    book_name_return_1=book_name_return.get()
    now = datetime.now()
    a=str(now.strftime("%Y-%m-%d %H:%M:%S"))
    
    c=0
    p="select fine from book_issue where Student_Id='%s'"%(stu_id_return_1)
    mycursor.execute(p)
    r =mycursor.fetchone()
    if r[0]==0:
        mycursor.execute("SELECT * FROM book_issue")
        myresult = mycursor.fetchall()
        for x in myresult:
            if x[0]==int(stu_id_return_1):
                c+=1
            if c==1:
                query="SELECT Student_name FROM book_issue where Student_Id='%s'"%(stu_id_return_1)
                mycursor.execute(query)
                myresult = mycursor.fetchall()
                for y in myresult:
                    stu_name_return_1=y[0]
                    c+=1
                    if c==2:
                        query="SELECT Book_name FROM book_issue where Student_Id='%s'"%(stu_id_return_1)
                        mycursor.execute(query)
                        myresult = mycursor.fetchone()[0]
                        if myresult==book_name_return_1:
                            c+=1
                            b="update booklist set Quantity=Quantity+1 where Book_name='%s'"%(book_name_return_1)
                            mycursor.execute(b)
           
            if c==3:
                insert_stu_base = "INSERT INTO book_return(Student_Id,Student_name,Book_name) VALUES ('%s','%s','%s')"%(stu_id_return_1,stu_name_return_1,book_name_return_1)
                p="select Gmail from studentname where Stu_Id='%s'"%(stu_id_return_1)
                mycursor.execute(p)
                gml=mycursor.fetchone()
                try:
                    mycursor.execute(insert_stu_base)
                    p="Delete from book_issue where Student_Id='%s'"%(stu_id_return_1)
                    mycursor.execute(p)
                    mydb.commit()
                    email_sender = 'rashijain1710@gmail.com'
                    email_password = 'vgadxfsxgjksnvnf'
                    email_receiver = gml
                    subject = 'Library Management System'
                    body ='Returned book '+book_name_return_1
                    em = EmailMessage()
                    em['From'] = email_sender
                    em['To'] = email_receiver
                    em['Subject'] = subject
                    em.set_content(body)
                    context = ssl.create_default_context()
                    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
                        smtp.login(email_sender, email_password)
                        smtp.sendmail(email_sender, email_receiver, em.as_string())
                    messagebox.showinfo('Success',"Details added successfully")
                except:
                    messagebox.showinfo("Error","Can't send mail but data added")
        if c==0:
            messagebox.showinfo("Error","Student ID invalid! Can't add data into Database")
        if c==1:
            messagebox.showinfo("Error","Student Name invalid! Can't add data into Database")
        if c==2:
            messagebox.showinfo("Error","Book name invalid! Can't add data into Database")
    else:
        messagebox.showinfo("Error","Fine not cleared")
    my_wind.destroy()
def return_stu():
    global stu_id_return,stu_name_return,book_name_return, Canvas1, mycursor,mydb,return_stu_table, my_wind
    my_wind=Tk()
    my_wind.title("Library Management System")
    my_wind.geometry("{0}x{1}+0+0".format(my_wind.winfo_screenwidth(),my_wind.winfo_screenheight()))
    my_wind.overrideredirect(True)
    
    return_stu_table= "book_return"
    Canvas1 = Canvas(my_wind) 
    Canvas1.config(bg="#b7413e")
    Canvas1.pack(expand=True,fill=BOTH)   
    headingFrame1 = Frame(my_wind,bg="#FFBB00",bd=5)
    headingFrame1.place(relx=0.25,rely=0.1,relwidth=0.5,relheight=0.13)
    headingLabel = Label(headingFrame1, text="Return Books-Student", bg='black', fg='white', font=('Courier New Baltic',20))
    headingLabel.place(relx=0,rely=0, relwidth=1, relheight=1)
    labelFrame = Frame(my_wind,bg='black')
    labelFrame.place(relx=0.1,rely=0.4,relwidth=0.8,relheight=0.3)
    def selected(event):
        book_name_return.delete(0,END)
        p=stu_id_return.get()
        q="Select Book_name from  book_issue where Student_Id='"+p+"'"
        mycursor.execute(q)
        c=mycursor.fetchone()[0]
        s1=c.replace("{","")
        s=s1.replace("}","")
        book_name_return.insert(END,s)  
    # Student ID
    q="Select DISTINCT Student_Id from book_issue"
    mycursor.execute(q)
    c=[]
    for i in mycursor.fetchall():
        c.append(i[0])
    n = StringVar()
    lb1 = Label(labelFrame,text="Student ID : ", bg='black', fg='white',font=('Courier New Baltic',15))
    lb1.place(relx=0.05,rely=0.26, relheight=0.08)
    stu_id_return = ttk.Combobox(my_wind, width = 27,values=c ,textvariable = n)
    stu_id_return.bind('<<ComboboxSelected>>',selected)
    stu_id_return.place(relx=0.35,rely=0.47, relwidth=0.53, relheight=0.03)

    # Book Name
    lb2 = Label(labelFrame,text="Book Name : ", bg='black', fg='white', font=('Courier New Baltic',15))
    lb2.place(relx=0.05,rely=0.58, relheight=0.08)
    book_name_return = Entry(labelFrame)
    book_name_return.place(relx=0.31,rely=0.58, relwidth=0.665, relheight=0.1)

    # Date
    now=datetime.now()
    a= str(now.strftime("%Y-%m-%d %H:%M:%S "))
    lb2 = Label(labelFrame,text="Datetime Entered(Default): ", bg='black', fg='white', font=('Courier New Baltic',15))
    lb2.place(relx=0.05,rely=0.85, relheight=0.08)
    lb3 = Label(labelFrame,text=a, bg='black', fg='white', font=('Courier New Baltic',15))
    lb3.place(relx=0.3,rely=0.85, relwidth=0.62, relheight=0.08)
        
    #Return Button
    SubmitBtn = Button(my_wind,text="Return",bg='#d1ccc0', fg='black', font=('Courier New Baltic',15),command=return_stu_base)
    SubmitBtn.place(relx=0.28,rely=0.85, relwidth=0.18,relheight=0.08)

    #Quit Button
    quitBtn = Button(my_wind,text="Quit",bg='#f7f1e3', fg='black', font=('Courier New Baltic',15),command=my_wind.destroy)
    quitBtn.place(relx=0.53,rely=0.85, relwidth=0.18,relheight=0.08)
    
    my_wind.mainloop()

def view_teacher_detail():

    root = Tk()
    root.title("Library Management System")
    root.configure(bg="#b7413e")
    root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(),root.winfo_screenheight()))
    root.overrideredirect(True)
    e=Label(root,width=40,text='Teachers Details',borderwidth=5,relief='ridge',anchor='center',bg='black',fg='white',font=('Courier New Baltic',25)).pack(side="top",fill='x')
    btn13 = Button(root,text="Exit...",bg='black', fg='white',padx=50, width=30,font=('Courier New Baltic',18),command=root.destroy).pack(side="bottom",pady=10,padx=50)
    btn09 = Button(root,text="Delete Teacher details",bg='black',padx=50, width=30, fg='white',font=('Courier New Baltic',18),command=lambda: [root.destroy(),del_teacher()]).pack(side="bottom",pady=10,padx=50)
    btn3 = Button(root,text="Add Teacher details",bg='black',padx=50, width=30, fg='white',font=('Courier New Baltic',18),command=lambda: [root.destroy(),add_teacher()]).pack(side="bottom",pady=10,padx=50)
    

    tree=ttk.Treeview(root,height=80)
    tree["columns"]=("Teacher Id","Teacher Name","Gmail")
    tree["show"]="headings"
    s = ttk.Style(root)
    s.theme_use('clam')
    s.configure('Treeview.Heading', background="black",foreground="white",font=['Times',22,'normal'])
    s.configure('Treeview', background="#b7ffff", fieldbackground="#b7ffff",foreground="black",font=['Courier New Baltic',12],rowheight=29)

    tree.column("Teacher Id",width=250,anchor=CENTER)
    tree.column("Teacher Name",width=350,anchor=CENTER)
    tree.column("Gmail",width=350,anchor=CENTER)
    tree.heading("Teacher Id",text="Teacher Id",anchor=CENTER)
    tree.heading("Teacher Name",text="Teacher Name",anchor=CENTER)
    tree.heading("Gmail",text="Gmail",anchor=CENTER)

    mycursor.execute('select * from teachername')
    i=0
    for teachername in mycursor:
        tree.insert('',i,text="",values=(teachername[0],teachername[1],teachername[2]))
        i=i+1
    hsb=ttk.Scrollbar(root,orient="vertical")
    hsb.configure(command=tree.yview)
    tree.configure(yscrollcommand=hsb.set)
    hsb.pack(fill=Y,side=RIGHT)
    tree.pack()
    root.mainloop()

def view_student_details():
    root = Tk()
    root.title("Library Management System")
    root.configure(bg="#b7413e")
    root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(),root.winfo_screenheight()))
    root.overrideredirect(True)
    e=Label(root,width=40,text='Student Details',borderwidth=5, relief='ridge',anchor='center',bg='black',fg='white',font=('Courier New Baltic',25)).pack(side="top",fill='x')
    btn13 = Button(root,text="Exit...",bg='black', fg='white',padx=50, width=30,font=('Courier New Baltic',18),command=root.destroy).pack(side="bottom",pady=10,padx=50)
    btn08 = Button(root,text="Delete Student Details",bg='black', width=30,padx=50, fg='white',font=('Courier New Baltic',18),command=lambda: [root.destroy(),del_stu()]).pack(side="bottom",pady=10,padx=50)

    btn4 = Button(root,text="Add Student details ",bg='black', width=30,padx=50, fg='white',font=('Courier New Baltic',18),command=lambda: [root.destroy(),add_student()]).pack(side="bottom",pady=10,padx=50)
    
    tree=ttk.Treeview(root,height=100)
    tree["columns"]=("Student Id","Student Name","Class","Gmail")
    tree["show"]="headings"
    s = ttk.Style(root)
    s.theme_use('clam')
    s.configure('Treeview.Heading', background="black",foreground="white",font=['Times',22,'normal'])
    s.configure('Treeview', background="#b7ffff", fieldbackground="#b7ffff",foreground="black",font=['Courier New Baltic',12],rowheight=29)

    tree.column("Student Id",width=250,anchor=CENTER)
    tree.column("Student Name",width=350,anchor=CENTER)
    tree.column("Class",width=350,anchor=CENTER)
    tree.column("Gmail",width=350,anchor=CENTER)
    tree.heading("Student Id",text="Student Id",anchor=CENTER)
    tree.heading("Student Name",text="Student Name",anchor=CENTER)
    tree.heading("Class",text="Class",anchor=CENTER)
    tree.heading("Gmail",text="Gmail",anchor=CENTER)

    mycursor.execute('select * from studentname')
    i=0
    for studentname in mycursor:
        tree.insert('',i,text="",values=(studentname[0],studentname[1],studentname[2],studentname[3]))
        i=i+1
    hsb=ttk.Scrollbar(root,orient="vertical")
    hsb.configure(command=tree.yview)
    tree.configure(yscrollcommand=hsb.set)
    hsb.pack(fill=Y,side=RIGHT)
    tree.pack()
    root.mainloop()

def view_admin_details():
    root = Tk()
    root.title("Library Management System")
    root.configure(bg="#b7413e")
    root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(),root.winfo_screenheight()))
    root.overrideredirect(True)
    e=Label(root,width=40,text='User Details',borderwidth=5, relief='ridge',anchor='center',bg='black',fg='white',font=('Courier New Baltic',25)).pack(side="top",fill='x')
    btn13 = Button(root,text="Exit...",bg='black', fg='white', width=30,padx=50,font=('Courier New Baltic',18),command=root.destroy).pack(side="bottom",pady=10,padx=50)
    btn15 = Button(root,text="Delete User",bg='black', fg='white', width=30,padx=50,font=('Courier New Baltic',18),command=lambda: [root.destroy(),del_login()]).pack(side="bottom",pady=10,padx=50)
    btn14 = Button(root,text="New User",bg='black', fg='white', width=30,padx=50,font=('Courier New Baltic',18),command=lambda: [root.destroy(),add_login()]).pack(side="bottom",pady=10,padx=50)

    tree=ttk.Treeview(root,height=100)
    tree["columns"]=("login_id","user_name")
    tree["show"]="headings"
    s = ttk.Style(root)
    s.theme_use('clam')
    s.configure('Treeview.Heading', background="black",foreground="white",font=['Times',22,'normal'])
    s.configure('Treeview', background="#b7ffff", fieldbackground="#b7ffff",foreground="black",font=['Courier New Baltic',12],rowheight=29)

    tree.column("login_id",width=350,anchor=CENTER)
    tree.column("user_name",width=350,anchor=CENTER)
    tree.heading("login_id",text="login_id",anchor=CENTER)
    tree.heading("user_name",text="user_name",anchor=CENTER)

    mycursor.execute('select * from login_id')
    i=0
    for login_id in mycursor:
        tree.insert('',i,text="",values=(login_id[0],login_id[1]))
        i=i+1
    hsb=ttk.Scrollbar(root,orient="vertical")
    hsb.configure(command=tree.yview)
    tree.configure(yscrollcommand=hsb.set)
    hsb.pack(fill=Y,side=RIGHT)
    tree.pack()
    root.mainloop()

def pay_fine_teach_base():
    tech_id_return_1 = tech_id_return.get()
    fine_return_1=int(fine_return.get())
    now = datetime.now()
    a=str(now.strftime("%Y-%m-%d %H:%M:%S"))
    p="select fine from book_issue_teach where Teacher_Id='%s'"%(tech_id_return_1)
    mycursor.execute(p)
    c=mycursor.fetchone()[0]
    m="select paid from book_issue_teach where Teacher_Id='%s'"%(tech_id_return_1)
    mycursor.execute(m)
    d=mycursor.fetchone()[0]
    pay=int(c)-fine_return_1
    qu="Update book_issue_teach set fine=%s where Teacher_Id='%s'"%(pay,tech_id_return_1) 
    mycursor.execute(qu)
    dep=int(d)+fine_return_1
    q="Update book_issue_teach set paid=%s where Teacher_Id='%s'"%(dep,tech_id_return_1) 
    mycursor.execute(q)
    mydb.commit()
    my_wind.destroy()
    
def pay_fine_teach():
    global tech_id_return,fine_return, Canvas1, mycursor,mydb,return_tech_table, my_wind
    my_wind=Tk()
    my_wind.title("Library Management System")
    my_wind.geometry("{0}x{1}+0+0".format(my_wind.winfo_screenwidth(),my_wind.winfo_screenheight()))
    my_wind.overrideredirect(True)
    
    return_tech_table= "book_issue_teach"
    Canvas1 = Canvas(my_wind) 
    Canvas1.config(bg="#b7413e")
    Canvas1.pack(expand=True,fill=BOTH)   
    headingFrame1 = Frame(my_wind,bg="#FFBB00",bd=5)
    headingFrame1.place(relx=0.25,rely=0.1,relwidth=0.5,relheight=0.13)
    headingLabel = Label(headingFrame1, text="Pay Fine-Teacher", bg='black', fg='white', font=('Courier New Baltic',20))
    headingLabel.place(relx=0,rely=0, relwidth=1, relheight=1)
    labelFrame = Frame(my_wind,bg='black')
    labelFrame.place(relx=0.1,rely=0.4,relwidth=0.8,relheight=0.3)
    def selected(event):
        p=tech_id_return.get()
        q="Select fine from  book_issue_teach where Teacher_Id='"+p+"'"
        mycursor.execute(q)
        c=mycursor.fetchone()[0]
        fine_return.insert(END,c)     
    # Teacher ID
    q="Select DISTINCT Teacher_Id from book_issue_teach where fine>0"
    mycursor.execute(q)
    c=[]
    for i in mycursor.fetchall():
        c.append(i[0])
    n = StringVar()
    lb1 = Label(labelFrame,text="Teacher ID : ", bg='black', fg='white',font=('Courier New Baltic',15))
    lb1.place(relx=0.05,rely=0.26, relheight=0.08)
    tech_id_return =ttk.Combobox(my_wind, width = 27,values=c ,textvariable = n)
    tech_id_return.bind('<<ComboboxSelected>>',selected)
    tech_id_return.place(relx=0.35,rely=0.47, relwidth=0.53, relheight=0.03)

    # Fine
    lb2 = Label(labelFrame,text="Amount : ", bg='black', fg='white', font=('Courier New Baltic',15))
    lb2.place(relx=0.05,rely=0.58, relheight=0.08)
    fine_return= Entry(labelFrame)
    fine_return.place(relx=0.31,rely=0.58, relwidth=0.665, relheight=0.1)

    # Date
    now = datetime.now()
    a=str(now.strftime("%Y-%m-%d %H:%M:%S"))
    lb2 = Label(labelFrame,text="Datetime Entered(Default): ", bg='black', fg='white', font=('Courier New Baltic',15))
    lb2.place(relx=0.05,rely=0.85, relheight=0.08)
    lb3 = Label(labelFrame,text=a, bg='black', fg='white', font=('Courier New Baltic',15))
    lb3.place(relx=0.3,rely=0.85, relwidth=0.62, relheight=0.08)
        
    #Pay Button
    SubmitBtn = Button(my_wind,text="Pay",bg='#d1ccc0', fg='black', font=('Courier New Baltic',15),command=pay_fine_teach_base)
    SubmitBtn.place(relx=0.28,rely=0.85, relwidth=0.18,relheight=0.08)

    #Quit Button
    quitBtn = Button(my_wind,text="Quit",bg='#f7f1e3', fg='black', font=('Courier New Baltic',15),command=my_wind.destroy)
    quitBtn.place(relx=0.53,rely=0.85, relwidth=0.18,relheight=0.08)
    
    my_wind.mainloop()    
    
def view_issue_teacher_details():
    root = Tk()
    root.title("Library Management System")
    root.configure(bg="#b7413e")
    root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(),root.winfo_screenheight()))
    root.overrideredirect(True)
    e=Label(root,width=40,text='Teacher Book Issue Details',borderwidth=5, relief='ridge',anchor='center',bg='black',fg='white',font=('Courier New Baltic',25)).pack(side="top",fill='x')
    btn13 = Button(root,text="Exit...",bg='black', fg='white', width=30,padx=50,font=('Courier New Baltic',18),command=root.destroy).pack(side="bottom",pady=10,padx=50)
    btn15 = Button(root,text="Pay Fine",bg='black', fg='white', width=30,padx=50,font=('Courier New Baltic',18),command=pay_fine_teach).pack(side="bottom",pady=10,padx=50)
    tree=ttk.Treeview(root,height=100)
    tree["columns"]=("Teacher Id","Teacher Name","Book Name","Issue Date","Fine","Paid")
    tree["show"]="headings"
    s = ttk.Style(root)
    s.theme_use('clam')
    s.configure('Treeview.Heading', background="black",foreground="white",font=['Times',22,'normal'])
    s.configure('Treeview', fieldbackground="#b7ffff",background="#b7ffff",foreground="black",font=['Courier New Baltic',12],rowheight=29)

    tree.column("Teacher Id",width=200,anchor=CENTER)
    tree.column("Teacher Name",width=300,anchor=CENTER)
    tree.column("Book Name",width=300,anchor=CENTER)
    tree.column("Issue Date",width=300,anchor=CENTER)
    tree.column("Fine",width=150,anchor=CENTER)
    tree.column("Paid",width=150,anchor=CENTER)
    tree.heading("Teacher Id",text="Teacher Id",anchor=CENTER)
    tree.heading("Teacher Name",text="Teacher Name",anchor=CENTER)
    tree.heading("Book Name",text="Book Name",anchor=CENTER)
    tree.heading("Issue Date",text="Issue Date",anchor=CENTER)
    tree.heading("Fine",text="Fine",anchor=CENTER)
    tree.heading("Paid",text="Paid",anchor=CENTER)

    mycursor.execute('select * from book_issue_teach')
    i=0
    for book_issue_teach in mycursor:
        tree.insert('',i,text="",values=(book_issue_teach[0],book_issue_teach[1],book_issue_teach[2],book_issue_teach[3],book_issue_teach[4],book_issue_teach[5]))
        i=i+1
    hsb=ttk.Scrollbar(root,orient="vertical")
    hsb.configure(command=tree.yview)
    tree.configure(yscrollcommand=hsb.set)
    hsb.pack(fill=Y,side=RIGHT)
    tree.pack()
    root.mainloop()
def pay_fine_base():
    tech_id_return_1 = tech_id_return.get()
    fine_return_1=int(fine_return.get())
    now = datetime.now()
    a=str(now.strftime("%Y-%m-%d %H:%M:%S"))
    p="select fine from book_issue where Student_Id='%s'"%(tech_id_return_1)
    mycursor.execute(p)
    c=mycursor.fetchone()[0]
    pay=int(c)-fine_return_1
    m="select paid from book_issue where Student_Id='%s'"%(tech_id_return_1)
    mycursor.execute(m)
    d=mycursor.fetchone()[0]
    qu="Update book_issue set fine=%s where Student_Id='%s'"%(pay,tech_id_return_1) 
    mycursor.execute(qu)
    dep=int(d)+fine_return_1
    qu="Update book_issue set paid=%s where Student_Id='%s'"%(dep,tech_id_return_1) 
    mycursor.execute(qu)
    mydb.commit()
    my_wind.destroy()
    
def pay_fine():
    global tech_id_return,fine_return, Canvas1, mycursor,mydb,return_tech_table, my_wind
    my_wind=Tk()
    my_wind.title("Library Management System")
    my_wind.geometry("{0}x{1}+0+0".format(my_wind.winfo_screenwidth(),my_wind.winfo_screenheight()))
    my_wind.overrideredirect(True)
    now = datetime.now()
    a=str(now.strftime("%Y-%m-%d %H:%M:%S"))
    return_tech_table= "book_issue_teach"
    Canvas1 = Canvas(my_wind) 
    Canvas1.config(bg="#b7413e")
    Canvas1.pack(expand=True,fill=BOTH)   
    headingFrame1 = Frame(my_wind,bg="#FFBB00",bd=5)
    headingFrame1.place(relx=0.25,rely=0.1,relwidth=0.5,relheight=0.13)
    headingLabel = Label(headingFrame1, text="Pay Fine-Teacher", bg='black', fg='white', font=('Courier New Baltic',20))
    headingLabel.place(relx=0,rely=0, relwidth=1, relheight=1)
    labelFrame = Frame(my_wind,bg='black')
    labelFrame.place(relx=0.1,rely=0.4,relwidth=0.8,relheight=0.3)
    def selected(event):
        p=tech_id_return.get()
        q="Select fine from  book_issue where Student_Id='"+p+"'"
        mycursor.execute(q)
        c=mycursor.fetchone()[0]
        fine_return.insert(END,c)   
    # Student ID
    q="Select DISTINCT Student_Id from book_issue where fine>0"
    mycursor.execute(q)
    c=[]
    for i in mycursor.fetchall():
        c.append(i[0])
    n = StringVar()
    lb1 = Label(labelFrame,text="Student ID : ", bg='black', fg='white',font=('Courier New Baltic',15))
    lb1.place(relx=0.05,rely=0.26, relheight=0.08)
    tech_id_return =ttk.Combobox(my_wind, width = 27,values=c ,textvariable = n)
    tech_id_return.bind('<<ComboboxSelected>>',selected)
    tech_id_return.place(relx=0.35,rely=0.47, relwidth=0.53, relheight=0.03)

    # Fine
    lb2 = Label(labelFrame,text="Amount : ", bg='black', fg='white', font=('Courier New Baltic',15))
    lb2.place(relx=0.05,rely=0.58, relheight=0.08)
    fine_return= Entry(labelFrame)
    fine_return.place(relx=0.31,rely=0.58, relwidth=0.665, relheight=0.1)

    # Date
    lb2 = Label(labelFrame,text="Datetime Entered(Default): ", bg='black', fg='white', font=('Courier New Baltic',15))
    lb2.place(relx=0.05,rely=0.85, relheight=0.08)
    lb3 = Label(labelFrame,text=a, bg='black', fg='white', font=('Courier New Baltic',15))
    lb3.place(relx=0.3,rely=0.85, relwidth=0.62, relheight=0.08)
        
    #Pay Button
    SubmitBtn = Button(my_wind,text="Pay",bg='#d1ccc0', fg='black', font=('Courier New Baltic',15),command=pay_fine_base)
    SubmitBtn.place(relx=0.28,rely=0.85, relwidth=0.18,relheight=0.08)

    #Quit Button
    quitBtn = Button(my_wind,text="Quit",bg='#f7f1e3', fg='black', font=('Courier New Baltic',15),command=my_wind.destroy)
    quitBtn.place(relx=0.53,rely=0.85, relwidth=0.18,relheight=0.08)
    
    my_wind.mainloop()
def view_issue_student_details():
    root = Tk()
    root.title("Library Management System")
    root.configure(bg="#b7413e")
    root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(),root.winfo_screenheight()))
    root.overrideredirect(True)
    e=Label(root,width=40,text='Student Book Issue Details',borderwidth=5, relief='ridge',anchor='center',bg='black',fg='white',font=('Courier New Baltic',25)).pack(side="top",fill='x')
    btn13 = Button(root,text="Exit...",bg='black', fg='white', width=30,padx=50,font=('Courier New Baltic',18),command=root.destroy).pack(side="bottom",pady=10,padx=50)
    btn15 = Button(root,text="Pay Fine",bg='black', fg='white', width=30,padx=50,font=('Courier New Baltic',18),command=pay_fine).pack(side="bottom",pady=10,padx=50)
    tree=ttk.Treeview(root,height=100)
    tree["columns"]=("Student Id","Student Name","Book Name","Issue Date","Fine","Paid")
    tree["show"]="headings"
    s = ttk.Style(root)
    s.theme_use('clam')
    s.configure('Treeview.Heading', background="black",foreground="white",font=['Times',22,'normal'])
    s.configure('Treeview', fieldbackground="#b7ffff",background="#b7ffff",foreground="black",font=['Courier New Baltic',12],rowheight=29)

    tree.column("Student Id",width=200,anchor=CENTER)
    tree.column("Student Name",width=300,anchor=CENTER)
    tree.column("Book Name",width=300,anchor=CENTER)
    tree.column("Issue Date",width=300,anchor=CENTER)  
    tree.column("Fine",width=150,anchor=CENTER)
    tree.column("Paid",width=150,anchor=CENTER)
    tree.heading("Student Id",text="Student Id",anchor=CENTER)
    tree.heading("Student Name",text="Student Name",anchor=CENTER)
    tree.heading("Book Name",text="Book Name",anchor=CENTER)
    tree.heading("Issue Date",text="Issue Date",anchor=CENTER)
    tree.heading("Fine",text="Fine",anchor=CENTER)
    tree.heading("Paid",text="Paid",anchor=CENTER)

    mycursor.execute('select * from book_issue')
    i=0
    for book_issue in mycursor:
        tree.insert('',i,text="",values=(book_issue[0],book_issue[1],book_issue[2],book_issue[3],book_issue[4],book_issue[5]))
        i=i+1
    hsb=ttk.Scrollbar(root,orient="vertical")
    hsb.configure(command=tree.yview)
    tree.configure(yscrollcommand=hsb.set)
    hsb.pack(fill=Y,side=RIGHT)
    tree.pack()
    root.mainloop()

def add_login_base():
    login_id_1 = login_id.get()
    login_name_1 = login_name.get()
    insert_login = "INSERT INTO login_id(login_id ,user_name) VALUES ('%s','%s')"%(login_id_1,login_name_1)
    try:
        mycursor.execute(insert_login)
        mydb.commit()
        messagebox.showinfo('Success',"New user details added successfully")
    except:
        messagebox.showinfo("Error","Can't add data into Database")
    my_wind.destroy()
def add_login():
    global login_id,login_name, Canvas1, mycursor,mydb, my_wind,log_table
    my_wind=Tk()
    my_wind.title("Library Management System")
    my_wind.geometry("{0}x{1}+0+0".format(my_wind.winfo_screenwidth(),my_wind.winfo_screenheight()))
    my_wind.overrideredirect(True)
    log_table=login_id
    Canvas1 = Canvas(my_wind) 
    Canvas1.config(bg="#ff4633")
    Canvas1.pack(expand=True,fill=BOTH)   
    headingFrame1 = Frame(my_wind,bg="#FFBB00",bd=5)
    headingFrame1.place(relx=0.25,rely=0.1,relwidth=0.5,relheight=0.13)
    headingLabel = Label(headingFrame1, text="Add new user details", bg='black', fg='white', font=('Courier New Baltic',20))
    headingLabel.place(relx=0,rely=0, relwidth=1, relheight=1)
    labelFrame = Frame(my_wind,bg='black')
    labelFrame.place(relx=0.1,rely=0.4,relwidth=0.8,relheight=0.3)
        
    # User ID
    lb1 = Label(labelFrame,text="Login ID : ", bg='black', fg='white',font=('Courier New Baltic',15))
    lb1.place(relx=0.05,rely=0.35, relheight=0.08)
    login_id = Entry(labelFrame)
    login_id.place(relx=0.3,rely=0.35, relwidth=0.62, relheight=0.08)
        
    # User name
    lb2 = Label(labelFrame,text="User Name : ", bg='black', fg='white', font=('Courier New Baltic',15))
    lb2.place(relx=0.05,rely=0.55, relheight=0.08)
    login_name = Entry(labelFrame)
    login_name.place(relx=0.3,rely=0.55, relwidth=0.62, relheight=0.08)
        
    #Submit Button
    SubmitBtn = Button(my_wind,text="SUBMIT",bg='#d1ccc0', fg='black', font=('Courier New Baltic',15),command=add_login_base)
    SubmitBtn.place(relx=0.28,rely=0.9, relwidth=0.18,relheight=0.08)

    #Quit Buttton
    quitBtn = Button(my_wind,text="Quit",bg='#f7f1e3', fg='black', font=('Courier New Baltic',15),command=my_wind.destroy)
    quitBtn.place(relx=0.53,rely=0.9, relwidth=0.18,relheight=0.08)
    
    my_wind.mainloop()

def del_login_base():
    login_id_1 = Login_id.get()
    
    delete = "delete from login_id where login_id=('%s')"%(login_id_1)
    try:
        if login_id_1!=Login_id_1:
            mycursor.execute(delete)
            mydb.commit()
            messagebox.showinfo('Success',"login details deleted successfully")
        else:
            messagebox.showinfo("Error","Can't delete data...User Id already in use")
    except:
        messagebox.showinfo("Error","Can't delete data")
    my_wind.destroy()
def del_login():
    global Login_id,Canvas1, mycursor,mydb,my_wind
    my_wind=Tk()
    my_wind.title("Library Management System")
    my_wind.geometry("{0}x{1}+0+0".format(my_wind.winfo_screenwidth(),my_wind.winfo_screenheight()))
    my_wind.overrideredirect(True)
    
    Canvas1 = Canvas(my_wind) 
    Canvas1.config(bg="#ff4633")
    Canvas1.pack(expand=True,fill=BOTH)   
    headingFrame1 = Frame(my_wind,bg="#FFBB00",bd=5)
    headingFrame1.place(relx=0.25,rely=0.1,relwidth=0.5,relheight=0.13)
    headingLabel = Label(headingFrame1, text="login Detail", bg='black', fg='white', font=('Courier New Baltic',20))
    headingLabel.place(relx=0,rely=0, relwidth=1, relheight=1)
    labelFrame = Frame(my_wind,bg='black')
    labelFrame.place(relx=0.1,rely=0.4,relwidth=0.8,relheight=0.3)

    #Login Id    
    q="Select login_id from login_id"
    mycursor.execute(q)
    c=mycursor.fetchall()
    n = StringVar()
    lb1 = Label(labelFrame,text="login Id : ", bg='black', fg='white',font=('Courier New Baltic',15))
    lb1.place(relx=0.05,rely=0.45, relheight=0.08)
    Login_id = ttk.Combobox(my_wind, width = 27, textvariable = n)
    Login_id['values']=[r for r in c]
    Login_id.place(relx=0.3,rely=0.53, relwidth=0.5, relheight=0.03)
    Login_id.current()        

    #Delete Button
    SubmitBtn = Button(my_wind,text="Delete",bg='#d1ccc0', fg='black', font=('Courier New Baltic',15),command=del_login_base)
    SubmitBtn.place(relx=0.28,rely=0.9, relwidth=0.18,relheight=0.08)

    #Quit Button
    quitBtn = Button(my_wind,text="Quit",bg='#f7f1e3', fg='black', font=('Courier New Baltic',15),command=my_wind.destroy)
    quitBtn.place(relx=0.53,rely=0.9, relwidth=0.18,relheight=0.08)
    
    my_wind.mainloop() 

def del_stu_base():
    stu_id_1 = stu_id.get() 
    delete = "delete from studentname where Stu_Id=('%s')"%(stu_id_1)
    q="SELECT COUNT(*) FROM studentname WHERE Stu_Id=('%s')"%(stu_id_1)
    mycursor.execute(q)
    c=mycursor.fetchall()
    try:
        if (c[-1][-1])==1:
            mycursor.execute(delete)
            mydb.commit()
            messagebox.showinfo('Success',"Student details deleted successfully")
        else:
            messagebox.showinfo("Error","Can't delete data")
    except:
        messagebox.showinfo("Error","Can't delete data")
    my_wind.destroy()
def del_stu():
    global stu_id,Canvas1, mycursor,mydb,my_wind
    my_wind=Tk()
    my_wind.title("Library Management System")
    my_wind.geometry("{0}x{1}+0+0".format(my_wind.winfo_screenwidth(),my_wind.winfo_screenheight()))
    my_wind.overrideredirect(True)
    
    Canvas1 = Canvas(my_wind) 
    Canvas1.config(bg="#ff4633")
    Canvas1.pack(expand=True,fill=BOTH)   
    headingFrame1 = Frame(my_wind,bg="#FFBB00",bd=5)
    headingFrame1.place(relx=0.25,rely=0.1,relwidth=0.5,relheight=0.13)
    headingLabel = Label(headingFrame1, text="Student Detail", bg='black', fg='white', font=('Courier New Baltic',20))
    headingLabel.place(relx=0,rely=0, relwidth=1, relheight=1)
    labelFrame = Frame(my_wind,bg='black')
    labelFrame.place(relx=0.1,rely=0.4,relwidth=0.8,relheight=0.3)
    def selected(event):
        stu_name.delete(0,END)
        p=stu_id.get()
        q="Select Student_name from studentname where Stu_Id='"+p+"'"
        mycursor.execute(q)
        c=mycursor.fetchone()[0]
        s1=c.replace("{","")
        s=s1.replace("}","")
        stu_name.insert(END,s)

    #Student Id
    q="Select Stu_Id from studentname"
    mycursor.execute(q)
    c=mycursor.fetchall()        
    n = StringVar()    
    lb1 = Label(labelFrame,text="Student Id : ", bg='black', fg='white',font=('Courier New Baltic',15))
    lb1.place(relx=0.05,rely=0.26, relheight=0.08)
    stu_id = ttk.Combobox(my_wind, width = 27, textvariable = n)
    stu_id['values']=[r for r in c]
    stu_id.bind('<<ComboboxSelected>>',selected)
    stu_id.place(relx=0.35,rely=0.47, relwidth=0.53, relheight=0.03)

    #Student Name    
    lb2 = Label(labelFrame,text="Student Name : ", bg='black', fg='white', font=('Courier New Baltic',15))
    lb2.place(relx=0.05,rely=0.58, relheight=0.08)
    stu_name = Entry(labelFrame)
    stu_name.place(relx=0.31,rely=0.58, relwidth=0.665, relheight=0.1)
    
    #Delete Button
    SubmitBtn = Button(my_wind,text="Delete",bg='#d1ccc0', fg='black', font=('Courier New Baltic',15),command=del_stu_base)
    SubmitBtn.place(relx=0.28,rely=0.9, relwidth=0.18,relheight=0.08)

    #Quit Button
    quitBtn = Button(my_wind,text="Quit",bg='#f7f1e3', fg='black', font=('Courier New Baltic',15),command=my_wind.destroy)
    quitBtn.place(relx=0.53,rely=0.9, relwidth=0.18,relheight=0.08)
    
    my_wind.mainloop() 

def del_teacher_base():
    teacher_id_1 = teacher_id.get()
    
    delete = "delete from teachername where Teacher_Id=('%s')"%(teacher_id_1)
    q="SELECT COUNT(*) FROM teachername WHERE Teacher_Id=('%s')"%(teacher_id_1)
    mycursor.execute(q)
    c=mycursor.fetchall()
    try:
        if (c[-1][-1])==1:
            mycursor.execute(delete)
            mydb.commit()
            messagebox.showinfo('Success',"Teacher details deleted successfully")
        else:
            messagebox.showinfo("Error","Can't delete data")
    except:
        messagebox.showinfo("Error","Can't delete data")
    my_wind.destroy()
def del_teacher():
    global teacher_id,Canvas1, mycursor,mydb,my_wind
    my_wind=Tk()
    my_wind.title("Library Management System")
    my_wind.geometry("{0}x{1}+0+0".format(my_wind.winfo_screenwidth(),my_wind.winfo_screenheight()))
    my_wind.overrideredirect(True)
    
    Canvas1 = Canvas(my_wind) 
    Canvas1.config(bg="#ff4633")
    Canvas1.pack(expand=True,fill=BOTH)   
    headingFrame1 = Frame(my_wind,bg="#FFBB00",bd=5)
    headingFrame1.place(relx=0.25,rely=0.1,relwidth=0.5,relheight=0.13)
    headingLabel = Label(headingFrame1, text="Teacher Detail", bg='black', fg='white', font=('Courier New Baltic',20))
    headingLabel.place(relx=0,rely=0, relwidth=1, relheight=1)
    labelFrame = Frame(my_wind,bg='black')
    labelFrame.place(relx=0.1,rely=0.4,relwidth=0.8,relheight=0.3)
    def selected(event):
        tech_name.delete(0,END)
        p=teacher_id.get()
        q="Select Teacher_name from teachername where Teacher_Id='"+p+"'"
        mycursor.execute(q)
        c=mycursor.fetchone()[0]
        s1=c.replace("{","")
        s=s1.replace("}","")
        tech_name.insert(END,s)    

    # Teacher ID
    q="Select Teacher_Id from teachername"
    mycursor.execute(q)
    c=mycursor.fetchall()
        
    n = StringVar()
    lb1 = Label(labelFrame,text="Teacher Id : ", bg='black', fg='white',font=('Courier New Baltic',15))
    lb1.place(relx=0.05,rely=0.26, relheight=0.08)
    teacher_id = ttk.Combobox(my_wind, width = 27, textvariable = n)
    teacher_id['values']=[r for r in c]
    teacher_id.place(relx=0.35,rely=0.47, relwidth=0.53, relheight=0.03)
    teacher_id.bind('<<ComboboxSelected>>',selected)

    #Teacher Name
    lb2 = Label(labelFrame,text="Teacher Name : ", bg='black', fg='white', font=('Courier New Baltic',15))
    lb2.place(relx=0.05,rely=0.58, relheight=0.08)
    tech_name= Entry(labelFrame)
    tech_name.place(relx=0.31,rely=0.58, relwidth=0.665, relheight=0.1)
    
    #Delete Button
    SubmitBtn = Button(my_wind,text="Delete",bg='#d1ccc0', fg='black', font=('Courier New Baltic',15),command=del_teacher_base)
    SubmitBtn.place(relx=0.28,rely=0.9, relwidth=0.18,relheight=0.08)

    #Quit Button
    quitBtn = Button(my_wind,text="Quit",bg='#f7f1e3', fg='black', font=('Courier New Baltic',15),command=my_wind.destroy)
    quitBtn.place(relx=0.53,rely=0.9, relwidth=0.18,relheight=0.08)
    
    my_wind.mainloop()
def main_p():
    global label_1
    #Tkinter connection
    my_window=Tk()
    my_window.title("Library Management System")
    my_window.geometry("{0}x{1}+0+0".format(my_window.winfo_screenwidth(),my_window.winfo_screenheight()))

    my_window.overrideredirect(True)
    my_window.configure(bg='black')
    same=True
    n=1.75
# Adding a background image
    background_image =Image.open("img.jpg")
    [imageSizeWidth, imageSizeHeight] = background_image.size

    newImageSizeWidth = int(imageSizeWidth*n)
    if same:
        newImageSizeHeight = int(imageSizeHeight*n) 
    else:
        newImageSizeHeight = int(imageSizeHeight/n) 
    
    background_image = background_image.resize((newImageSizeWidth,newImageSizeHeight),Image.Resampling.LANCZOS)
    img = ImageTk.PhotoImage(background_image)
    Canvas1 = Canvas(my_window)
    Canvas1.create_image(750,340,image = img)      
    Canvas1.config(bg="black",width = newImageSizeWidth, height = newImageSizeHeight)
    Canvas1.grid()

    #Framework
    headingFrame1 = Frame(my_window,bg="#FFBB00",bd=8)
    headingFrame1.place(relx=0.33,rely=0.1,relwidth=0.391,relheight=0.11)
    headingLabel = Label(headingFrame1, text="Welcome "+user_name_1, bg='black', fg='white',anchor="center",
                         font=('Courier New Baltic',47))
    headingLabel.grid(row=2,columnspan=10)


    label_1=Label(my_window,bg="Black",fg="white",font="Arial 20 bold",justify=LEFT,relief=RAISED)
    label_1.place(relx=0.78,rely=0.06, relwidth=0.24,relheight=0.1)
    time()
    photo = PhotoImage(file = "image.png")
    img_label= Label(image=photo)
    btn0 = Button(my_window,image = photo,bg='black', fg='white',font=('Courier New Baltic',18),command=sound)
    btn0.place(relx=0.0,rely=0.0, relwidth=0.05,relheight=0.1)
    
    btn1 = Button(my_window,text="Manage Books ",bg='black', fg='white',font=('Courier New Baltic',18),command=view_book_list)
    btn1.place(relx=0.28,rely=0.29, relwidth=0.235,relheight=0.1)
    
    btn14 = Button(my_window,text="Manage User",bg='black', fg='white',font=('Courier New Baltic',18),command=view_admin_details)
    btn14.place(relx=0.57,rely=0.29, relwidth=0.235,relheight=0.1)

    btn9 = Button(my_window,text="Teacher Record",bg='black', fg='white',font=('Courier New Baltic',18),command=view_teacher_detail)
    btn9.place(relx=0.28,rely=0.40, relwidth=0.235,relheight=0.1)

    btn10 = Button(my_window,text="Student Record ",bg='black', fg='white',font=('Courier New Baltic',18),command=view_student_details)
    btn10.place(relx=0.57,rely=0.40, relwidth=0.235,relheight=0.1)

    btn5 = Button(my_window,text="Issue Book to Teacher",bg='black', fg='white',font=('Courier New Baltic',18),command=issue_tech)
    btn5.place(relx=0.28,rely=0.51, relwidth=0.235,relheight=0.1)
    
    btn6 = Button(my_window,text="Issue Book to Student",bg='black', fg='white',font=('Courier New Baltic',18),command=issue_stu)
    btn6.place(relx=0.57,rely=0.51, relwidth=0.235,relheight=0.1)

    btn11 = Button(my_window,text="Issue Book Teacher's Record",bg='black', fg='white',font=('Courier New Baltic',18),command=view_issue_teacher_details)
    btn11.place(relx=0.28,rely=0.62, relwidth=0.235,relheight=0.1)
    
    btn12 = Button(my_window,text="Issue Book Student's Record",bg='black', fg='white',font=('Courier New Baltic',18),command=view_issue_student_details)
    btn12.place(relx=0.57,rely=0.62, relwidth=0.235,relheight=0.1)

    btn7 = Button(my_window,text="Book Return by Teacher",bg='black', fg='white',font=('Courier New Baltic',18),command=return_tech)
    btn7.place(relx=0.28,rely=0.73, relwidth=0.235,relheight=0.1)

    btn8 = Button(my_window,text="Book Return by Student",bg='black', fg='white',font=('Courier New Baltic',18),command=return_stu)
    btn8.place(relx=0.57,rely=0.73, relwidth=0.235,relheight=0.1)

    
    btn13 = Button(my_window,text="Log out...",bg='black', fg='white',font=('Courier New Baltic',18),command=lambda: [my_window.destroy(),login()])
    btn13.place(relx=0.44,rely=0.85, relwidth=0.17,relheight=0.1)
    
    my_window.mainloop()

def check_login_base():
    global user_name_1,Login_id_1
    Login_id_1= login_id.get()
    user_name_1 = user_name.get()

    c=0
    mycursor.execute("SELECT * FROM login_id")
    myresult = mycursor.fetchall()
    for x in myresult:
        if str(x[0])==Login_id_1:
            c+=1
        if c==1:
            query="SELECT user_name FROM login_id where login_Id='%s'"%(Login_id_1)
            mycursor.execute(query)
            myresult = mycursor.fetchall()
            for y in myresult:
                if y[0]==user_name_1:
                    c+=1
    if c==2:
        my_wind.destroy()
        main_p()
    else:
        messagebox.showinfo("Error","Invalid user Id or user name")
        my_wind.destroy()
    
def login():
    global login_id,user_name, Canvas1, mycursor,mydb, my_wind
    update_teach()
    update()
    my_wind=Tk()
    my_wind.title("Library Management System")
    my_wind.geometry("{0}x{1}+0+0".format(my_wind.winfo_screenwidth(),my_wind.winfo_screenheight()))
    my_wind.overrideredirect(True)
    same=True
    n=1.75
# Adding a background image
    background_image =Image.open("img.jpg")
    [imageSizeWidth, imageSizeHeight] = background_image.size

    newImageSizeWidth = int(imageSizeWidth*n)
    if same:
        newImageSizeHeight = int(imageSizeHeight*n) 
    else:
        newImageSizeHeight = int(imageSizeHeight/n) 
    
    background_image = background_image.resize((newImageSizeWidth,newImageSizeHeight),Image.Resampling.LANCZOS)
    img = ImageTk.PhotoImage(background_image)
    Canvas1 = Canvas(my_wind)
    Canvas1.create_image(750,340,image = img)      
    Canvas1.config(bg="black",width = newImageSizeWidth, height = newImageSizeHeight)

    Canvas1.pack(expand=True,fill=BOTH)   
    headingFrame1 = Frame(my_wind,bg="#FFBB00",bd=5)
    headingFrame1.place(relx=0.70,rely=0.2,relwidth=0.25,relheight=0.10)
    headingLabel = Label(headingFrame1, text="Login", bg='black', fg='white', font=('Courier New Baltic',25))
    headingLabel.place(relx=0.0,rely=0.0, relwidth=1, relheight=1)
    labelFrame = Frame(my_wind,bg='black')
    labelFrame.place(relx=0.60,rely=0.4,relwidth=0.8,relheight=0.3)
        
    # User ID
    lb1 = Label(labelFrame,text="Password  : ", bg='black', fg='white',font=('Courier New Baltic',15))
    lb1.place(relx=0.05,rely=0.5, relheight=0.08)
    login_id = Entry(labelFrame,show='*')
    login_id.place(relx=0.15,rely=0.5, relwidth=0.2, relheight=0.08)
        
    # User name
    lb2 = Label(labelFrame,text="User Name : ", bg='black', fg='white', font=('Courier New Baltic',15))
    lb2.place(relx=0.05,rely=0.3, relheight=0.08)
    user_name = Entry(labelFrame)
    user_name.place(relx=0.15,rely=0.3, relwidth=0.2, relheight=0.08)

    #Show pwd
    c_v1=IntVar(value=0)
    def my_show():
        if(c_v1.get()==1):
            login_id.config(show='')
        else:
            login_id.config(show='*')

    c1 = Checkbutton(labelFrame,text='Show Password',variable=c_v1,onvalue=1,offvalue=0, font=('Courier New Baltic',15),command=my_show)
    c1.place(relx=0.05,rely=0.7)
    # Submit Button
    SubmitBtn = Button(my_wind,text="Login",bg='#d1ccc0', fg='black', font=('Courier New Baltic',15),command=check_login_base)
    SubmitBtn.place(relx=0.68,rely=0.8, relwidth=0.18,relheight=0.08)
    
    quitBtn = Button(my_wind,text="Quit",bg='#f7f1e3', fg='black', font=('Courier New Baltic',15),command=my_wind.destroy)
    quitBtn.place(relx=0.68,rely=0.9, relwidth=0.18,relheight=0.08)

    my_wind.mainloop()

#Login Page
login()


