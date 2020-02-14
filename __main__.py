from argparse import ArgumentParser
from PyWC3 import Map
import sys
import os
from config import *
import re
def create_arg_parser():
    """Create and initialize an argument parser object"""
    parser = ArgumentParser(description="Python Warcraft III Mapscript Generator.")
    parser.add_argument("map", metavar="map", type=str,
                        help="The map folder in the maps directory.",
                        nargs="?", default="")
    parser.add_argument("--build", help="Generate lua code and build the map in the dist directory.",
                        dest="build",action="store_true")
    parser.add_argument("--debug", help="Print python ast tree before code.",
                        dest="debug", action="store_true")
    parser.add_argument("--run", help="Run Warcraft III.",
                        dest="run",action="store_true")
    parser.add_argument("--edit", help="Run Warcraft III World Editor.",
                        dest="edit", action="store_true")
    parser.add_argument("--update-jass", help="Translate the jass source files. Do this when a new WC3 version comes out",
                        dest="jass", action="store_true")
    return parser


def main():
    """Entry point function to the translator"""
    # with open("setup.py")
    print("PyWC3 version {} by Bart Limburg\n".format(_VERSION))
    parser = create_arg_parser()
    argv = parser.parse_args()

    mapfile = argv.map
    if mapfile:
        m = Map(mapfile,show_ast=argv.debug or SHOW_AST)

        m.generate_objects_file()

        if(not (argv.build or argv.run or argv.edit)):
            print("Incorrect usage: please pass --build, --run or --edit as follows: python PyWC3 map.w3x --build --run")
        if argv.build:
            print("Building map {}".format(mapfile))
            m.build_map()

        if argv.run:
            print("Running Warcraft III")
            m.run()

        if argv.edit:
            print("Running Warcraft III World Editor")
            m.edit()
    elif argv.jass:
        from PyWC3 import Jass
        Jass.convertCommonJ()
        Jass.convertCommonAI()
        Jass.convertBlizzardJ()
    else:
        print("Incorrect usage: please pass a mapfile to the script: python PyWC3 map.w3x --build --run")

if __name__ == "__main__":
    sys.exit(main())
