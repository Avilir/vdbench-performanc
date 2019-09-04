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
'''
    Setting the Base header line
'''
# Throughput - MB/s / QueueDepth - QD
base_heder_line = ["interval", "IOPS", "MB/s", "BS", "%Read",
                   "Latency", "R-Lat", "W-Lat", "Dev-Lat",
                   "QD", "%Tot-U", "%Sys-U" ]
'''
    verify that input filename passed to the script
'''
if len(sys.argv) > 1:
    file_name = sys.argv[1]
else:
    print ("Error: No input file !!!")
    sys.exit(1)

'''
    verify that the file is exist.
'''
if os.path.isfile(file_name) is not True:
    print ("Error: Input file dose not exist !")
    sys.exit(1)

'''
    the output file will be at the same location as the input file
'''
logdir = os.path.dirname(os.path.realpath(file_name))

print ("logdir = {}".format(logdir))
'''
    splliting the file name to create the output filename
    with differen extention.
'''
output_filename = os.path.splitext(os.path.basename(file_name))[0]

''' Excel output file '''
rep_file = "{}/{}.xlsx".format(logdir, output_filename)

''' Clean log file as coma seperated '''
output_filename = "{}/{}.clean.log".format(logdir, output_filename)

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

    if i in [1,2,5]:        
        title_formats[i].set_right(2)
        title_formats[i].set_left(2)
    else:
        title_formats[i].set_right(1)
        title_formats[i].set_left(1)

title_formats[0].set_left(2)
title_formats[11].set_right(2)

title_formats[1].set_bg_color('#66ccff')
title_formats[2].set_bg_color('#66ff99')
title_formats[5].set_bg_color('#ff6699')

''' creating worksheets for the data and summery '''
worksheet = workbook.add_worksheet("RawData")
worksheet.set_column('A:A',15)

summery = workbook.add_worksheet("Summery")
summery.set_column('A:A',25)

''' debuging information - print the names of the files. '''
print ("Input file name is {}".format(file_name))
print ("Output file name is {}".format(output_filename))
print ("Report file name is {}".format(rep_file))

''' Setting up file handleres for output files '''
out_file = open(output_filename, "w")


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

    worksheet.insert_chart('O{}'.format(pos_line), chart, {'width': 20}) #  , {'x_offset': 25, 'y_offset': 10}

def write_summery_chart(start_lin,end_line,title):
    global sum_pos_row
    print("create summery chart for {}".format(title))
    chart = workbook.add_chart({'type': 'line','subtype': 'smooth'})

    # Configure the first series.
    chart.add_series({
        'name':       'Latency',
        'values':     '=Summery!$F${}:$F${}'.format(start_lin,end_line),
        'categories':     '=Summery!$B${}:$B${}'.format(start_lin,end_line),
        'marker': {'type': 'automatic'},
    })

    chart.set_title ({'name': title})
    chart.set_y_axis({'name': 'Latency(ms)'})
    chart.set_x_axis({'name': 'IOPS'})

    chart.set_legend({'position': 'none'})

    summery.insert_chart('O{}'.format(sum_pos_row), chart, {'width': 20, 'hight':20}) #  , {'x_offset': 25, 'y_offset': 10}
    sum_pos_row = sum_pos_row + 16

def write_data_line(data):
    global row
    for index, res in enumerate(data):
                #if index >1:
        cell_format = workbook.add_format()
        cell_format.set_border(1)

        cell_format.set_align('center')
        if 'AVG' in data:
            cell_format.set_bottom(2)
            cell_format.set_top(2)
            cell_format.set_bold()

        if index > 0 and res is not "AVG":
            res = float(res)
            cell_format.set_num_format('#,##0')

        if index > 6 and index != 10:
            cell_format.set_num_format('#,##0.00')

        if index in [2, 3, 6]:
            cell_format.set_right(2)
            cell_format.set_left(2)
            cell_format.set_bold()

        if index == 0:
            cell_format.set_left(2)
            cell_format.set_num_format('HH:MM:SS')

        if index == 2:
            cell_format.set_bg_color('#66ccff')

        if index == 3:
            cell_format.set_bg_color('#66ff99')

        if index == 6:
            cell_format.set_bg_color('#ff6699')
            cell_format.set_num_format('#,##0.00')

        if index == 12:
            cell_format.set_right(2)

        worksheet.write(row, index,res,cell_format)
    row = row + 1

def write_summery_data_line(data):
    global summery_row

    for index, res in enumerate(data):
        if index > 1:
            cell_format = workbook.add_format()
            cell_format.set_border(1)

            cell_format.set_align('center')

            if index > 0 and res is not "AVG":
                res = float(res)
                cell_format.set_num_format('#,##0')

            if index > 6 and index != 10:
                cell_format.set_num_format('#,##0.00')

            if index in [2, 3, 6]:
                cell_format.set_right(2)
                cell_format.set_left(2)
                cell_format.set_bold()

            if index == 0:
                cell_format.set_left(2)
                cell_format.set_num_format('HH:MM:SS')

            if index == 2:
                cell_format.set_bg_color('#66ccff')

            if index == 3:
                cell_format.set_bg_color('#66ff99')

            if index == 6:
                cell_format.set_bg_color('#ff6699')
                cell_format.set_num_format('#,##0.00')

            if index == 12:
                cell_format.set_right(2)

            summery.write(summery_row, index-1,res,cell_format)
    summery_row = summery_row + 1

with open(file_name, "r") as fh:
    chart_start_line = 0
    summ_chart_start_line = 0 ;
    line = fh.readline()
    while line:

        # start the test results section with header
        if "interval" in line and start_section ==1:
            t_date = line[:12].replace(', ','-').replace(' ','-')
            test_date = "{}/{}/{}".format(t_date.split('-')[1], t_date.split('-')[0], t_date.split('-')[2])

            worksheet.write(row, 0, t_date,title_formats[0])
            for index, res in enumerate(base_heder_line):
                worksheet.write(row, index+1,res,title_formats[index])
            row = row + 1
            chart_start_line = row

            out_file.write(t_date + "," + ",".join(base_heder_line) + "\n")
            line = fh.readline()    # read the second line header.
            start_section = 2

        # Getting test results
        if ":" in line and start_section > 0 and "Reached" not in line:
            results = line.strip().split()
            del results[9:11]

            if "avg" in line:
                results[1] = "AVG"
                start_section = 0
                write_summery_data_line(results)
                write_chart(chart_start_line,row,'C','G','{} Results'.format(rd),'IOPS','Latency(ms)',chart_start_line)
            results[0] = results[0].split('.')[0]
            h,m,s = results[0].split(':')
            write_data_line(results)

            '''
            for index, res in enumerate(results):
                if index >1:
                    worksheet.write(row, index,float(res),lines_formats[index])
                else:
                    worksheet.write(row, index,res,lines_formats[index])
            row = row + 1
            '''
            if "avg" in line:
                row = row + 1
            results[0] = str(results[0])
            out_file.write(','.join(results) + "\n")

        # Getting the test name (RD) from the log
        if "Starting RD" in line:
            rd = line.split(';')[0].split('=')[-1]
            iorate = line.split(';')[1].split(':')[-1]
            out_file.write("{},IORATE={}\n".format(rd,iorate))
            worksheet.merge_range(row,0,row,6,rd, Head_format)
            worksheet.merge_range(row,7,row,12,"IORATE={}".format(iorate), Head_format)
            row = row + 1

            if "curve" in iorate:

                summery.merge_range(summery_row,0,summery_row,6,rd, Head_format)
                summery.merge_range(summery_row,7,summery_row,12,"IORATE={}".format(iorate), Head_format)
                summery_row = summery_row + 1
                for index, res in enumerate(base_heder_line):
                    if index >= 1:
                        summery.write(summery_row, index,res,title_formats[index])
                summery.write(summery_row, 0,"{}".format(rd),title_formats[0])
                summery_row = summery_row + 1
                summery.write(summery_row, 0,"MAX",title_formats[0])
                if summery_row > summ_chart_start_line and summ_chart_start_line > 0:
                    write_summery_chart(summ_chart_start_line+1,summery_row-2,'Curve results - {}'.format(rd),)
                summ_chart_start_line = summery_row + 1

            else:
                tit = rd.split('_')[-1]
                summery.write(summery_row, 0,tit,title_formats[0])

            start_section = 1

        line = fh.readline()

'''
    make sure the FileHandlers closed.
'''
fh.close()
out_file.close()
workbook.close()

