import objc


class HatchMetrics():
    descender = 800
    ascender = -200

    def __init__(self):
        super().__init__()

    @objc.python_method
    def setGlyphHeightFromLayer(self, layer):
        # GSMetricsTypeAscender = 1
        self.ascender = layer.ascender
        # GSMetricsTypeDescender = 7
        self.descender = layer.descender

    @objc.python_method
    def getHeight(self):
        return self.ascender + (self.descender * -1)
