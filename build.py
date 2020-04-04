#!/usr/bin/env python3

from os import listdir, getcwd, mkdir, remove
from os.path import isdir, isfile, join, splitext
import subprocess
from subprocess import check_output
from shutil import move
from PyPDF2 import PdfFileMerger


def getDirs(path='.'):
    dirs = []
    for dir in listdir(path):
        if isdir(join(path, dir)):
            try:
                int(dir[:2])
                dirs.append(dir)
            except:
                continue
    return dirs



def buildDirs(dirs):
    for dir in dirs:
        buildDir(dir)


def buildDir(dir):
    basename = "lezione" + str(int(dir[:2]))
    jobname = "-jobname=" + basename
    lezione = ".".join([basename, "tex"])

    buildCmd = ["docker", "run", "-i", "-v", "/".join([getcwd(), dir]) + ":/data", "blang/latex", "latexmk", "-pdf", jobname, lezione]
    subprocess.run(buildCmd)


def groupPdfs(dirs, outputDir='./output'):
    mkdir(outputDir)

    for dir in dirs:
        path = "/".join([getcwd(), dir])
        files = [f for f in listdir(path) if isfile(join(path, f))]
        for file in files:
            filename, file_extension = splitext(file)
            if file_extension == '.pdf':
                move("/".join([path, filename + file_extension]), "/".join([outputDir, filename + file_extension]))


def generateCompletePdf(outputDir='./output'):
    path = outputDir
    merger = PdfFileMerger()

    files = listdir(path)
    files = orderFiles(files)

    for pdf in files:
        merger.append("/".join([path, pdf]))

    merger.write("/".join([path, "lezioni.pdf"]))
    merger.close()


def orderFiles(files):
    indexes = [filename[7:] for filename, file_extension in [splitext(file) for file in files]]
    indexes.sort(key=int)
    return [''.join(["lezione", index, ".pdf"]) for index in indexes]



def main():
    dirs = getDirs()
    buildDirs(dirs)
    groupPdfs(dirs)
    generateCompletePdf()    

if __name__ == '__main__':
    main()
