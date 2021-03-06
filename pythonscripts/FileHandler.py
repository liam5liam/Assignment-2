""" Made by 3 students:
    Matthew Whitaker
    Liam Brydon
    Sarah Ball (providing the model)
"""
# Code passes the PEP8 Check. 4/04/19

import datetime
import re
from pythonscripts.FileView import FileView
fv = FileView()


class FileConverter:
    def __init__(self):
        self.classes = []
        self.converted_classes = []
        self.my_relationship_content = ""
        self.codeToText = ""

    # Made by Sarah - Modified by Matt
    def convert_file(self):
        fv.fc_plantuml_converting()
        for class_info in self.classes:
            class_name = class_info.split(' ')[1]
            attributes = []
            methods = []
            relationships = []
            for line in class_info.split("\n"):
                if line.find(":") != -1:
                    attributes.append(line)
            for line in class_info.split("\n"):
                if line.find("()") != -1:
                    methods.append(line)
            for relationship in self.my_relationship_content.split("\n"):
                if self.find_relationship(relationship, class_name):
                    relationships.append(
                        self.find_relationship(relationship, class_name))
            self.add_class(class_name, attributes, methods, relationships)

    # Made by Sarah
    def add_class(self, class_name, attributes, methods, relationships):
        new_class = ClassBuilder(class_name, attributes,
                                 methods, relationships)
        new_class.add_class_attributes()
        new_class.add_class_methods()
        self.converted_classes.append(new_class)

    # Some work on relationships
    def find_relationship(self, relationship, class_name):
        if relationship.startswith(class_name):
            pass
        elif relationship.endswith(class_name):
            if len(relationship.split(" ")) < 2:
                pass
            elif re.search(r"-->", relationship):
                ext_class = relationship.split(" ")[0]
                return tuple(("association of", ext_class))
            elif re.search(r"\*--", relationship):
                com_class = relationship.split(" ")[0]
                return tuple(("composition of", com_class))
            elif re.search(r"o-", relationship):
                as_class = relationship.split(" ")[0]
                return tuple(("aggregation of", as_class))

    # Made by Sarah
    def print_program(self):
        for x in self.converted_classes:
            x.print_class()

    # Made by Liam
    # Modified by Matt to pass the PEP8 checks.
    def return_program(self):
        out = "# File generated & created on: " + str(datetime.datetime.now())
        out += "\n# File passes the PEP8 check."
        out += "\n\n"
        for x in self.converted_classes:
            out += (x.return_class())
        # out += ""
        self.codeToText += out

    # Made by Matt & Liam
    def read_file(self, file):
        with open(file, "r") as filename:
            data = filename.read()
        rduml = FileReader(data)
        self.classes = rduml.find_classes()
        self.my_relationship_content = \
            self.classes[len(self.classes) - 1]


fc = FileConverter()


# Made by Liam & Matt
class FileReader:
    def __init__(self, filename):
        self.allMyClasses = []
        self.code = filename

    # Made by Matt
    def check_if_plantuml(self, code):
        is_plantuml = False
        try:
            if code.startswith("@startuml") and code.endswith("@enduml"):
                return True
        except IOError:
            fv.general_error()
            print("The file cannot be read.")
        except EOFError:
            fv.general_error()
            print("Unexpected End of File.")
        except TypeError:
            fv.general_error()
            print("The file must contain a string.")
        except Exception as e:
            fv.general_error()
            print("An Error Occurred" + str(e))
        return False

    # Made by Liam
    # Check if the file contains the word "Class"
    def count_occurrences(self, word, sentence):
        try:
            lower = sentence.lower()
            split = lower.split()
            count = split.count(word)
            if count == 0:
                fv.fr_plantuml_classes_not_found()
        except TypeError:
            fv.general_error()
            print("The file must contain a string.")
        except Exception as e:
            fv.general_error()
            print("An Error Occurred" + str(e))
        return count

    # Made by Liam Finds and splits up the classes then stores them in an array
    def find_classes(self):
        try:
            isplantuml = self.check_if_plantuml(self.code)
            if isplantuml:
                fv.fr_file_accepted()
                value = self.count_occurrences("class", self.code)

                for i in range(0, value):
                    self.allMyClasses.append(self.code.split("}\nclass")[i])
                return self.allMyClasses
            else:
                fv.fr_plantuml_error()
        except TypeError:
            fv.general_error()
            print("The file must contain a string.")
        except Exception as e:
            fv.general_error()
            print("An Error Occurred" + str(e))
        return


# Made by Sarah
class ClassBuilder:
    def __init__(self, class_name, new_attributes, new_methods, relationships):
        self.name = class_name
        self.attributes = new_attributes
        self.methods = new_methods
        self.relationships = relationships
        self.all_my_attributes = []
        self.all_my_methods = []
        self.all_my_relationships = []
        self.all_my_associated_classes = []
        self.all_my_aggregated_classes = []
        self.all_my_composite_classes = []

    def add_class_attributes(self):
        for an_attribute in self.attributes:
            new_a_name = an_attribute.split(": ")[0]
            new_a_return = an_attribute.split(": ")[1]
            new_a = Attribute(new_a_name, new_a_return)
            self.all_my_attributes.append(new_a)

    def add_class_methods(self):
        for a_method in self.methods:
            new_m_name = a_method.split(":")[0]
            new_m_return = a_method.split("()")[1]
            new_m = Method(new_m_name, new_m_return)
            self.all_my_methods.append(new_m)

    # Some work on relationships
    def add_class_relationships(self):
        for a_relationship in self.all_my_relationships:
            if "comp" in a_relationship:
                new_relationship = Relationship(a_relationship)
                self.all_my_composite_classes.append(new_relationship)
            if "aggreg" in a_relationship:
                new_relationship = Relationship(a_relationship)
                self.all_my_aggregated_classes.append(new_relationship)
            if "assoc" in a_relationship:
                new_relationship = Relationship(a_relationship)
                self.all_my_associated_classes.append(new_relationship)

    # Liam Brydon's modified code (originally created by Sarah Ball)
    # Used only for debug!
    def print_class(self):
        print("class", self.name, ":", end="\n\n")
        for x in self.all_my_attributes:
            print(x)
        print("")
        print("\tdef __init__(self):")
        print("\t\tpass")
        for x in self.all_my_methods:
            print(x)
        print("\n")

    # Made by Liam
    def return_class(self):
        out = ""
        out += str("\nclass {}:\n\n").format(self.name)

        length = len(self.all_my_attributes)
        count = 0
        for x in self.all_my_attributes:
            if count == length - 1:
                out += str("{}".format(x))
                out += str("\n\n")
                count += 1
            elif count < length:
                out += str("{}".format(x))
                out += str("\n")
                count += 1

        # Don't worry, I figured this out :P - Easy carry made by matt
        out += str("    " + "def __init__(self):\n")
        for a_class in self.relationships:
            out += str(
                "        "
                f"self.{str(a_class[1]).lower()}"
                f" = {a_class[1]}()  "
                f"# {a_class[0]}\n"
            )
        out += "\n"
        out += str("        " + "pass\n\n")

        for x in self.all_my_methods:
            out += str("{}".format(x))
            out += str("\n\n")
        return out


"""
Sarah Ball's code - Modified by Liam + Matt
for compatibility with PEP8
"""


class Attribute:
    def __init__(self, new_name, new_return):
        self.name = new_name
        self._return = new_return
        self.name = self.name.strip(' ')

    def __str__(self):
        if self._return == "String":
            return f"    {self.name}: str"
        elif self._return == "Integer":
            return f"    {self.name}: int"
        elif self._return == "ArrayObject":
            return f"    {self.name}: list"
        elif self._return == "Object":
            return f"    {self.name}: object"
        else:
            return f"    {self.name}: '{self._return}' "


"""
Sarah Ball's code - Modified by Liam + Matt
for compatibility with PEP8
"""


class Method:
    def __init__(self, new_name, new_return):
        self.name = new_name.replace("()", "")
        self._return = new_return

    def __str__(self):
        return f"    def {self.name}(self):\n        pass"


"""
Matt's Relationship code
"""


class Relationship:
    def __init__(self, new_type):
        self.name = new_type[1]
        self.type = new_type[0]

    def __str__(self):
        return f"{self.name}s"
