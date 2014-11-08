class Observer:
    def __init__(self):
        self.observables = dict()

    def observe(self, name, object):
        self.observables[name] = dict()
        self.observables[name]["object"] = object
        self.observables[name]["properties"] = dict()
        if type(object) is dict:
            properties = object.keys()
        else:
            properties = dir(object)
        for property in properties:
            if property.startswith("__") and property.endswith("__"):
                continue
            if type(object) is dict:
                code = "object['%s']" % property
            else:
                code = "object.%s" % property
            value = eval(code)
            self.observables[name]["properties"][property] = value

    def monitorize(self, name):
        object = self.observables[name]["object"]
        properties = self.observables[name]["properties"].keys()
        for property in properties:
            stored = self.observables[name]["properties"][property]
            if type(object) is dict:
                value = eval("object['%s']" % property)
            else:
                value = eval("object.%s" % property)
            if stored != value:
                print "on object %s property %s has changed from %d to %d" % (name, property, stored, value)

    def has_changed(self, name):
        object = self.observables[name]["object"]
        properties = self.observables[name]["properties"].keys()
        for property in properties:
            stored = self.observables[name]["properties"][property]
            if type(object) is dict:
                value = eval("object['%s']" % property)
            else:
                value = eval("object.%s" % property)
            if stored != value:
                return True

        return False

    def install_observable(self, name, widget):
        self.observables[name] = widget

    def get_observable(self, name):
        return self.observables[name]

if __name__ == "__main__":
    class Object:
        pass

    properties = dict()
    properties["x"] = 0
    properties["y"] = 0
    properties["width"] = 0
    properties["height"] = 0

    object = Object()
    object.x = 0
    object.y = 0
    object.width = 0
    object.height = 0

    observer = Observer()
    observer.observe("properties", properties)
    observer.observe("object", object)

    def print_changes(name):
        if observer.has_changed(name):
            observer.monitorize(name)
        else:
            print "nothing changed in %s" % name

    print_changes("object")
    object.x = 10
    object.y = 10
    object.width = 100
    object.height = 100
    print_changes("object")

    print_changes("properties")
    properties["x"] = 10
    properties["y"] = 10
    properties["width"] = 100
    properties["height"] = 100
    print_changes("properties")