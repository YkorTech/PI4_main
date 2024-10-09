import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry import MultiPolygon
import folium
from folium.plugins import HeatMap


# Load the dataset for Canadian provinces (replace with the path to your downloaded shapefile)
shapefile_path = 'C:/Users/xuebi/Downloads/lcd_000b16a_e/lcd_000b16a_e.shp'
canada_provinces = gpd.read_file(shapefile_path)

# shapefile_path = 'C:/Users/xuebi/Downloads/lcd_000b16a_e/lcd_000b16a_e.shx'
# canada_provincesD = gpd.read_file(shapefile_path)
# print(canada_provincesD)
# # Filter for Quebec (using the ISO code or province name)

quebec = canada_provinces[canada_provinces['CDUID'] == '2401']
print(quebec["CDNAME"])
# quebec = canada_provinces[canada_provinces['PRNAME'] == 'Quebec / Québec']
# print(quebec[quebec['CDUID'] == '2499'])
# multi_poly = quebec.loc[4,"geometry"]

# if isinstance(multi_poly, MultiPolygon):
#     # Iterate over the individual Polygons in the MultiPolygon
#     i = 0
#     for poly in multi_poly.geoms:
#         print(i)  # Each `poly` is a Polygon object
#         i +=1
# for geom in multi_poly.geoms:
#     plt.plot(*geom.exterior.xy)
#     break        

# # Plot the map of Quebec
fig, ax = plt.subplots(figsize=(10, 10))
quebec.plot(ax=ax, color='lightblue', edgecolor='black')
# Add title and remove axes
ax.set_title('Map of Quebec', fontsize=15)
ax.set_axis_off()

plt.show()