# encoding: utf-8

###########################################################################################################
#
#
#	Filter with dialog Plugin
#
#	Read the docs:
#	https://github.com/schriftgestalt/GlyphsSDK/tree/master/Python%20Templates/Filter%20with%20Dialog
#
#	For help on the use of Xcode:
#	https://github.com/schriftgestalt/GlyphsSDK/tree/master/Python%20Templates
#
#
###########################################################################################################

from __future__ import division, print_function, unicode_literals
# noinspection PyUnresolvedReferences
import objc
import copy
# noinspection PyUnresolvedReferences
from GlyphsApp import *
# noinspection PyUnresolvedReferences
from GlyphsApp.plugins import *
# noinspection PyUnresolvedReferences
from Foundation import NSClassFromString
from gradienthatchfilter import GradientHatchFilter

# noinspection PyUnresolvedReferences
class GradientHatch(FilterWithDialog):

	# Definitions of IBOutlets
	prefID = "com.tcarisland.GradientHatch"
	if Glyphs.versionNumber < 3:
		# GLYPHS 2
		pathOperator = NSClassFromString("GSPathOperator").alloc().init() # needs to be initialized only once
	# The NSView object from the User Interface. Keep this here!
	dialog = objc.IBOutlet()
	# Text field in dialog
	angleTextField = objc.IBOutlet()
	offsetPathCheckBox = objc.IBOutlet()
	offsetPathEndTextField = objc.IBOutlet()
	offsetPathStartTextField = objc.IBOutlet()
	originXTextField = objc.IBOutlet()
	originYTextField = objc.IBOutlet()
	stepWidthTextField = objc.IBOutlet()
	useBackgroundCheckBox = objc.IBOutlet()
	expandBeforeInsetSlider = objc.IBOutlet()

	@objc.python_method
	def settings(self):
		self.menuName = Glyphs.localize({
			'cs': 'Postupné šrafování',
			'de': 'Stufenweises Schraffieren',
			'en': 'Gradient Hatch',
			'es': 'Eclosión Gradual',
			'fr': 'Éclosion par étapes',
			'it': 'Cova graduale',
			'ja': '段階的なハッチング',
			'ko': '단계별 해칭',
			'pt': 'Incubação gradual',
			'ru': 'Поэтапная штриховка',
			'tr': 'Kademeli Kuluçka',
			'zh_CN': '逐步孵化',
		})		# Word on Run Button (default: Apply)
		self.actionButtonLabel = Glyphs.localize({
			'en': 'Apply',
			'de': 'Anwenden',
			'fr': 'Appliquer',
			'es': 'Aplicar',
			'pt': 'Aplique',
			'jp': '申し込む',
			'ko': '대다',
			'zh': '应用',
			})
		# Load dialog from .nib (without .extension)
		self.loadNib('IBdialog', __file__)

	# On dialog show
	@objc.python_method
	def start(self):
		self.registerDefaults()
		# Set value of text field
		self.angleTextField.setStringValue_(self.pref('angle'))
		self.offsetPathEndTextField.setStringValue_(self.pref('offsetPathEnd'))
		self.offsetPathStartTextField.setStringValue_(self.pref('offsetPathStart'))
		self.originXTextField.setStringValue_(self.pref('originX'))
		self.originYTextField.setStringValue_(self.pref('originY'))
		self.stepWidthTextField.setStringValue_(self.pref('stepWidth'))
		self.offsetPathCheckBox.setState_(self.pref('offsetPath'))
		self.useBackgroundCheckBox.setState_(self.pref('useBackground'))
		self.expandBeforeInsetSlider.setStringValue_(self.pref('expandBeforeInset'))
		self.update()

	@objc.python_method
	def domain(self, prefName):
		prefName = prefName.strip().strip(".")
		return self.prefID + "." + prefName.strip()

	@objc.python_method
	def pref(self, prefName):
		prefDomain = self.domain(prefName)
		return Glyphs.defaults[prefDomain]

	@objc.python_method
	def registerDefaults(self, sender=None):
		Glyphs.registerDefault(self.domain('angle'), 180.0)
		Glyphs.registerDefault(self.domain('offsetPath'), 1)
		Glyphs.registerDefault(self.domain('offsetPathStart'), 5)
		Glyphs.registerDefault(self.domain('offsetPathEnd'), 1)
		Glyphs.registerDefault(self.domain('originX'), 0.0)
		Glyphs.registerDefault(self.domain('originY'), 0.0)
		Glyphs.registerDefault(self.domain('stepWidth'), 5)
		Glyphs.registerDefault(self.domain('useBackground'), 1)
		Glyphs.registerDefault(self.domain('expandBeforeInset'), 20)


	@objc.IBAction
	def setAngle_(self, sender):
		Glyphs.defaults[self.domain('angle')] = sender.floatValue()
		self.update()

	@objc.IBAction
	def setOffsetPath_(self, sender):
		Glyphs.defaults[self.domain('offsetPath')] = sender.state()
		self.enableOffsetPathTextFields(bool(sender.state()))
		self.update()

	@objc.IBAction
	def setOffsetPathEnd_(self, sender):
		Glyphs.defaults[self.domain('offsetPathEnd')] = sender.floatValue()
		self.update()

	@objc.IBAction
	def setOffsetPathStart_(self, sender):
		Glyphs.defaults[self.domain('offsetPathStart')] = sender.floatValue()
		self.update()

	@objc.IBAction
	def enableOffsetPathTextFields(self, areCheckboxesEnabled):
		self.offsetPathStartTextField.setEnabled_(areCheckboxesEnabled)
		self.offsetPathEndTextField.setEnabled_(areCheckboxesEnabled)

	@objc.IBAction
	def setOriginX_(self, sender):
		Glyphs.defaults[self.domain('originX')] = sender.floatValue()
		self.update()

	@objc.IBAction
	def setOriginY_(self, sender):
		Glyphs.defaults[self.domain('originY')] = sender.floatValue()
		self.update()

	@objc.IBAction
	def setStepWidth_(self, sender):
		Glyphs.defaults[self.domain('stepWidth')] = sender.floatValue()
		self.update()

	@objc.IBAction
	def setUseBackground_(self, sender):
		Glyphs.defaults[self.domain('useBackground')] = sender.state()
		self.update()

	@objc.IBAction
	def setExpandBeforeInset_(self, sender):
		Glyphs.defaults[self.domain('expandBeforeInset')] = sender.floatValue()
		self.update()

	# Actual filter
	@objc.python_method
	def filter(self, layer, inEditView, customParameters):
		useBackground = False
		offsetPathStart = 1
		offsetPathEnd = 10
		originX = 0
		originY = 0
		angle = 0
		stepWidth = 10
		offsetPath = True
		expandBeforeInset = 20
		if len(customParameters) > 0:
			if customParameters.has_key('angle'):
				angle = customParameters['angle']
			if customParameters.has_key('offsetPath'):
				offsetPath = customParameters['offsetPath']
			if customParameters.has_key('offsetPathEnd'):
				offsetPathEnd = customParameters['offsetPathEnd']
			if customParameters.has_key('offsetPathStart'):
				offsetPathStart = customParameters['offsetPathStart']
			if customParameters.has_key('originX'):
				originX = customParameters['originX']
			if customParameters.has_key('originY'):
				originY = customParameters['originY']
			if customParameters.has_key('stepWidth'):
				stepWidth = customParameters['stepWidth']
			if customParameters.has_key('useBackground'):
				useBackground = customParameters['useBackground']
			if customParameters.has_key('expandBeforeInset'):
				expandBeforeInset = customParameters['expandBeforeInset']
		else:
			angle = float(self.pref('angle'))
			offsetPath = bool(self.pref('offsetPath'))
			offsetPathEnd = float(self.pref('offsetPathEnd'))
			offsetPathStart = float(self.pref('offsetPathStart'))
			originX = float(self.pref('originX'))
			originY = float(self.pref('originY'))
			stepWidth = float(self.pref('stepWidth'))
			useBackground = bool(self.pref('useBackground'))
			expandBeforeInset = float(self.pref('expandBeforeInset'))
		if useBackground:
			layer.shapes = layer.background.shapes
		self.runFilter(layer, angle, offsetPath, [offsetPathStart, offsetPathEnd], stepWidth, [originX, originY], expandBeforeInset)

	@objc.python_method
	def runFilter(self, layer, angle, offsetPathEnabled, strokeWidths, stepWidth, origin, expandBeforeInset):
		hatchFilter = GradientHatchFilter()
		layer.removeOverlap()
		originalShapeLayer = copy.deepcopy(layer)
		if offsetPathEnabled:
			layer.shapes = hatchFilter.prepareOutlineForIntersection(layer, expandBeforeInset).shapes
		layer = hatchFilter.hatchLayerWithOrigin(layer, angle, offsetPathEnabled, strokeWidths, stepWidth, origin)
		if offsetPathEnabled:
			layer = hatchFilter.cleanupDanglingShapes(layer, originalShapeLayer.shapes)
			layer = hatchFilter.intersectShapes(layer, originalShapeLayer.shapes)

	@objc.python_method
	def generateCustomParameter( self ):
		self.registerDefaults()
		return "%s; angle:%s offsetPath:%i offsetPathEnd:%s offsetPathStart:%s originX:%s originY:%s stepWidth:%s useBackground:%i expandBeforeInset:%s" % (
			self.__class__.__name__,
			self.pref('angle'),
			self.pref('offsetPath'),
			self.pref('offsetPathEnd'),
			self.pref('offsetPathStart'),
			self.pref('originX'),
			self.pref('originY'),
			self.pref('stepWidth'),
			self.pref('useBackground'),
			self.pref('expandBeforeInset'),
			)

	@objc.python_method
	def __file__(self):
		"""Please leave this method unchanged"""
		return __file__
