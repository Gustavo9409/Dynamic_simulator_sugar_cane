"""
Render to qt from agg
"""
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import six

import os  # not used
import sys
import ctypes
import warnings
directory=str(os.getcwd())
sys.path.insert(0, directory)

import matplotlib
from matplotlib.figure import Figure


from matplotlib.backends.backend_qt5agg import FigureCanvasQTAggBase as _FigureCanvasQTAggBase

from matplotlib.backends.backend_agg import FigureCanvasAgg
from backend_qt4_DynamicSim import QtCore
from backend_qt4_DynamicSim import FigureManagerQT
from backend_qt4_DynamicSim import FigureCanvasQT
from backend_qt4_DynamicSim import NavigationToolbar2QT
##### not used
from backend_qt4_DynamicSim import show
from backend_qt4_DynamicSim import draw_if_interactive
from backend_qt4_DynamicSim import backend_version
######

DEBUG = False

_decref = ctypes.pythonapi.Py_DecRef
_decref.argtypes = [ctypes.py_object]
_decref.restype = None


def new_figure_manager(num, *args, **kwargs):
    """
    Create a new figure manager instance
    """
    if DEBUG:
        print('backend_qt4agg.new_figure_manager')
    FigureClass = kwargs.pop('FigureClass', Figure)
    thisFig = FigureClass(*args, **kwargs)
    return new_figure_manager_given_figure(num, thisFig)


def new_figure_manager_given_figure(num, figure):
    """
    Create a new figure manager instance for the given figure.
    """
    canvas = FigureCanvasQTAgg(figure)
    return FigureManagerQT(canvas, num)


class FigureCanvasQTAggBase(_FigureCanvasQTAggBase):
    def __init__(self, figure):
        self._agg_draw_pending = False


class FigureCanvasQTAgg(FigureCanvasQTAggBase,
                        FigureCanvasQT, FigureCanvasAgg):
    """
    The canvas the figure renders into.  Calls the draw and print fig
    methods, creates the renderers, etc...

    Public attribute

      figure - A Figure instance
   """

    def __init__(self, figure):
        if DEBUG:
            print('FigureCanvasQtAgg: ', figure)
        FigureCanvasQT.__init__(self, figure)
        FigureCanvasQTAggBase.__init__(self, figure)
        FigureCanvasAgg.__init__(self, figure)
        self._drawRect = None
        self.blitbox = []
        self.setAttribute(QtCore.Qt.WA_OpaquePaintEvent)


FigureCanvas = FigureCanvasQTAgg
FigureManager = FigureManagerQT
