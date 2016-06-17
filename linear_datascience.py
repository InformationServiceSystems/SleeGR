"""
Contains code that prepares data to be sent to the
"""

import numpy as np
from scipy.optimize import minimize

def Comp1D(vals, A, B, regr=True, B_next_day=False):
    x, y = [], []
    for i in range(len(vals)):

        vx = (vals[i][A])

        if B_next_day:
            if i + 1 >= len(vals):
                continue;
            vy = (vals[i + 1][B])
        else:
            vy = (vals[i][B])

        if not vx is None and not vy is None:
            x.append(vx)
            y.append(vy)

    x = np.array(x)
    y = np.array(y)

    def ln(x, p):
        return x * p[0] + p[1]

    def obj(p):
        return np.mean((ln(x, p) - y) ** 2)

    p0 = np.array([0, 0])

    sol = minimize(obj, p0)
    p = sol.x

    xlabel = A
    ylabel = B + ", next day" if B_next_day else B
    title = A + ' -> ' + ylabel

    data = x,y
    xmn, xmx = min(x), max(x)
    ymn, ymx = ln(xmn, p), ln(xmx, p)

    # dictionary that can be turned into json
    r = {}

    # plot labels
    r['xlabel'] = xlabel
    r['ylabel'] = ylabel
    r['title'] = title

    # raw data, set of pairs [x,y]
    r['data'] = np.column_stack([x,y]).tolist()

    # points that define the linear function
    r['x0'], r['x1'] = xmn, xmx
    r['y0'], r['y1'] = ymn, ymx

    return r