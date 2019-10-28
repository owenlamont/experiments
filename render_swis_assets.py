#%%
import geopandas as gpd
from pathlib import Path

#%%
western_power_shapes_dir = Path('../WesternPower')

#%%
shape_file_list = list(western_power_shapes_dir.glob('**/*.shp'))

#%%
