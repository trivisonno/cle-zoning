# Takes a QGIS layer named 'fbc-parcels', dissolves the parcels together 
# based on their fbc_zoning value, then splits them into single parts.
# This layer can then be exported to GeoJSON or another format.

from qgis.core import QgsProject, QgsVectorLayer
import processing

# Define the layer name
layer_name = "fbc-parcels"

# Get the layer by name
layer = QgsProject.instance().mapLayersByName(layer_name)[0]

# Step 1: Dissolve the features based on the 'fbc_zoning' field
dissolve_params = {
    'INPUT': layer,
    'FIELD': ['fbc_zoning'],
    'OUTPUT': 'memory:dissolved_layer'
}
dissolved_layer = processing.run("native:dissolve", dissolve_params)['OUTPUT']

# Step 2: Convert multipart features to single parts
multipart_to_singleparts_params = {
    'INPUT': dissolved_layer,
    'OUTPUT': 'memory:fbc_large_zones'
}
fbc_large_zones_layer = processing.run("native:multiparttosingleparts", multipart_to_singleparts_params)['OUTPUT']

# Add the result to the project
QgsProject.instance().addMapLayer(fbc_large_zones_layer)

print("Process complete. The resulting layer has been added to the project.")

