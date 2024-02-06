import copy
import math
# noinspection PyUnresolvedReferences
import objc
# noinspection PyUnresolvedReferences
from Foundation import NSPoint

class AdvancedHatchUtils():

    def __init__(self, outlineStrokeWidth, insetWidth) -> None:
        super().__init__()
        self.outlineStrokeWidth = outlineStrokeWidth
        self.insetWidth = insetWidth

    @objc.python_method
    def createOutlineGlyphCopy(self, sourceLayer):
        layer = copy.deepcopy(sourceLayer)
        for newPath in layer.shapes:
            newPath.setAttribute_forKey_(self.outlineStrokeWidth, "strokeWidth")
        layer.flattenOutlinesRemoveOverlap_origHints_secondaryPath_extraHandles_error_(False, None, None, None, None)
        return layer

    @objc.python_method
    def prepareOutlineForIntersection(self, sourceLayer):
        layer = copy.deepcopy(sourceLayer)
        for newPath in layer.shapes:
            newPath.setAttribute_forKey_(self.outlineStrokeWidth, "strokeWidth")
        layer.flattenOutlinesRemoveOverlap_origHints_secondaryPath_extraHandles_error_(False, None, None, None, None)
        layer.shapes = layer.shapes + sourceLayer.shapes
        layer.removeOverlap()
        return layer

    @objc.python_method
    def createInsetGlyphCopy(self, sourceLayer):
        layer = copy.deepcopy(sourceLayer)
        for newPath in layer.shapes:
            newPath.setAttribute_forKey_(self.insetWidth, "strokeWidth")
        layer.flattenOutlinesRemoveOverlap_origHints_secondaryPath_extraHandles_error_(False, None, None, None, None)
        layer.removeOverlap()
        layer.shapes = self.removeOuter(layer)
        if len(layer.shapes) > 1:
            layer.shapes = self.removeCounter(layer)
        return layer

    @objc.python_method
    def split(self, sourceLayer, yInitial, theta, width):
        layer = copy.deepcopy(sourceLayer)
        layer.cutBetweenPoints(NSPoint(0, yInitial),
                               NSPoint(width, self.getAngleEndCoordinates(width, yInitial, theta)))
        lower = []
        upper = []
        errormargin = 1
        for myShape in layer.shapes:
            isBelow = True
            for node in myShape.nodes:
                y_final = self.getAngleEndCoordinates(node.position.x, yInitial, theta)
                if (node.position.y - errormargin) >= y_final:
                    isBelow = False
            if isBelow:
                lower.append(myShape)
            else:
                upper.append(myShape)
        return [lower, upper]

    @objc.python_method
    def getAngleEndCoordinates(self, x, y, theta):
        theta_rad = math.radians(theta)
        delta_y = math.tan(theta_rad) * x
        y_final = y + delta_y
        return round(y_final)

    @objc.python_method
    def findMinMax(self, thisLayer):
        minx = -1
        miny = -1
        maxx = -1
        maxy = -1
        for shape in thisLayer.shapes:
            for node in shape.nodes:
                if (minx > node.position.x or minx == -1):
                    minx = node.position.x
                if (miny > node.position.y or miny == -1):
                    miny = node.position.y
                if (maxx < node.position.x or maxx == -1):
                    maxx = node.position.x
                if (maxy < node.position.y or maxy == -1):
                    maxy = node.position.y
        return [minx, miny, maxx, maxy]

    @objc.python_method
    def removeCounter(self, thisLayer):
        shapes = []
        minMax = self.findMinMax(thisLayer)
        for myShape in thisLayer.shapes:
            addShape = False
            for node in myShape.nodes:
                if (node.position.x == minMax[0]):
                    addShape = True
                if (node.position.y == minMax[1]):
                    addShape = True
                if (node.position.x == minMax[2]):
                    addShape = True
                if (node.position.y == minMax[3]):
                    addShape = True
            if addShape == True:
                shapes.append(myShape)
        return shapes

    @objc.python_method
    def removeOuter(self, thisLayer):
        shapes = []
        minMax = self.findMinMax(thisLayer)
        for myShape in thisLayer.shapes:
            if (self.isShapeOuter(myShape, minMax) == False):
                shapes.append(myShape)
        return shapes

    @objc.python_method
    def isShapeOuter(self, myShape, minMax):
        minx = False
        miny = False
        maxx = False
        maxy = False
        for node in myShape.nodes:
            if (node.position.x == minMax[0]):
                minx = True
            if (node.position.y == minMax[1]):
                miny = True
            if (node.position.x == minMax[2]):
                maxx = True
            if (node.position.y == minMax[3]):
                maxy = True
        return minx and miny and maxx and maxy

