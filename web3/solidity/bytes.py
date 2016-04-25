import solidity.formatters as f
import solidity.types as types
import re


class SolidityTypeBytes(types.SolidityType):

    def __init__(self):
        self._inputFormatter = f.formatInputBytes
        self._outputFormatter = f.formatOutputBytes

    @classmethod
    def isType(self, name):
        return re.match(r"^bytes([0-9]{1,})(\[([0-9]*)\])*$", name) is not None

    @classmethod
    def staticPartLength(self, name):
        matches = re.findall(r"^bytes([0-9]*)")
        size = int(matches[1])
        return size * self.staticArrayLength(name)
