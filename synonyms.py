#!/usr/bin/env python3

import re

class synonyms:

    def __init__(self):

        list_from   = "ŞüÉéçčňİış"
        list_to     = "SuEeccnIis"

        self.trans_list = str.maketrans(list_from, list_to)

        self.characters_to_remove = ["'", "."]
        self.replace_by_whitespace = ["-"]

        self.prefixes = [
                ('AA '          , ''),
                ('AC '          , ''),
                ('AD '          , ''),
                ('ADO '         , ''),
                ('AFC '         , ''),
                ('BK '          , ''),
                ('CFR '         , ''),
                ('CSU '         , ''),
                ('Borussia '    , ''),
                ('FBC '         , ''),
                ('FC '          , ''),
                ('FCB '         , ''),
                ('FCM '         , ''),
                ('FK '          , ''),
                ('FSV '         , ''),
                ('GIF '         , ''),
                ('IF '          , ''),
                ('IFK '         , ''),
                ('IK '          , ''),
                ('HNK '         , ''),
                ('KAA '         , ''),
                ('NK '          , ''),
                ('PAOK '        , ''),
                ('PAS '         , ''),
                ('PEC '         , ''),
                ('RNK '         , ''),
                ('RC '          , ''),
                ('RJ '          , ''),
                ('SC '          , ''),
                ('SG '          , ''),
                ('SK '          , ''),
                ('TSG '         , ''),
                ('VfB '         , ''),
                ('VfL '         , ''),
                ('VfR '         , '')]

        self.suffixes = [
                ('s BK'         , ''),
                ('s BoIS'       , ''),
                ('s IF'         , ''),
                ('s FF'         , ''),
                ('s FK'         , ''),
                (' AC'          , ''),
                (' AD'          , ''),
                (' Am'          , ''),
                (' AS'          , ''),
                (' BoIS'        , ''),
                (' BK'          , ''),
                (' CD'          , ''),
                (' IF'          , ''),
                (' IS'          , ''),
                (' FF'          , ''),
                (' FK'          , ''),
                (' FC'          , ''),
                (' Fören'       , ''),
                (' JC'          , ''),
                (' SK'          , ''),
                (' United'      , ' U'),
                (' Utd'         , ' U'),
                (' Unidos'      , ' U')]

    def sanitize_characters(self, string):

        for char in self.characters_to_remove:
            string = string.replace(char, "")

        for char in self.replace_by_whitespace:
            string = string.replace(char, " ")

        return string.translate(self.trans_list)

    def sanitize_ixes(self, string):

        for (old, new) in self.prefixes:
            string = re.sub("^" + old, new, string)
        
        for (old, new) in self.suffixes:
            string = re.sub(old + "$", new, string)

        return string

    def get_synonym(self, string):

        string = self.sanitize_characters(string)

        if string in self.synonym_list:
            string = self.synonym_list[string]

        return self.sanitize_ixes(string)
