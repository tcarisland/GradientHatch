import objc
import copy
from Foundation import NSClassFromString
from hatchmetrics import HatchMetrics


class GradientHatchFilter():

    def __init__(self) -> None:
        super().__init__()

    @objc.python_method
    def hatchLayerWithOrigin(self, layer, angle, offsetPathEnabled, strokeWidths, stepWidth, origin):
        HatchOutlineFilter = NSClassFromString("HatchOutlineFilter")
        OffsetCurveFilter = NSClassFromString("GlyphsFilterOffsetCurve")
        hatchMetrics = HatchMetrics()
        hatchMetrics.setGlyphHeightFromLayer(layer)
        self.runHatchLayer(HatchOutlineFilter, layer, [int(origin[0]), int(origin[1])], stepWidth, angle)
        glyphHeight = hatchMetrics.getHeight()
        hatchStart = int(strokeWidths[0])
        hatchEnd = int(strokeWidths[1])
        shapes = []
        if offsetPathEnabled:
            for myShape in layer.shapes:
                if myShape.shapeType != 4:
                    yPos = myShape.nodes[0].position.y + abs(hatchMetrics.descender)
                    yPos = self.clamp(yPos, 0, glyphHeight)
                    endRatio = yPos / glyphHeight
                    startShare = (1.0 - endRatio) * (hatchStart * 1.0)
                    endShare = endRatio * hatchEnd
                    offsetPath = int(startShare + endShare)
                    offsetShapes = OffsetCurveFilter.offsetPath_offsetX_offsetY_makeStroke_position_(myShape, offsetPath,
                                                                                                     offsetPath, True, 0.0)
                    shapes += offsetShapes
            layer.shapes = shapes
        layer.removeOverlap()
        return layer

    @objc.python_method
    def clamp(self, value, minValue, maxValue):
        if value < minValue:
            return minValue
        if value > maxValue:
            return maxValue
        return value

    @objc.python_method
    def runHatchLayer(self, HatchOutlineFilter, layer, origin, stepWidth, angle):
        if hasattr(HatchOutlineFilter, 'hatchLayer_useBackground_origin_stepWidth_angle_') and callable(
                HatchOutlineFilter.hatchLayer_useBackground_origin_stepWidth_angle_):
            HatchOutlineFilter.hatchLayer_useBackground_origin_stepWidth_angle_(layer, False, origin, stepWidth,
                                                                                angle)
        else:
            HatchOutlineFilter.hatchLayer_origin_stepWidth_angle_offset_checkSelection_shadowLayer_(layer, origin,
                                                                                                    stepWidth, angle, 0,
                                                                                                    False, None)

    @objc.python_method
    def getEmptyLayerWithShape(self, layer, shape):
        emptyLayer = copy.deepcopy(layer)
        emptyLayer.shapes = [shape]
        return emptyLayer

    @objc.python_method
    def intersectShapes(self, layer, originalShapes):
        layerShapes = copy.deepcopy(layer.shapes)
        intersectedShapes = []
        for shape in originalShapes:
            for hatchShape in layerShapes:
                shapeOne = [hatchShape]
                shapeTwo = [shape]
                shapeOne = self.intersect(shapeTwo, shapeOne)
                for intersectedShape in shapeOne:
                    intersectedShapes.append(intersectedShape)
        layer.shapes = intersectedShapes
        return layer

    @objc.python_method
    def intersect(self, shapeTwo, shapeOne):
        GSPathOperator = NSClassFromString("GSPathOperator")
        if hasattr(GSPathOperator, 'intersectPaths_with_error_') and callable(
                GSPathOperator.intersectPaths_with_error_):
            GSPathOperator.intersectPaths_with_error_(shapeTwo, shapeOne, None)
        else:
            GSPathOperator.intersectPaths_from_error_(shapeTwo, shapeOne, None)
        return shapeOne

    @objc.python_method
    def prepareOutlineForIntersection(self, sourceLayer, outlineStrokeWidth):
        layer = copy.deepcopy(sourceLayer)
        outlineStrokeWidth = int(outlineStrokeWidth)
        for newPath in layer.shapes:
            newPath.setAttribute_forKey_(outlineStrokeWidth, "strokeWidth")
        layer.flattenOutlinesRemoveOverlap_origHints_secondaryPath_extraHandles_error_(False, None, None, None, None)
        layer.shapes = layer.shapes + sourceLayer.shapes
        layer.removeOverlap()
        return layer

    @objc.python_method
    def cleanupDanglingShapes(self, layer, originalShapes):
        remainingShapes = []
        for shape in originalShapes:
            for hatchShape in layer.shapes:
                danglingShapesLayer = copy.deepcopy(layer)
                danglingShapesLayer.shapes = [shape, hatchShape]
                intersections = danglingShapesLayer.intersections()
                if self.getLength(intersections) > 0:
                    remainingShapes.append(hatchShape)
        layer.shapes = remainingShapes
        return layer

    @objc.python_method
    def getLength(self, intersections):
        if hasattr(intersections, 'count'):
            return intersections.count()
        else:
            return len(intersections)
