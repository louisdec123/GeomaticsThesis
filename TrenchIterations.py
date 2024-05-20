from qgis.core import QgsFeature, QgsGeometry, QgsVectorLayer, QgsField, QgsProject, QgsPointXY
from PyQt5.QtCore import QVariant

def add_csv_as_layer(file_path, layer_name, x_field, y_field, crs_epsg, field_types):
    uri = f"file:///{file_path}?delimiter=,&xField={x_field}&yField={y_field}&crs=epsg:{crs_epsg}&fieldTypes={field_types}"
    return iface.addVectorLayer(uri, layer_name, "delimitedtext")

def calculate_average_point(points):
    x_coords, y_coords = zip(*[(point.x(), point.y()) for point in points])
    centroid = QgsPointXY(sum(x_coords) / len(x_coords), sum(y_coords) / len(y_coords))
    return centroid

def calculate_dynamic_intermediate_point(t1_points, t2_points):
    # Calculate average points for each trench
    avg_t1_point = calculate_average_point(t1_points)
    avg_t2_point = calculate_average_point(t2_points)
    
    count_t1 = len(t1_points)
    count_t2 = len(t2_points)
    bias_ratio = 0.1 if count_t1 > count_t2 else 0.9  # Adjust the bias ratio as needed for your use-case
    
    # Calculate the intermediate point using the determined bias
    intermediate_x = avg_t1_point.x() * (1 - bias_ratio) + avg_t2_point.x() * bias_ratio
    intermediate_y = avg_t1_point.y() * (1 - bias_ratio) + avg_t2_point.y() * bias_ratio
    
    return QgsPointXY(intermediate_x, intermediate_y)



# List of trench file paths
trench_files = [
    #Add Trench CSV Paths
]

x_field, y_field, crs_epsg, field_types = "E", "N", "28992", "integer,double,string,double,double,double,string"

# Create lines layer to store connections
crs = "EPSG:28992"
lines_layer = QgsVectorLayer(f"LineString?crs={crs}", "Trench_Connections", "memory")
pr = lines_layer.dataProvider()
pr.addAttributes([QgsField("description", QVariant.String)])
lines_layer.updateFields()
QgsProject.instance().addMapLayer(lines_layer)
lines_layer.startEditing()

# Load and connect each trench sequentially
for i in range(len(trench_files) - 1):
    trench_1_layer = add_csv_as_layer(trench_files[i], f"Trench{i+1}", x_field, y_field, crs_epsg, field_types)
    trench_2_layer = add_csv_as_layer(trench_files[i+1], f"Trench{i+2}", x_field, y_field, crs_epsg, field_types)
    
    if trench_1_layer is None or trench_2_layer is None:
        continue

    descriptions = set(feat['description'] for feat in trench_1_layer.getFeatures())
    for desc in descriptions:
        t1_points = [QgsPointXY(feat.geometry().asPoint()) for feat in trench_1_layer.getFeatures() if feat['description'] == desc]
        t2_points = [QgsPointXY(feat.geometry().asPoint()) for feat in trench_2_layer.getFeatures() if feat['description'] == desc]
        if t2_points:
            intermediate_point = calculate_dynamic_intermediate_point(t1_points, t2_points)
            for t1_feat in [feat for feat in trench_1_layer.getFeatures() if feat['description'] == desc]:
                t1_point = QgsPointXY(t1_feat.geometry().asPoint())
                line_to_intermediate = QgsFeature()
                line_to_intermediate.setGeometry(QgsGeometry.fromPolylineXY([t1_point, intermediate_point]))
                line_to_intermediate.setAttributes([desc])
                pr.addFeature(line_to_intermediate)
                for t2_feat in [feat for feat in trench_2_layer.getFeatures() if feat['description'] == desc]:
                    t2_point = QgsPointXY(t2_feat.geometry().asPoint())
                    line_from_intermediate = QgsFeature()
                    line_from_intermediate.setGeometry(QgsGeometry.fromPolylineXY([intermediate_point, t2_point]))
                    line_from_intermediate.setAttributes([desc])
                    pr.addFeature(line_from_intermediate)

lines_layer.commitChanges()
