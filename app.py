import tkinter as tk
from tkinter import *
from tkinter.filedialog import askopenfilename
from tkinter import font as tkfont
from tkinter.ttk import *
from tkinter import messagebox
from lxml import etree
import xml.etree.ElementTree as ET


class SampleApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title("XML app")
        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")

        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartPage, Menu):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage") #indicates which is the 1st page

    def show_frame(self, page_name):
        #Show a frame for the given page name
        frame = self.frames[page_name]
        frame.tkraise()


class StartPage(tk.Frame):
#Starting page of the app, user is asked to input corresponding files
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(background='white')
        helv36 = tkfont.Font(family='Helvetica', size=13)

        label = tk.Label(self, text="Please insert XML file",
                         font=controller.title_font, background='white')
        label.pack(side="top", fill="x", pady=10)
        #file1 represents XML and file2 represents XSD
        global currfile1
        global currfile2
        def getxmlfile():
            global currfile1
            currfile1=askopenfilename() #opens file browser to select file
            print(currfile1) #prints path on console
        fileno1 = tk.Button(self, text="Browse...", font=helv36, background='white',
                             command=lambda: getxmlfile())
        fileno1.pack(side="top",  pady=35, padx=35)

        label = tk.Label(self, text="Please insert XML Schema(SXD)",
                         font=controller.title_font, background='white')
        label.pack(side="top", fill="x", pady=10)
        def getxsdfile():
            global currfile2
            currfile2=askopenfilename()
            print(currfile2)
        fileno2 = tk.Button(self, text="Browse...", font=helv36, background='white',
                            command=lambda: getxsdfile())
        fileno2.pack(padx=200, pady=20)
        def validate_it(x , y):
            # Validates the XML file based on XSD
            #x being the XML file and y being the XML Schema
            xmlschemadoc = etree.parse(y)
            xmlschema = etree.XMLSchema(xmlschemadoc)
            doc = etree.parse(x)
            if  xmlschema(doc): #true
                messagebox.showinfo("Message", "XML is Valid.\n Press OK to proceed.") #pop-up window with message
                controller.show_frame("Menu") #after "OK" is pressed, this redirects you to the next page
            else: #false
                messagebox.showinfo("Error", "XML Invalid.\nPlease try again.")
                #stays on the same page so the user can re-insert files

        confirmation = tk.Button(self, text="Validate!", font=helv36,background='white', command=lambda: validate_it(currfile1, currfile2))
        confirmation.pack(side="bottom", anchor="se", pady=15, padx=15)


class Menu(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(background='white')
        helv36 = tkfont.Font(family='Helvetica', size=13)
        label = tk.Label(self, text="New Lecture",
                         font=controller.title_font, background='white')
        label.pack(side="top", fill="x", pady=10)
        label = tk.Label(self, text="Title",
                         font=controller.title_font, background='white')
        label.place(x=35,y=35)
        lecTitle = StringVar()
        E1 = Entry(self, textvariable=lecTitle).place(x=195, y=40)
        label = tk.Label(self, text="Professor",
                         font=controller.title_font, background='white')
        label.place(x=35, y=75)
        lecProf = StringVar()
        E2 = Entry(self, textvariable=lecProf).place(x=195, y=80)
        label = tk.Label(self, text="Day",
                         font=controller.title_font, background='white')
        label.place(x=35, y=115)
        lecDay = StringVar()
        E3 = Entry(self, textvariable=lecDay).place(x=195, y=120)
        label = tk.Label(self, text="Time",
                         font=controller.title_font, background='white')
        label.place(x=35, y=155)
        lecTime = StringVar()
        E4 = Entry(self, textvariable=lecTime).place(x=195, y=160)
        label = tk.Label(self, text="Classroom",
                         font=controller.title_font, background='white')
        label.place(x=35, y=195)
        lecClass = StringVar()
        E5 = Entry(self, textvariable=lecClass).place(x=195, y=200)

        def insert_data(x,y,z,w, q):
            #x is for title, y for professor, z for day, w for time, q for classroom
            currtitle = x.get()
            currprof = y.get()
            currday = str(z.get())
            currtim = w.get()
            currclassroom = q.get()
            temp = currfile1
            tree = ET.parse(temp)
            root = tree.getroot()
            lesson_elem = ET.Element("Lesson") #create element Lesson
            tit_elem = ET.Element("Title") #create element Title
            tit_elem.text = currtitle
            lect_elem = ET.Element("Lecture", {"Classroom": currclassroom})
            day_elem = ET.Element("Day")
            day_elem.text = currday
            time_elem = ET.Element("Time")
            time_elem.text = currtim
            lect_elem.append(day_elem) #append to parent
            lect_elem.append(time_elem)
            prof_elem = ET.Element("Professor")
            prof_elem.text = currprof
            lesson_elem.append(tit_elem)
            lesson_elem.append(lect_elem)
            lesson_elem.append(prof_elem)
            root.append(lesson_elem)
            tree.write(currfile1) #add the changes to the previous file


        submit = tk.Button(self, text="Add", font=helv36, background='white', command=lambda: insert_data(lecTitle, lecProf, lecDay, lecTime, lecClass))
        submit.place(x=350, y=120)
        label = tk.Label(self, text="Select Day:",
                         font=controller.title_font, background='white')
        label.place(x=35, y=235)
        week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        chosenDay =StringVar(self)
        chosenDay.set(week[0]) #default value
        dropdown = OptionMenu(self, chosenDay, *week) #creates a dropdown list with all the days of the week
        dropdown.place(x=180, y=242)
        def showXMLdata(x):
            #x is the day that the use chose from the dropdown list
            tree = etree.parse(currfile1) #the XML file that the user submitted on the 1st page
            root = tree.getroot()
            #all XML given have 'schedule' as their namespace, so using {schedule} is mandatory
            for k in root.findall('{schedule}Lesson'): #find all Lesson nodes
                #save data in variables
                curtitle = k.find("{schedule}Title").text
                curprofessor = k.find("{schedule}Professor").text
                for j in k.findall('{schedule}Lecture'): #find sub-node Lecture inside node Lesson
                    classroom = j.get('Classroom')
                    selectedDay = j.find("{schedule}Day").text
                    if selectedDay == str(x.get()): #check if day in XML is the one the user chose
                        #show data on console
                        #in case something doesn't exist in XML, it shows in console as "None"
                        print("Title: ", curtitle , "\n")
                        print("Professor: ", curprofessor , "\n")
                        print("Day: ", x.get() , "\n")
                        print("Classroom: ", classroom)

        showData = tk.Button(self, text="Show Data", font=helv36, background='white', command=lambda: showXMLdata(chosenDay)) #shows data from XML based on the chosen day
        showData.place(x=300, y=240)





if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()