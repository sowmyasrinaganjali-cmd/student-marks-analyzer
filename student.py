"""
Student Marks Analyzer
----------------------
A console-based project that lets you:
  1. Add students and their marks
  2. View a report card / ranking of all students
  3. Search for a single student
  4. See subject-wise analysis (average, highest, lowest, pass %)
  5. See class summary (topper, class average, pass/fail count)
  6. Save to / load from a CSV file

Only built-in Python modules are used, so no installation is needed.
Run with:  python student_marks_analyzer.py
"""

import csv
import os

# ---------- Settings (change these to fit your project) ----------
SUBJECTS = ["Maths", "Physics", "Chemistry", "English", "Computer"]
MAX_MARKS = 100          # maximum marks per subject
PASS_MARKS = 40          # minimum marks needed to pass a subject
DATA_FILE = "students.csv"

# students = [{"name": "Asha", "marks": {"Maths": 90, ...}}, ...]
students = []


# ---------- Helper functions ----------
def read_int(prompt, low, high):
    """Keep asking until the user enters a whole number between low and high."""
    while True:
        try:
            value = int(input(prompt))
            if low <= value <= high:
                return value
            print(f"  Please enter a number between {low} and {high}.")
        except ValueError:
            print("  Invalid input. Please enter a whole number.")


def get_grade(percentage):
    if percentage >= 90:
        return "A+"
    if percentage >= 80:
        return "A"
    if percentage >= 70:
        return "B"
    if percentage >= 60:
        return "C"
    if percentage >= 50:
        return "D"
    if percentage >= PASS_MARKS:
        return "E"
    return "F"


def calculate(student):
    """Return total, percentage, grade and pass/fail result for one student."""
    total = sum(student["marks"].values())
    percentage = total / (MAX_MARKS * len(SUBJECTS)) * 100
    failed_any = any(m < PASS_MARKS for m in student["marks"].values())
    result = "FAIL" if failed_any else "PASS"
    grade = "F" if failed_any else get_grade(percentage)
    return total, percentage, grade, result


def ranked_students():
    """Students sorted from highest total to lowest total."""
    return sorted(students, key=lambda s: calculate(s)[0], reverse=True)


def find_student(name):
    for s in students:
        if s["name"].lower() == name.lower():
            return s
    return None


# ---------- Menu actions ----------
def add_student():
    name = input("Enter student name: ").strip()
    if not name:
        print("  Name cannot be empty.")
        return
    if find_student(name):
        print("  A student with this name already exists.")
        return

    marks = {}
    for subject in SUBJECTS:
        marks[subject] = read_int(f"  Marks in {subject} (0-{MAX_MARKS}): ", 0, MAX_MARKS)

    students.append({"name": name, "marks": marks})
    print(f"  Added {name} successfully!")


def view_all():
    if not students:
        print("  No student data yet.")
        return

    header = f"{'Rank':<5}{'Name':<15}" + "".join(f"{s[:7]:<9}" for s in SUBJECTS)
    header += f"{'Total':<7}{'%':<8}{'Grade':<6}{'Result'}"
    print("\n" + header)
    print("-" * len(header))

    for rank, s in enumerate(ranked_students(), start=1):
        total, pct, grade, result = calculate(s)
        row = f"{rank:<5}{s['name'][:14]:<15}"
        row += "".join(f"{s['marks'][sub]:<9}" for sub in SUBJECTS)
        row += f"{total:<7}{pct:<8.2f}{grade:<6}{result}"
        print(row)


def search_student():
    name = input("Enter student name to search: ").strip()
    s = find_student(name)
    if not s:
        print("  Student not found.")
        return

    total, pct, grade, result = calculate(s)
    rank = ranked_students().index(s) + 1
    print(f"\n--- Report Card: {s['name']} ---")
    for sub in SUBJECTS:
        m = s["marks"][sub]
        status = "" if m >= PASS_MARKS else "  (failed)"
        print(f"  {sub:<12}: {m}/{MAX_MARKS}{status}")
    print(f"  Total       : {total}/{MAX_MARKS * len(SUBJECTS)}")
    print(f"  Percentage  : {pct:.2f}%")
    print(f"  Grade       : {grade}")
    print(f"  Result      : {result}")
    print(f"  Class rank  : {rank} of {len(students)}")


def subject_analysis():
    if not students:
        print("  No student data yet.")
        return

    print(f"\n{'Subject':<12}{'Average':<10}{'Highest':<18}{'Lowest':<18}{'Pass %'}")
    print("-" * 70)
    for sub in SUBJECTS:
        scores = [(s["marks"][sub], s["name"]) for s in students]
        avg = sum(m for m, _ in scores) / len(scores)
        high = max(scores)
        low = min(scores)
        passed = sum(1 for m, _ in scores if m >= PASS_MARKS)
        pass_pct = passed / len(scores) * 100
        print(f"{sub:<12}{avg:<10.2f}{str(high[0]) + ' (' + high[1][:8] + ')':<18}"
              f"{str(low[0]) + ' (' + low[1][:8] + ')':<18}{pass_pct:.1f}%")


def class_summary():
    if not students:
        print("  No student data yet.")
        return

    ranked = ranked_students()
    percentages = [calculate(s)[1] for s in students]
    passed = sum(1 for s in students if calculate(s)[3] == "PASS")

    print("\n--- Class Summary ---")
    print(f"  Total students : {len(students)}")
    print(f"  Class average  : {sum(percentages) / len(percentages):.2f}%")
    print(f"  Passed         : {passed}")
    print(f"  Failed         : {len(students) - passed}")
    print("  Top 3 students :")
    for i, s in enumerate(ranked[:3], start=1):
        total, pct, _, _ = calculate(s)
        print(f"    {i}. {s['name']} - {total} marks ({pct:.2f}%)")


def save_data():
    with open(DATA_FILE, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Name"] + SUBJECTS)
        for s in students:
            writer.writerow([s["name"]] + [s["marks"][sub] for sub in SUBJECTS])
    print(f"  Saved {len(students)} students to {DATA_FILE}")


def load_data():
    if not os.path.exists(DATA_FILE):
        print("  No saved file found yet.")
        return

    students.clear()
    with open(DATA_FILE, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            marks = {sub: int(row[sub]) for sub in SUBJECTS}
            students.append({"name": row["Name"], "marks": marks})
    print(f"  Loaded {len(students)} students from {DATA_FILE}")


# ---------- Main program ----------
def main():
    actions = {
        "1": ("Add student", add_student),
        "2": ("View all students (ranked)", view_all),
        "3": ("Search student / report card", search_student),
        "4": ("Subject-wise analysis", subject_analysis),
        "5": ("Class summary", class_summary),
        "6": ("Save to CSV", save_data),
        "7": ("Load from CSV", load_data),
    }

    load_data_silently = os.path.exists(DATA_FILE)
    if load_data_silently:
        load_data()

    while True:
        print("\n===== STUDENT MARKS ANALYZER =====")
        for key, (label, _) in actions.items():
            print(f"  {key}. {label}")
        print("  0. Exit")

        choice = input("Choose an option: ").strip()
        if choice == "0":
            print("Goodbye!")
            break
        elif choice in actions:
            actions[choice][1]()
        else:
            print("  Invalid choice, try again.")


if __name__ == "__main__":
    main()