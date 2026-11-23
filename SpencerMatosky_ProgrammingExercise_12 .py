"""
SpencerMatosky_ProgrammingExercise_12.py

A console application that uses numpy to analyze student exam grades
stored in a CSV file. The file must have a header row, an optional first
column of student names, and one numeric column for each exam. The
program loads the grades into a numpy array, prints the first few rows,
and then prints the mean, median, standard deviation, minimum, and
maximum for each exam and for all exams combined. It also reports how
many students passed and failed each exam (a passing grade is 60 or
above) and the overall pass percentage.

Usage:
    python SpencerMatosky_ProgrammingExercise_12.py             analyze the
        default file, SpencerMatosky_ProgrammingExercise_12_Grades.csv
    python SpencerMatosky_ProgrammingExercise_12.py file.csv    analyze
        a different CSV file
    python SpencerMatosky_ProgrammingExercise_12.py --test      run the
        built-in tests
"""

import csv
import os
import sys
import tempfile

import numpy as np

# CSV file analyzed when no file name is given on the command line. It is
# looked for in the same folder as this program, so the program works no
# matter which folder it is run from.
DEFAULT_FILE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "SpencerMatosky_ProgrammingExercise_12_Grades.csv",
)

# Lowest grade that counts as a pass
PASSING_GRADE = 60

# Number of rows shown in the preview of the data
PREVIEW_ROWS = 5


def load_grades(filename):
    """
    Load student names, exam names, and grades from a CSV file.

    The first row must be a header. Any column whose first data value is
    not a number (normally the student name) is treated as a name column;
    every numeric column is treated as an exam. The grades are loaded
    into a two-dimensional numpy array with one row per student and one
    column per exam.

    Args:
        filename (str): path of the CSV file to read.

    Returns:
        tuple: (student_names, exam_names, grades) where student_names
            is a list of str, exam_names is a list of str, and grades is
            a numpy array of floats.

    Raises:
        FileNotFoundError: if the file does not exist.
        ValueError: if the file has no data rows or has missing grades.
    """
    # Read the header and the text of every row so names can be found
    with open(filename, newline="") as file:
        rows = [row for row in csv.reader(file) if row]

    if len(rows) < 2:
        raise ValueError("The CSV file must have a header and data rows.")

    header = rows[0]
    first_row = rows[1]
    exam_columns = []
    name_column = None

    # Decide which columns hold grades and which hold student names
    for column, value in enumerate(first_row):
        try:
            float(value)
            exam_columns.append(column)
        except ValueError:
            if name_column is None:
                name_column = column

    # Load the numeric columns into a numpy array
    grades = np.genfromtxt(
        filename, delimiter=",", skip_header=1, usecols=exam_columns, ndmin=2
    )

    if np.isnan(grades).any():
        raise ValueError("The CSV file has missing or invalid grades.")

    # Use the name column if there is one; otherwise number the students
    if name_column is None:
        student_names = [f"Student {n}" for n in range(1, len(rows))]
    else:
        student_names = [row[name_column] for row in rows[1:]]

    exam_names = [header[column] for column in exam_columns]
    return student_names, exam_names, grades


def display_preview(student_names, exam_names, grades, count=PREVIEW_ROWS):
    """
    Print the first few rows of the dataset.

    Args:
        student_names (list of str): the student names.
        exam_names (list of str): the exam names.
        grades (numpy.ndarray): the grades, one row per student.
        count (int): the number of rows to print (default 5).

    Returns:
        None
    """
    print(f"First {min(count, len(student_names))} rows of the dataset:")
    print(f"  {'Student':<16}" + "".join(f"{name:>9}" for name in exam_names))

    # Loop through the first rows and print each student's grades
    for name, row in zip(student_names[:count], grades[:count]):
        print(f"  {name:<16}" + "".join(f"{grade:>9.1f}" for grade in row))

    print(f"\nDataset shape: {grades.shape[0]} students, "
          f"{grades.shape[1]} exams")


def calculate_statistics(grades, axis=None):
    """
    Calculate the mean, median, standard deviation, minimum, and maximum.

    Args:
        grades (numpy.ndarray): the grades to analyze.
        axis (int or None): 0 for one result per exam (column), or None
            for a single result across all of the grades.

    Returns:
        dict: keys "mean", "median", "std", "min", and "max". Each value
            is a numpy array (axis=0) or a single number (axis=None).
            The standard deviation is the population standard deviation.
    """
    return {
        "mean": np.mean(grades, axis=axis),
        "median": np.median(grades, axis=axis),
        "std": np.std(grades, axis=axis),
        "min": np.min(grades, axis=axis),
        "max": np.max(grades, axis=axis),
    }


def display_exam_statistics(exam_names, stats):
    """
    Print the statistics for each exam.

    Args:
        exam_names (list of str): the exam names.
        stats (dict): per-exam results from calculate_statistics(axis=0).

    Returns:
        None
    """
    print("Statistics for each exam:")
    print(f"  {'Exam':<10}{'Mean':>9}{'Median':>9}{'Std Dev':>9}"
          f"{'Min':>9}{'Max':>9}")

    # Loop through the exams and print one row of statistics for each
    for index, name in enumerate(exam_names):
        print(f"  {name:<10}{stats['mean'][index]:>9.2f}"
              f"{stats['median'][index]:>9.2f}{stats['std'][index]:>9.2f}"
              f"{stats['min'][index]:>9.2f}{stats['max'][index]:>9.2f}")


def display_overall_statistics(stats):
    """
    Print the statistics for all exams combined.

    Args:
        stats (dict): overall results from calculate_statistics().

    Returns:
        None
    """
    print("Overall statistics (all exams combined):")
    print(f"  Mean grade:         {stats['mean']:.2f}")
    print(f"  Median grade:       {stats['median']:.2f}")
    print(f"  Standard deviation: {stats['std']:.2f}")
    print(f"  Minimum grade:      {stats['min']:.2f}")
    print(f"  Maximum grade:      {stats['max']:.2f}")


def count_pass_fail(grades):
    """
    Count the students who passed and failed each exam.

    A grade of PASSING_GRADE (60) or above is a pass.

    Args:
        grades (numpy.ndarray): the grades, one row per student.

    Returns:
        tuple: (passed, failed), two numpy arrays with one count per
            exam.
    """
    passed = np.sum(grades >= PASSING_GRADE, axis=0)
    failed = grades.shape[0] - passed
    return passed, failed


def calculate_pass_percentage(grades):
    """
    Calculate the overall pass percentage across all exams.

    Args:
        grades (numpy.ndarray): the grades, one row per student.

    Returns:
        float: the percent of all grades that are 60 or above.
    """
    return float(np.sum(grades >= PASSING_GRADE) / grades.size * 100)


def display_pass_fail(exam_names, passed, failed, pass_percentage):
    """
    Print the pass and fail counts for each exam and the pass percentage.

    Args:
        exam_names (list of str): the exam names.
        passed (numpy.ndarray): number of students who passed each exam.
        failed (numpy.ndarray): number of students who failed each exam.
        pass_percentage (float): the overall pass percentage.

    Returns:
        None
    """
    print(f"Pass/fail counts (passing grade is {PASSING_GRADE} or above):")
    print(f"  {'Exam':<10}{'Passed':>9}{'Failed':>9}")

    # Loop through the exams and print the counts for each
    for index, name in enumerate(exam_names):
        print(f"  {name:<10}{passed[index]:>9}{failed[index]:>9}")

    print(f"\nOverall pass percentage: {pass_percentage:.2f}%")


def run_tests():
    """
    Test the loading, statistics, and pass/fail functions.

    Uses a small array with known answers and a temporary CSV file. The
    function prints PASS or FAIL for every check and a final summary.

    Returns:
        bool: True if every check passed, otherwise False.
    """
    grades = np.array([[90, 60], [70, 50], [50, 40], [30, 100]], dtype=float)
    exam = calculate_statistics(grades, axis=0)
    overall = calculate_statistics(grades)
    passed, failed = count_pass_fail(grades)

    # Write a temporary CSV file to test load_grades
    with tempfile.NamedTemporaryFile(
            "w", suffix=".csv", delete=False, newline="") as temp:
        temp.write("Student,Exam 1,Exam 2\nAva,90,80\nBen,70,60\n")
    names, exams, loaded = load_grades(temp.name)

    # A file with grades only (no name column)
    with tempfile.NamedTemporaryFile(
            "w", suffix=".csv", delete=False, newline="") as temp_nameless:
        temp_nameless.write("Exam 1,Exam 2\n90,80\n70,60\n")
    nameless_names, _, nameless = load_grades(temp_nameless.name)

    # A file with only a header row
    with tempfile.NamedTemporaryFile(
            "w", suffix=".csv", delete=False, newline="") as temp_empty:
        temp_empty.write("Student,Exam 1\n")

    try:
        load_grades("no_such_file.csv")
        missing_file_error = False
    except FileNotFoundError:
        missing_file_error = True

    try:
        load_grades(temp_empty.name)
        empty_file_error = False
    except ValueError:
        empty_file_error = True

    for path in (temp.name, temp_nameless.name, temp_empty.name):
        os.remove(path)

    def rounded(values):
        """Round a numpy array or number to 2 places for comparison."""
        return np.round(values, 2).tolist()

    checks = [
        ("load_grades reads the student names", names, ["Ava", "Ben"]),
        ("load_grades reads the exam names", exams, ["Exam 1", "Exam 2"]),
        ("load_grades loads a 2-D array of grades", loaded.tolist(),
         [[90.0, 80.0], [70.0, 60.0]]),
        ("load_grades numbers students when there is no name column",
         nameless_names, ["Student 1", "Student 2"]),
        ("load_grades loads grades when there is no name column",
         nameless.shape, (2, 2)),
        ("load_grades raises FileNotFoundError for a missing file",
         missing_file_error, True),
        ("load_grades raises ValueError for a file with no data",
         empty_file_error, True),
        ("per-exam mean", rounded(exam["mean"]), [60.0, 62.5]),
        ("per-exam median", rounded(exam["median"]), [60.0, 55.0]),
        ("per-exam standard deviation", rounded(exam["std"]),
         [22.36, 22.78]),
        ("per-exam minimum", rounded(exam["min"]), [30.0, 40.0]),
        ("per-exam maximum", rounded(exam["max"]), [90.0, 100.0]),
        ("overall mean", rounded(overall["mean"]), 61.25),
        ("overall median", rounded(overall["median"]), 55.0),
        ("overall standard deviation", rounded(overall["std"]), 22.6),
        ("overall minimum", rounded(overall["min"]), 30.0),
        ("overall maximum", rounded(overall["max"]), 100.0),
        ("students who passed each exam (60 counts as a pass)",
         passed.tolist(), [2, 2]),
        ("students who failed each exam", failed.tolist(), [2, 2]),
        ("overall pass percentage", calculate_pass_percentage(grades),
         50.0),
        ("pass percentage when everyone passes",
         calculate_pass_percentage(np.array([[60.0, 100.0]])), 100.0),
        ("pass percentage when everyone fails",
         calculate_pass_percentage(np.array([[59.9, 0.0]])), 0.0),
    ]

    # Accumulators: count the checks that passed and failed
    passed_count = 0
    failed_count = 0

    # Loop through every check and compare the result to expected
    for description, actual, expected in checks:
        if actual == expected:
            passed_count += 1
            print(f"PASS  {description}")
        else:
            failed_count += 1
            print(f"FAIL  {description}")
            print(f"      expected: {expected!r}")
            print(f"      actual:   {actual!r}")

    print(f"\n{passed_count} passed, {failed_count} failed, "
          f"{len(checks)} total.")
    return failed_count == 0


def main(filename=DEFAULT_FILE):
    """
    Load the grades from a CSV file and print the full analysis.

    Args:
        filename (str): the CSV file to analyze.

    Returns:
        None
    """
    print(f"Student Grade Analysis ({os.path.basename(filename)})\n")

    try:
        student_names, exam_names, grades = load_grades(filename)
    except (FileNotFoundError, ValueError) as error:
        print(f"Could not load the grades: {error}")
        return

    display_preview(student_names, exam_names, grades)

    print()
    display_exam_statistics(exam_names, calculate_statistics(grades, axis=0))

    print()
    display_overall_statistics(calculate_statistics(grades))

    print()
    passed, failed = count_pass_fail(grades)
    display_pass_fail(
        exam_names, passed, failed, calculate_pass_percentage(grades)
    )


# Run the tests with "--test", otherwise analyze the CSV file
if __name__ == "__main__":
    if "--test" in sys.argv:
        run_tests()
    elif len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        main()
