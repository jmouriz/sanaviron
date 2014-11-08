#!/usr/bin/env python
# -*- coding: utf-8 -*-
#!/usr/bin/python

import threading


class ResultCatcher:
    def __init__(self, f):
        self.f = f
        self.val = None

    def __call__(self, *args, **kwargs):
        self.val = self.f(*args, **kwargs)


def run_in_thread(f):
    def run(*arg, **kwargs):
        retVal = ResultCatcher(f)
        t = threading.Thread(target=retVal, args=arg, kwargs=kwargs)
        t.daemon = True
        t.start()
        t.join()
        return retVal.val

    run.__name__ = f.__name__
    return run
