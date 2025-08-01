# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DividirLotes
                                 A QGIS plugin
 Divide polígonos seleccionados horizontal o verticalmente en partes iguales
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                              -------------------
        begin                : 2025-07-24
        git sha              : $Format:%H$
        author               : Geografo Edwin Calle Condori
        email                : eddycc66@gmail.com
 ***************************************************************************/
"""

# -*- coding: utf-8 -*-
from qgis.PyQt.QtWidgets import QAction, QMessageBox
from qgis.core import (
    QgsFeature,
    QgsVectorLayer,
    QgsGeometry,
    QgsProject,
    QgsPointXY,
    QgsWkbTypes
)
import os

from .DividirLotes_dialog import DividirLotesDialog


class DividirLotes:
    def __init__(self, iface):
        self.iface = iface
        self.plugin_dir = os.path.dirname(__file__)
        self.dlg = None
        self.actions = []
        self.menu = "Dividir Lotes"
        self.toolbar = self.iface.addToolBar("DividirLotes")
        self.toolbar.setObjectName("DividirLotes")

    def initGui(self):
        icon_path = ":/plugins/DividirLotes/icon.png"
        self.add_action(icon_path, text="Dividir Lotes", callback=self.run, parent=self.iface.mainWindow())

    def unload(self):
        for action in self.actions:
            self.iface.removePluginMenu(self.menu, action)
            self.iface.removeToolBarIcon(action)
        del self.toolbar

    def add_action(self, icon_path, text, callback, parent=None):
        action = QAction(text, parent)
        action.triggered.connect(callback)
        self.toolbar.addAction(action)
        self.iface.addPluginToMenu(self.menu, action)
        self.actions.append(action)
        return action

    def run(self):
        if self.dlg is None:
            self.dlg = DividirLotesDialog(self.iface)

        self.dlg.show()
        result = self.dlg.exec_()

        if result:
            capa_lotes = self.getLayerByName(self.dlg.obtenerCapa())
            if not capa_lotes:
                QMessageBox.critical(None, "Error", "Seleccione una capa válida.")
                return

            # Validamos que la capa tenga los atributos requeridos
            if "num_lotes" not in [f.name() for f in capa_lotes.fields()] or \
               "orientacio" not in [f.name() for f in capa_lotes.fields()]:
                QMessageBox.critical(None, "Error", "La capa debe tener los campos 'num_lotes' y 'orientacio'.")
                return

            self.dividir_lotes(capa_lotes)

    def getLayerByName(self, name):
        for layer in QgsProject.instance().mapLayers().values():
            if layer.name() == name:
                return layer
        return None

    def dividir_lotes(self, capa):
        crs = capa.crs().authid()
        salida = QgsVectorLayer(f"Polygon?crs={crs}", "Parcelas Divididas", "memory")
        prov = salida.dataProvider()
        prov.addAttributes(capa.fields())
        salida.updateFields()

        for feat in capa.getFeatures():
            geom = feat.geometry()
            num_lotes = int(feat["num_lotes"]) if feat["num_lotes"] else 1
            orientacio = str(feat["orientacio"]).lower()

            if num_lotes <= 1 or geom.isEmpty():
                prov.addFeature(feat)  # No se divide, se copia igual
                continue

            partes = self.dividir_geometria(geom, num_lotes, orientacio)
            for p in partes:
                nueva = QgsFeature(salida.fields())
                nueva.setGeometry(p)
                nueva.setAttributes(feat.attributes())
                prov.addFeature(nueva)

        salida.updateExtents()
        QgsProject.instance().addMapLayer(salida)
        QMessageBox.information(None, "Éxito", f"Parcelas generadas: {salida.featureCount()}")

    def dividir_geometria(self, geom, num_partes, orientacio):
        bbox = geom.boundingBox()
        minx, maxx = bbox.xMinimum(), bbox.xMaximum()
        miny, maxy = bbox.yMinimum(), bbox.yMaximum()
        ancho = maxx - minx
        alto = maxy - miny
        partes = []

        for i in range(num_partes):
            if orientacio == "vertical":
                x1 = minx + i * (ancho / num_partes)
                x2 = minx + (i + 1) * (ancho / num_partes)
                rect = QgsGeometry.fromPolygonXY([[
                    QgsPointXY(x1, miny), QgsPointXY(x2, miny),
                    QgsPointXY(x2, maxy), QgsPointXY(x1, maxy),
                    QgsPointXY(x1, miny)
                ]])
            else:  # horizontal
                y1 = miny + i * (alto / num_partes)
                y2 = miny + (i + 1) * (alto / num_partes)
                rect = QgsGeometry.fromPolygonXY([[
                    QgsPointXY(minx, y1), QgsPointXY(maxx, y1),
                    QgsPointXY(maxx, y2), QgsPointXY(minx, y2),
                    QgsPointXY(minx, y1)
                ]])

            inter = geom.intersection(rect)
            if inter and not inter.isEmpty():
                if inter.isMultipart():
                    partes.extend(inter.asGeometryCollection())
                else:
                    partes.append(inter)

        return partes
