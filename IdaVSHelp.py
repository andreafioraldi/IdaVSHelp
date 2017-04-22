__author__ = "Andrea Fioraldi"
__copyright__ = "Copyright 2017, Andrea Fioraldi"
__license__ = "MIT"
__email__ = "andreafioraldi@gmail.com"

import idaapi
import subprocess
import os

def query():
    func = idaapi.get_highlighted_identifier()
    args = [os.environ["ProgramFiles"] + '\\Microsoft Help Viewer\\v2.2\\HlpViewer.exe',
        '/catalogName',
        'VisualStudio14',
        '/helpQuery',
        'method=f1&query=' + func,
        '/locale',
        'en-US',
        '/launchingApp',
        'Microsoft,VisualStudio,14.0'
        ]
    subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

def open_help():
    args = [os.environ["ProgramFiles"] + '\\Microsoft Help Viewer\\v2.2\\HlpViewer.exe',
        '/catalogName',
        'VisualStudio14',
        '/locale',
        'en-US',
        '/launchingApp',
        'Microsoft,VisualStudio,14.0'
        ]
    subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)


MENU_PATH = 'Edit/Other'
class IdaVSHelp_plugin_t(idaapi.plugin_t):
    flags = idaapi.PLUGIN_KEEP
    comment = ""

    help = "IdaVSHelp: Visual Studio Help Referene for IDA"
    wanted_name = "IDA Visual Studio Help"
    wanted_hotkey = "Alt-9"

    def init(self):
        r = idaapi.add_menu_item(MENU_PATH, 'Open Microsoft Help Viewer', '', 1, open_help, tuple())
        if r is None:
            idaapi.msg("IdaVSHelp: add menu failed!\n")
        idaapi.msg("IdaVSHelp: initialized\n")
        return idaapi.PLUGIN_KEEP

    def run(self, arg):
        query()

    def term(self):
        idaapi.msg("IdaVSHelp: terminated\n")

def PLUGIN_ENTRY():
    return IdaVSHelp_plugin_t()

