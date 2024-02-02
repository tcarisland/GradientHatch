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
from advancedhatcheffects import AdvancedHatchEffects

# noinspection PyUnresolvedReferences
class AdvancedHatch(FilterWithDialog):

	# Definitions of IBOutlets
	prefID = "com.tcarisland.AdvancedHatch"
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

	@objc.python_method
	def settings(self):
		self.menuName = Glyphs.localize({
			'en': 'Advanced Hatch',
			'de': 'Advanced Hatch',
			'fr': 'Advanced Hatch',
			'es': 'Advanced Hatch',
			'pt': 'Advanced Hatch',
			'jp': 'Advanced Hatch',
			'ko': 'Advanced Hatch',
			'zh': 'Advanced Hatch',
			})
		# Word on Run Button (default: Apply)
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


	@objc.IBAction
	def setAngle_(self, sender):
		Glyphs.defaults[self.domain('angle')] = sender.floatValue()
		self.update()

	@objc.IBAction
	def setOffsetPath_(self, sender):
		Glyphs.defaults[self.domain('offsetPath')] = sender.state()
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
		Glyphs.defaults[self.domain('useBackground_')] = sender.state()
		self.update()

	# Actual filter
	@objc.python_method
	def filter(self, layer, inEditView, customParameters):
		layer.removeOverlap()
		if len(customParameters) > 0:
			print("")
		else:
			angle = float(self.pref('angle'))
			offsetPath = bool(self.pref('offsetPath'))
			offsetPathEnd = float(self.pref('offsetPathEnd'))
			offsetPathStart = float(self.pref('offsetPathStart'))
			originX = float(self.pref('originX'))
			originY = float(self.pref('originY'))
			stepWidth = float(self.pref('stepWidth'))
			useBackground = bool(self.pref('useBackground'))
		effects = AdvancedHatchEffects()
		hatchAngle = angle
		enableHatchStroke = offsetPath
		hatchStroke = [offsetPathStart, offsetPathEnd]
		hatchStep = stepWidth
		hatchOrigin = [originX, originY]
		layer = effects.hatchLayerWithOrigin(layer, hatchAngle, enableHatchStroke, hatchStroke, hatchStep, hatchOrigin)
		effects.hatchLayerWithOrigin()
		print("filter done")

	@objc.python_method
	def generateCustomParameter( self ):
		self.registerDefaults()
		return "%s; angle:%s offsetPath:%i offsetPathEnd:%s offsetPathStart:%s originX:%s originY:%s stepWidth:%s useBackground:%i" % (
			self.__class__.__name__,
			self.pref('angle'),
			self.pref('offsetPath'),
			self.pref('offsetPathEnd'),
			self.pref('offsetPathStart'),
			self.pref('originX'),
			self.pref('originY'),
			self.pref('stepWidth'),
			self.pref('useBackground')
			)

	@objc.python_method
	def __file__(self):
		"""Please leave this method unchanged"""
		return __file__
