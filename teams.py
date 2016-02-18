#!/usr/bin/env python3

from synonyms import synonyms

class teams(synonyms):

    def __init__(self):

        super().__init__()

        self.synonym_list = {
            'Blackburn Rovers'      : 'Blackburn',
            'Degerfors FF'          : 'Degerfors',
            'Dynamo Kyiv'           : 'Dynamo Kiev',
            'Ajaccio GFCO'          : 'Ajaccio',
            'Leicester City'        : 'Leicester',
            'Lincoln City'          : 'Lincoln',
            'Milton Keynes Dons'    : 'Milton Keynes',
            'Norwich City'          : 'Norwich',
            'Olympiakos Piraeus'    : 'Olympiakos',
            'Stoke City'            : 'Stoke',
            'Swansea City'          : 'Swansea',
            'Tottenham Hotspur'     : 'Tottenham',
            'West Bromwich'         : 'West Brom',
            'Zenit St Petersburg'   : 'Zenit',
            'Fleetwood Town'        : 'Fleetwood',
            'Huddersfield Town'     : 'Huddersfield',
            'Mansfield Town'        : 'Mansfield',
            'Macclesfield Town'     : 'Macclesfield',
            'Queens Park Rangers FC': 'QPR',
            'Queens Park Rangers'   : 'QPR',
            'Northampton Town'      : 'Northampton'}
