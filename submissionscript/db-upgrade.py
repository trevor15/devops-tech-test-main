#!/usr/bin/python
import sys
import os
import MySQLdb

def main(argv):
    # Initiate connection with Database
    db = MySQLdb.connect("mysql_container","dev","123456","devopstt" )
    cursor = db.cursor()

    # Check number of argusments
    if len(sys.argv) != 6:
        print("Missing argument! Please check your command line syntax")
        exit()

    # Get thie latest database version
    cursor.execute("SELECT version FROM versionTable")

    dbVersion = cursor.fetchone()
    dbVersion = dbVersion[0]
    print("Current database version: %s " % dbVersion)

    # Look for scripts in folder
    path = os.getcwd()
    scriptsPath = os.path.abspath(os.path.join(path, os.pardir)) + "/scripts/"
    scripts = os.listdir(scriptsPath)

    # Get a list of scripts that need to be run
    scriptsList = []
    for file in scripts:
        if isfloat(file[:2]):
            # Check if script number is higher than dbVersion, if so the script is added list
            if float(dbVersion) < float(file[:2]):
                scriptsList.append(file)

    scriptsList.sort()
    print("\nScripts to be run: ", scriptsList)

    # Run the sql scripts
    for i in scriptsList:
        print("\nNow running: '%s'" % i)
        result = executeScriptsFromFile(scriptsPath+i, cursor)

        # Change name of dbversion to latest ran script
        if result:
            print("%s ran successfully." % i)
            newCommand = "UPDATE versionTable SET version='" + i[:2] + "';"
            cursor.execute(newCommand)
        else:
            print("%s did not run." % i)

    # Print the up to date database version
    cursor.execute("SELECT version FROM versionTable")
    newVersion = cursor.fetchone()
    newVersion = newVersion[0]
    print("\nDatabase version updated to: %s" % newVersion)

    # Disconnect from the database server
    db.close()


# Function to convert values to a numerical value
def isfloat(value):
  try:
    float(value)
    return True
  except ValueError:
    return False


# Function to execute SQL statements from a chosen file
def executeScriptsFromFile(filename,cursor):
    with open(filename) as f:
        try:
            cursor.execute(f.read())
            return True
        except:
            return False



if __name__ == "__main__": main(sys.argv[1:])
