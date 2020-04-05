import os


def list_files(startpath: str):
    """
        Print a summary of directory's tree
        Arguments:
            startpath {str} -- A path to a directory to inspect
        """
    for root, dirs, files in os.walk(startpath):
        level = root.replace(startpath, "").count(os.sep)
        indent = " " * 4 * (level)
        print("{}{}/".format(indent, os.path.basename(root)))
        subindent = " " * 4 * (level + 1)
        for f in files:
            if ".DS_Store" not in f:
                print("{}{}".format(subindent, f))
