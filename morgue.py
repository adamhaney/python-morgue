"""

A script that searches a directory of python code and attempts to find
instances of dead code

"""

import os
import sys
import ast


def python_files(path):
    """
    Generate all python files in a given directory
    """
    for dirpath, dirname, filenames in os.walk(path):
        python_files = [f for f in filenames if ".py" in f]
        for pyf in python_files:
            yield dirpath, dirname, pyf


def python_files_with_contents(path):
    for dirpath, dirname, pyf in python_files(path):
        try:
            pyf_contents = open(os.path.join(dirpath, pyf)).read()
            yield dirpath, dirname, pyf, pyf_contents
        except IOError:
            continue

def parseable_python_nodes(path):
    for dirpath, dirname, pyf, pyf_contents in python_files_with_contents(path):
        try:
            print dirpath
            file_node = ast.parse(pyf_contents)
            yield dirpath, dirname, pyf, pyf_contents, file_node
        except SyntaxError:
            # Couldn't parse the file
            pass
        except TypeError:
            # The file was empty
            pass


def main(path):
    definitions = {}

    for dirpath, dirname, pyf, pyf_contents, file_node in parseable_python_nodes(path):

        for node in ast.walk(file_node):
            if type(node) == ast.FunctionDef:
                # Create an occurence count of 0
                definitions[node.name] = 0


    for dirpath, dirname, pyf, pyf_contents, file_node in parseable_python_nodes(path):

        for node in ast.walk(file_node):
            if type(node) == ast.Call:
                #print dir(node)
                print dir(node)
                print dir(node.func)
                print node.func
                print dir(node.func.ctx)
                print node.func.id
                exit()


if "__main__" == __name__:
    main(sys.argv[1])
