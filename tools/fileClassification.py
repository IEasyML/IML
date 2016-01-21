#!/usr/bin/env python

import sys
import os
import shutil
import random

def filterFiles(sourceFolder, outputFolder, keywords):
	if keywords != None:
		for name in os.listdir(sourceFolder):
			fileFullName = os.path.join(sourceFolder, name)
			if os.path.isfile(fileFullName):
				f = open(fileFullName, "r", encoding='UTF-8')
				isFound = False
				for line in f:
					for keyword in keywords:
						if line.lower().find(keyword) != -1:
							#print("file:{0}->[{1}]-->{2}".format(name, keyword, line.lower().find(keyword)))
							isFound = True
							break

					if isFound:
						break
				f.close()
				if isFound:
					shutil.move(fileFullName, outputFolder)


if len(sys.argv) < 4:
	print('Usage: {0} sourceFolder outputFolder [keyword] ... [keyword]'.format(sys.argv[0]))
	raise SystemExit

sourceFolder = sys.argv[1]
assert os.path.exists(sourceFolder),"sourceFolder not found"

outputFolder = sys.argv[2]
assert os.path.exists(outputFolder),"outputFolder not found"

keywords = []
for index in range(3, len(sys.argv) -1):
	#print("[{0}]".format(sys.argv[index]))
	keywords.append(sys.argv[index])

filterFiles(sourceFolder, outputFolder, keywords)