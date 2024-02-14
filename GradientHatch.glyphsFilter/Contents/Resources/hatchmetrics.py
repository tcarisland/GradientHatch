import objc


class HatchMetrics():
    descender = 0
    ascender = 0

    def __init__(self):
        super().__init__()

    @objc.python_method
    def getMetricFromLayer(self, layer, metricName):
        for metricValueName in layer.master.metricValues:
            if layer.master.metricValues[metricValueName].title() == metricName:
                return int(layer.master.metricValues[metricValueName].position)

    @objc.python_method
    def setGlyphHeightFromLayer(self, layer):
        self.ascender = self.getMetricFromLayer(layer, 'Ascender')
        self.descender = self.getMetricFromLayer(layer, 'Descender')

    @objc.python_method
    def getHeight(self):
        return self.ascender + (self.descender * -1)
