import os

def findAllPumlaFiles(path):
    pumlafiles = []

    for dirpath, dirs, files in os.walk(path):
        for filename in files:
            fname = os.path.join(dirpath, filename)
            if fname.endswith('.puml'):
                with open(fname) as myfile:
                    line = myfile.read()
                    if (line.startswith("'PUMLAMR")):
                        pumlafiles.append(fname)
    return pumlafiles