from Utilities import _shell
import Schemas
import math

class MySQLConnection:
    """
    Manages a MySQL connection and sends commands.
    """

    def __init__(self, username, password, database, address, port=None):
        """
        Initialize a MySQLConnection with the given connection information
        :param username: the database user
        :param password: the password for the user
        :param database: the name of the database to store the data in
        :param address: the address of the database server
        :param port: the port of the database server
        """

        self.username = username
        self.password = password
        self.database = database
        self.address = address
        self.port = port

    def __run(self, command):
        """
        Runs the given command within the MySQL connection
        :param command: the command to be run
        :return: the stdout of running the command
        :raises ConnectionError: if the connection fails
        """

        stdOut, stdErr = _shell("export MYSQL_PWD=%s; mysql -u%s %s -B -e \"%s\"" %
                                (self.password, self.username, self.database, command))
        if stdErr:
            if_port = ""
            if self.port:
                if_port = ":%s" % self.port
            raise ConnectionError("Failed to connect to MySQL database %s at %s@%s%s : %s" %
                                  (self.database, self.username, self.address, if_port, stdErr))
        else:
            return stdOut


    def create_database(self):
        """
        Creates database and tables as documented on `GitHub <https://github.com/liam923/sabersql>`_.
        :raises ConnectionError: if the connection fails
        """

        self.__run("create database if not exists %s;" % (self.database))
        for schema in Schemas.schemas:
            self.__run(schema)

    def import_data(self, table, headers, data, batch_size=100):
        """
        Imports data into a given table.
        :param table: the name of the table to add data to
        :param headers: the column names of the values to add, as an array of strings
        :param data: the values to add to the table, as an array of arrays of strings that are the value literal
        :param batch_size: how many values to send at once
        :raises ConnectionError: if the connection fails
        """

        for i in range(0, math.ceil(len(data) / batch_size)):
            command = "INSERT INTO %s (" % table
            command += ','.join(headers)
            command += ") VALUES"
            command += ','.join(["(" + ','.join(row) + ")" for row in data[batch_size*i:min(batch_size*(i + 1), len(data))]])
            command += ";"
            self.__run(command)
