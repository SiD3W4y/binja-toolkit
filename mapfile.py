from binaryninja import *

import os

symboltype_map = {
        'a': SymbolType.FunctionSymbol,
        'b': SymbolType.DataSymbol,
        'd': SymbolType.DataSymbol,
        'g': SymbolType.DataSymbol,
        't': SymbolType.FunctionSymbol,
        'r': SymbolType.DataSymbol,
        's': SymbolType.DataSymbol,
        'u': SymbolType.ExternalSymbol
}

def loadmap(bv):
    path = get_open_filename_input("Select symbol map", "*.map")

    if not path or not os.path.exists(path):
        show_message_box("Error", "Could not open symbol file", icon=MessageBoxIcon.ErrorIcon)
        return

    lines = filter(lambda a: len(a) > 0, map(str.strip, open(path, "r").readlines()))
    count = 0

    for line in lines:
        chunks = line.split(" ")

        if len(chunks) != 3:
            show_message_box("Error", "Encountered invalid line while parsing: \"{}\"".format(line), icon=MessageBoxIcon)
            return

        addr, mode, name = chunks[0], chunks[1], chunks[2]

        addr = int(addr, 16) # Let's hope this won't break
        mode = mode.strip().lower()

        if mode in symboltype_map:
            count += 1
            bv.define_user_symbol(Symbol(symboltype_map[mode], addr, name))

    show_message_box("Ok", "Loaded {} symbols from file \"{}\"".format(count, path))


typesymbol_map = {
        SymbolType.FunctionSymbol: 't',
        SymbolType.ImportAddressSymbol: 'u',  # May need to fix that later with a proper symbol
        SymbolType.ImportedFunctionSymbol: 'u',
        SymbolType.DataSymbol: 'd', # Binja doesn't care about the specifics so we don't either
        SymbolType.ImportedDataSymbol: 'u',
        SymbolType.ExternalSymbol: 'u'
}

def savemap(bv):
    path = get_save_filename_input("Save symbol map", "*.map", "symbol.map")

    if not path:
        return

    fd = open(path, "w")

    for sym in bv.get_symbols():
        fd.write("{} {} {}\n".format(hex(sym.address)[2:].replace('L', ''), typesymbol_map[sym.type], sym.name))

    fd.close()

