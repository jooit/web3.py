from utils import utils, config
from solidity.param import SolidityParam
from math import floor


def formatInputInt(value):
    if isinstance(value, tuple):
        value = value[0]
    result = utils.padLeft(hex(int(value))[2:], 64)  # utils.toTwosComplement
    return SolidityParam(result)


def formatInputBytes(value):
    result = utils.toHex(value)[2:]
    l = floor(float(len(result) + 63) / 64)
    result = utils.padRight(result, l * 64)
    return SolidityParam(result)


def formatInputDynamicBytes(value):
    result = utils.toHex(value)[2:]
    length = len(result) / 2
    l = floor(float(len(result) + 63) / 64)
    result = utils.padRight(result, l * 64)
    return SolidityParam(formatInputInt(length).value + result)


def formatInputString(value):
    result = utils.fromUtf8(value)[2:]
    length = len(result) / 2
    l = floor(float(len(result) + 63) / 64)
    result = utils.padRight(result, l * 64)
    return SolidityParam(formatInputInt(length).value + result)


def formatInputBool(value):
    result = "0" * 63 + ("1" if value else "0")
    return SolidityParam(result)


def formatInputReal(value):
    return formatInputInt(value * 2 ** 128)


def formatOutputInt(param):
    value = param.staticPart()
    if not value:
        value = "0"

    # if value < 0:
    #    return int(value, 16) - int("f" * 64, 16) + 1

    return int(value, 16)


def formatOutputUInt(param):
    value = param.staticPart()
    if not value:
        value = "0"
    return int(value, 16)


def formatOutputReal(param):
    return formatOutputInt(param) / 2 ** 128


def formatOutputUReal(param):
    return formatOutputInt(param) / 2 ** 128


def formatOutputBool(param):
    if param.staticPart() == "0" * 63 + "1":
        return True
    else:
        return False


def formatOutputBytes(param):
    return "0x" + param.staticPart()


def formatOutputDynamicBytes(param):
    length = int(param.dynamicPart()[:64], 16) * 2
    return "0x" + param.dynamicPart()[64:64 + length]


def formatOutputString(param):
    length = int(param.dynamicPart()[:64], 16) * 2
    return utils.toUtf8(param.dynamicPart()[64:64 + length])


def formatOutputAddress(param):
    value = param.staticPart()
    return "0x" + value[len(value) - 40:]
