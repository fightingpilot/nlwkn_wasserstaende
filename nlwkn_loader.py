import json, time, argparse
import urllib.request

def main(argv):

    coordinates = (argv[0], argv[1])
    update_interval = argv[2]
    url = argv[3]
    out = argv[4]
    ov = argv[5]

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

        if ov:
            with open(out, 'w') as gj:
                json.dump(data, gj, indent=4)
        else:
            with open(out + time.strftime("%d%m%Y_%H%M%S", time.localtime()), 'w') as gj:
                json.dump(data, gj, indent=4)

        time.sleep(update_interval)

if __name__ == '__main__':

    lat_def = "WGS84Hochwert"
    lon_def = "WGS84Rechtswert"
    interval_def = 60
    url_def = "https://bis.azure-api.net/PegelonlinePublic/REST/stammdaten/stationen/All?key=9dc05f4e3b4a43a9988d747825b39f43"
    out_def = "output.geojson"

    parser = argparse.ArgumentParser(description='Read and store the NLWKN data into GeoJson')

    parser.add_argument("--lat", default=lat_def, help="Name of the field to get the latitude from.\nIf not given default value will be used (" + lat_def + ")")
    parser.add_argument("--lon", default=lon_def, help="Name of the field to get the longitude from.\nIf not given default value will be used (" + lon_def + ")")
    parser.add_argument("-i", "--interval", default=interval_def, type=int, help="The interval of the data-request in seconds.\nIf not given default value will be used (" + str(interval_def) + ")")
    parser.add_argument("-u", "--url", default=url_def, help="The URL for the request.\nIf not given default value will be used (" + url_def + ")")
    parser.add_argument("-o", "--outfile", default=out_def, help="The name of the output-geojson.\nIf not given default value will be used (" + out_def + ")")
    parser.add_argument("--overwrite", default="True", choices=["True", "False"], help="Whether the existing geojson should be overwritten or not. Default is True")

    args = parser.parse_args()

    argv = []

    argv.append(args.lat)
    argv.append(args.lon)
    argv.append(args.interval)
    argv.append(args.url)
    argv.append(args.outfile)
    argv.append(eval(args.overwrite))

    #print(args)
    #print(argv)
    #print(time.strftime("%d%m%Y_%H%M%S", time.localtime()))
    main(argv)