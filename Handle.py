import sip
sip.setapi('QVariant',2)
sip.setapi('QString', 2)

from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import *
from PyQt4.QtCore import *

class HandleItem(QGraphicsEllipseItem):
   """ A handle that can be moved by the mouse """
   def __init__(self, parent=None):
      super(HandleItem, self).__init__(QRectF(-4.0,-4.0,8.0,8.0), parent)
      self.posChangeCallbacks = []
      self.setBrush(QtGui.QBrush(Qt.white))
      self.setFlag(self.ItemIsMovable, True)
      self.setFlag(self.ItemSendsScenePositionChanges, True)
      self.setCursor(QtGui.QCursor(Qt.SizeFDiagCursor))

   def itemChange(self, change, value):
      if change == self.ItemPositionChange:
         x, y = value.x(), value.y()
         # TODO: make this a signal?
         # This cannot be a signal because this is not a QObject
         for cb in self.posChangeCallbacks:
            res = cb(x, y)
            if res:
               x, y = res
               value = QPointF(x, y)
         return value
      # Call superclass method:
      return super(HandleItem, self).itemChange(change, value)