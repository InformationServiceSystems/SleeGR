"""
Contains code that prepares data to be sent to the
"""
from typing import Dict, List
import numpy as np
import re
from scipy.optimize import minimize
from datawrapper.correl_wrapper import CorrelWrapper

import inspect

def isprop(v):
  return isinstance(v, property)

def Comp1D(vals: List[Dict], x_label: str, y_label: str, regr=True, B_next_day=False) -> Dict:

    field_names = {
        'Day of week': CorrelWrapper.day_of_week,
        'Sleep length' : CorrelWrapper.sleep_length,
        'Load': CorrelWrapper.load,
        'Sleep start': CorrelWrapper.sleep_start,
        'Sleep end': CorrelWrapper.sleep_end,
        'Deep sleep': CorrelWrapper.deep_sleep,
        'Activity A': CorrelWrapper.activity_a,
        'Activity G': CorrelWrapper.activity_g,
        'RPE': CorrelWrapper.rpe,
        'DALDA': CorrelWrapper.dalda}

    x_label_method = field_names[x_label]
    y_label_method = field_names[y_label]
    x, y = [], []
    for i in range(len(vals)):

        #vx = (vals[i][x_label])
        vx = x_label_method(vals[i])
        if B_next_day:
            if i + 1 >= len(vals):
                continue;
            #vy = (vals[i + 1][y_label])
            vy = y_label_method(vals[i + 1])
        else:
            vy = y_label_method(vals[i])

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

    xlabel = x_label
    ylabel = y_label + ", next day" if B_next_day else y_label
    title = x_label + ' -> ' + ylabel

    if not (any(x) and any(y)):
        return None
    data = x, y

    xmn, xmx = min(x), max(x)
    ymn, ymx = ln(xmn, p), ln(xmx, p)

    # dictionary that can be turned into json
    r = {}

    # plot labels
    r['xlabel'] = xlabel
    r['ylabel'] = ylabel
    r['title'] = title

    # raw data, set of pairs [x,y]
    r['data'] = np.column_stack([x, y]).tolist()

    # points that define the linear function
    r['x0'], r['x1'] = xmn, xmx
    r['y0'], r['y1'] = ymn, ymx

    return r
