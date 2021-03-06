from psd_CodeLines import *

class psd_MemoryRangeMetadata(object):
    """
    This class is encapsulation of meta-data about the different memory ranges.
    """
    def __init__(self, range_name = "", section = None , display = "hexview", is_code = False, psd_code_lines = psd_CodeLines([]), header = None ):
        self._range_name=range_name
        #self.section_name=section_name
        self._section=section
        self._display=display
        self._is_code=is_code
        self._psd_code_lines = psd_code_lines
        self._header = header

    def __str__(self):
        return "range_name:%s" %(self._range_name)

    def get_display(self):
        return self._display

    def set_display(self, display):
        self._display = display

    def get_section(self):
        return self._section

    def set_section(self, section):
        self._section = section

    def get_range_name(self):
        return self._range_name

    def set_range_name(self, str):
        self._range_name = str

    def get_is_code(self):
        return self._is_code

    def set_is_code(self, is_code):
        self._is_code = is_code

    def get_psd_code_lines(self):
        return self._psd_code_lines

    def set_psd_code_lines(self, code_lines):
        self._psd_code_lines = code_lines

    def get_header(self):
        return self._header

    def set_header(self, header):
        self._header = header