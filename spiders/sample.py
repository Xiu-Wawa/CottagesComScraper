from geopy.geocoders import Nominatim

address = "Boylestone Near Ashbourne, Peak District & Derbyshire Dales"

# Create a Nominatim geocoder instance
geolocator = Nominatim(user_agent="my-app")

# Use the geocoder to get the location information for the address
location = geolocator.geocode(address)

# Extract the latitude and longitude from the location information
latitude = location.latitude
longitude = location.longitude

print("Latitude:", latitude)
print("Longitude:", longitude)
