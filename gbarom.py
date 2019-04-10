from binaryninja import *
import struct
import os

class GBAView(BinaryView):
    name = "GBA"
    long_name = "GBA Rom"

    def __init__(self, data):
        BinaryView.__init__(self, parent_view=data, file_metadata=data.file)
        self.size = len(data.read(0, 0x1000000))
        self.platform = Architecture["armv7"].standalone_platform
    
    @classmethod
    def is_valid_for_data(self, data):
        hdr = data.read(0, 0xc0)


        if len(hdr) < 0xc0:
            return False

        magic_byte = struct.unpack("B", hdr[0xb2])[0]
        
        if magic_byte != 0x96:
            return False

        return True

    def init(self):
        try:
            # Adding segments
            rwx_mask = SegmentFlag.SegmentReadable | SegmentFlag.SegmentWritable | SegmentFlag.SegmentExecutable
            self.add_auto_segment(0x2000000, 0x40000, 0, 0, rwx_mask) # WRAM
            self.add_auto_segment(0x3000000, 0x08000, 0, 0, rwx_mask) # IRAM
            self.add_auto_segment(0x4000000, 0x003FF, 0, 0, SegmentFlag.SegmentReadable | SegmentFlag.SegmentWritable) # IO
            self.add_auto_segment(0x6000000, 0x18000, 0, 0, rwx_mask) # VRAM
            self.add_auto_segment(0x7000000, 0x00400, 0, 0, SegmentFlag.SegmentReadable | SegmentFlag.SegmentWritable) # OBJ Attributes
            self.add_auto_segment(0x8000000, 0x1000000, 0, self.size, SegmentFlag.SegmentReadable | SegmentFlag.SegmentExecutable)

            # IO Registers
            self.define_auto_symbol(Symbol(SymbolType.DataSymbol, 0x4000000, "DISPCNT"))
            self.define_auto_symbol(Symbol(SymbolType.DataSymbol, 0x4000004, "DISPSTAT"))
            self.define_auto_symbol(Symbol(SymbolType.DataSymbol, 0x4000006, "VCOUNT"))
            self.define_auto_symbol(Symbol(SymbolType.DataSymbol, 0x4000008, "BG0CNT"))
            self.define_auto_symbol(Symbol(SymbolType.DataSymbol, 0x400000A, "BG1CNT"))
            self.define_auto_symbol(Symbol(SymbolType.DataSymbol, 0x400000C, "BG2CNT"))
            self.define_auto_symbol(Symbol(SymbolType.DataSymbol, 0x400000E, "BG3CNT"))
            self.define_auto_symbol(Symbol(SymbolType.DataSymbol, 0x4000010, "BG0HOFS"))
            self.define_auto_symbol(Symbol(SymbolType.DataSymbol, 0x4000012, "BG0VOFS"))
            self.define_auto_symbol(Symbol(SymbolType.DataSymbol, 0x4000014, "BG1HOFS"))
            self.define_auto_symbol(Symbol(SymbolType.DataSymbol, 0x4000016, "BG1VOFS"))
            self.define_auto_symbol(Symbol(SymbolType.DataSymbol, 0x4000018, "BG2HOFS"))
            self.define_auto_symbol(Symbol(SymbolType.DataSymbol, 0x400001A, "BG2VOFS"))
            self.define_auto_symbol(Symbol(SymbolType.DataSymbol, 0x400001C, "BG3HOFS"))
            self.define_auto_symbol(Symbol(SymbolType.DataSymbol, 0x400001E, "BG3VOFS"))
            self.define_auto_symbol(Symbol(SymbolType.DataSymbol, 0x4000020, "BG2PA"))
            self.define_auto_symbol(Symbol(SymbolType.DataSymbol, 0x4000022, "BG2PB"))
            self.define_auto_symbol(Symbol(SymbolType.DataSymbol, 0x4000024, "BG2PC"))
            self.define_auto_symbol(Symbol(SymbolType.DataSymbol, 0x4000026, "BG2PD"))
            self.define_auto_symbol(Symbol(SymbolType.DataSymbol, 0x4000028, "BG2X"))
            self.define_auto_symbol(Symbol(SymbolType.DataSymbol, 0x400002C, "BG2Y"))
            self.define_auto_symbol(Symbol(SymbolType.DataSymbol, 0x4000030, "BG3PA"))
            self.define_auto_symbol(Symbol(SymbolType.DataSymbol, 0x4000032, "BG3PB"))
            self.define_auto_symbol(Symbol(SymbolType.DataSymbol, 0x4000034, "BG3PC"))
            self.define_auto_symbol(Symbol(SymbolType.DataSymbol, 0x4000036, "BG3PD"))
            self.define_auto_symbol(Symbol(SymbolType.DataSymbol, 0x4000038, "BG3X"))
            self.define_auto_symbol(Symbol(SymbolType.DataSymbol, 0x400003C, "BG3Y"))
            self.define_auto_symbol(Symbol(SymbolType.DataSymbol, 0x4000040, "WIN0H"))
            self.define_auto_symbol(Symbol(SymbolType.DataSymbol, 0x4000042, "WIN1H"))
            self.define_auto_symbol(Symbol(SymbolType.DataSymbol, 0x4000044, "WIN0V"))
            self.define_auto_symbol(Symbol(SymbolType.DataSymbol, 0x4000046, "WIN1V"))
            self.define_auto_symbol(Symbol(SymbolType.DataSymbol, 0x4000048, "WININ"))
            self.define_auto_symbol(Symbol(SymbolType.DataSymbol, 0x400004A, "WINOUT"))
            self.define_auto_symbol(Symbol(SymbolType.DataSymbol, 0x400004C, "MOSAIC"))
            self.define_auto_symbol(Symbol(SymbolType.DataSymbol, 0x4000050, "BLDCNT"))
            self.define_auto_symbol(Symbol(SymbolType.DataSymbol, 0x4000052, "BLDALPHA"))
            self.define_auto_symbol(Symbol(SymbolType.DataSymbol, 0x4000054, "BLDY"))
            self.define_auto_symbol(Symbol(SymbolType.DataSymbol, 0x4000060, "SOUND1CNT_L"))
            self.define_auto_symbol(Symbol(SymbolType.DataSymbol, 0x4000062, "SOUND1CNT_H"))
            self.define_auto_symbol(Symbol(SymbolType.DataSymbol, 0x4000064, "SOUND1CNT_X"))
            self.define_auto_symbol(Symbol(SymbolType.DataSymbol, 0x4000068, "SOUND2CNT_L"))
            self.define_auto_symbol(Symbol(SymbolType.DataSymbol, 0x400006C, "SOUND2CNT_H"))
            self.define_auto_symbol(Symbol(SymbolType.DataSymbol, 0x4000070, "SOUND3CNT_L"))
            self.define_auto_symbol(Symbol(SymbolType.DataSymbol, 0x4000072, "SOUND3CNT_H"))
            self.define_auto_symbol(Symbol(SymbolType.DataSymbol, 0x4000074, "SOUND3CNT_X"))
            self.define_auto_symbol(Symbol(SymbolType.DataSymbol, 0x4000078, "SOUND4CNT_L"))
            self.define_auto_symbol(Symbol(SymbolType.DataSymbol, 0x400007C, "SOUND4CNT_H"))
            self.define_auto_symbol(Symbol(SymbolType.DataSymbol, 0x4000080, "SOUNDCNT_L"))
            self.define_auto_symbol(Symbol(SymbolType.DataSymbol, 0x4000082, "SOUNDCNT_H"))
            self.define_auto_symbol(Symbol(SymbolType.DataSymbol, 0x4000084, "SOUNDCNT_X"))
            self.define_auto_symbol(Symbol(SymbolType.DataSymbol, 0x4000088, "SOUNDBIAS"))
            self.define_auto_symbol(Symbol(SymbolType.DataSymbol, 0x4000090, "2x10h"))
            self.define_auto_symbol(Symbol(SymbolType.DataSymbol, 0x40000A0, "FIFO_A"))
            self.define_auto_symbol(Symbol(SymbolType.DataSymbol, 0x40000A4, "FIFO_B"))
            self.define_auto_symbol(Symbol(SymbolType.DataSymbol, 0x40000B0, "DMA0SAD"))
            self.define_auto_symbol(Symbol(SymbolType.DataSymbol, 0x40000B4, "DMA0DAD"))
            self.define_auto_symbol(Symbol(SymbolType.DataSymbol, 0x40000B8, "DMA0CNT_L"))
            self.define_auto_symbol(Symbol(SymbolType.DataSymbol, 0x40000BA, "DMA0CNT_H"))
            self.define_auto_symbol(Symbol(SymbolType.DataSymbol, 0x40000BC, "DMA1SAD"))
            self.define_auto_symbol(Symbol(SymbolType.DataSymbol, 0x40000C0, "DMA1DAD"))
            self.define_auto_symbol(Symbol(SymbolType.DataSymbol, 0x40000C4, "DMA1CNT_L"))
            self.define_auto_symbol(Symbol(SymbolType.DataSymbol, 0x40000C6, "DMA1CNT_H"))
            self.define_auto_symbol(Symbol(SymbolType.DataSymbol, 0x40000C8, "DMA2SAD"))
            self.define_auto_symbol(Symbol(SymbolType.DataSymbol, 0x40000CC, "DMA2DAD"))
            self.define_auto_symbol(Symbol(SymbolType.DataSymbol, 0x40000D0, "DMA2CNT_L"))
            self.define_auto_symbol(Symbol(SymbolType.DataSymbol, 0x40000D2, "DMA2CNT_H"))
            self.define_auto_symbol(Symbol(SymbolType.DataSymbol, 0x40000D4, "DMA3SAD"))
            self.define_auto_symbol(Symbol(SymbolType.DataSymbol, 0x40000D8, "DMA3DAD"))
            self.define_auto_symbol(Symbol(SymbolType.DataSymbol, 0x40000DC, "DMA3CNT_L"))
            self.define_auto_symbol(Symbol(SymbolType.DataSymbol, 0x40000DE, "DMA3CNT_H"))
            self.define_auto_symbol(Symbol(SymbolType.DataSymbol, 0x4000100, "TM0CNT_L"))
            self.define_auto_symbol(Symbol(SymbolType.DataSymbol, 0x4000102, "TM0CNT_H"))
            self.define_auto_symbol(Symbol(SymbolType.DataSymbol, 0x4000104, "TM1CNT_L"))
            self.define_auto_symbol(Symbol(SymbolType.DataSymbol, 0x4000106, "TM1CNT_H"))
            self.define_auto_symbol(Symbol(SymbolType.DataSymbol, 0x4000108, "TM2CNT_L"))
            self.define_auto_symbol(Symbol(SymbolType.DataSymbol, 0x400010A, "TM2CNT_H"))
            self.define_auto_symbol(Symbol(SymbolType.DataSymbol, 0x400010C, "TM3CNT_L"))
            self.define_auto_symbol(Symbol(SymbolType.DataSymbol, 0x400010E, "TM3CNT_H"))
            self.define_auto_symbol(Symbol(SymbolType.DataSymbol, 0x4000120, "SIODATA32"))
            self.define_auto_symbol(Symbol(SymbolType.DataSymbol, 0x4000120, "SIOMULTI0"))
            self.define_auto_symbol(Symbol(SymbolType.DataSymbol, 0x4000122, "SIOMULTI1"))
            self.define_auto_symbol(Symbol(SymbolType.DataSymbol, 0x4000124, "SIOMULTI2"))
            self.define_auto_symbol(Symbol(SymbolType.DataSymbol, 0x4000126, "SIOMULTI3"))
            self.define_auto_symbol(Symbol(SymbolType.DataSymbol, 0x4000128, "SIOCNT"))
            self.define_auto_symbol(Symbol(SymbolType.DataSymbol, 0x400012A, "SIOMLT_SEND"))
            self.define_auto_symbol(Symbol(SymbolType.DataSymbol, 0x400012A, "SIODATA8"))
            self.define_auto_symbol(Symbol(SymbolType.DataSymbol, 0x4000130, "KEYINPUT"))
            self.define_auto_symbol(Symbol(SymbolType.DataSymbol, 0x4000132, "KEYCNT"))
            self.define_auto_symbol(Symbol(SymbolType.DataSymbol, 0x4000134, "RCNT"))
            self.define_auto_symbol(Symbol(SymbolType.DataSymbol, 0x4000140, "JOYCNT"))
            self.define_auto_symbol(Symbol(SymbolType.DataSymbol, 0x4000150, "JOY_RECV"))
            self.define_auto_symbol(Symbol(SymbolType.DataSymbol, 0x4000154, "JOY_TRANS"))
            self.define_auto_symbol(Symbol(SymbolType.DataSymbol, 0x4000158, "JOYSTAT"))
            self.define_auto_symbol(Symbol(SymbolType.DataSymbol, 0x4000200, "IE"))
            self.define_auto_symbol(Symbol(SymbolType.DataSymbol, 0x4000202, "IF"))
            self.define_auto_symbol(Symbol(SymbolType.DataSymbol, 0x4000204, "WAITCNT"))
            self.define_auto_symbol(Symbol(SymbolType.DataSymbol, 0x4000208, "IME"))
            self.define_auto_symbol(Symbol(SymbolType.DataSymbol, 0x4000300, "POSTFLG"))
            self.define_auto_symbol(Symbol(SymbolType.DataSymbol, 0x4000301, "HALTCNT"))

            # Entry point
            self.add_entry_point(0x8000000)
            return True
        except:
            log_error(traceback.format_exc())
            return False


def getvals(path):
    lines = open(path, "r").readlines()
    lst = []

    for line in lines:
        line = line.strip()

        if len(line) >= 10:
            addr, cnt = line.split(" ")
            lst.append((int(addr, 16), int(cnt)))

    resmap = {}
    resset = set()

    for addr, cnt in lst:
        resmap[addr] = cnt
        resset.add(addr)
    
    return resset, resmap

highlight_rgb = (0x42, 0xf4, 0x4b)
highlightval = highlight.HighlightColor(red=highlight_rgb[0],
        green=highlight_rgb[1],
        blue=highlight_rgb[2])

def get_markdown_entry(fn):
    addr = "[0x{:08x}](binaryninja://?expr=0x{:08x})".format(fn.start, fn.start)
    name = "[{}](binaryninja://?expr={})".format(fn.name, fn.name)

    return "{} - {}\n".format(addr, name)

def microcov_fnlist(bv):
    path = get_open_filename_input("Select microcov bb dump file")

    if not path or not os.path.exists(path):
        show_message_box("Error", "Could not open cov file", icon=MessageBoxIcon.ErrorIcon)

    values, valuemap = getvals(path)
    validbbs = set()
    results = {}

    for v in values:
        fnlist = bv.get_functions_containing(v)
        bblist = bv.get_basic_blocks_at(v)

        if fnlist:
            fn = fnlist[0]
            
            if bblist:
                curbb = bblist[0]
                curbb.set_user_highlight(highlightval)
                
                # Check to see if we did not land in the middle of a block as a
                # result of a return through bx <reg>
                if v == curbb.start:
                    validbbs.add(v)
                    if fn.start not in results:
                        results[fn.start] = fn, 1
                    else:
                        fn, cnt = results[fn.start]
                        results[fn.start] = fn, cnt+1
    
    # Function hit report
    report = "| *Address* | *BB Count* | Function name |\n"
    report += "|:-----:|:-----:|-----|\n"

    for start in results:
        fn, bbcount = results[start]

        addr = "0x{:08x}".format(fn.start)
        bbcount = "{} / {}".format(bbcount, len(fn.basic_blocks))
        name = "[{}](binaryninja://?expr={})".format(fn.name, fn.name)

        report += "| {} | {} | {} |\n".format(addr, bbcount, name)

    bv.show_markdown_report("Function coverage", report)

    # Block hit report
    report = "| *Address* | *Hitcount* |\n"
    report += "|:-----:|:-----:|\n"

    entrylist = []

    for addr in validbbs:
        entrylist.append((addr, valuemap[addr]))

    entrylist = sorted(entrylist, key=lambda a: a[1])

    for entry in entrylist:
        addr = "[0x{:08x}](binaryninja://?expr=0x{:08x})".format(entry[0], entry[0])
        report += "| {} | {} |\n".format(addr, entry[1])

    bv.show_markdown_report("BB Hits", report)

def microcov_clean(bv):
    path = get_open_filename_input("Select microcov bb dump file")

    if not path or not os.path.exists(path):
        show_message_box("Error", "Could not open cov file", icon=MessageBoxIcon.ErrorIcon)

    values, _ = getvals(path)

    for v in values:
        bbs = bv.get_basic_blocks_at(v)

        if bbs:
            bbs[0].set_user_highlight(HighlightStandardColor.NoHighlightColor)
