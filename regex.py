# Lightweight shim that exposes a minimal subset of the `regex` API
# Uses stdlib `re` to provide findall functionality used by tests
import re

def findall(pattern, text):
    return re.findall(pattern, text)
