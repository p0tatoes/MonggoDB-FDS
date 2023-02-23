import tkinter as tk
from tkinter import messagebox

import pymongo


# TODO: add mongodb collection containing subject's id, code, description, units, schedule
class SubjectForm:
    def subjectform():
        client = pymongo.MongoClient("mongodb://127.0.0.1:27017")

        db = client["fundadb"]
        collection = db["courses"]

        dbList = list()

        def callback(event):
            li = list()
            li = event.widget._values
            courseId.set(dbList[li[1]][0])
            courseCode.set(dbList[li[1]][1])
            courseDescription.set(dbList[li[1]][2])
            courseUnits.set(dbList[li[1]][3])
            courseSchedule.set(dbList[li[1]][4])
            print(
                dbList[li[1]][0],
                dbList[li[1]][1],
                dbList[li[1]][2],
                dbList[li[1]][3],
                dbList[li[1]][4],
            )

        def createGrid(x):
            dbList.clear()
            dbList.append(["ID", "CODE", "DESCRIPTION", "UNITS", "SCHEDULE"])
            coursesCursor = collection.find()
            for entry in coursesCursor:
                entryId = entry["id"]
                entryCode = entry["code"]
                entryDesc = entry["description"]
                entryUnits = entry["units"]
                entrySchedule = entry["schedule"]
                dbList.append(
                    [entryId, entryCode, entryDesc, entryUnits, entrySchedule]
                )

            for i in range(len(dbList)):
                for j in range(len(dbList[0])):
                    mgrid = tk.Entry(subjectWindow, width=10)
                    mgrid.insert(tk.END, dbList[i][j])
                    mgrid._values = mgrid.get(), i
                    mgrid.grid(row=i + 8, column=j + 6)
                    mgrid.bind("<Button-1>", callback)

            if x == 1:
                for label in subjectWindow.grid_slaves():
                    if int(label.grid_info()["row"] > 7):
                        label.grid_forget()

        def save():
            option = messagebox.askokcancel("Save", "Save entry to record?")
            if option:
                newId = collection.count_documents({})
                if newId > 0:
                    newId = collection.find_one(sort=[("id", -1)])["id"]
                id = newId + 1
                courseId.set(id)
                insertDict = {
                    "id": int(courseId.get()),
                    "code": codeField.get(),
                    "description": descField.get(),
                    "units": int(unitsField.get()),
                    "schedule": scheduleField.get(),
                }
                collection.insert_one(insertDict)
                createGrid(1)
                createGrid(0)

        def delete():
            option = messagebox.askokcancel("Delete", "Delete record entry?")
            if option:
                delQuery = {"id": int(idField.get())}
                collection.delete_one(delQuery)
                createGrid(1)
                createGrid(0)

        def update():
            option = messagebox.askokcancel("Update", "Update an entry?")
            if option:
                idQuery = {"id": int(idField.get())}
                updateValues = {
                    "$set": {
                        "code": codeField.get(),
                        "description": descField.get(),
                        "units": unitsField.get(),
                        "schedule": scheduleField.get(),
                    }
                }
                collection.update_one(idQuery, updateValues)
                createGrid(1)
                createGrid(0)

        # * subjectWindow
        subjectWindow = tk.Tk()
        subjectWindow.title("Courses Form")
        subjectWindow.geometry("1000x750")
        subjectWindow.configure(bg="purple")

        # * Labels
        titleBar = tk.Label(
            subjectWindow,
            text="Courses Enlistment Form",
            width=30,
            height=1,
            bg="cyan",
            anchor="center",
            font="Roboto 18 bold",
        )
        titleBar.grid(column=1, row=1, columnspan=2)

        idLabel = tk.Label(
            subjectWindow,
            text="Course ID:",
            width=15,
            height=1,
            bg="orange",
            font="Roboto 14 bold",
        )
        idLabel.grid(column=1, row=2)

        codeLabel = tk.Label(
            subjectWindow,
            text="Course Code:",
            width=15,
            height=1,
            bg="orange",
            font="Roboto 14 bold",
        )
        codeLabel.grid(column=1, row=3)

        descriptionLabel = tk.Label(
            subjectWindow,
            text="Course Description:",
            width=15,
            height=1,
            bg="orange",
            font="Roboto 14 bold",
        )
        descriptionLabel.grid(column=1, row=4)

        unitsLabel = tk.Label(
            subjectWindow,
            text="Course Units:",
            width=15,
            height=1,
            bg="orange",
            font="Roboto 14 bold",
        )
        unitsLabel.grid(column=1, row=5)

        scheduleLabel = tk.Label(
            subjectWindow,
            text="Course Schedule:",
            width=15,
            height=1,
            bg="orange",
            font="Roboto 14 bold",
        )
        scheduleLabel.grid(column=1, row=6)

        # * Enter Fields
        courseId = tk.StringVar(subjectWindow)
        idField = tk.Entry(subjectWindow, textvariable=courseId, state=tk.DISABLED)
        idField.grid(column=2, row=2)

        courseCode = tk.StringVar(subjectWindow)
        codeField = tk.Entry(subjectWindow, textvariable=courseCode, width=40)
        codeField.grid(column=2, row=3)

        courseDescription = tk.StringVar(subjectWindow)
        descField = tk.Entry(subjectWindow, textvariable=courseDescription, width=40)
        descField.grid(column=2, row=4)

        courseUnits = tk.StringVar(subjectWindow)
        unitsField = tk.Entry(subjectWindow, textvariable=courseUnits, width=40)
        unitsField.grid(column=2, row=5)

        courseSchedule = tk.StringVar(subjectWindow)
        scheduleField = tk.Entry(subjectWindow, textvariable=courseSchedule, width=40)
        scheduleField.grid(column=2, row=6)

        createGrid(0)

        # * Buttons
        saveBtn = tk.Button(master=subjectWindow, text="Save", command=save, width=25)
        saveBtn.grid(column=1, row=7)

        updateBtn = tk.Button(
            master=subjectWindow, text="Update", command=update, width=25
        )
        updateBtn.grid(column=2, row=7)

        deleteBtn = tk.Button(
            master=subjectWindow, text="Delete", command=delete, width=25
        )
        deleteBtn.grid(column=3, row=7)

        # TODO: Refactor to filter subjects
        # ! Filters
        filterLabel = tk.Label(
            subjectWindow, text="Filters", bg="cyan", font="Robot 12 bold", width=30
        )
        filterLabel.grid(column=6, row=2, columnspan=4)
        # * ID Filter Option Menu
        idFilterLabel = tk.Label(subjectWindow, text="ID", bg="orange")
        idFilterLabel.grid(column=6, row=4)
        idFilterOptions = [">", ">=", "<", "<=", "!=", "="]
        idFilterOption = tk.StringVar(subjectWindow)
        idFilterOption.set(idFilterOptions[0])
        idFilterDrpDwn = tk.OptionMenu(subjectWindow, idFilterOption, *idFilterOptions)
        idFilterDrpDwn.grid(column=6, row=5)

        # * ID Filter Text Field
        idFilter = tk.IntVar()
        idFilterField = tk.Entry(subjectWindow, textvariable=idFilter, width=10)
        idFilterField.grid(column=6, row=6)

        # * Name Start Text Field
        nameStartLabel = tk.Label(subjectWindow, text="Name Start", bg="orange")
        nameStartLabel.grid(column=7, row=3)
        nameStartFilter = tk.StringVar()
        nameStartFilterField = tk.Entry(
            subjectWindow, textvariable=nameStartFilter, width=10
        )
        nameStartFilterField.grid(column=7, row=4)

        # * Name End Text Field
        nameEndLabel = tk.Label(subjectWindow, text="Name End", bg="orange")
        nameEndLabel.grid(column=7, row=5)
        nameEndFilter = tk.StringVar()
        nameEndFilterField = tk.Entry(
            subjectWindow, textvariable=nameEndFilter, width=10
        )
        nameEndFilterField.grid(column=7, row=6)

        # * Mail Start Text Field
        mailStartLabel = tk.Label(subjectWindow, text="Mail Start", bg="orange")
        mailStartLabel.grid(column=8, row=5)
        mailStartFilter = tk.StringVar()
        mailStartFilterField = tk.Entry(
            subjectWindow, textvariable=mailStartFilter, width=10
        )
        mailStartFilterField.grid(column=8, row=6)

        # * Program Text Field
        programLabel = tk.Label(subjectWindow, text="Program", bg="orange")
        programLabel.grid(column=9, row=5)
        programFilter = tk.StringVar()
        programFilterField = tk.Entry(
            subjectWindow, textvariable=programFilter, width=10
        )
        programFilterField.grid(column=9, row=6)

        # ! End of Filters

        subjectWindow.mainloop()
