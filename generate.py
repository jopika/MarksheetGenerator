import xlsxwriter

MARK_COLUMNS = []


# Workbook generator
def generate_workbook(name):
    """Consumes a name and returns a workbook object with filename name"""
    if(name.endswith("xlsx")):
        workbook = xlsxwriter.Workbook(name)
    else:
        workbook = xlsxwriter.Workbook(name + ".xlsx")
    return workbook

# Lab Sheet Setup
def setup_worksheet(worksheet, lab_section):
    """Sets up formats for the worksheet,
        such as orientation, margins and headers"""
    # TODO: Complete method
    worksheet.set_landscape()
    pass


# Generate grading columns
def setup_grading_columns(worksheet, lab_number, lab_section):
    """Sets up the grading columns of the workbook"""
    pass

# Fills the marksheet with student's names
def setup_student_names(worksheet, lab_number, lab_section):
    pass
    