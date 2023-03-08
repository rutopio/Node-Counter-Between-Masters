# encoding: utf-8

###########################################################################################################
#
#
#	Reporter Plugin
#
#	Read the docs:
#	https://github.com/schriftgestalt/GlyphsSDK/tree/master/Python%20Templates/Reporter
#
#
###########################################################################################################

from __future__ import division, print_function, unicode_literals
import objc
from GlyphsApp import *
from GlyphsApp.plugins import *

class NodeCounterBetweenMasters(ReporterPlugin):

	@objc.python_method
	def settings(self):
		self.menuName = Glyphs.localize({
			"en": "Node Counter Between Masters",
			"zh-Hant": "各主板間的路經總節點數",
			"zh-Hant": "各主板间的路径总节点数",
			})

	@objc.python_method
	def drawNodeCount( self, Layer ):
		FontMaster = Layer.associatedFontMaster()

		glyph = Layer.parent
		masters = glyph.parent.masters
		ascender = FontMaster.ascender

		fontDisplaySize = 15
		sepDisplay = "/"
		yesEmoji = "✅"
		noEmoji = "❌"

		masterIds = []
		layerCount = []

		for master in masters:
			masterIds.append(master.id)
			nodeCount = 0
			for path in glyph.layers[master.id].paths:
				nodeCount += len(path.nodes)
			layerCount.append(str(nodeCount))

		displayString = ""

		if len(layerCount) > 1:
			displayString = f" {sepDisplay} ".join(layerCount)
			if len(set(layerCount)) == 1:
				displayString = f"{yesEmoji} {displayString}"
			elif len(set(layerCount)) > 1:
				displayString = f"{noEmoji} {displayString}"
		elif len(layerCount) == 1:
			displayString = layerCount[0]

		coordY = max(ascender + 30, Layer.bounds.origin.y+Layer.bounds.size.height + 30.0)
		coordX = max(Layer.width, Layer.bounds.origin.x + Layer.bounds.size.width - 50.0)

		self.drawTextAtPoint( displayString, NSPoint(coordX, coordY), align = "bottomright", fontColor = NSColor.colorWithString_("#2E5C6E"), fontSize = fontDisplaySize)

	@objc.python_method
	def background(self, layer):
		if self.getScale() >= 0.2:
			self.drawNodeCount( layer )
	
	@objc.python_method
	def __file__(self):
		"""Please leave this method unchanged"""
		return __file__


