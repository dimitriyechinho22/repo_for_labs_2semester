# Map


## Description
Module creates an HTML map based on given loaction and year. The map shows the nearest locations where films were shot.
<br><br>
Libraries used in this module:
 + **argparse**
 + **itertools**
 + **haversine**
 + **folium**
 + **geopy**
## USAGE
main.py is launched from command line.
```python
(venv) C:\Users\dima2\PycharmProjects\lab1_1\venv\Scripts>main.py 2016 49.83826 24.02324 locations.list
```
Arguments:
 + **year**(str)
 + **latitude**(float)
 + **longitude**(float)
 + **path to dataset**(str)
## Output
Map with the information
![image](https://user-images.githubusercontent.com/92580268/153600019-241fc20a-946f-4e1e-aef2-b42f13177c58.png)
## Layers
On the map we have 3 additions:
  + MousePosition
  + ScrollZoomToggler
  + MiniMap
  + CirclePattern
## Main func
In the main fuction I connect argparse and call all of the functions.
```python
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
```

