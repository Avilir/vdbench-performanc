#!/usr/bin/env python3

'''
    This script is used for create a clean test results report.
    
    Author : Avi Liani <alayani@redhat.com>
    Created : Aug-29-2019
'''

import sys
import os
import xlsxwriter

''' some global parameters '''
row = 0  # the row to print in the excel file
summery_row = 0  # the row to print in the excel file - summery tab
test_date = ''
start_section = 0  # this will tell the script to print the output
sum_pos_row = 1  # the row position for the summery carts.

''' verify that input filename passed to the script '''

if len(sys.argv) > 1:
    file_name = sys.argv[1]
else:
    print ("Error: No input file !!!")
    sys.exit(1)

''' verify that the file is exist. '''
if os.path.isfile(file_name) is not True:
    print ("Error: Input file dose not exist !")
    sys.exit(1)

''' the output file will be at the same location as the input file '''
logdir = os.path.dirname(os.path.realpath(file_name))

'''
    splitting the file name to create the output filename
    with different extension.
'''

''' Excel output file '''
rep_file = "{}.xlsx".format(os.path.splitext(file_name)[0])


# The excel workbook object
workbook = xlsxwriter.Workbook(rep_file)

''' Creating the cells formatting '''
# Header format for each section
Head_format = workbook.add_format()
Head_format.set_border(2)
Head_format.set_bg_color('yellow')
Head_format.set_align('center')
Head_format.set_bold()

lines_formats = []  # results line format
title_formats = []  # the section title results format
format_summery_title = []  # the summery section test name format

''' setting up the formats fot the titles in the summery tab '''
for i in range(4):
    j_format = workbook.add_format()
    j_format.set_bg_color('white')
    j_format.set_bold()
    j_format.set_align('center')
    j_format.set_top(1)
    j_format.set_bottom(1)
    j_format.set_right(2)
    j_format.set_left(2)

    if i > 0:
        j_format.set_top(2)
        j_format.set_bottom(2)

    format_summery_title.append(j_format)
format_summery_title[1].set_bg_color('#B6B6B6')
format_summery_title[2].set_bg_color('#82B5DE')
format_summery_title[3].set_bg_color('#8BC572')

''' creating formats object for the results and the title '''
for i in range(13):
    line_format = workbook.add_format()
    lines_formats.append(line_format)
    lines_formats[i].set_border(1)

''' creating the results title line format '''
for i in range(13):
    lf = workbook.add_format()
    title_formats.append(lf)
    title_formats[i].set_top(2)
    title_formats[i].set_bottom(2)
    title_formats[i].set_bold()
    title_formats[i].set_align('center')

    if i in [0,1,4,7]:
        title_formats[i].set_right(2)
        title_formats[i].set_left(2)
    else:
        title_formats[i].set_right(1)
        title_formats[i].set_left(1)

    if i in [2,5,8]:
        title_formats[i].set_left(2)

    if i in [4,7,9,10]:
        title_formats[i].set_right(2)

''' creating worksheets for the data and summery '''
worksheet = workbook.add_worksheet("RawData")
worksheet.set_column('A:A',15)

summery = workbook.add_worksheet("Summery")
summery.set_column('A:A',25)

''' debuging information - print the names of the files. '''
print ("logdir = {}".format(logdir))
print ("Base Filename : {}".format(os.path.splitext(file_name)[0]))
print ("Input file name is {}".format(file_name))
print ("Report file name is {}".format(rep_file))


def print_header(ws, row, test_date):

    def print_ops(line, col, title):
        ws.merge_range(line-1, col, line-1, int(col+2), title, title_formats[0])
        ws.write(line, col, 'Read', title_formats[col])
        ws.write(line, col+1, 'Write', title_formats[col+1])
        ws.write(line, col+2, 'Total', title_formats[col+2])

    ws.merge_range('A{}:A{}'.format(row+1, row+2), test_date, title_formats[0])
    ws.merge_range('B{}:B{}'.format(row+1, row+2), 'Interval', title_formats[1])
    print_ops(row+1, 2, 'IOPS')
    print_ops(row+1, 5, 'Bandwidth(MB / Sec)')
    print_ops(row+1, 8, 'Latency(ms)')
    ws.merge_range('L{}:L{}'.format(row+1, row+2), "BS (K)", title_formats[0])
    ws.merge_range('M{}:M{}'.format(row+1, row+2), "% Read", title_formats[0])

    row = row + 2
    return row


''' read the input file and cleanup the unnecceray data '''

def write_chart(start_lin,end_line,col,sec_col,title,yaxis_title,y2axsi_title,pos_line):
    chart = workbook.add_chart({'type': 'line','subtype': 'smooth'})

    # Configure the first series.
    chart.add_series({
        'name':       'IOPS',
        'values':     '=RawData!${}${}:${}${}'.format(col,start_lin,col,end_line),
        'y2_axis': 1,
    })
    chart.add_series({
        'name':       'Latency',
        'values':     '=RawData!${}${}:${}${}'.format(sec_col,start_lin,sec_col,end_line),
    })
    #chart.set_size(7)
    chart.set_title ({'name': title})
    chart.set_x_axis({'name': 'Time Interval (10sec)'})

    chart.set_y_axis({'name': y2axsi_title})
    chart.set_y2_axis({'name': yaxis_title, 'major_gridlines': {'visible': 0}})

    chart.set_legend({'position': 'bottom'})

    worksheet.insert_chart('O{}'.format(pos_line-3), chart, {'width': 20}) #  , {'x_offset': 25, 'y_offset': 10}

def write_data_line(ws, row, data):

    write_order = [0, 1, 4, 10,-1,-1, 12, 2, 8, 3, 9, 5, 6, 7, 11]

    for index, res in enumerate(data):
        if res == "NaN":
            res=0

        if write_order[index] >= 0:
            cell_format = workbook.add_format()
            cell_format.set_border(1)

            cell_format.set_align('center')
            if 'AVG' in data:
                cell_format.set_bottom(2)
                cell_format.set_top(2)
                cell_format.set_bold()
                cell_format.set_bg_color('#b6b6b6')

            if write_order[index] == 0:
                cell_format.set_left(2)
                cell_format.set_right(2)
                cell_format.set_num_format('HH:MM:SS.00')

            if write_order[index] > 0 and res is not "AVG":
                res = float(res)
                cell_format.set_num_format('#,##0')

            if write_order[index] in [4, 7, 10]:
                cell_format.set_left(2)
                cell_format.set_bold()

            if write_order[index] == 11:
                res = float (res/1024)

            if write_order[index] in range(5,11):
                cell_format.set_num_format('#,##0.00')

            if write_order[index] in [1, 4, 7, 10,12]:
                cell_format.set_right(2)

            if ws.name == "Summery":
                if "max" in rd.lower():
                    cell_format.set_bg_color('#82B5DE')
                    cell_format.set_top(2)
                    cell_format.set_bottom(2)
                if "curve" in tit.lower():
                    cell_format.set_bg_color('#8BC572')
                    cell_format.set_top(2)
                    cell_format.set_bottom(2)
                if "format" in rd.lower():
                    cell_format.set_bg_color('#b6b6b6')
                    cell_format.set_top(2)
                    cell_format.set_bottom(2)

            ws.write(row, write_order[index], res, cell_format)
    row = row + 1
    return row

class CurveChart(object):
    def __init__(self, title,start,pos):
        self.title = title
        self.start_line = start
        self.pos = pos
        self.end_line = 0

    def endline(self, line):
        self.end_line = line

    def write_chart(self):
        chart = workbook.add_chart({'type': 'line', 'subtype': 'smooth'})

        chart.add_series({
            'name': 'Latency',
            'values': '=Summery!$K${}:$K${}'.format(self.start_line, self.end_line),
            'categories': '=Summery!$E${}:$E${}'.format(self.start_line, self.end_line),
        })

        chart.set_title({'name': self.title})
        chart.set_y_axis({'name': 'Latency(ms)'})
        chart.set_x_axis({'name': 'IOPS'})

        chart.set_legend({'position': 'none'})

        summery.insert_chart('O{}'.format(self.start_line), chart,
                             {'width': 20, 'hight': 20})


cchart = CurveChart(None, 0,0)

with open(file_name, "r") as fh:
    chart_start_line = 0
    summ_chart_start_line = 0 ;
    line = fh.readline()
    adata=[]

    while line:
        line = line.strip('\n')
        if "Estimated totals for all" in line:
            fdata = line.split(':')

            totla_clients = fdata[2].split()[5]

            total_dirs = fdata[4].split(';')[0]
            total_files = fdata[5].split(';')[0]
            total_data = fdata[6]

            summery.merge_range('A2:B2', "Number of Clients is   {}".format(
                totla_clients), Head_format)
            summery.merge_range('C2:D2', "Total Dirs : {}".format(
                total_dirs), Head_format)
            summery.merge_range('E2:I2', "Total Files is : {}".format(
                total_files), Head_format)
            summery.merge_range('J2:M2', "Total Size is : {}".format(
                total_data), Head_format)
            summery_row = 4

        if "Anchor size:" in line:
            adata = line.split(':')

            summery.merge_range('A1:D1', "Number of Directories is   {}".format(
                adata[5].split(';')[0].strip()), Head_format)
            summery.merge_range('E1:I1', "Number of Files is   {}".format(
                adata[6].split(';')[0].strip()), Head_format)
            summery.merge_range('J1:M1', "Total Size is   {}".format(
                adata[7].strip().split(' ')[0]), Head_format)
            summery_row = 2
            summery_row = print_header(summery, summery_row, '')
            summery.merge_range (summery_row-2,0,summery_row-1,1, "Test Name", title_formats[0])

        # start the test results section with header
        if "Interval" in line and start_section ==1:
            t_date = line[:12].replace(', ','-').replace(' ','-')
            test_date = "{}/{}/{}".format(t_date.split('-')[1], t_date.split('-')[0], t_date.split('-')[2])

            worksheet.write(row, 0, t_date,title_formats[0])

            row = print_header(worksheet, row, t_date)
            chart_start_line = row + 2

            line = fh.readline()    # read the second line header.
            start_section = 2

        # Getting test results
        if ":" in line and start_section > 0 and "Reached" not in line and "anchor" not in line:
            results = line.strip().split()
            del results[15:]
            if "avg" in line:
                results[1] = 0
                summery_row = write_data_line(summery, summery_row, results)
                if "format" in tit:
                    summery.merge_range(summery_row-1, 0, summery_row-1, 1, tit, format_summery_title[1])
                elif "max" in tit:
                    summery.merge_range(summery_row-1, 0, summery_row-1, 1, tit, format_summery_title[2])
                elif "curve" in tit:
                    summery.merge_range(summery_row-1, 0, summery_row-1, 1, tit, format_summery_title[3])
                else:
                    summery.merge_range(summery_row-1, 0, summery_row-1, 1, tit, format_summery_title[0])
                results[1] = "AVG"
                start_section = 0
                write_chart(chart_start_line,row,'E','K','{} Results'.format(rd),
                            'IOPS','Latency(ms)',chart_start_line-1)
            results[0] = results[0].split('.')[0]
            h,m,s = results[0].split(':')

            row = write_data_line(worksheet, row, results)

            if "avg" in line:
                row = row + 1
            results[0] = str(results[0])

        # Getting the test name (RD) from the log
        if "Starting RD" in line:
            if cchart.title is not None and "curve" not in line.lower():
                cchart.endline(summery_row)
                cchart.write_chart()
                cchart  = CurveChart(None, 0,0)

            rd = line.split(';')[0].split('=')[-1]
            tit = rd
            if "format" not in line.lower():
                tit = rd.split('_')[-1]

            if "format" not in line:
                iorate = line.split(';')[2].split()[0].split('=')[-1].capitalize()
            else:
                iorate = "Max"
            worksheet.merge_range(row,0,row,6,rd, Head_format)
            worksheet.merge_range(row,7,row,12,"IORATE={}".format(iorate), Head_format)
            row = row + 1


            if "curve" in iorate.lower():
                if cchart.title == None:
                    cchart = CurveChart(rd, summery_row + 2, summery_row)


            start_section = 1

        line = fh.readline()

    if cchart.title is not None:
        cchart.endline(summery_row)
        cchart.write_chart()

'''
    make sure the FileHandlers closed.
'''
fh.close()
workbook.close()

