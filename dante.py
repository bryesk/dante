import os

def makeNewFileName (directory, input_file, ext):
    d = os.path.normcase(directory)
    if not os.path.exists(d):
        os.makedirs(d)
    file_name = os.path.splitext(os.path.basename(input_file))[0] + ext
    return os.path.join(os.path.normpath(directory), file_name)
