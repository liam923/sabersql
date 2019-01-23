#!/usr/bin/env python
import subprocess

def _download(url, target):
    """
    Synchronously downloads a file to a given location

    :param url: the url of the file to download
    :param target: the location to download the file to
    :return: None
    """


    pass

def _shell(command):
    """
    Calls a shell command

    :param command: the command to be run
    :return: (stdOut, stdErr)
    """

    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = process.communicate()
    if out is not None:
        out = out.decode('utf-8')
    if err is not None:
        err = err.decode('utf-8')
    return out, err
