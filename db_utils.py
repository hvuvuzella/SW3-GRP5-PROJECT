import mysql.connector # module that allows to establish database connection
from config import USER, PASSWORD, HOST
import sys

class DbConnectionError(Exception):
    pass



if __name__ == '__main__':
    main()

