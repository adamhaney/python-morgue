"""

A script that searches a directory of python code and attempts to find
instances of dead code

"""

import os
import sys
import ast

from ast import NodeVisitor


def python_files(path):
    """
    Generate all python files in a given directory
    """
    for dirpath, dirname, filenames in os.walk(path):
        for f in filenames:
            fullpath = os.path.join(dirpath, f)
            if fullpath.endswith(".py"):
                yield fullpath


class UsageAnalyzer(NodeVisitor):
    """
    Keep track of which functions and methods are being called on
    which objects and from which modules

    NOTE: Currently we just look for function names that are never
    invoked anywhere this ignores the fact that two functions in
    different modules or classes both get credit for being called if
    any call object references their name. BUT, this helps us get
    around inheritence, meta class issues, the whole 9.
    """
    def __init__(self, *args, **kwargs):
        self.called_function_names = set()
        self.defined_function_names = set()

        return super(UsageAnalyzer, self).__init__(*args, **kwargs)

    def visit_Call(self, node, *args, **kwargs):
        def get_name(node):
            # function calls
            if hasattr(node.func, 'id'):
                return node.func.id, node.func.ctx

            # method calls
            if hasattr(node.func, 'value'):
                return node.func.attr, node.func.ctx

            if hasattr(node.func, 'func'):
                return get_name(node.func)

        name, ctx = get_name(node)
        self.called_function_names.add(name)

        self.generic_visit(node, *args, **kwargs)

    def visit_ImportFrom(self, node, *args, **kwargs):
        self.generic_visit(node, *args, **kwargs)

    def visit_FunctionDef(self, node, *args, **kwargs):
        self.defined_function_names.add(node.name)

        self.generic_visit(node, *args, **kwargs)

    def find_dead(self):
        return self.defined_function_names - self.called_function_names


def main(paths):
    usage_analyzer = UsageAnalyzer()
    for path in paths:
        for f in python_files(path):
            tree = ast.parse(open(f).read(), f)
            usage_analyzer.visit(tree)
            #print ast.dump(tree)

    for dead in usage_analyzer.find_dead():
        print dead


if "__main__" == __name__:
    main(sys.argv[1:])
