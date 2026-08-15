# University Management System
# OOPs, Functions, list comprehension, Git & Github, Cloud

# to build the frontend
import streamlit as st
import json

# app front page configuration
st.set_page_config(
    page_title = "UMS portal",
    layout = "wide"
)

st.title("University Management System")

# create a empty list to store list of colleges
if "colleges" not in st.session_state:
    st.session_state.colleges = []


# side bar
menu_choice = st.sidebar.radio(
    "SELECT ACTION",
    (
        "Create College",
        "Add Student",
        "Add Teacher",
        "Display Students",
        "Search Student",
        "Update Student",
        "Delete Student",
        "Academic Management",
        "View Academic Record",
        "Display Teachers",
        "Search Teacher",
        "Update Teacher",
        "Delete Teacher",
        "List College"
    )
)
# This class will add new student and teacher in a college
class college:
    def __init__(self, cname):
        self.cname = cname  # storing name of college
        self.students = []  # list of student objects
        self.teachers = []  # list of teacher objects

    def add_student(self, s):  # adding new student in the student list
        self.students.append(s)
    def add_teacher(self, t):  # New teacher will be added into teacher list
        self.teachers.append(t)

class person:
    def __init__(self, branch, name):
        self.branch = branch
        self.name = name

class student(person):
    def __init__(self, rollno, name, branch):
        super().__init__(branch, name)
        self.rollno = rollno
        self.semester = None
        self.subjects = []
        self.attendance = {}
        self.marks = None
        self.grade = None

class teacher(person):
    def __init__(self, branch, name, subject):
        super().__init__(branch, name)
        self.subject = subject

# finding and returning the college which student selected
def find_college(cname):
    return next((c for c in st.session_state.colleges if c.cname == cname), None)

# load saved data
if "data_loaded" not in st.session_state:
    st.session_state.data_loaded = True

    try:
        with open("ums_data.json", "r") as file:
            saved_data = json.load(file)

        for college_data in saved_data.get("colleges", []):

            clg = college(college_data["cname"])

            for student_data in college_data.get("students", []):
                s = student(
                    student_data["rollno"],
                    student_data["name"],
                    student_data["branch"]
                )

                s.semester = student_data.get("semester")
                s.subjects = student_data.get("subjects", [])
                s.attendance = student_data.get("attendance", {})
                s.marks = student_data.get("marks")
                s.grade = student_data.get("grade")

                clg.add_student(s)

            for teacher_data in college_data.get("teachers", []):

                t = teacher(
                    teacher_data["branch"],
                    teacher_data["name"],
                    teacher_data["subject"]
                )

                clg.add_teacher(t)

            st.session_state.colleges.append(clg)

    except (FileNotFoundError, json.JSONDecodeError):
        pass

def save_data():
    data = {
        "colleges": []
    }

    for c in st.session_state.colleges:

        college_data = {
            "cname": c.cname,
            "students": [],
            "teachers": []
        }

        for s in c.students:
            student_data = {
                "rollno": s.rollno,
                "name": s.name,
                "branch": s.branch,
                "semester": s.semester,
                "subjects": s.subjects,
                "attendance": s.attendance,
                "marks": getattr(s, "marks", None),
                "grade": getattr(s, "grade", None)
            }

            college_data["students"].append(student_data)

        for t in c.teachers:
            teacher_data = {
                "name": t.name,
                "branch": t.branch,
                "subject": t.subject
            }

            college_data["teachers"].append(teacher_data)

        data["colleges"].append(college_data)

    with open("ums_data.json", "w") as file:
        json.dump(data, file, indent=4)


# Create a New college
if menu_choice == "Create College":
    cname = st.text_input("Enter New College Name")
    if st.button("CREATE"):
        st.session_state.colleges.append(college(cname))
        save_data()
        st.success(f"{cname} created successfully")

elif menu_choice == "Add Student":
    if not st.session_state.colleges:
        st.info("Please insert a college first")
    else:
        clgname = st.selectbox("Choose college", [c.cname for c in st.session_state.colleges])
        roll = st.text_input("Enter your Roll Number")
        sname = st.text_input("Enter Student Name")
        branch = st.text_input("Enter the branch")
        if st.button("ADD STUDENT"):
            if not(roll and sname and branch and clgname):
                st.error("Please Enter all the details")
            else:
                clg = find_college(clgname)
                clg.add_student(student(roll, sname, branch))
                save_data()
                st.success("Student added successfully")

elif menu_choice == "Add Teacher":
    if not st.session_state.colleges:
        st.info("Please insert a college first")
    else:
        clgname = st.selectbox("Choose college", [c.cname for c in st.session_state.colleges])
        subject = st.text_input("Enter your subject")
        tname = st.text_input("Enter teacher Name")
        branch = st.text_input("Enter the branch")
        if st.button("ADD TEACHER"):
            if not(subject and tname and branch and clgname):
                st.error("Please Enter all the details")
            else:
                clg = find_college(clgname)
                clg.add_teacher(teacher(branch, tname, subject))
                save_data()
                st.success("teacher added successfully")

elif menu_choice == "Display Students":
    if not st.session_state.colleges:
        st.info("Please insert a college first")
    else:
        clgname = st.selectbox(
            "Choose college",
            [c.cname for c in st.session_state.colleges]
        )

        clg = find_college(clgname)

        st.subheader(f"List of students in {clgname}")

        if clg.students:
            for i, s in enumerate(clg.students, 1):
                st.write(f"{i}. {s.name}")
        else:
            st.warning("No student Found")

elif menu_choice == "Search Student":

    if not st.session_state.colleges:
        st.info("Please insert a college first")

    else:
        clgname = st.selectbox(
            "Choose college",
            [c.cname for c in st.session_state.colleges]
        )

        clg = find_college(clgname)

        roll = st.text_input("Enter Student Roll Number")

        if st.button("SEARCH"):

            found_student = None

            for s in clg.students:
                if s.rollno == roll:
                    found_student = s
                    break

            if found_student:
                st.success("Student found!")
                st.write("Roll Number:", found_student.rollno)
                st.write("Name:", found_student.name)
                st.write("Branch:", found_student.branch)

            else:
                st.error("Student not found")

elif menu_choice == "Update Student":

    if not st.session_state.colleges:
        st.info("Please insert a college first")

    else:
        clgname = st.selectbox(
            "Choose college",
            [c.cname for c in st.session_state.colleges]
        )

        clg = find_college(clgname)

        roll = st.text_input("Enter Student Roll Number")

        if st.button("FIND STUDENT"):

            found_student = None

            for s in clg.students:
                if s.rollno == roll:
                    found_student = s
                    break

            if found_student:

                st.success("Student found!")

                new_name = st.text_input(
                    "Enter New Name",
                    value=found_student.name
                )

                new_branch = st.text_input(
                    "Enter New Branch",
                    value=found_student.branch
                )

                if st.button("UPDATE"):

                    found_student.name = new_name
                    found_student.branch = new_branch
                    save_data()

                    st.success("Student updated successfully!")

            else:
                st.error("Student not found")

elif menu_choice == "Delete Student":

    if not st.session_state.colleges:
        st.info("Please insert a college first")

    else:
        clgname = st.selectbox(
            "Choose college",
            [c.cname for c in st.session_state.colleges]
        )

        clg = find_college(clgname)

        roll = st.text_input("Enter Student Roll Number")

        if st.button("DELETE"):

            found_student = None

            for s in clg.students:
                if s.rollno == roll:
                    found_student = s
                    break

            if found_student:

                clg.students.remove(found_student)

                save_data()

                st.success("Student deleted successfully!")

            else:
                st.error("Student not found")


elif menu_choice == "Display Teachers":
    if not st.session_state.colleges:
        st.info("Please insert a college first")
    else:
        clgname = st.selectbox(
            "Choose college",
            [c.cname for c in st.session_state.colleges]
        )

        clg = find_college(clgname)

        st.subheader(f"List of teachers in {clgname}")

        if clg.teachers:
            for i, t in enumerate(clg.teachers, 1):
                st.write(f"{i}. {t.name}")
        else:
            st.warning("No Teacher Found")

elif menu_choice == "Academic Management":


    if not st.session_state.colleges:
        st.info("Please insert a college first")

    else:
        clgname = st.selectbox(
            "Choose college",
            [c.cname for c in st.session_state.colleges]
        )

        clg = find_college(clgname)

        roll = st.text_input("Enter Student Roll Number")

        semester = st.selectbox(
            "Select Semester",
            ["Semester 1", "Semester 2", "Semester 3",
             "Semester 4", "Semester 5", "Semester 6",
             "Semester 7", "Semester 8"]
        )

        subjects = st.text_input(
            "Enter Subjects (separate with comma)"
        )
        attendence = st.number_input(
            "Enter Attendance Percentage",
            min_value=0.0,
            max_value=100.0,
            step=1.0
        )

        marks = st.number_input(
            "Enter Marks",
            min_value=0.0,
            max_value=100.0,
            step=1.0
        )

        if st.button("SAVE ACADEMIC DETAILS"):

            found_student = None

            for s in clg.students:
                if s.rollno == roll:
                    found_student = s
                    break

            if found_student:

                found_student.semester = semester

                found_student.subjects = [
                    subject.strip()
                    for subject in subjects.split(",")
                    if subject.strip()
                ]
                found_student.attendance = attendence
                
                found_student.marks = marks
                if marks >=90:
                    found_student.grade = "A+"
                elif marks >=80:
                    found_student.grade = "A"
                elif marks >=70:
                    found_student.grade = "B+"
                elif marks >=60:
                    found_student.grade = "B"
                elif marks >=50:
                    found_student.grade = "C"
                else:
                    found_student.grade = "F"

                save_data()

                st.success("Academic details saved successfully!")

                st.write("Student:", found_student.name)
                st.write("Semester:", found_student.semester)
                st.write("Subjects:", found_student.subjects)
                st.write("Attendance:", found_student.attendance)
                st.write("Marks:", found_student.marks)
                st.write("Grade:", found_student.grade)
            else:
                st.error("Student not found")

elif menu_choice == "View Academic Record":

    if not st.session_state.colleges:
        st.info("Please insert a college first")

    else:
        clgname = st.selectbox(
            "Choose college",
            [c.cname for c in st.session_state.colleges]
        )

        clg = find_college(clgname)

        roll = st.text_input("Enter Student Roll Number")

        if st.button("VIEW RECORD"):

            found_student = None

            for s in clg.students:
                if s.rollno == roll:
                    found_student = s
                    break
            if found_student:

                st.success("Academic Record Found!")

                st.write("Student:", found_student.name)
                st.write("Roll Number:", found_student.rollno)
                st.write("Branch:", found_student.branch)
                st.write("Semester:", found_student.semester)
                st.write("Subjects:", found_student.subjects)
                st.write("Attendance:", found_student.attendance)
                st.write("Marks:", found_student.marks)
                st.write("Grade:", found_student.grade)

            else:
                st.error("Student not found")


elif menu_choice == "Search Teacher":


    if not st.session_state.colleges:
        st.info("Please insert a college first")


    else:
        clgname = st.selectbox(
            "Choose college",
            [c.cname for c in st.session_state.colleges]
        )


        clg = find_college(clgname)


        tname = st.text_input("Enter Teacher Name")


        if st.button("SEARCH"):


            found_teacher = None


            for t in clg.teachers:
                if t.name == tname:
                    found_teacher = t
                    break


            if found_teacher:
                st.success("Teacher found!")
                st.write("Name:", found_teacher.name)
                st.write("Branch:", found_teacher.branch)
                st.write("Subject:", found_teacher.subject)


            else:
                st.error("Teacher not found")


elif menu_choice == "Update Teacher":


    if not st.session_state.colleges:
        st.info("Please insert a college first")


    else:
        clgname = st.selectbox(
            "Choose college",
            [c.cname for c in st.session_state.colleges]
        )


        clg = find_college(clgname)


        tname = st.text_input("Enter Teacher Name")


        if st.button("FIND TEACHER"):
            found_teacher = None


            for t in clg.teachers:
                if t.name == tname:
                    found_teacher = t
                    break


            if found_teacher:


                st.success("Teacher found!")


                new_name = st.text_input(
                    "Enter New Name",
                    value=found_teacher.name
                )


                new_branch = st.text_input(
                    "Enter New Branch",
                    value=found_teacher.branch
                )


                new_subject = st.text_input(
                    "Enter New Subject",
                    value=found_teacher.subject
                )


                if st.button("UPDATE"):


                    found_teacher.name = new_name
                    found_teacher.branch = new_branch
                    found_teacher.subject = new_subject

                    save_data()
                    st.success("Teacher updated successfully!")


            else:
                st.error("Teacher not found")


elif menu_choice == "Delete Teacher":


    if not st.session_state.colleges:
        st.info("Please insert a college first")


    else:
        clgname = st.selectbox(
            "Choose college",
            [c.cname for c in st.session_state.colleges]
        )


        clg = find_college(clgname)


        tname = st.text_input("Enter Teacher Name")


        if st.button("DELETE"):


            found_teacher = None


            for t in clg.teachers:
                if t.name == tname:
                    found_teacher = t
                    break


            if found_teacher:


                clg.teachers.remove(found_teacher)

                save_data()
                st.success("Teacher deleted successfully!")


            else:
                st.error("Teacher not found")


elif menu_choice == "List College":
    if not st.session_state.colleges:
        st.info("Please insert a college first")
    else:
        for i,c in enumerate(st.session_state.colleges,1):
            st.write(f"{i}:{c.cname}")