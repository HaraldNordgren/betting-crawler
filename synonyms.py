#!/usr/bin/env python3

class synonyms:

    def get_synonym(self, string):

        if string not in self.synonym_list:
            return string
        
        return self.synonym_list[string]
