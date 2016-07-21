from model.project import Project
import random
import string
import os.path
import jsonpickle
import getopt
import sys


try:
    opts, args = getopt.getopt(sys.argv[1:], "n:f:", ["number of groups", "file"])
except getopt.GetoptError as err:
    getopt.usage()
    sys.exit(2)

number = 2
file = "data/projects.json"

for o, a in opts:
    if o == "-n":
        number = int(a)
    elif o == "-f":
        file = a

def random_string(prefix, maxlen):
    char = string.ascii_letters + string.hexdigits + ' '*5 #+ string.punctuation
    return prefix + "".join([random.choice(char) for i in range(random.randrange(maxlen))])

random_data = [
    Project(name=random_string("name", 20), description=random_string("description", 20))
    for i in range(number)
]

file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", file)

with open(file, "w") as f:
    jsonpickle.set_encoder_options("json", indent=2)
    f.write(jsonpickle.encode(random_data))
