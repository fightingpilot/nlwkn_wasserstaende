import json, time, sys, argparse
import urllib.request

def main(argv):

    coordinates = (argv[0], argv[1])
    update_interval = argv[2]
    url = argv[3]
    out = argv[4]

    while True:
        websource = urllib.request.urlopen(url)
        raw_data = json.loads(websource.read().decode())["getStammdatenResult"]
        data = {"type": "FeatureCollection", "features": []}
        for stelle in raw_data:
            s = {
                "type": "Feature",
                "geometry": {"type": "Point", "coordinates": [stelle[coordinates[0]], stelle[coordinates[1]]]},
                "properties": stelle
            }
            data["features"].append(s)
        with open('out', 'w') as gj:
            json.dump(data, gj, indent=4)
        print(data)
        time.sleep(update_interval)

if __name__ == '__main__':

    lat_def = "WGS84Hochwert"
    lon_def = "WGS84Rechtswert"
    interval_def = 60
    url_def = "https://bis.azure-api.net/PegelonlinePublic/REST/stammdaten/stationen/All?key=9dc05f4e3b4a43a9988d747825b39f43"
    out_def = "output.geojson"

    parser = argparse.ArgumentParser(description='Read and store the NLWKN data into GeoJson')

    parser.add_argument("--lat", help="Name of the field to get the latitude from.\nIf not given default value will be used (" + lat_def + ")")
    parser.add_argument("--lon", help="Name of the field to get the longitude from.\nIf not given default value will be used (" + lon_def + ")")
    parser.add_argument("-i", "--interval", type=int, help="The interval of the data-request in seconds.\nIf not given default value will be used (" + str(interval_def) + ")")
    parser.add_argument("-u", "--url", help="The URL for the request.\nIf not given default value will be used (" + url_def + ")")
    parser.add_argument("-o", "--outfile", help="The name of the output-geojson.\nIf not given default value will be used (" + out_def + ")")

    args = parser.parse_args()

    argv = []

    if args.lat:
        argv.append(args.lat)
    else:
        argv.append(lat_def)

    if args.lon:
        argv.append(args.lon)
    else:
        argv.append(lon_def)

    if args.interval:
        argv.append(args.interval)
    else:
        argv.append(interval_def)

    if args.url:
        argv.append(args.url)
    else:
        argv.append(url_def)

    if args.outfile:
        argv.append(args.out)
    else:
        argv.append(out_def)

    print(argv)
    #main(argv)