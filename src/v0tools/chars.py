#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Print / show characters."""
import unicodedata

ASCII_LIST = [
    {"hex": "00", "rep": "^@", "int": 0, "description": "null :: NUL"},
    {"hex": "01", "rep": "^A", "int": 1, "description": "startofheading :: SOH"},
    {"hex": "02", "rep": "^B", "int": 2, "description": "startoftext :: STX"},
    {"hex": "03", "rep": "^C", "int": 3, "description": "endoftext :: EOT"},
    {"hex": "04", "rep": "^D", "int": 4, "description": "endoftransmission :: EOT"},
    {"hex": "05", "rep": "^E", "int": 5, "description": "enquiry :: ENQ"},
    {"hex": "06", "rep": "^F", "int": 6, "description": "acknowledge :: ACK"},
    {"hex": "07", "rep": "^G", "int": 7, "description": "bell :: BEL"},
    {"hex": "08", "rep": "^H", "int": 8, "description": "backspace :: BS"},
    {"hex": "09", "rep": "^I", "int": 9, "description": "horizontaltab :: HT"},
    {"hex": "0A", "rep": "^J", "int": 10, "description": "linefeed,newline :: LF,NL"},
    {"hex": "0B", "rep": "^K", "int": 11, "description": "verticaltab :: VT"},
    {"hex": "0C", "rep": "^L", "int": 12, "description": "formfeed,newpage :: FF,NP"},
    {"hex": "0D", "rep": "^M", "int": 13, "description": "carriagereturn :: CR"},
    {"hex": "0E", "rep": "^N", "int": 14, "description": "shiftout :: SO"},
    {"hex": "0F", "rep": "^O", "int": 15, "description": "shiftin :: SI"},
    {"hex": "10", "rep": "^P", "int": 16, "description": "datalinkescape :: DLE"},
    {"hex": "11", "rep": "^Q", "int": 17, "description": "devicecontrol1 :: DC1"},
    {"hex": "12", "rep": "^R", "int": 18, "description": "devicecontrol2 :: DC2"},
    {"hex": "13", "rep": "^S", "int": 19, "description": "devicecontrol3 :: DC3"},
    {"hex": "14", "rep": "^T", "int": 20, "description": "devicecontrol4 :: DC4"},
    {"hex": "15", "rep": "^U", "int": 21, "description": "negativeacknowledge :: NAK"},
    {"hex": "16", "rep": "^V", "int": 22, "description": "synchonousidle :: SYN"},
    {
        "hex": "17",
        "rep": "^W",
        "int": 23,
        "description": "endoftransmissionblock :: ETB",
    },
    {"hex": "18", "rep": "^X", "int": 24, "description": "cancel :: CAN"},
    {"hex": "19", "rep": "^Y", "int": 25, "description": "endofmedium :: EM"},
    {"hex": "1A", "rep": "^Z", "int": 26, "description": "substitute :: SUB"},
    {"hex": "1B", "rep": "^[", "int": 27, "description": "escape :: ESC"},
    {"hex": "1C", "rep": "^\\", "int": 28, "description": "fileseparator :: FS"},
    {"hex": "1D", "rep": "^]", "int": 29, "description": "groupseparator :: GS"},
    {"hex": "1E", "rep": "^^", "int": 30, "description": "recordseparator :: RS"},
    {"hex": "1F", "rep": "^", "int": 31, "description": "unitseparator :: US"},
    {"hex": "20", "rep": "&sp;", "int": 32, "description": "space :: &sp;"},
    {"hex": "21", "rep": "!", "int": 33, "description": "&excl; :: exclamationmark"},
    {
        "hex": "22",
        "rep": '"',
        "int": 34,
        "description": "&quot; :: doublequotationmark",
    },
    {"hex": "23", "rep": "#", "int": 35, "description": "&num; :: numbersign,pound"},
    {"hex": "24", "rep": "$", "int": 36, "description": "&dollar; :: dollarsign"},
    {"hex": "25", "rep": "%", "int": 37, "description": "&percnt; :: percentsign"},
    {"hex": "26", "rep": "&", "int": 38, "description": "&amp; :: ampersand"},
    {
        "hex": "27",
        "rep": "'",
        "int": 39,
        "description": "&apos; :: apostrophe, single quote",
    },
    {"hex": "28", "rep": "(", "int": 40, "description": "&lpar; :: leftparenthesis"},
    {"hex": "29", "rep": ")", "int": 41, "description": "&rpar; :: rightparenthesis"},
    {"hex": "2A", "rep": "*", "int": 42, "description": "&ast; :: asterisk"},
    {"hex": "2B", "rep": "+", "int": 43, "description": "&plus; :: plussign"},
    {"hex": "2C", "rep": ",", "int": 44, "description": "&comma; :: comma"},
    {
        "hex": "2D",
        "rep": "-",
        "int": 45,
        "description": "&minus;\u00a0&hyphen; :: minussign,hyphen",
    },
    {
        "hex": "2E",
        "rep": ".",
        "int": 46,
        "description": "&period; :: period, decimal point,",
    },
    {
        "hex": "2F",
        "rep": "/",
        "int": 47,
        "description": "&sol; :: slash,virgule,solidus",
    },
    {"hex": "30", "rep": "0", "int": 48, "description": "digit0 :: 0"},
    {"hex": "31", "rep": "1", "int": 49, "description": "digit1 :: 1"},
    {"hex": "32", "rep": "2", "int": 50, "description": "digit2 :: 2"},
    {"hex": "33", "rep": "3", "int": 51, "description": "digit3 :: 3"},
    {"hex": "34", "rep": "4", "int": 52, "description": "digit4 :: 4"},
    {"hex": "35", "rep": "5", "int": 53, "description": "digit5 :: 5"},
    {"hex": "36", "rep": "6", "int": 54, "description": "digit6 :: 6"},
    {"hex": "37", "rep": "7", "int": 55, "description": "digit7 :: 7"},
    {"hex": "38", "rep": "8", "int": 56, "description": "digit8 :: 8"},
    {"hex": "39", "rep": "9", "int": 57, "description": "digit9 :: 9"},
    {"hex": "3A", "rep": ":", "int": 58, "description": "&colon; :: colon"},
    {"hex": "3B", "rep": ";", "int": 59, "description": "&semi; :: semicolon"},
    {"hex": "3C", "rep": "<", "int": 60, "description": "&lt; :: less-thansign"},
    {"hex": "3D", "rep": "=", "int": 61, "description": "&equals; :: equalsign"},
    {"hex": "3E", "rep": ">", "int": 62, "description": "&gt; :: greater-thansign"},
    {"hex": "3F", "rep": "?", "int": 63, "description": "&quest; :: questionmark"},
    {"hex": "40", "rep": "@", "int": 64, "description": "&commat; :: commercialatsign"},
    {"hex": "41", "rep": "A", "int": 65, "description": "capitalA :: A"},
    {"hex": "42", "rep": "B", "int": 66, "description": "capitalB :: B"},
    {"hex": "43", "rep": "C", "int": 67, "description": "capitalC :: C"},
    {"hex": "44", "rep": "D", "int": 68, "description": "capitalD :: D"},
    {"hex": "45", "rep": "E", "int": 69, "description": "capitalE :: E"},
    {"hex": "46", "rep": "F", "int": 70, "description": "capitalF :: F"},
    {"hex": "47", "rep": "G", "int": 71, "description": "capitalG :: G"},
    {"hex": "48", "rep": "H", "int": 72, "description": "capitalH :: H"},
    {"hex": "49", "rep": "I", "int": 73, "description": "capitalI :: I"},
    {"hex": "4A", "rep": "J", "int": 74, "description": "capitalJ :: J"},
    {"hex": "4B", "rep": "K", "int": 75, "description": "capitalK :: K"},
    {"hex": "4C", "rep": "L", "int": 76, "description": "capitalL :: L"},
    {"hex": "4D", "rep": "M", "int": 77, "description": "capitalM :: M"},
    {"hex": "4E", "rep": "N", "int": 78, "description": "capitalN :: N"},
    {"hex": "4F", "rep": "O", "int": 79, "description": "capitalO :: O"},
    {"hex": "50", "rep": "P", "int": 80, "description": "capitalP :: P"},
    {"hex": "51", "rep": "Q", "int": 81, "description": "capitalQ :: Q"},
    {"hex": "52", "rep": "R", "int": 82, "description": "capitalR :: R"},
    {"hex": "53", "rep": "S", "int": 83, "description": "capitalS :: S"},
    {"hex": "54", "rep": "T", "int": 84, "description": "capitalT :: T"},
    {"hex": "55", "rep": "U", "int": 85, "description": "capitalU :: U"},
    {"hex": "56", "rep": "V", "int": 86, "description": "capitalV :: V"},
    {"hex": "57", "rep": "W", "int": 87, "description": "capitalW :: W"},
    {"hex": "58", "rep": "X", "int": 88, "description": "capitalX :: X"},
    {"hex": "59", "rep": "Y", "int": 89, "description": "capitalY :: Y"},
    {"hex": "5A", "rep": "Z", "int": 90, "description": "capitalZ :: Z"},
    {"hex": "5B", "rep": "[", "int": 91, "description": "&lsqb; :: leftsquarebracket"},
    {
        "hex": "5C",
        "rep": "\\",
        "int": 92,
        "description": "&bsol; :: backslash,reversesolidus",
    },
    {"hex": "5D", "rep": "]", "int": 93, "description": "&rsqb; :: rightsquarebracket"},
    {
        "hex": "5E",
        "rep": "^",
        "int": 94,
        "description": "&circ; :: spacingcircumflexaccent",
    },
    {
        "hex": "5F",
        "rep": "&lowbar; \u00a0 &horbar",
        "int": 95,
        "description": "spacing underscore, low :: &lowbar; \u00a0 &horbar",
    },
    {
        "hex": "60",
        "rep": "`",
        "int": 96,
        "description": "&grave; :: spacing grave accent, back",
    },
    {"hex": "61", "rep": "a", "int": 97, "description": "smalla :: a"},
    {"hex": "62", "rep": "b", "int": 98, "description": "smallb :: b"},
    {"hex": "63", "rep": "c", "int": 99, "description": "smallc :: c"},
    {"hex": "64", "rep": "d", "int": 100, "description": "smalld :: d"},
    {"hex": "65", "rep": "e", "int": 101, "description": "smalle :: e"},
    {"hex": "66", "rep": "f", "int": 102, "description": "smallf :: f"},
    {"hex": "67", "rep": "g", "int": 103, "description": "smallg :: g"},
    {"hex": "68", "rep": "h", "int": 104, "description": "smallh :: h"},
    {"hex": "69", "rep": "i", "int": 105, "description": "smalli :: i"},
    {"hex": "6A", "rep": "j", "int": 106, "description": "smallj :: j"},
    {"hex": "6B", "rep": "k", "int": 107, "description": "smallk :: k"},
    {"hex": "6C", "rep": "l", "int": 108, "description": "smalll :: l"},
    {"hex": "6D", "rep": "m", "int": 109, "description": "smallm :: m"},
    {"hex": "6E", "rep": "n", "int": 110, "description": "smalln :: n"},
    {"hex": "6F", "rep": "o", "int": 111, "description": "smallo :: o"},
    {"hex": "70", "rep": "p", "int": 112, "description": "smallp :: p"},
    {"hex": "71", "rep": "q", "int": 113, "description": "smallq :: q"},
    {"hex": "72", "rep": "r", "int": 114, "description": "smallr :: r"},
    {"hex": "73", "rep": "s", "int": 115, "description": "smalls :: s"},
    {"hex": "74", "rep": "t", "int": 116, "description": "smallt :: t"},
    {"hex": "75", "rep": "u", "int": 117, "description": "smallu :: u"},
    {"hex": "76", "rep": "v", "int": 118, "description": "smallv :: v"},
    {"hex": "77", "rep": "w", "int": 119, "description": "smallw :: w"},
    {"hex": "78", "rep": "x", "int": 120, "description": "smallx :: x"},
    {"hex": "79", "rep": "y", "int": 121, "description": "smally :: y"},
    {"hex": "7A", "rep": "z", "int": 122, "description": "smallz :: z"},
    {
        "hex": "7B",
        "rep": "{",
        "int": 123,
        "description": "&lcub; :: left brace, left curly",
    },
    {
        "hex": "7C",
        "rep": "&verbar;",
        "int": 124,
        "description": "verticalbar :: &verbar;",
    },
    {
        "hex": "7D",
        "rep": "}",
        "int": 125,
        "description": "&rcub; :: right brace, right curly",
    },
    {"hex": "7E", "rep": "~", "int": 126, "description": "&tilde; :: tildeaccent"},
    {"hex": "7F", "rep": "^?", "int": 127, "description": "delete :: DEL"},
]
"""Fill in ASCII description values for Unicode names."""

ASCII_MAP = {i["int"]: i for i in ASCII_LIST}
"""Dictionary Map of ASCII_LIST."""


def unicodes() -> dict:
    """yield all Unicode values.

    returns iterator of dictionaries in the following format::
        {
            "int": i,
            "hex": hval,
            "chr": char,
            "name": name.lower(),
            "pref": pref,
            "htmlent": htmlent
        }

    example for letter "a"::
        {
            "int": 97,
            "hex": "61",
            "chr": "a",
            "name": "latin small letter a",
            "pref": "\\\\u0061",
            "htmlent": "&#97;"
        }
    """
    for i in range(0x10FFFF):
        try:
            name = unicodedata.name(chr(i))
        except ValueError:
            name = ""
        if not name and i in ASCII_MAP:
            name = ASCII_MAP[i]["description"]
        if not name:
            continue
        char = chr(i)
        hval = str(hex(i)).replace("0x", "")
        if i < 0xFFFF:
            pref = f"\\u{hval.zfill(4)}"
        else:
            pref = f"\\U{hval.zfill(8)}"

        htmlent = f"&#{i};"
        try:
            yield {
                "int": i,
                "hex": hval,
                "chr": char,
                "name": name.lower(),
                "pref": pref,
                "htmlent": htmlent,
            }
        except UnicodeEncodeError:
            pass
