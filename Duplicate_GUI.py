import re
from tkinter import *
from tkinter import ttk
import email
from email.message import EmailMessage
import smtplib
import os
import hashlib
import datetime
from tkinter import filedialog

def delete_dups(duplicate_file,root):
    filtered_lists = list(filter(lambda x : len(x)>1 , duplicate_file.values()))
    no1=0
    file_name=[]
    
    if len(filtered_lists)>0:
        for lists in filtered_lists:
            num = 0
            for path in lists:
               num+=1
               if num>1:
                   file_name.append(path) 
                   no1+=1
                   os.remove(path) 
    else:
        a = ttk.Label(root,text="       Files NA            ",padding=3).grid(column=0,row=8)
        a
        
    write = str(no1) +" Duplicate File found"
    a = ttk.Label(root,text=write,padding=3).grid(column=0,row=8)
    a
    return no1
    
def dups_finder(paths):
    dict = {}
    no = 0
    for path in paths:
        if os.path.exists(path):
            no+=1
            open_path = open(path, "rb")
            hasher = hashlib.md5(open_path.read())
            open_path.close()
            hexa = hasher.hexdigest()
                       
            if hexa in dict:
                dict[hexa].append(path)
            else:
                dict[hexa]= [path]
    
    return dict, no

def files(folder,root1):
    file_list = []
    if os.path.exists(folder):
        for root, folder_name, file_name in os.walk(folder):
            for filen in file_name:
                file_list.append(os.path.join(root,filen))
    
        return file_list
    else:
        a = ttk.Label(root1,text="         Path NA            ",padding=3).grid(column=0,row=8)
        a
        
def checkemail(id):        
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    return re.fullmatch(regex, id)
        
def mail(id,Scan,time,delete_scan):
    mail= email.message.EmailMessage()
    mail['Subject']= 'Automated Mail:- Log File'
    mail['From']= 'Scan Report'
    mail['Bcc']= id
    mail.set_content(f'Hello,\n\nScan Time:- {time}\nNumber of Files Scanned:- {Scan}\nDuplicate Files deleted:- {delete_scan}\n\nRegards, ')

    server= smtplib.SMTP_SSL('smtp.gmail.com',465)
    server.login('demo87991@gmail.com', '1234Abc**')
    server.send_message(mail)

def main(root):
    global startb
    if os.path.isabs(enty1.get()):
        start_time = datetime.datetime.now().strftime('%H:%M:%S')
        file_path = files(enty1.get(),root)
        duplicate, total_files = dups_finder(file_path)
        delete_no = delete_dups(duplicate,root)
        
        if checkemail(enty2.get()):
            try:
                mail(enty2.get(),total_files,start_time,delete_no)
                a = ttk.Label(root,text="Mail Sent    ",padding=3).grid(column=0,row=9)
                a
            #   startb['state']= DISABLED
            except Exception as E:
                w = f"Email Error   "
                a = ttk.Label(root,text=w,padding=3).grid(column=0,row=9)
                a
            #startb['state']= DISABLED
        else:
            w = f"Email Error   "
            a = ttk.Label(root,text=w,padding=3).grid(column=0,row=9)
            a
    else:
        word = "            Path Error            "
        a = ttk.Label(root,text=word,padding=3).grid(column=0,row=8)
        a
        #startb['state']= DISABLED
    
if __name__=="__main__":    
    root = Tk()
    root.title("Duplicate File Deletion")
#For getting bracket for getting data
    enty1 = Entry(root,width=50,borderwidth=10)
    enty1.grid(column=0,row=1)
    ttk.Label(root,text= "Select Folder", padding=3).grid(column=0,row=0)
    ttk.Label(root,text= "Provide Email ID", padding=3).grid(column=0,row=2)

    enty2 = Entry(root,width=50,borderwidth=10)
    enty2.grid(column=0,row=3)

    def browse():
        currdir = os.getcwd()
        tempdir = filedialog.askdirectory(parent=root, initialdir=currdir, title='Please select a directory')
        enty1.insert(10,tempdir)

    browseb= ttk.Button(root,text="Browse ",padding=6,command=browse)
    #clearb= ttk.Button(root,text="Clear ",padding=6,command=clear).grid(column=0,row=7)    
    startb= ttk.Button(root,text="Start ",padding=6,command=lambda: main(root)) #Here Command is important
    quitb= ttk.Button(root,text="Quit ",padding=6,command=root.destroy)
    startb.grid(column=0,row=5)
    quitb.grid(column=0,row=6)
    browseb.grid(column=1,row=1)

    root.mainloop()
