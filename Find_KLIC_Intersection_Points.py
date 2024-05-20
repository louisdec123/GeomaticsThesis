from qgis.core import (
    QgsProject, QgsFeature, QgsGeometry, QgsVectorLayer,
    QgsField, QgsWkbTypes, QgsPointXY
)
from PyQt5.QtCore import QVariant

gpkg_path = "[...]/Proefsleuven Deurningerstraat.gpkg"

# Layer names that should intersect with 'Profielen'
layer_names = [
    #....Add KLIC CABLE LAYERS
    ]

# Load 'Profielen' layer
profielen_layer = QgsVectorLayer(f"{gpkg_path}|layername=polylines|subset=\"layer\"='Profielen'", "Profielen", "ogr")
if not profielen_layer.isValid():
    print("Failed to load 'Profielen' layer")
else:
    # Create a memory layer for storing intersection points, adding a 'layer_name' attribute
    intersection_layer = QgsVectorLayer("Point?crs=EPSG:28992", "Intersection Points", "memory")
    dp = intersection_layer.dataProvider()
    dp.addAttributes([
        QgsField("id", QVariant.Int),
        QgsField("layer_name", QVariant.String)
    ])
    intersection_layer.updateFields()

    id_counter = 1  # Counter for intersection points

    # Process intersections with other specified layers
    for layer_name in layer_names:
        other_layer = QgsVectorLayer(f"{gpkg_path}|layername=polylines|subset=\"layer\"='{layer_name}'", layer_name, "ogr")
        if other_layer.isValid():
            for feature1 in profielen_layer.getFeatures():
                for feature2 in other_layer.getFeatures():
                    intersection = feature1.geometry().intersection(feature2.geometry())
                    if intersection and not intersection.isEmpty():
                        if intersection.wkbType() == QgsWkbTypes.PointZ:
                            point = intersection.asPoint()
                            new_point = QgsPointXY(point.x(), point.y())
                            new_feature = QgsFeature()
                            new_feature.setGeometry(QgsGeometry.fromPointXY(new_point))
                            new_feature.setAttributes([id_counter, layer_name])
                            dp.addFeature(new_feature)
                            id_counter += 1
                        elif intersection.wkbType() == QgsWkbTypes.MultiPointZ:
                            points = intersection.asMultiPoint()
                            for point in points:
                                new_point = QgsPointXY(point.x(), point.y())
                                new_feature = QgsFeature()
                                new_feature.setGeometry(QgsGeometry.fromPointXY(new_point))
                                new_feature.setAttributes([id_counter, layer_name])
                                dp.addFeature(new_feature)
                                id_counter += 1

    # Add the new layer to the project
    QgsProject.instance().addMapLayer(intersection_layer)
    print("Intersection points have been added to the map.")
