import objc


class HatchMetrics():
    descender = 800
    ascender = -200

    def __init__(self):
        super().__init__()

    @objc.python_method
    def setGlyphHeightFromLayer(self, layer):
        self.ascender = layer.ascender
        self.descender = layer.descender

    @objc.python_method
    def getHeight(self):
        return self.ascender + (self.descender * -1)
