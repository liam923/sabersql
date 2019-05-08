#!/usr/bin/env python3

import os
import pandas
import subprocess

def _download(url, target, unzip=None, overwrite=False):
    """
    Synchronously downloads a file to a given location

    :param url: the url of the file to download
    :param target: the location to download the file to
    :param overwrite: if True, the file will be overwritten if it already exists (default False)
    :return: None
    """

    _shell("mkdir -p \"%s\"" % os.path.dirname(target))

    if overwrite or (not unzip and not os.path.isfile(target)) or (unzip and not os.path.isdir(unzip)):
        _shell("curl \"%s\" -L -s --connect-timeout 3 -o \"%s\"" % (url, target))
        if unzip:
            _shell("unzip \"%s\" -d \"%s\"" % (target, unzip))
            _shell("rm \"%s\"" % target)

def _import_csv(path, header=None):
    """
    Reads a csv file into memory

    :param path: the path to the csv
    :param header: the header for the file (as array of strings); if None (default), the headers will come from the first line of the file
    :return: a pandas DataFrame of the csv
    """

    if header:
        return pandas.read_csv(path, header=None, names=header)
    else:
        dataframe = pandas.read_csv(path, low_memory=False)
        names_so_far = set()
        for col in dataframe.columns:
            if col in names_so_far:
                dataframe = dataframe.drop(columns=col)
            else:
                names_so_far.add(col + ".1")
        return dataframe


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
