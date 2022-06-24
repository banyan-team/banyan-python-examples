"""
All code in this file (stockflow.py) was taken from https://github.com/jdherman/stockflow
and is licensed under the MIT license.

Copyright (c) 2014 Jon Herman

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation
files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy,
modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software
is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR
IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

import numpy as np
from scipy.integrate import odeint


class simulation:
    def __init__(self, t):
        self.t = t
        self.ix = {}
        self.flows = {}
        self.current = []
        self.done = False
        self.results = None

    def __getattr__(self, key):
        if not self.done:
            return self.current[self.ix[key]]
        else:
            return self.results[:, self.ix[key]]

    def __validate_key(self, key):
        if key in self.ix:
            raise NameError("Variable " + key + " already defined.")

    def __new_state_var(self, key, IC):
        self.__validate_key(key)
        self.current.append(IC)
        self.ix[key] = len(self.current) - 1

    def stocks(self, icdict):
        for k, v in icdict.items():
            self.__new_state_var(k, v)

    def flow(self, key, f, start=None, end=None):
        self.__new_state_var(key, f(0))
        s = self.ix[start] if start is not None else None
        e = self.ix[end] if end is not None else None
        self.flows[key] = {"f": f, "start": s, "end": e}

    def xdot(self, y, t):
        self.current = y
        d = np.zeros((len(y),))
        for (
            k,
            f,
        ) in self.flows.items():  # calculate flows only once. distribute to stocks.
            i = self.ix[k]
            ft = f["f"](t)
            d[i] = ft - self.current[i]
            if f["start"] is not None:
                d[f["start"]] -= ft
            if f["end"] is not None:
                d[f["end"]] += ft
        return d

    def run(self, discrete=False):
        self.done = False
        if not discrete:
            self.results = odeint(self.xdot, self.current, self.t)
        else:
            self.results = np.zeros((len(self.t), len(self.current)))
            self.results[0, :] = self.current
            for i in np.arange(1, len(self.t)):
                self.results[i, :] = self.results[i - 1, :] + self.xdot(
                    self.results[i - 1, :], self.t[i]
                )
        self.done = True
        self.current = self.results[0, :]  # restore initial conditions
