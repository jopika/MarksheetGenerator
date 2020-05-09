# MarksheetGenerator
A script that can quicky generate Marksheets using CSV inputs

## Introduction
This script was created due to the repetative task of generating Marksheets for the classes/labs I teach.  
I wanted a quicker way to pull information and then generate marksheets from information that was accessible from other sources.

The solution I came up with was this, using CSVs it is possible to describe the Grading scheme (columns) and specify the Students, divided into Sections.

## Prerequisites
* Python 3.6+
* xlsxwriter

## Using the script
You must create files the describe the marksheets you wish to generate.  

There are three main files you need to have:
* Students
* Grading (Rubric)
* Sections (Partion)

Each file has a slightly different format, but they are all CSVs.

Install the needed libraries by running `pip -r requirements.txt`.
x
After this, you can edit the flags and constants in the python script.

Finally, run the python script doing something like `py generate.py`.

## File formats
### Students File
Files follow this format, where each line corresponds to a student
```
{First Name},{Last Name},{Section_ID}
Bradd,Pitt,ClassA
Tom,Cruise,ClassB
Angelina,Jolie,ClassB
```

### Grading File
Files follow this format, where each line corresponds to a grading rubric
```
{Grading_ID}, {Column_1}, {Column_2}, {Column_3}, {Column_4}, {Column_5}, {Column_6}, ...
Marksheet 1, Todo 1, Todo 2, Checkpoint
Marksheet 2, Todo 1, Todo 2, Todo 3, Final
```

### Sections File
Files follow this format, where each line corresponds to a section and it's corresponding information
```
{Sections_ID},{LeftText},{CenterText},{RightText}
ClassA,,Monday,10-12
ClassB,,Wednesday,13-15
ClassC,,,
```

## Disclaimer
No warranty is provided when using this software, though I don't see what can go wrong...
This software is provided "*AS IS*", and I am _not_ responsible for any damages or losses caused.

