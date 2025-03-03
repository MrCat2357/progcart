# Obter o caminho para o shapefile (exemplo: /usr/share/qgis/resources/data/world_map.shp)
path_to_shp = os.path.join(QgsApplication.pkgDataPath(), "resources", "data", "camadas_ibge", "AREA_ESPECIAL.shp")

# Criar a camada vetorial a partir do shapefile
vlayer = QgsVectorLayer(path_to_shp, "AREA_ESPECIAL", "ogr")

# Verificar se a camada foi carregada corretamente
if not vlayer.isValid():
    print("Layer failed to load!")
else:
    # Adicionar a camada ao projeto QGIS
    QgsProject.instance().addMapLayer(vlayer)
