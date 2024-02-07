import copy
import math
# noinspection PyUnresolvedReferences
import objc
# noinspection PyUnresolvedReferences
from Foundation import NSPoint

class AdvancedHatchUtils():

    def __init__(self) -> None:
        super().__init__()

    @objc.python_method
    def prepareOutlineForIntersection(self, sourceLayer, outlineStrokeWidth):
        layer = copy.deepcopy(sourceLayer)
        for newPath in layer.shapes:
            newPath.setAttribute_forKey_(outlineStrokeWidth, "strokeWidth")
        layer.flattenOutlinesRemoveOverlap_origHints_secondaryPath_extraHandles_error_(False, None, None, None, None)
        layer.shapes = layer.shapes + sourceLayer.shapes
        layer.removeOverlap()
        return layer

    @objc.python_method
    def cleanupDanglingShapes(self, layer, originalShapes):
        remainingShapes = []
        layerShapes = copy.deepcopy(layer.shapes)
        for shape in originalShapes:
            for hatchShape in layer.shapes:
                danglingShapesLayer = copy.deepcopy(layer)
                danglingShapesLayer.shapes = [shape, hatchShape]
                if(len(danglingShapesLayer.intersections()) > 0):
                    remainingShapes.append(hatchShape)
        layer.shapes = remainingShapes
        return layer