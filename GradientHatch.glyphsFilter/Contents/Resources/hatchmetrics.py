import objc


class HatchMetrics():
    descender = 800
    ascender = -200

    def __init__(self):
        super().__init__()

    @objc.python_method
    def getMetricFromLayer(self, layer, metricTypeEnumOrdinal):
        try:
            for metricValueName in layer.master.metricValues:
                if (layer.master.metricValues[metricValueName] is not None
                        and layer.master.metricValues[metricValueName].metric is not None
                        and layer.master.metricValues[metricValueName].metric.type == metricTypeEnumOrdinal):
                    return int(layer.master.metricValues[metricValueName].position)
        except TypeError:
            for metricValue in layer.master.metrics:
                if (metricValue is not None
                        and metricValue.metric is not None
                        and metricValue.metric.type == metricTypeEnumOrdinal):
                    return int(metricValue.position)

    @objc.python_method
    def setGlyphHeightFromLayer(self, layer):
        # GSMetricsTypeAscender = 1
        self.ascender = self.getMetricFromLayer(layer, 1)
        # GSMetricsTypeDescender = 7
        self.descender = self.getMetricFromLayer(layer, 7)

    @objc.python_method
    def getHeight(self):
        return self.ascender + (self.descender * -1)
