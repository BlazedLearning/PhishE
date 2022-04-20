#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pymisp import PyMISP
from pymisp import ExpandedPyMISP
from pymisp import MISPAttribute
from keys import misp_url, misp_key, misp_verifycert

class Pusher:
    def __init__(self, Type, Value, Category, Comment, EventId):
        self.Type = Type
        self.Value = Value
        self.Category = Category
        self.Comment = Comment
        self.EventId = EventId

        self.attribute = MISPAttribute()
        self.attribute.type = self.Type
        self.attribute.value = self.Value
        self.attribute.category = self.Category
        self.attribute.comment = self.Comment

    def create_attribute(self):
        misp = ExpandedPyMISP(misp_url, misp_key, misp_verifycert, debug=True)
        misp.add_attribute(self.EventId, self.attribute, pythonify=False)
