import csv
from qgis.core import (
    QgsProject,
    QgsFeatureRequest,
    QgsDistanceArea,
    QgsGeometry,
    QgsPointXY,
    QgsVectorLayer,
    QgsField,
    QgsFeature,
    QgsWkbTypes,
    QgsPalLayerSettings,
    QgsVectorLayerSimpleLabeling,
    QgsTextFormat
)
from qgis.PyQt.QtCore import QVariant
from qgis.PyQt.QtGui import QColor

# Define a list of trench layer names
trench_layer_names = ['Trench1', 'Trench2', 'Trench3', 'Trench4', 'Trench13', 'Trench16', 'Trench17', 'Trench18', 'Trench19', 'Trench21']  # Add more trench names as needed

# Load KLICPOINTS layer
klicpoints_layer = QgsProject.instance().mapLayersByName('Intersection Points')[0]

# Prepare a QgsDistanceArea object for distance calculations
d = QgsDistanceArea()
d.setEllipsoid('intl')  # Set the ellipsoid used for distance calculations

# Create a new memory layer for lines with EPSG:28992
line_layer = QgsVectorLayer('LineString?crs=EPSG:28992', 'Trench to KLIC Distances', 'memory')
line_provider = line_layer.dataProvider()

# Add fields for line layer
line_provider.addAttributes([
    QgsField('Trench', QVariant.String),
    QgsField('Description', QVariant.String),
    QgsField('Distance', QVariant.Double)
])
line_layer.updateFields()

# List to store results for all trenches
all_results = []
unmatched_counts = {}

# Process each trench layer
for trench_layer_name in trench_layer_names:
    trench_layer = QgsProject.instance().mapLayersByName(trench_layer_name)[0]
    d.setSourceCrs(trench_layer.crs(), QgsProject.instance().transformContext())

    results = []  # Results for this trench layer
    unmatched_count = 0  # Unmatched count for this trench layer

    # Loop through each feature in the trench layer
    for trench_feat in trench_layer.getFeatures():
        trench_point = trench_feat.geometry().asPoint()
        description = trench_feat['description']  # Get the description of the trench feature
        matched = False  # Track if a match is found

        # Create a request to filter KLICPOINTS within 4 meters radius
        request = QgsFeatureRequest().setFilterRect(trench_feat.geometry().buffer(4, 5).boundingBox())

        # Loop through potential nearby points in KLICPOINTS
        for klic_feat in klicpoints_layer.getFeatures(request):
            if klic_feat['layer_name'] == description:
                klic_point = klic_feat.geometry().asPoint()
                distance = d.measureLine(QgsPointXY(trench_point), QgsPointXY(klic_point))
                results.append((trench_layer_name, description, distance))  # Store trench name, description and distance
                matched = True

                # Create a line feature for the offset
                line = QgsFeature()
                line_geom = QgsGeometry.fromPolylineXY([QgsPointXY(trench_point), QgsPointXY(klic_point)])
                line.setGeometry(line_geom)
                line.setAttributes([trench_layer_name, description, distance])
                line_provider.addFeature(line)

        # Check if the current trench feature was unmatched
        if not matched:
            unmatched_count += 1  # Increment the count of unmatched trench points

    unmatched_counts[trench_layer_name] = unmatched_count  # Store unmatched count for this trench
    all_results.extend(results)  # Add this trench's results to the all results list

# Sort all results by distance, smallest first
all_results.sort(key=lambda x: x[2])

# Define file path for CSV output
csv_file_path = 'C:/Users/louis/Desktop/Thesis/AnalysisInfo/combined_distance_results.csv'

# Write all results to a single CSV file
with open(csv_file_path, 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(['Trench', 'Description', 'Distance (m)'])  # Writing the headers
    for result in all_results:
        csvwriter.writerow([result[0], result[1], f"{result[2]:.4f}"])  # Writing the data with four decimal places

# Add the line layer to the project
QgsProject.instance().addMapLayer(line_layer)

# Style the line layer with red lines
line_symbol = line_layer.renderer().symbol()
line_symbol.setColor(QColor(255, 0, 0))  # Set line color to red
line_layer.triggerRepaint()

# Create label settings for distance labels
label_settings = QgsPalLayerSettings()
label_settings.fieldName = 'Distance'
label_settings.placement = QgsPalLayerSettings.Line
text_format = QgsTextFormat()
text_format.setSize(10)
text_format.setColor(QColor(255, 0, 0))  # Set label color to red
label_settings.setFormat(text_format)

# Apply labeling settings to the line layer
line_layer.setLabeling(QgsVectorLayerSimpleLabeling(label_settings))
line_layer.setLabelsEnabled(True)
line_layer.triggerRepaint()

# Report unmatched counts
print(f"Results saved to {csv_file_path}")
for trench, count in unmatched_counts.items():
    print(f"Number of unmatched {trench} points: {count}")
