#!/usr/bin/env python

import sys
import os
import shutil
import random

def listFiles(sourceFolder, keyword):
	allFiles = []
	for name in os.listdir(sourceFolder):
		fileFullName = os.path.join(sourceFolder, name)
		if os.path.isfile(fileFullName):
			allFiles.append(fileFullName)

	filteredFiles = []
	if keyword != None:
		for name in allFiles:
			f = open(name, "r", encoding='UTF-8')
			for line in f:
				if line.lower().find(keyword) != -1:
					filteredFiles.append(name)
					break
			f.close()
	else:
		filteredFiles = allFiles

	return filteredFiles

def groupFiles(sourceFiles, destFolder, fileCount, groupCount, identifier, keyword):
	random.shuffle(sourceFiles)

	outputFolders = []
	index = 0
	while index < groupCount:
		folderName = os.path.join(destFolder, "%s-%s%d" % (identifier, keyword, index))
		if not os.path.exists(folderName):
			os.mkdir(folderName)
		outputFolders.append(folderName)
		index += 1

	predictionFolder = os.path.join(destFolder, "prediction-%s-%s" % (keyword, identifier))
	if not os.path.exists(predictionFolder):
		os.mkdir(predictionFolder)

	index = 0
	outputFolderIndex = 0
	allFileCount = fileCount * groupCount;
	while index < allFileCount:
		shutil.copy(sourceFiles[index], outputFolders[outputFolderIndex])
		shutil.copy(sourceFiles[index], predictionFolder)
		index += 1
		outputFolderIndex += 1
		if outputFolderIndex >= len(outputFolders):
			outputFolderIndex = 0

	allFileCount = len(sourceFiles)
	while index < allFileCount:
		shutil.copy(sourceFiles[index], predictionFolder)
		index += 1


if len(sys.argv) < 5:
	print('Usage: {0} positiveFolder negativeFolder outputFolder sampleFileCount [positiveKeyword] [negativeKeyword]'.format(sys.argv[0]))
	raise SystemExit

positiveFolder = sys.argv[1]
assert os.path.exists(positiveFolder),"positiveFolder not found"

negativeFolder = sys.argv[2]
assert os.path.exists(negativeFolder),"negativeFolder not found"

outputFolder = sys.argv[3]
assert os.path.exists(outputFolder),"outputFolder not found"

sampleFileCount = int(sys.argv[4])

positiveKeyword = None
negativeKeyword = None

if len(sys.argv) > 5:
	positiveKeyword = sys.argv[5].lower()

if len(sys.argv) > 6:
	negativeKeyword = sys.argv[6].lower()

positiveFiles = listFiles(positiveFolder, positiveKeyword)
negativeFiles = listFiles(negativeFolder, negativeKeyword)

minLength = min(len(positiveFiles), len(negativeFiles))

currentGroupCount = int(minLength / sampleFileCount)

groupFiles(positiveFiles, outputFolder, sampleFileCount, currentGroupCount, "positive", positiveKeyword)
groupFiles(negativeFiles, outputFolder, sampleFileCount, currentGroupCount, "negative", negativeKeyword)