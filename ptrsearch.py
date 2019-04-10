from binaryninja import *
import struct

endian_map = {
        Endianness.LittleEndian: '<',
        Endianness.BigEndian: '>'
}

ptrsize_map = {
        4: "I",
        8: "Q"
}

class TargetPointer:
    def __init__(self, ptrfrom, segfrom, ptrto, segto):
        self.ptrfrom = ptrfrom
        self.segfrom = segfrom
        self.ptrto = ptrto
        self.segto = segto

def __segperm_to_rwx(segment):
    return "{}{}{}".format("-R"[segment.readable],
            "-W"[segment.writable],
            "-X"[segment.executable])

def __search_segment(bv, segment, result):
    ptrsize = bv.arch.address_size
    ptrfmt = "{}{}".format(endian_map[bv.arch.endianness], ptrsize_map[ptrsize])
    segment_data = bv.read(segment.start, segment.data_length)

    for i in range(0, len(segment_data) - ptrsize, ptrsize):
        ptr = struct.unpack(ptrfmt, segment_data[i:i+ptrsize])[0]
        section = bv.get_sections_at(ptr)

        if section:
            section = section[0] # We get the first result section
            seg = bv.get_segment_at(ptr)

            addr = segment.start + i
            result.append(TargetPointer(addr, segment, ptr, seg))

def __format_row(bv, result):
    permfrom = __segperm_to_rwx(result.segfrom)
    permto = __segperm_to_rwx(result.segto)

    symfrom = bv.get_symbol_at(result.ptrfrom)

    if not symfrom:
        symfrom = "(Unknown)"
    else:
        symfrom = symfrom.name

    symto = bv.get_symbol_at(result.ptrto)

    if not symto:
        symto = "(Unknown)"
    else:
        symto = symto.name

    color = ["data", "code"][result.segto.executable]

    return rowfmt.format(color, result.ptrfrom, permfrom, symfrom,
            result.ptrto,
            permto,
            symto)

rowfmt = """
<tr class="{}">
    <td>0x{:08x}</td>
    <td>{}</td>
    <td>{}</td>
    <td>0x{:08x}</td>
    <td>{}</td>
    <td>{}</td>
</tr>
"""

html_template = """
<style>
tr {{
    padding: 5px;
}}

.code {{
    background-color: #ff1641;
}}

.data {{
    background-color: #1687ff;
}}

</style>
<table>
    <tr>
        <th>Pointer from</th>
        <th>Perms from</th>
        <th>Symbol from</th>
        <th>Pointer to</th>
        <th>Perms to</th>
        <th>Symbol to</th>
    </tr>
    {}
</table>
"""

found_entries = []

def ptrsearch(bv):
    global found_entries

    if found_entries:
        res = show_message_box("Warning", "Search data already in cache. Do you want to thrash it ?", MessageBoxButtonSet.YesNoButtonSet)
        
        if not res:
            return

    # Collect the results
    for s in bv.segments:
        if not s.executable and (s.readable or s.writable):
            __search_segment(bv, s, found_entries)
    html = html_template.format("\n".join(map(lambda a: __format_row(bv, a), found_entries)))

    show_html_report("Pointers to code", html, "")

def ptrlookup(bv, addr):
    global found_entries

    if not found_entries:
        show_message_box("Error", "No data in the cache. Do a search first")
        return
    
    result = []

    for e in found_entries:
        if e.ptrto == addr:
            result.append(e)

    
    html = html_template.format("\n".join(map(lambda a: __format_row(bv, a), result)))
    show_html_report("References to 0x{:016x}".format(addr), html, "")
