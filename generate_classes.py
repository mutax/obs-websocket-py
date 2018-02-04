#!/usr/bin/env python
# -*- coding: utf-8 -*-

import six
import six.moves.urllib.request
import json

import_url = "https://raw.githubusercontent.com/Palakis/obs-websocket/master/docs/generated/comments.json"

def toPyVar(string):
    """Converts a string to a suitable variable name by removing not allowed characters."""
    for ch in ["-",".","*"]:
            string=string.replace(ch,"_")
    string=string.replace("[]","")
    return string


def generate_classes():
    """Generates the necessary classes."""
    data = json.loads(six.moves.urllib.request.urlopen(import_url).read().decode('utf-8'))

    for event in data:
        with open("obswebsocket/{}.py".format(event),"w") as file:

            file.write("#!/usr/bin/env python\n")
            file.write("# -*- coding: utf-8 -*-\n")
            file.write("\n")
            file.write("### THIS FILE WAS GENERATED BY ./generate_classes.py - DO NOT EDIT ###\n")
            file.write("\n")
            file.write("from . import base_classes\n")
            file.write("\n")
            for sec in data[event]:
                for i in data[event][sec]:
                    file.write("class {}(base_classes.Base{}):\n".format(i["name"], event))
                    file.write("    \"\"\"{}\n\n".format(i["description"]))

                    arguments_default = []
                    arguments = []
                    try:
                        if len(i["params"]) > 0:
                            file.write("    :Arguments:\n")
                            for a in i["params"]:
                                file.write("       *{}*\n".format(toPyVar(a["name"])))
                                file.write("            type: {}\n".format(a["type"]))
                                file.write("            {}\n".format(a["description"]))
                                if "optional" in a["type"]:
                                    arguments_default.append(a["name"])
                                else:
                                    arguments.append(a["name"])
                    except KeyError:
                        pass

                    returns = []
                    try:
                        if len(i["returns"]) > 0:
                            file.write("    :Returns:\n")
                            for r in i["returns"]:
                                file.write("       *{}*\n".format(toPyVar(r["name"])))
                                file.write("            type: {}\n".format(r["type"]))
                                file.write("            {}\n".format(r["description"]))
                                returns.append(r["name"])
                    except KeyError:
                        pass

                    file.write("    \"\"\"\n")
                    file.write("    def __init__({}):\n".format(
                        ", ".join(["self"] +
                                [toPyVar(a) for a in arguments] +
                                [toPyVar(a)+" = None" for a in arguments_default])
                                )
                    )
                    file.write("        base_classes.Base{}.__init__(self)\n".format(event))
                    file.write("        self.name = \"{}\"\n".format(i["name"]))
                    for r in returns:
                        file.write("        self.datain[\"{}\"] = None\n".format(r))
                    for a in arguments:
                        file.write("        self.dataout[\"{}\"] = {}\n".format(a, toPyVar(a)))
                    for a in arguments_default:
                        file.write("        self.dataout[\"{}\"] = {}\n".format(a, toPyVar(a)))
                    file.write("\n")
                    for r in returns:
                        cc = "".join(x.capitalize() for x in r.split("-"))
                        file.write("    def get{}(self):\n".format(toPyVar(cc)))
                        file.write("        return self.datain[\"{}\"]\n".format(r))
                        file.write("\n")
                    file.write("\n")
                    
if __name__ == "__main__":
    generate_classes()
