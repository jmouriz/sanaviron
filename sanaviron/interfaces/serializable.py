#!/usr/bin/python
# -*- coding: utf-8 -*-

AUTOMATIC = "AUTOMATIC"

def bool(value):
    return eval("%s" % str(value))

class Property(dict):
    """This class represents a single typed and XML representable/serializable property"""

    def __init__(self, name, value, type=AUTOMATIC):
        dict.__init__(self)
        self.name = name
        self.type = type
        if type == AUTOMATIC:
            self.type = self.get_type_from_value(value)
            self.value = value
        elif type == "list":
            self.value = eval('%s(%s)' % (type, value))
        elif type.startswith("objects."):
            module = str(type).split('.')
            location = '.'.join(module[0:2])
            object = module[-1]
            import objects
            self.value = eval('%s.%s(string="%s")' % (location, object, value))
        else:
            self.value = eval('%s("%s")' % (type, value))

    def get_type_from_value(self, value):
        return str(type(value)).split("'")[1]

    def get_value(self):
        return self.value

    def serialize(self):
        return "<property name=\"%s\" type=\"%s\" value=\"%s\"/>" % (self.name, self.type, self.value)

class Properties(dict):
    """This class represents a collection of properties"""

    def __init__(self):
        dict.__init__(self)

    def set_property(self, property):
        self[property.name] = property

    def get_property(self, name):
        return self[name].get_value()

    def serialize(self):
        representation = ""
        for property in self.values():
            representation += "%s" % property.serialize()
        return representation

class Holder(object):
    """This class represents a object properties container"""

    def __init__(self):
        self.properties = Properties()

    def __str__(self):
        return self.serialize()

    def __repr__(self):
        return self.serialize()

    def __setattr__(self, name, value):
        if name in self.get_properties():
            self.set_property(name, value)
        else:
            super(Holder, self).__setattr__(name, value)

    def __getattr__(self, name):
        if name in self.get_properties():
            return self.get_property(name)
        try:
            value = super(Holder, self).__getattr__(name)
        except:
            raise AttributeError
        return value

    def get_properties(self):
        return []

    def set_property(self, name, value, type=AUTOMATIC):
        self.properties.set_property(Property(name, value, type))

    def get_property(self, name):
        return self.properties.get_property(name)

class Serializable(Holder):
    """This class represents a object which can be serialized"""

    def __init__(self):
        Holder.__init__(self)

    def serialize(self):
        representation = "<object type=\"%s\">" % self.__name__
        representation += self.properties.serialize()
        representation += "</object>"
        return representation

    def unserialize(self):
        pass
