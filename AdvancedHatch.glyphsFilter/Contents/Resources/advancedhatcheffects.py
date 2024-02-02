# noinspection PyUnresolvedReferences
import objc
# noinspection PyUnresolvedReferences
from GlyphsApp import *
# noinspection PyUnresolvedReferences
from GlyphsApp.plugins import *
# noinspection PyUnresolvedReferences
from Foundation import NSMakePoint
# noinspection PyUnresolvedReferences
from Foundation import NSClassFromString

class AdvancedHatchEffects():

    def __init__(self) -> None:
        super().__init__()

    @objc.python_method
    def hatchLayerWithOrigin(self, layer, theta, enableHatchStroke, hatchStroke, hatchStep, hatchOrigin):
        HatchOutlineFilter = NSClassFromString("HatchOutlineFilter")
        HatchOutlineFilter.hatchLayer_origin_stepWidth_angle_offset_checkSelection_shadowLayer_(layer, (int(hatchOrigin[0]), int(hatchOrigin[1])), hatchStep, theta, 0, False, None)
        shapesLength = len(layer.shapes)
        hatchStart = int(hatchStroke[0])
        hatchEnd = int(hatchStroke[1])
        i = 0;
        if enableHatchStroke:
            for myShape in layer.shapes:
                endRatio = i / shapesLength
                startShare = (1.0 - endRatio) * (hatchStart * 1.0)
                endShare = endRatio * hatchEnd
                strokeWidth = int(startShare + endShare)
                print("endRatio" + str(endRatio))
                print("startShare" + str(startShare))
                print("endShare" + str(endShare))
                print("strokeWidth " + str(strokeWidth))
                myShape.setAttribute_forKey_(strokeWidth, "strokeWidth")
                myShape.setAttribute_forKey_(0, "lineCapEnd")
                myShape.setAttribute_forKey_(0, "lineCapStart")
                i += 1
        return layer