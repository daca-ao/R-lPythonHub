# -*- coding: UTF-8 -*-

columnHeader = ['学号', '姓名', '性别', '民族', '血型', '政治面貌', '户口类别', '出生年月日', '联系方式', 'QQ号', '微信号', '身份证号', '籍贯', '现住地址', '中考成绩', '生源学校', '是否住宿', '父亲姓名', '父亲联系方式', '父亲工作单位', '母亲姓名', '母亲联系方式', '母亲工作单位']
sourceFilePath = "/Users/aohuijun/Documents/students/"
sourceFileSuffix1 = ".xls"
sourceFileSuffix2 = ".xlsx"
fileArray = []
destFilePath = "/Users/aohuijun/Documents/"
destFile = "高一（9）班学生信息统计"

import glob
from numpy import *
for fileName in glob.glob(sourceFilePath + "*" + sourceFileSuffix1):
	fileArray.append(fileName)
for fileName in glob.glob(sourceFilePath + "*" + sourceFileSuffix2):
	fileArray.append(fileName)

sourceFilesNum = len(fileArray)
dataMatrix = [None] * sourceFilesNum

if sourceFilesNum <= 0:
	print("没有文档，撤退")
	exit()
print("在%s一共有%d位学生提交的文档" %(sourceFilePath, sourceFilesNum))

import xlrd
for n in range(sourceFilesNum):
	fileName = fileArray[n]
	infoBook = xlrd.open_workbook(fileName)
	try:
		sheet = infoBook.sheet_by_name("Sheet1")
	except:
		print("文件%s中无 Sheet1" %fileName)
	rowsNum = sheet.nrows
	dataMatrix[n] = [0] * (rowsNum - 1)

	colsNum = sheet.ncols
	for r in range(rowsNum - 1):
		dataMatrix[n][r] = ["0"] * colsNum

	for r in range(1, rowsNum):
		for c in range(0,colsNum):
			dataMatrix[n][r - 1][c] = sheet.cell(r, c).value


import xlwt
destFileName = xlwt.Workbook(encoding='utf-8')
sheet = destFileName.add_sheet("student_info")

for i in range(0, len(columnHeader)):
	sheet.write(0, i, columnHeader[i])

zh = 1
for i in range(sourceFilesNum):
	for j in range(len(dataMatrix[i])):
		for k in range(len(dataMatrix[i][j])):
			sheet.write(zh,k,dataMatrix[i][j][k])
		zh=zh+1

savedFileName = destFilePath + destFile + sourceFileSuffix1
destFileName.save(savedFileName)
print("已合并%d个文件，并生成%s" %(sourceFilesNum, savedFileName))
