#!/usr/bin/env python
# -*- coding: utf-8 -*-

from paper import Paper

class Page(Paper):
    """This class represents a single document page"""

    __name__ = "Page"

    def __init__(self):
        Paper.__init__(self)

        self.children = list()

    def draw(self, context, hints):
        Paper.draw(self, context)
        for child in sorted(self.children, key=lambda child: child.z):
            child.hints = hints # TODO Not here
            child.draw(context)

    def serialize(self):
        text = "<object type=\"%s\">" % self.__name__
        text += "<children>"
        for child in self.children:
            text += child.serialize()
        text += "</children>"
        text += "</object>"
        return text