# Import All Necessary Libraries
import gempy as gp
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
#import shapefile
import csv
import vtk

#np.random.seed(1515)
#pd.set_option('precision', 2)

# Create Geologic Model Object/Container
geo_model = gp.create_model('VNC')

# Import CSV Files and Set Extent (xmin,xmax,ymin,ymax,zmin,zmax) and Resolution (X,Y,Z) of Model
# - Model Voxels are cubes, OT prisms, so extent can be different shape than resolution
# - Aim for less than 1,000,000 voxels in resolution (100 cells in every direction)
gp.init_data(geo_model, [483846.3365999999805354, 492015.6969999999855645, 5143944.1747000003233552, 5149806.7099999999627471, 250, 305], [10, 10, 10],
             path_o = 'C:/Users/acgr9/Documents/Vale_North_Creighton/ADAM/VNC_Geologic_Model/VNC_Geomodel_Orientations.csv',
             path_i = 'C:/Users/acgr9/Documents/Vale_North_Creighton/ADAM/VNC_Geologic_Model/VNC_Geomodel_Points.csv',
             default_values=True)

#Create Topography
#CHANGE FILEPATH HERE IF NEEDED
#geo_model.set_topography(source='gdal', filepath="C:/Users/acgr9/Documents/Vale_North_Creighton/ADAM/GIS/VNC_Geomodel_DEM_Compressed16.tif")

#gp.plot_2d(geo_model, show_topography=True, section_names=['topography'], show_lith=False,
#           show_boundaries=False,
#           kwargs_topography={'cmap': 'gray', 'norm': None}
#           )
#plt.show()

#Create Lithology Series
geo_model.add_features('Lith')

#Map Lithology to Lithology Series
gp.map_stack_to_surfaces(geo_model, {'Lith':('Organics',
                                             'ConcreteCrush',
                                             'Sand/Silt/Till1',
                                             'Clay',
                                             'Sand/Silt/Till2',
                                             'Cobbles',
                                             'Bedrock',
                                             'basement')})

#Visualize Surfacepoints and Orientations in 2D with Matplotlib
#plot = gp.plot_2d(geo_model, show_lith=True, show_boundaries=True, ve=50)
#plt.show()

#Visualize Surfacepoints and Orientations in 3D Cartesian Plane with VTK
#gpv = gp.plot_3d(geo_model, ve=50)

# Prepare Input Data for Interpolation via Theano
gp.set_interpolator(geo_model,
                    theano_optimizer='fast_compile',
                    verbose=[])

# Compute Model
sol = gp.compute_model(geo_model, compute_mesh=True, set_solutions=True)

# Display 2D Model
#gp.plot_2d(geo_model, show_data=True, show_topography=False, show_lith=True, direction='y', cell_number='mid', ve=50)
#plt.show()

# Automatically extract vertices to create 3D traingle complexes via gp.get_surfaces
ver, sim = gp.get_surfaces(geo_model)

# Display 3D Model
# - plotter_type = PyVista Plotter Type (Basic, Background or Notebook)
g3d = gp.plot_3d(geo_model, plotter_type="basic", show_topography=False, show_lith=True, show_surfaces=True, show_results=True, ve=50)

# Save Model - Outputs a zip file of all model inputs and outputs to the desktop
##gp.save_model(geo_model)

# Export Model as VTP Surfaces
##gp._plot.export_to_vtk(geo_model, 'C:/Users/acgr9/Desktop/CBay_Crand/Geomodel/VTK_Export/CBayCRand')
