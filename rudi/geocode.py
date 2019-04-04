import os,csv
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut

#Minimal example
#geolocator = Nominatim(user_agent="specify_your_app_name_here")
#location = geolocator.geocode("Fuldastrasse 3, 12043 Berlin")
#print(location.address)
#print((location.latitude, location.longitude))

#set file paths
data_dir=os.getcwd()
input_file=os.path.join(data_dir,"sample data","input_simpletext.csv")
encoding=None #change to 'utf-8' in case your input data is in utf-8

#prepare geocoder and list to store results
geolocator = Nominatim(user_agent="nominatim_testing")
results=[]

#recursive function to keep trying to geocode avoiding service-time out errors
def do_geocode(address):
    try:
        return geolocator.geocode(address)
    except GeocoderTimedOut:
        return do_geocode(address)


# open the input file
with open(input_file, 'r',encoding=encoding) as infile:
    csvreader = csv.reader(infile)
    
    for row in csvreader:
        location = do_geocode(row[0])
        if location is not None:
            results.append((row[0],location.latitude, location.longitude))
        else:
            results.append((row[0],"No result found"))

# write 'results' list var to new csv
output_file=os.path.join(data_dir,"output_nominatim.csv")
with open(output_file,"w",newline="",encoding='utf-8') as f: #wb for py2
    writer = csv.writer(f)
    writer.writerow(('Address','Latitude','Longitude')) #add header
    writer.writerows(results)
