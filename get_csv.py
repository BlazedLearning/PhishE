#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pymisp import ExpandedPyMISP
from keys import misp_url, misp_key, misp_verifycert
import Configuration

class Getter:
    def __init__(self, Controller = 'attributes', Event_id = None, Attribute = None, Object_attribute = None, Misp_types = None, context = False, outfile = Configuration.MISP_outfile()):
        # description: 'Get MISP stuff as CSV.'
        # controller", default='attributes', help="Attribute to use for the search (events, objects, attributes)")
        # event_id", help="Event ID to fetch. Without it, it will fetch the whole database.")
        # attribute", nargs='+', help="Attribute column names")
        # object_attribute", nargs='+', help="Object attribute column names")
        # misp_types", nargs='+', help="MISP types to fetch (ip-src, hostname, ...)")
        # context", action='store_true', help="Add event level context (tags...)")
        # outfile", help="Output file to write the CSV.")

        self.Controller = Controller
        self.Event_id = Event_id
        self.Attribute = Attribute
        self.Object_attribute = Object_attribute
        self.Misp_types = Misp_types
        self.context = context
        self.outfile = outfile

    def Get(self):
        pymisp = ExpandedPyMISP(misp_url, misp_key, misp_verifycert, debug=True)
        attr = []

        if self.Attribute != None:
            attr.append(self.Attribute)
        if self.Object_attribute != None:
            attr.append(self.Object_attribute)
        if not attr:
            attr = None

        response = pymisp.search(return_format='csv', controller=self.Controller, eventid=self.Event_id, requested_attributes=attr,
                                 type_attribute=self.Misp_types, include_context=self.context)


        with open(self.outfile, 'w') as f:
            f.write(response)
