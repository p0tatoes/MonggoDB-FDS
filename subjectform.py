import tkinter as tk
from tkinter import messagebox

import pymongo


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
                    mgrid.grid(column=j + 6, row=i + 8)
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

        def courseFilter():
            for label in subjectWindow.grid_slaves():
                if int(label.grid_info()["row"] > 7):
                    label.grid_forget()

            filterId = int(idFilterField.get())

            idOption = unitsOption = str()

            dbList.clear()
            dbList.append(["ID", "CODE", "DESCRIPTION", "UNITS", "SCHEDULE"])

            if idFilterOption.get() == ">":
                idOption = "$gt"
            elif idFilterOption.get() == ">=":
                idOption = "$gte"
            elif idFilterOption.get() == "<":
                idOption = "$lt"
            elif idFilterOption.get() == "<=":
                idOption = "$lte"
            elif idFilterOption.get() == "!=":
                idOption = "$ne"
            elif idFilterOption.get() == "=":
                idOption = "$eq"

            if unitsFilterOption.get() == ">":
                unitsOption = "$gt"
            elif unitsFilterOption.get() == ">=":
                unitsOption = "$gte"
            elif unitsFilterOption.get() == "<":
                unitsOption = "$lt"
            elif unitsFilterOption.get() == "<=":
                unitsOption = "$lte"
            elif unitsFilterOption.get() == "!=":
                unitsOption = "$ne"
            elif unitsFilterOption.get() == "=":
                unitsOption = "$eq"
            codeStart = f"^{codeFilterField.get()}"
            descStart = f"^{descriptionFilterField.get()}"
            units = int(unitsFilterField.get())
            schedStart = f"^{scheduleFilterField.get()}"
            coursesCursor = collection.find(
                {
                    "id": {idOption: filterId},
                    "code": {"$regex": codeStart},
                    "description": {"$regex": descStart},
                    "units": {unitsOption: units},
                    "schedule": {"$regex": schedStart},
                }
            )
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
                    mgrid.grid(column=j + 6, row=i + 8)
                    mgrid.bind("<Button-1>", callback)

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
        courseId = tk.IntVar(subjectWindow)
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
        idFilter = tk.IntVar(subjectWindow)
        idFilterField = tk.Entry(subjectWindow, textvariable=idFilter, width=10)
        idFilterField.grid(column=6, row=6)

        # * Code Text Field
        codeFilterLabel = tk.Label(subjectWindow, text="Code", bg="orange")
        codeFilterLabel.grid(column=7, row=5)
        codeFilter = tk.StringVar(subjectWindow)
        codeFilterField = tk.Entry(subjectWindow, textvariable=codeFilter, width=10)
        codeFilterField.grid(column=7, row=6)

        # * Description Start Text Field
        descFilterLabel = tk.Label(subjectWindow, text="Description", bg="orange")
        descFilterLabel.grid(column=8, row=5)
        descriptionFilter = tk.StringVar(subjectWindow)
        descriptionFilterField = tk.Entry(
            subjectWindow, textvariable=descriptionFilter, width=10
        )
        descriptionFilterField.grid(column=8, row=6)

        # * Units Filter Option Menu
        unitsFilterLabel = tk.Label(subjectWindow, text="Units", bg="orange")
        unitsFilterLabel.grid(column=9, row=4)
        unitsFilterOptions = [">", ">=", "<", "<=", "!=", "="]
        unitsFilterOption = tk.StringVar(subjectWindow)
        unitsFilterOption.set(unitsFilterOptions[0])
        unitsFilterDrpDwn = tk.OptionMenu(
            subjectWindow, unitsFilterOption, *unitsFilterOptions
        )
        unitsFilterDrpDwn.grid(column=9, row=5)

        # * Units Text Field
        unitsFilter = tk.IntVar(subjectWindow)
        unitsFilterField = tk.Entry(subjectWindow, textvariable=unitsFilter, width=10)
        unitsFilterField.grid(column=9, row=6)

        # * Schedule Text Field
        scheduleLabel = tk.Label(subjectWindow, text="schedule", bg="orange")
        scheduleLabel.grid(column=10, row=5)
        scheduleFilter = tk.StringVar(subjectWindow)
        scheduleFilterField = tk.Entry(
            subjectWindow, textvariable=scheduleFilter, width=10
        )
        scheduleFilterField.grid(column=10, row=6)

        # * Filter Button
        filterBtn = tk.Button(
            subjectWindow, text="Filter", command=courseFilter, width=10, bg="deep pink"
        )
        filterBtn.grid(column=11, row=6)

        # ! End of Filters

        subjectWindow.mainloop()
