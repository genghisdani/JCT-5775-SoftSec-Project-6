import math
from psd_visualizer.psd_View import psd_View
from psd_helpers.psd_Helpers import *

__author__ = 'Noam'


class psd_CodeView(psd_View):
    def __init__(self, pe, memory_range):
        super(psd_CodeView, self).__init__(pe, memory_range)
        self._psd_code_lines = memory_range.get_memory_range_metadata().get_psd_code_lines()

    def calculate_line_count(self):
        if not self._psd_code_lines:
            return 0
        else:
            return len(self._psd_code_lines.get_clines())

    def get_html_line_list(self, line_range_tup):
        (line_start, line_end) = line_range_tup

        html_lines = []
        code_lines = self._psd_code_lines.get_clines()
        for l_idx in range(line_start, line_end):
            line = code_lines[l_idx]
            line_str = self.html_line(line)
            html_lines.append(line_str)

        return html_lines

    def html_line(self, line):
        str_rowheader = self.html_rowheader(self._memory_range_metadata.get_range_name(), line.address)
        str_opcode = self.html_opcode(line)
        str_mnemonic = self.html_mnemonic(line.mnemonic)
        str_operands = self.html_operands(line)

        return str_rowheader + str_opcode + str_mnemonic + str_operands

    def html_rowheader(self, rangename, address):
        return "<span class=\"codeview-row-header\"><div class=\"bookmark-button\" style=\"float: left; visibility: hidden;\"><span class=\"glyphicon glyphicon-bookmark\" aria-hidden=\"true\"></span></div>{0: >20} <span class=\"header-address\">0x{1:08x}</span>:</span>".format(rangename, address)

    def html_opcode(self, line):
        max_padding = 30 # 15*3-1 # max bytes in x86 is 15. we don't use this because it not nice in the view
        opcode_str = ""

        for i, byte in enumerate(line.bytes):
            opcode_str += self.html_bytedata(line.address+i, byte)

        padding_str = " " * max(max_padding - (line.size*3), 0)
        #print opcode_str
        return ("<span class=\"codeview-opcode spaceafter\">{0}{1}</span>").format(opcode_str, padding_str)

    def html_bytedata(self, rva_address, byte, specialclass=""):
        return "<span data-address-rva=\"{0:08x}\" class=\"datahex-byte-data spaceafter {1:s}\">{2:02x}</span>".format(rva_address, specialclass, byte)

    def html_mnemonic(self, mnemonic):
        return "<span class=\"codeview-mnemonic spaceafter\">{0: <5}</span>".format(mnemonic)

    def html_operands(self, line):
        op_str = line.op_str
        if op_str == "":
            return ""

        c_html_str=[]
        #1. get constants
        constants = get_constants(line)
        if len(constants) > 0:
            #2. split constants from operand string
            constants.sort(reverse=True) # we sort, just in a case that the smaller is a substring of to bigger.
            for i, c in enumerate(constants):
                c_str = hex(c) if c > 0xf else str(c)

                #3. add jump to constants that can be and va or rva
                c_jump_address = None
                if self._pe.get_section_by_rva(c) is not None: #it can be RVA
                    c_jump_address = hex(c)
                elif (c - self._pe.OPTIONAL_HEADER.ImageBase) > 0: #it can be VA
                    rva = c - self._pe.OPTIONAL_HEADER.ImageBase
                    if self._pe.get_section_by_rva(rva) is not None:
                        c_jump_address = hex(rva)

                #4. replace the constants with a place
                c_html_str.append(self.constant_html(c_str, c_jump_address))
                #the str(i+ord('a')) thing is a workaround for substring wrong substitution in case where
                #the second number is 0/1/2
                op_str = op_str.replace(c_str, "{"+chr(i+ord('a'))+"}", 1)


            #changing back to numbers
            for i in range(4):
                op_str = op_str.replace("{"+chr(i+ord('a'))+"}", "{"+str(i)+"}", 1)

            #inject the html constants representation
            op_str = op_str.format(*c_html_str)

        #print ("<span class=\"codeview-param\">{0}</span>").format(op_str)
        return ("<span class=\"codeview-param\">{0}</span>").format(op_str)

    def constant_html(self, constant_str, c_jump_address=None):
        class_str = "constant"
        jump_str = ""
        if c_jump_address is not None:
            class_str += " jump"
            jump_str = " data-jump-location=\""+c_jump_address+"\""
        #print ("<span class=\"{0}\""+jump_str+">{1}</span>").format(class_str, constant_str)
        return ("<span class=\"{0}\""+jump_str+">{1}</span>").format(class_str, constant_str)

    def find_line_by_address(self, address):
        code_lines = self._psd_code_lines.get_clines()
        for id, l in enumerate(code_lines):
            address_start = l.address
            address_end = address_start + (l.size - 1)
            #print "id:",id,"start:",hex(address_start),"end:",hex(address_end),"address:",hex(address)
            if address in range(address_start, address_end + 1):
                return id

        return None