# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DividirLotesDialog
                                 A QGIS plugin
 Ventana de diálogo para configurar parámetros de división de lotes
                              -------------------
        begin                : 2025-07-24
        author               : Geografo Edwin Calle Condori
        email                : eddycc66@gmail.com
 ***************************************************************************/
"""

from qgis.PyQt import QtWidgets
from qgis.core import QgsProject, QgsVectorLayer


class DividirLotesDialog(QtWidgets.QDialog):
    def __init__(self, iface, parent=None):
        super().__init__(parent)
        self.iface = iface
        self.setWindowTitle("Dividir Lotes")
        self.setMinimumWidth(300)

        layout = QtWidgets.QVBoxLayout()

        self.label = QtWidgets.QLabel("Seleccione la capa de lotes:")
        self.combo = QtWidgets.QComboBox()
        layout.addWidget(self.label)
        layout.addWidget(self.combo)

        botones = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel
        )
        botones.accepted.connect(self.accept)
        botones.rejected.connect(self.reject)
        layout.addWidget(botones)

        self.setLayout(layout)
        self.cargarCapas()

    def cargarCapas(self):
        self.combo.clear()
        for layer in QgsProject.instance().mapLayers().values():
            if isinstance(layer, QgsVectorLayer) and layer.geometryType() == 2:  # Polígonos
                self.combo.addItem(layer.name())

    def obtenerCapa(self):
        return self.combo.currentText()
