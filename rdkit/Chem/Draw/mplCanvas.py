# $Id$
#
#  Copyright (C) 2008 Greg Landrum
#
#   @@ All Rights Reserved @@
#  This file is part of the RDKit.
#  The contents are covered by the terms of the BSD license
#  which is included in the file license.txt, found at the root
#  of the RDKit source tree.
#
from matplotlib.lines import Line2D
from matplotlib.patches import Polygon
from matplotlib.axes import Axes
from matplotlib.pyplot import figure
import numpy

from canvasbase import CanvasBase
class Canvas(CanvasBase):
  def __init__(self, size, name='', imageType='png'):
    self._name = name
    self.size=size
    dpi = max(size[0],size[1])
    figsize=(int(float(size[0])/dpi),int(float(size[1])/dpi))
    self._figure = figure(figsize=figsize)
    self._axes = self._figure.add_axes([0,0,2.5,2.5])
    self._axes.set_xticklabels('')
    self._axes.set_yticklabels('')
    self._dpi = dpi


  def rescalePt(self,p1):
    return [float(p1[0])/self._dpi,float(self.size[1]-p1[1])/self._dpi]
  
  def addCanvasLine(self,p1,p2,color=(0,0,0),color2=None,**kwargs):
    canvas = self._axes
    p1 = self.rescalePt(p1)
    p2 = self.rescalePt(p2)
    if color2 and color2!=color:
      mp = (p1[0]+p2[0])/2.,(p1[1]+p2[1])/2.
      canvas.add_line(Line2D((p1[0],mp[0]),(p1[1],mp[1]),
                             color=color,**kwargs))
      canvas.add_line(Line2D((mp[0],p2[0]),(mp[1],p2[1]),
                             color=color2,**kwargs))
    else:
      canvas.add_line(Line2D((p1[0],p2[0]),(p1[1],p2[1]),
                             color=color,**kwargs))

  def addCanvasText(self,text,pos,font,color=(0,0,0),**kwargs):
    import re
    pos = self.rescalePt(pos)
    canvas = self._axes
    text = re.sub(r'<.*?>','',text)
    canvas.annotate(text,(pos[0],pos[1]),color=color,
                    verticalalignment='center',
                    horizontalalignment='center',
                    weight=font.weight,
                    size=font.size*2.0,
                    family=font.face,
                    backgroundcolor="white")

  def addCanvasPolygon(self,ps,color=(0,0,0),**kwargs):
    canvas = self._axes
    ps = [self.rescalePt(x) for x in ps]
    canvas.add_patch(Polygon(ps,linewidth=0,facecolor=color))

