import trimesh
from pygltflib import GLTF2
import json
from shapely.geometry import shape
import numpy as np
import geopandas as gpd

# Utility function to convert Trimesh to GLTF
def convert_trimesh_to_gltf(mesh, output_filename):
    # Convert to GLTF using pygltflib
    mesh.export(output_filename, file_type='gltf')
    print(f"Converted to {output_filename}")

# Convert OBJ file to GLTF
def convert_obj_to_gltf(input_obj, output_gltf):
    mesh = trimesh.load(input_obj, file_type='obj')
    convert_trimesh_to_gltf(mesh, output_gltf)

# Convert DEM file to GLTF (assuming DEM as elevation data)
def convert_dem_to_gltf(dem_data, output_gltf):
    # Process DEM data as a heightmap and create a mesh (basic approach)
    height, width = dem_data.shape
    x = np.linspace(0, width, width)
    y = np.linspace(0, height, height)
    x, y = np.meshgrid(x, y)
    z = dem_data

    vertices = np.column_stack((x.ravel(), y.ravel(), z.ravel()))
    faces = []

    for i in range(height - 1):
        for j in range(width - 1):
            faces.append([i * width + j, (i + 1) * width + j, i * width + j + 1])
            faces.append([(i + 1) * width + j, (i + 1) * width + j + 1, i * width + j + 1])

    mesh = trimesh.Trimesh(vertices=vertices, faces=faces)
    convert_trimesh_to_gltf(mesh, output_gltf)

# Convert GeoJSON to GLTF
def convert_geojson_to_gltf(input_geojson, output_gltf):
    with open(input_geojson, 'r') as f:
        geojson_data = json.load(f)

    features = geojson_data['features']
    all_vertices = []
    all_faces = []

    for feature in features:
        geom = shape(feature['geometry'])
        if geom.geom_type == 'Polygon' or geom.geom_type == 'MultiPolygon':
            for polygon in geom.geoms if geom.geom_type == 'MultiPolygon' else [geom]:
                vertices = np.array(polygon.exterior.coords)
                faces = [[i, i + 1, i + 2] for i in range(len(vertices) - 2)]
                all_vertices.extend(vertices)
                all_faces.extend(faces)

    mesh = trimesh.Trimesh(vertices=np.array(all_vertices), faces=np.array(all_faces))
    convert_trimesh_to_gltf(mesh, output_gltf)

# Convert Shapefile (SHP) to GLTF
def convert_shp_to_gltf(input_shp, output_gltf):
    gdf = gpd.read_file(input_shp)
    
    all_vertices = []
    all_faces = []

    for geom in gdf.geometry:
        if geom.geom_type == 'Polygon' or geom.geom_type == 'MultiPolygon':
            for polygon in geom.geoms if geom.geom_type == 'MultiPolygon' else [geom]:
                vertices = np.array(polygon.exterior.coords)
                faces = [[i, i + 1, i + 2] for i in range(len(vertices) - 2)]
                all_vertices.extend(vertices)
                all_faces.extend(faces)

    mesh = trimesh.Trimesh(vertices=np.array(all_vertices), faces=np.array(all_faces))
    convert_trimesh_to_gltf(mesh, output_gltf)

# Main function to handle conversion
def convert_to_gltf(input_file, output_gltf):
    file_extension = input_file.split('.')[-1].lower()

    if file_extension == 'obj':
        convert_obj_to_gltf(input_file, output_gltf)
    elif file_extension == 'dem':
        dem_data = np.loadtxt(input_file)
        convert_dem_to_gltf(dem_data, output_gltf)
    elif file_extension in ['geojson', 'json']:
        convert_geojson_to_gltf(input_file, output_gltf)
    elif file_extension == 'shp':
        convert_shp_to_gltf(input_file, output_gltf)
    elif file_extension == 'gbl':
        # Direct conversion to GLTF (glTF Binary is essentially the same)
        import shutil
        shutil.copyfile(input_file, output_gltf)
        print(f"Copied {input_file} to {output_gltf}")
    else:
        print(f"File format {file_extension} is not supported.")

# Example usage
# Uncomment the following lines to test the conversion:
# input_file = 'example.shp'  # Change to your file path
# output_gltf = 'output_model.gltf'
# convert_to_gltf(input_file, output_gltf)
