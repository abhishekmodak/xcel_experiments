
import sys
import xlrd
import xlsxwriter
import os.path

source_file_name = sys.argv[1]
destination_file_name = sys.argv[2]

headers = ['Week', 'Task', 'Employee Name', 'Task ID', 'Sub Project', 'Project', 'noscript', 'script', 'Billed (Yes/No)', 'Quality',
			'Total Work', 'Hours Spent', 'Approver']

wb = xlrd.open_workbook(source_file_name)
all_sheet_names = wb.sheet_names()
no_sheet = len(all_sheet_names)

workbook = xlsxwriter.Workbook(destination_file_name)
worksheet = workbook.add_worksheet()
bold = workbook.add_format({'bold': True})
for i in xrange(len(headers)):
	worksheet.write(0, i, headers[i], bold)

#import pdb;pdb.set_trace()
try:
	i = 1
	for no in xrange(no_sheet):
		sh = wb.sheet_by_index(no)
		if not sh.name.startswith("W"):
			continue
		#sh.nrows
		for row_id in xrange(sh.nrows):
				#if col_id == 1:
			if not sh.cell(row_id, 4).value or sh.cell(row_id, 4).value in ["", "Veveo Ticket"]:
				continue
			task_id = "%s%s%s" % (sh.name.split("(")[0], sh.cell(row_id, 0).value, sh.cell(row_id, 1).value)
			data = [sh.name.split("(")[0], sh.cell(row_id, 0).value, sh.cell(row_id, 1).value, task_id, sh.cell(row_id, 2).value, sh.cell(row_id, 3).value,
					sh.cell(row_id, 8).value, sh.cell(row_id, 9).value, sh.cell(row_id, 12).value, sh.cell(row_id, 13).value,
					sh.cell(row_id, 11).value, "", sh.cell(row_id, 17).value]

			for j in xrange(len(data)):
				worksheet.write(i, j, data[j])
			i += 1

except:
	import pdb;pdb.set_trace()
	print "aaaaa"
workbook.close()