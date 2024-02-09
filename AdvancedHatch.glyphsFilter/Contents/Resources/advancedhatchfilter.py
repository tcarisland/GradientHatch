# noinspection PyUnresolvedReferences
import objc
import copy
# noinspection PyUnresolvedReferences
from GlyphsApp import *
# noinspection PyUnresolvedReferences
from GlyphsApp.plugins import *
# noinspection PyUnresolvedReferences
from Foundation import NSMakePoint
# noinspection PyUnresolvedReferences
from Foundation import NSClassFromString


class AdvancedHatchFilter():

    def __init__(self) -> None:
        super().__init__()

    @objc.python_method
    def hatchLayerWithOrigin(self, layer, theta, enableHatchStroke, hatchStroke, hatchStep, hatchOrigin):
        HatchOutlineFilter = NSClassFromString("HatchOutlineFilter")
        hatchOrigin = (int(hatchOrigin[0]), int(hatchOrigin[1]))
        self.runHatchLayer(HatchOutlineFilter, layer, hatchOrigin, hatchStep, theta)
        OffsetCurveFilter = NSClassFromString("GlyphsFilterOffsetCurve")
        shapesLength = len(layer.shapes)
        hatchStart = int(hatchStroke[0])
        hatchEnd = int(hatchStroke[1])
        i = 0
        shapes = []
        if enableHatchStroke:
            for myShape in layer.shapes:
                endRatio = i / shapesLength
                startShare = (1.0 - endRatio) * (hatchStart * 1.0)
                endShare = endRatio * hatchEnd
                strokeWidth = int(startShare + endShare)
                offsetShapes = OffsetCurveFilter.offsetPath_offsetX_offsetY_makeStroke_position_(myShape, strokeWidth,
                                                                                                 strokeWidth, True, 0.0)
                shapes += offsetShapes
                i += 1
            layer.shapes = shapes
        layer.removeOverlap()
        return layer

    @objc.python_method
    def runHatchLayer(self, HatchOutlineFilter, layer, hatchOrigin, hatchStep, theta):
        if hasattr(HatchOutlineFilter, 'hatchLayer_useBackground_origin_stepWidth_angle_') and callable(
                HatchOutlineFilter.hatchLayer_useBackground_origin_stepWidth_angle_):
            HatchOutlineFilter.hatchLayer_useBackground_origin_stepWidth_angle_(layer, False, hatchOrigin, hatchStep,
                                                                                theta)
        else:
            HatchOutlineFilter.hatchLayer_origin_stepWidth_angle_offset_checkSelection_shadowLayer_(layer, hatchOrigin,
                                                                                                    hatchStep, theta, 0,
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
    def getLength(selfself, intersections):
        if hasattr(intersections, 'count'):
            return intersections.count()
        else:
            return len(intersections)
