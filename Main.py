# Import modules here
# from plantuml import *
import os


class MakeClassDiagram:
    def __init__(self, filename):
        self.allMyClasses = []
        self.code = filename

    def count_occurrences(self, word, sentence):
        return sentence.lower().split().count(word)

    def find_classes(self):
        value = self.count_occurrences("class", self.code)

        for i in range(0, value):
            self.allMyClasses.append(self.code.split("class")[i + 1])


with open("Graph.txt", "r") as filename:
    data = filename.read().replace('\n', ' ')
print(data)
mkd = MakeClassDiagram(data)
mkd.find_classes()
print(mkd.allMyClasses)

"""
contents = Alice -> Bob: test
if os.path.exists("Graph.txt"):
    os.remove("Graph.txt")
if os.path.exists("Graph.png"):
    os.remove("Graph.png")
else:
    print("The file does not exist. skipping...")
file = open("Graph.txt", "x")
file.write("@startuml\n")
file.write(contents + "\n")
file.write("@enduml")
"""

# Refresh Graph
os.system('C:\\Windows\\System32\\cmd.exe /c CreateGraph.bat')
