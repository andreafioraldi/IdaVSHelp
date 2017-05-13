__author__ = "Andrea Fioraldi"
__copyright__ = "Copyright 2017, Andrea Fioraldi"
__license__ = "MIT"
__email__ = "andreafioraldi@gmail.com"

import idaapi
import subprocess
import os

MENU_PATH = 'Edit/Other'
class IdaVSHelpPlugin(idaapi.plugin_t):
    flags = idaapi.PLUGIN_KEEP
    comment = ""

    help = "IdaVSHelp: Visual Studio Help for IDA Pro"
    wanted_name = "IDA Visual Studio Help"
    wanted_hotkey = "Alt-R"

    hlpviewer_path = ""
    catalog_name = ""

    def init(self):
        self.grabInfo()
        r = idaapi.add_menu_item(MENU_PATH, 'Open Microsoft Help Viewer', '', 1, self.openHelp, tuple())
        if r is None:
            idaapi.msg("IdaVSHelp: add menu failed!\n")
        idaapi.msg("IdaVSHelp: initialized\n")
        return idaapi.PLUGIN_KEEP

    def run(self, arg):
        self.query()

    def term(self):
        idaapi.msg("IdaVSHelp: terminated\n")

    def grabInfo(self):
        prog_dir = os.environ["ProgramFiles"]
        data_dir = os.environ["ProgramData"]
        
        # check if Help Viewer directory exists
        hlp_basedir = os.path.join(prog_dir, "Microsoft Help Viewer")
        if not os.path.isdir(hlp_basedir):
            raise Exception("Microsoft Help Viewer not installed")

        # get the lastest version of Help Viewer installed
        maxver = 0.0
        for elem in os.listdir(hlp_basedir):
            p = os.path.join(hlp_basedir, elem)
            if os.path.isdir(p):
                if elem[0] == 'v':
                    try:
                        ver = float(elem[1:])
                    except:
                        continue
                    maxver = max(ver, maxver)

        if maxver == 0.0:
            raise Exception("Microsoft Help Viewer not installed")

        self.hlpviewer_path = os.path.join(hlp_basedir, 'v' + str(maxver), "HlpViewer.exe")

        # get HelpLibrary directory
        helplib_dir = os.path.join(data_dir, "Microsoft", "HelpLibrary")
        if int(maxver) > 1:
            helplib_dir = helplib_dir + str(int(maxver))

        if not os.path.isdir(hlp_basedir):
            raise Exception("Microsoft Help Library not in ProgramData directory")

        catalogs_dir = os.path.join(helplib_dir, "Catalogs")

        # get Visual Studio catalog
        maxver = 0
        for elem in os.listdir(catalogs_dir):
            p = os.path.join(catalogs_dir, elem)
            if os.path.isdir(p):
                try:
                    if elem[:12] == "VisualStudio":
                        ver = int(elem[12:])
                        maxver = max(ver, maxver)
                except:
                    continue

        if maxver == 0:
            raise Exception("Visual Studio catalog is not present, try to run Help Viewer from Visual Studio to create it")

        self.catalog_name = "VisualStudio" + str(maxver)

    def openHelp(self):
        args = [self.hlpviewer_path,
            '/catalogName',
            self.catalog_name,
            '/locale',
            'en-US',
            ]
        subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    def query(self):
        func = idaapi.get_highlighted_identifier()
        args = [self.hlpviewer_path,
            '/catalogName',
            self.catalog_name,
            '/helpQuery',
            'method=f1&query=' + func,
            '/locale',
            'en-US',
            ]
        subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)


def PLUGIN_ENTRY():
    return IdaVSHelpPlugin()

