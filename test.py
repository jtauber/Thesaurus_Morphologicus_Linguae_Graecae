#!/usr/bin/env python3

from unicodedata import normalize
from xml.etree import ElementTree

VARIA = GRAVE = "\u0300"
OXIA = ACUTE = "\u0301"
MACRON = LONG = "\u0304"
BREVE = SHORT = "\u0306"
DIAERESIS = "\u0308"
PSILI = SMOOTH = "\u0313"
DASIA = ROUGH = "\u0314"
PERISPOMENI = CIRCUMFLEX = "\u0342"
YPOGEGRAMMENI = IOTA_SUBSCRIPT = "\u0345"


def remove_diacritic(*diacritics):
    def _(text):
        return normalize("NFC", "".join(
            ch
            for ch in normalize("NFD", text)
            if ch not in diacritics)
        )
    return _


strip1 = remove_diacritic(MACRON, BREVE, DIAERESIS)
strip2 = remove_diacritic(MACRON, BREVE, DIAERESIS, GRAVE, ACUTE, CIRCUMFLEX)


def test(filename):
    tree = ElementTree.parse(filename)
    root = tree.getroot()

    for word in root.findall("l"):
        assert word.attrib.keys() == {
            "id", "key", "key2", "gnt", "gnd", "dcl", "bse", "end"
        }

        lsj_id = word.attrib["id"]  # noqa
        lsj_key = word.attrib["key"]
        lsj_key2 = word.attrib["key2"]
        gnt = word.attrib["gnt"]
        gnd = word.attrib["gnd"]
        dcl = word.attrib["dcl"]
        bse = word.attrib["bse"]
        end = word.attrib["end"]

        assert lsj_key2 == strip1(lsj_key)

        assert dcl in {"1", "2"}

        if dcl == "1":
            assert bse + strip2(end) == strip2(lsj_key)
            assert (gnd, end, gnt) in {
                ("ἡ", "α", "ας"),
                ("ἡ", "ά", "ᾶς"),
                ("ἡ", "ᾶ", "ᾶς"),
                ("ἡ", "α", "ης"),
                ("ἡ", "η", "ης"),
                ("ἡ", "ή", "ῆς"),
                ("ἡ", "ῆ", "ῆς"),
                ("ὁ", "α", "ας"),
                ("ὁ", "ας", "ου"),
                ("ὁ", "ᾶς", "οῦ"),
                ("ὁ", "ης", "ου"),
                ("ὁ", "ής", "οῦ"),
                ("ὁ", "ῆς", "οῦ"),
                ("τά", "α", "ας"),
                ("τά", "α", "ης"),
            }
        elif dcl == "2":
            assert bse + strip2(end) == strip2(lsj_key)
            assert (gnd, end, gnt) in {
                ("ἡ", "ός", "ᾶς"),
                ("ἡ", "ος", "ου"),
                ("ἡ", "ός", "οῦ"),
                ("ὁ", "εώς", "εώ"),
                ("ὁ", "ος", "ου"),
                ("ὁ", "ός", "οῦ"),
                ("ὁ", "ους", "οῦ"),
                ("ὁ", "οῦς", "ου"),
                ("τά", "ος", "ου"),
                ("τό", "ον", "ου"),
                ("τό", "ος", "ου"),
                ("τό", "οῦν", "οῦ"),
            }


if __name__ == "__main__":
    test("1st_declension.xml")
    test("2nd_declension.xml")
