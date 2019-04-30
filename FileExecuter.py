# Ignore errors below this line.
import sys
import cmd
from typing import Dict, List

from pythonscripts.FileController import FileController
from pythonscripts.FileView import FileView

# Execute code here
# Matthew Whitaker's code.
fv = FileView()
fc = FileController()


# 4/04/19 Code passes the PEP8 Check.
# CMD based code - Matt


class Main(cmd.Cmd):
    def __init__(self):
        super(Main, self).__init__()
        self.intro = \
            "===============================================\n" \
            "PlantUML to Python Converter\n" \
            "Please type 'help' for all available commands.\n" \
            "Please type 'allhelp' to view the help file.\n" \
            "To continue with a default graph.txt in the\n" \
            "root directory, press [Enter]\n" \
            "=============================================="

    # CMD - Matt
    def cmdloop(self, intro=None):
        print(self.intro)
        while True:
            try:
                super(Main, self).cmdloop(intro="")
                break
            except KeyboardInterrupt:
                print("Ctrl + C pressed, but ignored. "
                      "Please use 'exit' or 'quit' "
                      "to stop the program.")
            except TypeError and ValueError:
                fv.general_error()
                print("Please verify your command, and try again.")
            except Exception:
                fv.general_error()
                print("An error has occurred.")

    # Continues when no command is entered - Matt
    def emptyline(self):
        fv.fe_defaults()
        fc.handle_command('', '')

    # Load method - Matt
    def do_load(self, line):
        """
        LOADS your SOURCE PlantUML text file, and translates it
        into a python file, from the current working directory.
        Usage: LOAD [filename.txt]
        """
        fc.handle_command("load", line)

        """
        userinput = input("Would you like to view the file? (Y/N) ")
        if userinput.lower() == "y":
            # open the file
            pass
        elif userinput.lower() == "n":
            pass
        else:
            # ask them again
            pass
        """

    # Absload method - Matt
    def do_absload(self, line):
        """
        LOADS your SOURCE PlantUML text file, and translates it
        into a python file, from the directory of your choosing.
        Usage: ABSLOAD [path_to_filename.txt]
        """
        if "\\" in line:
            fc.handle_command("absload", line)
            fv.next_command()
        else:
            fv.general_error()
            fv.fe_abs_path_error()

    # View help file - Matt and Liam
    def do_allhelp(self, line):
        """
        SHOWS all HELP relating to this program.
        Usage: ALLHELP
        """
        fv.print_help()

    # Exit method - Matt
    def do_exit(self, line):
        """
        EXITS the program cleanly. (same as QUIT)
        Usage: exit
        """
        exit()

    # Quit method - Matt
    def do_quit(self, line):
        """
        QUITS the program cleanly. (same as EXIT)
        Usage: quit
        """
        self.do_exit(line)

    # Save method - Liam
    def do_save(self, line):
        """
        Saves the converted plantuml code from the database to a textfile
        Usage: save {filename.txt} {code_id}
        """
        line = line.split(' ')
        fc.save_file(line[0], line[1])

    # Printcode method - Liam
    def do_printcode(self, line):
        """
        Prints the converted plantuml code from the database to the cmd
        Usage: printcode {code_id}
        """
        fc.print_code(line)

    # Loadcode method - Liam
    def do_loadcode(self, line):
        """
        Loads code from the database into self.data
        Usage: loadcode {code_id}
        """
        fc.load_code(line)

    # Printfile method - Liam
    def do_printfile(self, line):
        """
        Prints the data saved inside self.data to the cmd
        Usage: printfile
        """
        fc.print_file()

    fv.next_command()

# Liam
def print_to_screen():
    their_answer = input("Would you like to print the "
                         "code to the screen? y/n: ")
    if their_answer == "y":
        fc.print_file()

    their_answer = input("Would you like to save the code to Output.txt y/n: ")
    if their_answer == "y":
        fc.save_file("Output.txt")


m = Main()

class CheckDictionary():

    def __init__(self, cmd, arg1, arg2, length):
        self.arg1 = arg1
        self.arg2 = arg2
        self.cmd = cmd
        self.length = length
        self.command_dict = {
            "save": [fv.fe_command_syntax("Save"), self.save_cmd()],
            "help": [fc.view_help()],
            "loadcode": [fv.fe_loadcode_syntax("loadcode"), self.loadcode_cmd()],
            "printcode": [fv.fe_loadcode_syntax("printcode"), self.printcode_cmd()],
            "load": [fv.fe_command_syntax("Load"), self.load_cmd()],
            "absload": [fv.fe_abs_path_error(), self.absload_cmd()]
        }

    def save_cmd(self):
         fc.save_file(self.arg1, self.arg2)

    def loadcode_cmd(self):
         fc.load_code(self.arg1)

    def printcode_cmd(self):
        fc.print_code(self.arg1)

    def load_cmd(self):
        fc.handle_command("load", str(self.arg1))

    def absload_cmd(self):
        fc.handle_command("absload", str(self.arg1))

    def get_error(self):
        self.command_dict[self.cmd][0]()

    def check(self):
        if self.cmd in self.command_dict:
            if self.length > 3:
                fv.fe_too_many_args()
            elif self.length == 2:
                fv.general_error()
                self.get_error()
            elif self.length > 2:
                self.command_dict[cmd][1]()
            else:
                fv.general_error()
                fv.output("Command not found!")
                m.cmdloop()


if __name__ == "__main__":
    # For Debugging Sys.Argv
    # print('Number of arguments:', len(sys.argv), 'arguments.')
    # print('Argument List:', str(sys.argv))


    length = len(sys.argv)
    cmd = str(sys.argv[1]).lower()
    sys.argv.insert(1, -1)

    checkDictionary = CheckDictionary(cmd, sys.argv[2], sys.argv[3], length)


    try:
        checkDictionary.check();


    # Ignores issues with Sys.argv
    except IndexError:
        pass
    # Checks for file permission errors.
    except PermissionError:
        print("Permission Error!\n"
              "Check you have the permission to read the file!")
    else:
        pass
        # m.cmdloop()
