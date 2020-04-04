#!/usr/bin/env python3

from os import listdir, getcwd, mkdir, remove
from os.path import isdir, isfile, join, splitext
import subprocess
from subprocess import check_output


def build():
    dirs = getDirs()

    mkdir('output')

    for dir in dirs:
        basename = "lezione" + str(int(dir[:2])) 
        jobname = "-jobname=" + "/".join(["output", basename])
        lezione = "/".join([dir, basename]) + ".tex"

        buildCmd = ["docker", "run", "-i", "-v", getcwd() + ":/data", "blang/latex", "latexmk", "-interaction=nonstopmode", "-pdf", jobname, lezione]

        subprocess.run(buildCmd)
        clearOutputDir()


def getDirs(path='.'):
    return [f for f in listdir(path) if (isdir(join(path, f)) and not (f == '.git'))]


def clearOutputDir(path = './output'):
    files = [f for f in listdir(path) if isfile(join(path, f))]

    for file in files:
        filename, file_extension = splitext(file)
        if file_extension != '.pdf':
            remove('./output/' + filename + file_extension)


def main():
    build()


if __name__ == '__main__':
    main()
