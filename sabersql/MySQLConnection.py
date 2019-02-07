from Utilities import _shell

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

        stdOut, stdErr = _shell("mysql -u%s -p%s %s -B -e %s" % (self.username, self.password, self.database, command))
        if stdErr:
            if_port = ""
            if self.port:
                if_port = ":%s" % self.port
            raise ConnectionError("Failed to connect to MySQL database %s at %s@%s%s" %
                                  (self.database, self.username, self.address, if_port))
        else:
            return stdOut


    def create_database(self):
        """
        Creates database and tables as documented on `GitHub <https://github.com/liam923/sabersql>`_.
        :raises ConnectionError: if the connection fails
        """

        self.__run("create database if not exists %s" % (self.database))
