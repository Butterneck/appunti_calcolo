#!/usr/bin/env python3

from os import listdir, getcwd, mkdir, remove
from os.path import isdir, isfile, join, splitext
import subprocess
from subprocess import check_output
from shutil import move


def getDirs(path='.'):
    return [f for f in listdir(path) if (isdir(join(path, f)) and not (f == '.git'))]


def buildDirs(dirs):
    for dir in dirs:
        buildDir(dir)


def buildDir(dir):
    basename = "lezione" + str(int(dir[:2]))
    jobname = "-jobname=" + basename
    lezione = ".".join([basename, "tex"])

    buildCmd = ["docker", "run", "-i", "-v", "/".join([getcwd(), dir]) + ":/data", "blang/latex", "latexmk", "-interaction=nonstopmode", "-pdf", jobname, lezione]
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


def main():
    dirs = getDirs()
    buildDirs(dirs)
    groupPdfs(dirs)


if __name__ == '__main__':
    main()
