# University Management System
# OOPs, Functions, list comprehension, Git & Github, Cloud

# to build the frontend
import streamlit as st

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

class teacher(person):
    def __init__(self, branch, name, subject):
        super().__init__(branch, name)
        self.subject = subject

# finding and returning the college which student selected
def find_college(cname):
    return next((c for c in st.session_state.colleges if c.cname == cname), None)
# Create a New college
if menu_choice == "Create College":
    cname = st.text_input("Enter New College Name")
    if st.button("CREATE"):
        st.session_state.colleges.append(college(cname))
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


                st.success("Teacher deleted successfully!")


            else:
                st.error("Teacher not found")
elif menu_choice == "List College":
    if not st.session_state.colleges:
        st.info("Please insert a college first")
    else:
        for i,c in enumerate(st.session_state.colleges,1):
            st.write(f"{i}:{c.cname}")