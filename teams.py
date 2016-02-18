#!/usr/bin/env python3

from synonyms import synonyms

class teams(synonyms):

    def __init__(self):

        super().__init__()

        self.synonym_list = {
            'Ajaccio GFCO'          : 'Ajaccio',
            'Blackburn Rovers'      : 'Blackburn',
            'Bradford City'         : 'Bradford',
            'Brighton & Hove Albion': 'Brighton',
            'Cambridge United'      : 'Cambridge',
            'Cardiff City'          : 'Cardiff',
            'Colchester United'     : 'Colchester',
            'Dag & Redbridge'       : 'Dag & Red',
            'Degerfors IF'          : 'Degerfors',
            'Dynamo Kyiv'           : 'Dynamo Kiev',
            'Forest Green Rovers'   : 'Forest Green',
            'IK Sirius FK'          : 'Sirius',
            'Kidderminster Harriers': 'Kidderminster',
            'Leicester City'        : 'Leicester',
            'Lincoln City'          : 'Lincoln',
            'Milton Keynes Dons'    : 'Milton Keynes',
            'Norwich City'          : 'Norwich',
            'Oldham Athletic'       : 'Oldham',
            'Olympiakos Piraeus'    : 'Olympiakos',
            'Peterborough United'   : 'Peterborough',
            'Plymouth Argyle'       : 'Plymouth',
            'Preston North End'     : 'Preston',
            'Queens Park Rangers FC': 'QPR',
            'Queens Park Rangers'   : 'QPR',
            'Rotherham United'      : 'Rotherham',
            'Sheffield Wednesday'   : 'Sheffield Wed',
            'Sirius FK'             : 'Sirius',
            'Stoke City'            : 'Stoke',
            'Swansea City'          : 'Swansea',
            'Tottenham Hotspur'     : 'Tottenham',
            'Torquay United'        : 'Torquay',
            'Varbergs BoIS FC'      : 'Varberg',
            'West Bromwich'         : 'West Brom',
            'Zenit St Petersburg'   : 'Zenit',
            'Zenit StPetersburg'    : 'Zenit',
            'York City'             : 'York'}
