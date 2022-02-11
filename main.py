"""
Project for lab1_2
"""
import itertools
import argparse
from geopy.geocoders import Nominatim
import haversine
import folium
from folium import plugins
from geopy.distance import geodesic


def read_and_analyze_file(path_to_dataset: str) -> dict:
    """
    :param path_to_dataset: path to data
    :return: dict with needed info
    >>> dict(itertools.islice(read_and_analyze_file('locations.list').items(), 1))
    {'2006': [['#1 Single', 'Los Angeles, California, USA'], ['#1 Single', 'New York City, New York, USA']]}
    """
    result_lst = []
    needed_info = []
    with open('locations.list', 'r') as file: #opening the file
        for line in file:
            if line[0].startswith('"') or len(line) == 0:
                needed_info.append(line)
    for line in needed_info:
        index_of_duzh = []
        for element in enumerate(line):
            if element[1] == '"':
                index_of_duzh.append(element)
        if len(index_of_duzh) > 2:
            index_of_duzh = index_of_duzh[2:]
            for item in index_of_duzh:
                if index_of_duzh.index(item) > 0:
                    line = line[:(item[0]-1)] + line[(item[0]-1) + 1:]
                else:
                    line = line[:item[0]] + line[item[0] + 1:]
        line = line.split('"')
        line = line[1:]
        line[1] = line[1].strip()
        if line[-1][-1] == ')':
            left_duzh = line[-1].rfind('(')
            line[-1] = line[-1][:left_duzh]
        if '{' in line[-1]:
            left_skob = line[-1].find('{')
            right_skob = line[-1].rfind('}')
            line[-1] = line[-1][:left_skob] + line[-1][right_skob:]
            line[-1] = line[-1].replace('}', '')
        line = [i.strip() for i in line]
        line[-1] = " ".join(line[-1].split())
        find_the_skob = line[-1].rfind(')')
        new_lst = []
        year = line[-1][1:find_the_skob] #deleting useless info
        location = line[-1][find_the_skob + 1:].strip()
        new_lst.append(line[0])
        new_lst.append(location)
        new_lst.append(year)
        result_lst.append(new_lst)
    resulted_dict = {}
    for element in result_lst:
        if element[-1] in resulted_dict:
            resulted_dict[element[-1]].append(element[:-1])
            continue
        else:
            resulted_dict[element[-1]] = [element[:-1]]
    return resulted_dict


def analyze_the_coordinates(resulted_dict: dict, year: str, latitude: float, longitude: float) -> dict:
    """
    :param resulted_dict: dict with needed data
    :param year: the year that is given by user
    :param latitude: the latitude that is given by user
    :param longitude: the latitude that is given by user
    :return: dict where keys are films and values are all the distances from a certain coordinate.
    >>> analyze_the_coordinates(read_and_analyze_file('locations.list'), '2016', 49.83826, 24.02324)['#ActorsLife']
    [(7193.75759367353, (40.7127281, -74.0060152))]
    """
    geolocator = Nominatim(user_agent='distances')
    list_of_coords = []
    list_of_films = []
    list_of_locations = []
    for element in resulted_dict:
        if element == year:
            for item in resulted_dict[element]:
                try:
                    geo_location = item[-1]
                    geo_locate = geo_location.strip()
                    location = geolocator.geocode(geo_locate) # trying to find the coordinates of a place
                    list_of_coords.append((location.latitude, location.longitude)) 
                    list_of_films.append(item[0])
                except AttributeError:
                    continue
    list_of_distances = []
    init_coord = (latitude, longitude)
    for item in list_of_coords:
        distance = geodesic(init_coord, item).km #finding the distance
        list_of_distances.append(distance)
    final_dict = {}
    for element in range(len(list_of_distances)):
        if list_of_films[element] in final_dict:
            final_dict[list_of_films[element]].append((list_of_distances[element], list_of_coords[element]))
            continue
        else:
            final_dict[list_of_films[element]] = [(list_of_distances[element], list_of_coords[element])]
    for item in final_dict:
        final_dict[item] = sorted(final_dict[item], key= lambda x:x[0])
        if len(final_dict[item]) > 10:
            final_dict[item] = final_dict[item][:10]
        else:
            final_dict[item] = sorted(final_dict[item])
    return final_dict # the dict with films, distances and coordinates


def generate_map(main_dict, latitude, longitude, year, path_to_dataset):
    """
    :param main_dict: the dict with the corrected information
    :param latitude: the latitude
    :param longitude: the longitude
    :param year: the year where we have to find distance
    :return: dict with the minimal distances
    """
    map = folium.Map(tiles="Stamen Terrain", location=[latitude, longitude], zoom_start=15) #creating a map
    feature_group = folium.FeatureGroup(name="Close films")
    main_dict = analyze_the_coordinates(read_and_analyze_file(path_to_dataset), year, latitude, longitude)
    for item in main_dict:
        optional_latitude = main_dict[item][0][1][0] #taking the coordinates
        optional_longitude = main_dict[item][0][1][1]
        feature_group.add_child(folium.Marker(location=[optional_latitude, optional_longitude], popup=item, icon=folium.Icon(icon='needed_film', color="green")))
    map.add_child(feature_group)
    m_position = plugins.MousePosition(position='bottomleft', separator=' : ', empty_string='Unavailable', lng_first=False,
                          num_digits=7, prefix='', lat_formatter=None, lng_formatter=None)
    map.add_child(m_position)
    #zoom
    plugins.ScrollZoomToggler().add_to(map)
    #making a fullscreen
    plugins.Fullscreen(position="topright").add_to(map)
    feature_group_2 = folium.FeatureGroup(name="Starting location")
    feature_group_2.add_child(folium.Marker(location=[latitude, longitude], popup="Current location",
                                icon=folium.Icon(color="cadetblue", icon='blue')))
    #create a minimap
    mini_map = plugins.MiniMap(toggle_display=True)
    map.add_child(mini_map)
    circle_pattern = plugins.CirclePattern(width=20, height=20, radius=12, weight=2.0, color='#DEB887', fill_color='#33B3FF',
                          opacity=0.75, fill_opacity=0.5)
    map.add_child(circle_pattern)
    map.add_child(feature_group_2)
    map.add_child(folium.LayerControl())
    map.save('my_Map.html')

def main_func():
    """
    The main fuction to push everything.
    return: HTML-file
    """
    parser = argparse.ArgumentParser(description='Change a substring to another one')
    parser.add_argument('year', type=str, help='The year')
    parser.add_argument('latitude', type=str, help='The latitude')
    parser.add_argument('longitude', type=str, help='The longitude')
    parser.add_argument('path_to_dataset', type=str, help='The path to a file')
    args = parser.parse_args()
    year = args.year
    needed_dict_first = read_and_analyze_file(args.path_to_dataset)
    needed_dict_second = analyze_the_coordinates(needed_dict_first, year, args.latitude, args.longitude)
    generate_map(needed_dict_second, args.latitude, args.longitude, year, args.path_to_dataset)


if __name__ == "__main__":
    main_func()
    import doctest
    doctest.testmod()





