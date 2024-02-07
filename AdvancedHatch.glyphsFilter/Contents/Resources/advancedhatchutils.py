import copy
import math
# noinspection PyUnresolvedReferences
import objc
# noinspection PyUnresolvedReferences
from Foundation import NSPoint

class AdvancedHatchUtils():

    def __init__(self, outlineStrokeWidth) -> None:
        super().__init__()
        self.outlineStrokeWidth = outlineStrokeWidth

    @objc.python_method
    def prepareOutlineForIntersection(self, sourceLayer):
        layer = copy.deepcopy(sourceLayer)
        for newPath in layer.shapes:
            newPath.setAttribute_forKey_(self.outlineStrokeWidth, "strokeWidth")
        layer.flattenOutlinesRemoveOverlap_origHints_secondaryPath_extraHandles_error_(False, None, None, None, None)
        layer.shapes = layer.shapes + sourceLayer.shapes
        layer.removeOverlap()
        return layer



