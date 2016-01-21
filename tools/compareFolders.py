#!/usr/bin/env python

import sys
import os
import shutil
import random
import hashlib

def getFileMD5(fileName):
	hash = hashlib.md5()
	with open(fileName, "rb") as f:
		for chunk in iter(lambda: f.read(4096), b""):
			hash.update(chunk)
	return hash.hexdigest()

def getFilesMD5(folderName, removeDuplicateFile):
	fileMD5s = {}
	for name in os.listdir(folderName):
		fileFullName = os.path.join(folderName, name)
		md5 = getFileMD5(fileFullName)
		if md5 in fileMD5s:
			print("Duplicated File:{0}, File:{1}, MD5:{2}".format(name, fileMD5s[md5], md5))
			if removeDuplicateFile:
				os.remove(fileFullName)
		else:
			fileMD5s[md5] = fileFullName
	return fileMD5s


def compareFolders(sourceFolder, destinationFolder, removeDuplicateFile, compareMD5):
	for name in os.listdir(sourceFolder):
		fileFullName = os.path.join(destinationFolder, name)
		if os.path.exists(fileFullName):
			print(name)
			if removeDuplicateFile:
				os.remove(fileFullName)
				os.remove(os.path.join(sourceFolder, name))

	if compareMD5:
		sourceMD5 = getFilesMD5(sourceFolder, removeDuplicateFile)
		destMD5 = getFilesMD5(destinationFolder, removeDuplicateFile)

		for k,v in destMD5.items():
			if k in sourceMD5:
				print("Duplicate source:{0}, destination:{1}, MD5:{2}".format(sourceMD5[k], v, k))
				if removeDuplicateFile:
					os.remove(v)
					os.remove(sourceMD5[k])



if len(sys.argv) < 3:
	print('Usage: {0} sourceFolder destinationFolder [removeDuplicateFile] [compareMD5]'.format(sys.argv[0]))
	raise SystemExit

sourceFolder = sys.argv[1]
assert os.path.exists(sourceFolder),"sourceFolder not found"

destinationFolder = sys.argv[2]
assert os.path.exists(destinationFolder),"destinationFolder not found"

removeDuplicateFile = False

if len(sys.argv) > 3:
	removeDuplicateFile = ('true' == sys.argv[3].lower())

compareMD5 = False

if len(sys.argv) > 4:
	compareMD5 = ('true' == sys.argv[4].lower())

compareFolders(sourceFolder, destinationFolder, removeDuplicateFile, compareMD5)