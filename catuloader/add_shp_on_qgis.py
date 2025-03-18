import os
from qgis.core import QgsApplication, QgsVectorLayer, QgsProject

class ShapefileLayerLoader:
    def __init__(self, shapefile_path):
        # Recebe o caminho completo para o shapefile diretamente
        self.shapefile_path = shapefile_path

    def load_layer(self):
        # Cria a camada vetorial a partir do shapefile
        vlayer = QgsVectorLayer(self.shapefile_path, os.path.basename(self.shapefile_path).split(".")[0], "ogr")

        # Adiciona a camada ao projeto QGIS
        QgsProject.instance().addMapLayer(vlayer)
        print(f"Layer '{self.shapefile_path}' loaded successfully!")
        return vlayer

#Exemplo de uso da classe
shapefile_path = "C:/Users/catul/OneDrive/Área de Trabalho/aleatorios/arquivos_ibge/AREA_ESPECIAL.shp"  # Caminho completo para o shapefile
loader = ShapefileLayerLoader(shapefile_path)
vlayer = loader.load_layer()
