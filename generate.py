import xlsxwriter
import collections

# Global Values
GLOBAL_STUDENTS = {}
GLOBAL_SECTIONS = collections.OrderedDict()
GLOBAL_GRADING = {}

# Students before drawing heavy line separator (-1 to disable)
HEAVY_ROW_MODIFIER = 5

# File Path to descriptions
STUDENT_FILE_PATH = "./data/students.csv"
GRADING_FILE_PATH = "./data/grading.csv"
SECTION_FILE_PATH = "./data/sections.csv"

# Set both flags to true for PDF Batch DUPLEX Printing
PADDING_FLAG = False
DUPLICATE_FLAG = False
MARKSHEET_COUNT = 2

# Workbook generator
def generate_workbook(name):
    """Consumes a name and returns a workbook object with filename name"""
    if(name.endswith("xlsx")):
        workbook = xlsxwriter.Workbook(name)
    else:
        workbook = xlsxwriter.Workbook(name + ".xlsx")
    return workbook

# Lab Sheet Setup
def setup_worksheet(worksheet, section_id):
    """Sets up formats for the worksheet,
        such as orientation, margins and headers"""
    worksheet.set_landscape()
    header_info = GLOBAL_SECTIONS.get(section_id)
    if header_info is not None:
        # If there is header info, set the headers in the right positions
        l_text = header_info[0]
        c_text = header_info[1]
        r_text = header_info[2]
        worksheet.set_header('&L' + l_text + '&C' + c_text + '&R' + r_text)
    worksheet.set_margins(left=0.75, right=0.75, top=1, bottom=1)
    worksheet.hide_gridlines(0)


# Generate grading columns
def setup_grading_columns(workbook, worksheet, grading_id, section_id):
    """Sets up the grading columns of the workbook"""
    right_bold = workbook.add_format()
    right_bold.set_align('right')
    right_bold.set_bold()
    left_bold = workbook.add_format()
    left_bold.set_bold()
    merged_cell = workbook.add_format()
    merged_cell.set_text_wrap()
    merged_cell.set_align('center')
    merged_cell.set_align('vcenter')
    merged_cell.set_bottom(2)

    columns = GLOBAL_GRADING.get(grading_id)
    worksheet.write(0, 0, section_id, right_bold)
    worksheet.write(0, 1, grading_id, left_bold)
    worksheet.write(1, 0, "First Name", merged_cell)
    worksheet.write(1, 1, "Last Name", merged_cell)
    cur_pos = 2
    if columns is not None and len(columns) > 0:
        for entry in columns:
            worksheet.merge_range(first_row=0, first_col=cur_pos, last_row=1, last_col=cur_pos,
                                  data=entry, cell_format=merged_cell)
            cur_pos = cur_pos + 1
    else:
        # No grading scheme, just generate student names and total
        worksheet.merge_range(first_row=0, first_col=cur_pos, last_row=1, last_col=cur_pos,
                              data="Total", cell_format=merged_cell)
        cur_pos = cur_pos + 1

    worksheet.set_column(0,1,15)
    worksheet.set_column(2,cur_pos,12)
    worksheet.fit_to_pages(1,1)


# Fills the marksheet with student's names
def setup_student_names(workbook, worksheet, grading_id, section_id):
    heavy_bottom = workbook.add_format()
    heavy_bottom.set_bottom(2)

    students = GLOBAL_STUDENTS.get(section_id)
    grading = GLOBAL_GRADING.get(grading_id)
    if students is not None and len(students) > 0:
        student_count = 0
        row_count = 2
        students = sorted(students)
        for student in students:
            student_count = (student_count + 1) % HEAVY_ROW_MODIFIER
            first_name  = student[0]
            last_name   = student[1]
            if student_count == 0:
                if grading is not None and len(grading) > 0:
                    worksheet.write(row_count, 0, first_name,heavy_bottom)
                    worksheet.write(row_count, 1, last_name,heavy_bottom)
                    for x in range(len(grading)):
                        worksheet.write_blank(row_count,x + 2, None, heavy_bottom)
                    # worksheet.write_array_formula(row_count-HEAVY_ROW_MODIFIER-1,2,
                    #                               row_count,2+len(grading),
                    #                               "{}",heavy_box)
            else:
                worksheet.write(row_count, 0, first_name)
                worksheet.write(row_count, 1, last_name)
            row_count = row_count + 1
    else:
        # No Students
        pass



def add_student_info(input_string):
    """Adds student to global map, based on input_string
    String format is csv where: {FirstName},{LastName},{Section/Division}"""
    values = input_string.split(",")
    if len(values) != 3:
        print("Error parsing: " + input_string)
        return
    values = list(map(lambda x: x.replace("\n", ""), values))
    values = list(map(lambda x: x.replace("\r", ""), values))
    student_info = values[0:2]
    student_array = GLOBAL_STUDENTS.get(values[2])
    if student_array is None:
        student_array = [student_info]
    else:
        student_array.append(student_info)

    GLOBAL_STUDENTS[values[2]] = student_array


def add_grading_info(input_string):
    """Adds grading scheme to global map, based on input_string
    String format is csv where: {Grading_ID}, [{grading_1}, {grading_2}, ...]"""
    # TODO: Complete this
    values = input_string.split(",")
    if len(values) == 0:
        print("Error parsing: " + input_string)
        return
    grading_info = values[1:]
    GLOBAL_GRADING[values[0]] = grading_info

def add_section_info(input_string):
    """Adds section info, to generate extra information in the headers
    String format is csv where: {SectionName},{LeftText},{CenterText},{RightText}"""
    # TODO: Complete this
    values = input_string.split(",")
    if len(values) != 4:
        print("Error parsing: " + input_string)
        return
    section_info = values[1:]
    GLOBAL_SECTIONS[values[0]] = section_info


def read_section_file(path):
    f = open(path, 'r')
    for line in f:
        add_section_info(line)
    f.close()

def read_student_file(path):
    f = open(path, 'r')
    for line in f:
        add_student_info(line)
    f.close()

def read_grading_file(path):
    f = open(path, 'r')
    for line in f:
        add_grading_info(line)
    f.close()


if __name__ == '__main__':
    read_grading_file(GRADING_FILE_PATH)
    read_section_file(SECTION_FILE_PATH)
    read_student_file(STUDENT_FILE_PATH)

    if DUPLICATE_FLAG:
        generate_count = MARKSHEET_COUNT
    else:
        generate_count = 1

    for grading_scheme in GLOBAL_GRADING:
        workbook = generate_workbook(grading_scheme)
        for section_id in GLOBAL_SECTIONS:
            for x in range(0,generate_count):
                if DUPLICATE_FLAG:
                    worksheet = workbook.add_worksheet(section_id + str(x))
                else:
                    worksheet = workbook.add_worksheet(section_id)
                setup_worksheet(worksheet, section_id)
                setup_grading_columns(workbook, worksheet, grading_scheme, section_id)
                setup_student_names(workbook, worksheet, grading_scheme, section_id)
                if PADDING_FLAG:
                    # Add extra white pages for PDF duplex printing
                    padding_sheet = workbook.add_worksheet()
                    padding_sheet.write(0,0," ")
                    padding_sheet.set_landscape()
        workbook.close()
