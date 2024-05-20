from qgis.core import (
    QgsProject, QgsFeature, QgsGeometry, QgsVectorLayer,
    QgsField, QgsWkbTypes, QgsPointXY
)
from PyQt5.QtCore import QVariant

gpkg_path = "C:/Users/louis/Desktop/Thesis/Enschede/Deurningerstraat/Deurningerstraat/Proefsleuven Deurningerstraat.gpkg"

# Layer names that should intersect with 'Profielen'
layer_names = [
    "B-RO-KL-DATA_BT NEDERLAND NV-G", "B-RO-KL-DATA_COAXIAAL_10_ZIGGO BV-G", "B-RO-KL-DATA_COAXIAAL_17_ZIGGO BV-G", "B-RO-KL-DATA_COAXIAAL_7_ZIGGO BV-G", "B-RO-KL-DATA_DUCT_ZIGGO BV-G", "B-RO-KL-DATA_EUROFIBER NEDERLAND BV-G", "B-RO-KL-DATA_GEMEENTE ENSCHEDE PA VW TELECOM SERVICE-G", "B-RO-KL-DATA_GEMEENTE ENSCHEDE-G", "B-RO-KL-DATA_KABELBED_KPN BV-G", "B-RO-KL-DATA_KABELBED_ZIGGO BV-G", "B-RO-KL-DATA_MANTELBUIS_100_KPN BV-G", "B-RO-KL-DATA_MANTELBUIS_110_KPN BV-G", "B-RO-KL-DATA_MANTELBUIS_110_ZIGGO BV-G", "B-RO-KL-DATA_MANTELBUIS_125_ZIGGO BV-G", "B-RO-KL-DATA_MANTELBUIS_25_ZIGGO BV-G", "B-RO-KL-DATA_MANTELBUIS_75_ZIGGO BV-G", "B-RO-KL-DATA_MANTELBUIS_ASBESTCEMENT_100_KPN BV-G", "B-RO-KL-DATA_MANTELBUIS_ASBESTCEMENT_125_KPN BV-G", "B-RO-KL-DATA_MANTELBUIS_ASBESTCEMENT_KPN BV-G", "B-RO-KL-DATA_MANTELBUIS_KPN BV-G", "B-RO-KL-DATA_MANTELBUIS_PE_100_KPN BV-G", "B-RO-KL-DATA_MANTELBUIS_PE_160_KPN BV-G", "B-RO-KL-DATA_MANTELBUIS_PVC_100_KPN BV-G", "B-RO-KL-DATA_MANTELBUIS_PVC_110_KPN BV-G", "B-RO-KL-DATA_MANTELBUIS_PVC_70_KPN BV-G", "B-RO-KL-DATA_MANTELBUIS_STAAL_100_KPN BV-G", "B-RO-KL-DATA_MANTELBUIS_STAAL_125_KPN BV-G", "B-RO-KL-DATA_MANTELBUIS_ZIGGO BV-G", "B-RO-KL-DATA_REGGEFIBER OPERATOR BV-G", "B-RO-KL-DATA_T MOBILE NETHERLANDS BV-G", "B-RO-KL-DATA_TRENT INFRASTRUCTUUR-G", "B-RO-KL-ET_LS_230 V_ENEXIS NETBEHEER BV-G", "B-RO-KL-ET_LS_400 V_ENEXIS NETBEHEER BV-G", "B-RO-KL-ET_LS_500 V_GEMEENTE ENSCHEDE-G", "B-RO-KL-ET_LS_DUCT_ENEXIS NETBEHEER BV-G", "B-RO-KL-ET_LS_ENEXIS NETBEHEER BV-G", "B-RO-KL-ET_LS_KABELBED_ENEXIS NETBEHEER BV-G", "B-RO-KL-ET_LS_MANTELBUIS_GEMEENTE ENSCHEDE-G", "B-RO-KL-ET_LS_MANTELBUIS_OVERIG_50_ENEXIS NETBEHEER BV-G", "B-RO-KL-ET_MS_10 KV_ENEXIS NETBEHEER BV-G", "B-RO-KL-ET_MS_DUCT_ENEXIS NETBEHEER BV-G", "B-RO-KL-ET_MS_KABELBED_ENEXIS NETBEHEER BV-G", "B-RO-KL-ET_MS_MANTELBUIS_50_ENEXIS NETBEHEER BV-G", "B-RO-KL-ET_MS_MANTELBUIS_PVC_110_ENEXIS NETBEHEER BV-G", "B-RO-KL-GAS_HD_MANTELBUIS_PVC_250_ENEXIS NETBEHEER BV-G", "B-RO-KL-GAS_HD_MANTELBUIS_STAAL_250_ENEXIS NETBEHEER BV-G", "B-RO-KL-GAS_HD_MANTELBUIS_STAAL_300_ENEXIS NETBEHEER BV-G", "B-RO-KL-GAS_HD_PE_200_1 BAR_ENEXIS NETBEHEER BV-G", "B-RO-KL-GAS_HD_PE_63_1 BAR_ENEXIS NETBEHEER BV-G", "B-RO-KL-GAS_LD_ASBESTCEMENT_100_ENEXIS NETBEHEER BV-G", "B-RO-KL-GAS_LD_MANTELBUIS_OVERIG_150_ENEXIS NETBEHEER BV-G", "B-RO-KL-GAS_LD_MANTELBUIS_PVC_110_ENEXIS NETBEHEER BV-G", "B-RO-KL-GAS_LD_MANTELBUIS_PVC_160_ENEXIS NETBEHEER BV-G", "B-RO-KL-GAS_LD_MANTELBUIS_PVC_200_ENEXIS NETBEHEER BV-G", "B-RO-KL-GAS_LD_MANTELBUIS_PVC_500_ENEXIS NETBEHEER BV-G", "B-RO-KL-GAS_LD_MANTELBUIS_SPVC_200_ENEXIS NETBEHEER BV-G", "B-RO-KL-GAS_LD_MANTELBUIS_STAAL_200_ENEXIS NETBEHEER BV-G", "B-RO-KL-GAS_LD_MANTELBUIS_STAAL_250_ENEXIS NETBEHEER BV-G", "B-RO-KL-GAS_LD_MANTELBUIS_STAAL_500_ENEXIS NETBEHEER BV-G", "B-RO-KL-GAS_LD_OVERIG_15_0.3 BAR_ENEXIS NETBEHEER BV-G", "B-RO-KL-GAS_LD_OVERIG_22_0.3 BAR_ENEXIS NETBEHEER BV-G", "B-RO-KL-GAS_LD_OVERIG_28_0.3 BAR_ENEXIS NETBEHEER BV-G", "B-RO-KL-GAS_LD_OVERIG_35_0.3 BAR_ENEXIS NETBEHEER BV-G", "B-RO-KL-GAS_LD_PE_110_0.3 BAR_ENEXIS NETBEHEER BV-G", "B-RO-KL-GAS_LD_PE_160_0.3 BAR_ENEXIS NETBEHEER BV-G", "B-RO-KL-GAS_LD_PE_25_0.3 BAR_ENEXIS NETBEHEER BV-G", "B-RO-KL-GAS_LD_PE_32_0.3 BAR_ENEXIS NETBEHEER BV-G", "B-RO-KL-GAS_LD_PE_40_0.3 BAR_ENEXIS NETBEHEER BV-G", "B-RO-KL-GAS_LD_PE_50_0.3 BAR_ENEXIS NETBEHEER BV-G", "B-RO-KL-GAS_LD_PVC_110_0.3 BAR_ENEXIS NETBEHEER BV-G", "B-RO-KL-GAS_LD_PVC_200_0.3 BAR_ENEXIS NETBEHEER BV-G", "B-RO-KL-GAS_LD_PVC_50_0.3 BAR_ENEXIS NETBEHEER BV-G", "B-RO-KL-GAS_LD_SPVC_110_0.3 BAR_ENEXIS NETBEHEER BV-G", "B-RO-KL-GAS_LD_SPVC_160_0.3 BAR_ENEXIS NETBEHEER BV-G", "B-RO-KL-GAS_LD_SPVC_160_ENEXIS NETBEHEER BV-G", "B-RO-KL-GAS_LD_SPVC_200_0.3 BAR_ENEXIS NETBEHEER BV-G", "B-RO-KL-GAS_LD_SPVC_315_0.3 BAR_ENEXIS NETBEHEER BV-G", "B-RO-KL-GAS_LD_SPVC_32_0.3 BAR_ENEXIS NETBEHEER BV-G", "B-RO-KL-GAS_LD_SPVC_40_0.3 BAR_ENEXIS NETBEHEER BV-G", "B-RO-KL-GAS_LD_SPVC_50_0.3 BAR_ENEXIS NETBEHEER BV-G", "B-RO-KL-GAS_LD_SPVC_63_0.3 BAR_ENEXIS NETBEHEER BV-G", "B-RO-KL-GAS_LD_STAAL_25_0.3 BAR_ENEXIS NETBEHEER BV-G", "B-RO-KL-GAS_LD_STAAL_30_0.3 BAR_ENEXIS NETBEHEER BV-G", "B-RO-KL-GAS_LD_STAAL_40_0.3 BAR_ENEXIS NETBEHEER BV-G", "B-RO-KL-GAS_LD_STAAL_60_0.3 BAR_ENEXIS NETBEHEER BV-G", "B-RO-KL-WARMTENET_ENNATUURLIJK BV-G", "B-RO-KL-WARMTENET_MANTELBUIS_ENNATUURLIJK BV-G", "B-RO-KL-WATER_100_VITENS-G", "B-RO-KL-WATER_110_VITENS-G", "B-RO-KL-WATER_150_VITENS-G", "B-RO-KL-WATER_160_VITENS-G", "B-RO-KL-WATER_200_VITENS-G", "B-RO-KL-WATER_250_VITENS-G", "B-RO-KL-WATER_315_VITENS-G", "B-RO-KL-WATER_32_VITENS-G", "B-RO-KL-WATER_355_VITENS-G", "B-RO-KL-WATER_40_VITENS-G", "B-RO-KL-WATER_50_VITENS-G", "B-RO-KL-WATER_63_VITENS-G", "B-RO-KL-WATER_75_VITENS-G", "B-RO-KL-WATER_MANTELBUIS_100_VITENS-G", "B-RO-KL-WATER_MANTELBUIS_190.2_VITENS-G", "B-RO-KL-WATER_MANTELBUIS_VITENS-G", "B-RO-KL-WATER_VITENS-G", "B-RO-KL-WEESLEIDING_GEMEENTE ENSCHEDE-G", "B-RO-OG-INFO_BT NEDERLAND NV-G", "B-RO-OG-INFO_ENEXIS NETBEHEER BV-G", "B-RO-OG-INFO_EUROFIBER NEDERLAND BV-G", "B-RO-OG-INFO_REGGEFIBER OPERATOR BV-G", "B-RO-OG-INFO_TRENT INFRASTRUCTUUR-G", "B-RO-OG-INFO_VITENS-G", "B-RO-RI-VRIJVERVAL_GEMEENTE ENSCHEDE-G", "N-RO-KL-WATER_MANTELBUIS_VITENS-G", "N-RO-KL-WATER_VITENS-G", "V-RO-KL-ET_LS_ENEXIS NETBEHEER BV-G", "V-RO-KL-ET_LS_KABELBED_ENEXIS NETBEHEER BV-G", "V-RO-KL-ET_MS_ENEXIS NETBEHEER BV-G", "V-RO-KL-ET_MS_KABELBED_ENEXIS NETBEHEER BV-G", "V-RO-KL-GAS_HD_NODULAIR GIETIJZER_200_ENEXIS NETBEHEER BV-G", "V-RO-KL-GAS_LD_GRIJS GIETIJZER_100_ENEXIS NETBEHEER BV-G", "V-RO-KL-GAS_LD_GRIJS GIETIJZER_150_ENEXIS NETBEHEER BV-G", "V-RO-KL-GAS_LD_SPVC_25_ENEXIS NETBEHEER BV-G", "V-RO-KL-WATER_100_VITENS-G", "V-RO-KL-WATER_160_VITENS-G", "V-RO-KL-WATER_300_VITENS-G", "V-RO-KL-WATER_315_VITENS-G", "V-RO-KL-WATER_32_VITENS-G", "V-RO-KL-WATER_MANTELBUIS_VITENS-G", "V-RO-KL-WATER_VITENS-G" 
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
