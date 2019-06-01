from binaryninja import *
from mapfile import loadmap, savemap
from ptrsearch import ptrsearch, ptrlookup
from gbarom import GBAView, microcov_fnlist, microcov_clean, microcov_search

PluginCommand.register("[Toolkit] Load symbol map", "Loads symbols from a symbol map file", loadmap)
PluginCommand.register("[Toolkit] Save symbol map", "Saves the analysed functions to a symbol map file", savemap)
PluginCommand.register("[Toolkit] Find target pointers", "Tries to find pointers pointing to code/data in the rw sections", ptrsearch)
PluginCommand.register_for_address("[Toolkit] Find references to target pointer", "Tries to find references to a specific pointer", ptrlookup)

GBAView.register()
PluginCommand.register("[Toolkit] GBA - Load micro cov", "Lists the functions called from the microcov bb dump", microcov_fnlist)
PluginCommand.register("[Toolkit] GBA - clean micro cov", "Cleans the highlights done by the plugin", microcov_clean)

PluginCommand.register("[Toolkit] GBA - Search instructions in micro cov", "Searches a specific instruction through regex", microcov_search)
