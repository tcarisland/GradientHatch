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
        # TODO there seems to be different versions of the HatchOutlineFilter
        # either add if-checks for versions with subsequent compatible calls or implement hatching manually
        #HatchOutlineFilter.hatchLayer_useBackground_origin_stepWidth_angle_(layer, False, hatchOrigin, hatchStep, theta)
        HatchOutlineFilter.hatchLayer_origin_stepWidth_angle_offset_checkSelection_shadowLayer_(layer, hatchOrigin, hatchStep, theta, 0, False, None)
        #self.runHatchLayer(HatchOutlineFilter, layer, hatchOrigin, hatchStep, theta)
        OffsetCurveFilter = NSClassFromString("GlyphsFilterOffsetCurve")
        shapesLength = len(layer.shapes)
        hatchStart = int(hatchStroke[0])
        hatchEnd = int(hatchStroke[1])
        i = 0;
        shapes = []
        if enableHatchStroke:
            for myShape in layer.shapes:
                endRatio = i / shapesLength
                startShare = (1.0 - endRatio) * (hatchStart * 1.0)
                endShare = endRatio * hatchEnd
                strokeWidth = int(startShare + endShare)
                offsetShapes = OffsetCurveFilter.offsetPath_offsetX_offsetY_makeStroke_position_(myShape, strokeWidth, strokeWidth, True, 0.0)
                shapes += offsetShapes
                i += 1
            layer.shapes = shapes
        layer.removeOverlap()
        return layer

    @objc.python_method
    def runHatchLayer(self, HatchOutlineFilter, layer, hatchOrigin, hatchStep, theta):
        if hasattr(HatchOutlineFilter, 'hatchLayer_useBackground_origin_stepWidth_angle_') and callable(HatchOutlineFilter.hatchLayer_useBackground_origin_stepWidth_angle_):
            print("using case 1 " + "hatchLayer_useBackground_origin_stepWidth_angle_")
            HatchOutlineFilter.hatchLayer_useBackground_origin_stepWidth_angle_(layer, False, hatchOrigin, hatchStep, theta)
        else:
            print("using case 2 " + "hatchLayer_origin_stepWidth_angle_offset_checkSelection_shadowLayer_")
            HatchOutlineFilter.hatchLayer_origin_stepWidth_angle_offset_checkSelection_shadowLayer_(layer, hatchOrigin, hatchStep, theta, 0, False, None)


    @objc.python_method
    def getEmptyLayerWithShape(self, layer, shape):
        emptyLayer = copy.deepcopy(layer)
        emptyLayer.shapes = [shape]
        return emptyLayer

    @objc.python_method
    def intersectShapes(self, layer, originalShapes):
        GSPathOperator = objc.lookUpClass("GSPathOperator")
        layerShapes = copy.deepcopy(layer.shapes)
        intersectedShapes = []
        for shape in originalShapes:
            for hatchShape in layerShapes:
                shapeOne = [hatchShape]
                shapeTwo = [shape]
                GSPathOperator.intersectPaths_with_error_(shapeTwo, shapeOne, None)
                for intersectedShape in shapeOne:
                    intersectedShapes.append(intersectedShape)
        layer.shapes = intersectedShapes
        return layer

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
                if len(danglingShapesLayer.intersections()) > 0:
                    remainingShapes.append(hatchShape)
        layer.shapes = remainingShapes
        return layer
