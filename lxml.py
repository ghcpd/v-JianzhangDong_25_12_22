# Minimal lxml.etree shim implemented using stdlib xml.etree.ElementTree
import xml.etree.ElementTree as ET

class _etree:
    @staticmethod
    def fromstring(s):
        return ET.fromstring(s)

etree = _etree()
