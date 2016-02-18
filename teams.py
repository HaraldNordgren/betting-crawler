#!/usr/bin/env python3

from synonyms import synonyms

class teams(synonyms):

    def __init__(self):

        super().__init__()

        self.synonym_list = {
            'Tottenham Hotspur'     : 'Tottenham',
            'West Bromwich'         : 'West Brom',
            'Leicester City'        : 'Leicester',
            'Swansea City'          : 'Swansea',
            'Norwich City'          : 'Norwich',
            'Zenit St Petersburg'   : 'Zenit',
            'Olympiakos Piraeus'    : 'Olympiakos'}
