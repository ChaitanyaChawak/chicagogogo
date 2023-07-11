# this is the main file where the functions exist

from geopy.geocoders import Nominatim


class Chicagoify:
    """
    This converts a given address into the number of blocks it is away from the center of Chicago, and vice versa!


    """

    def __init__(self):

        def get_coordinates(address):
            geolocator = Nominatim(user_agent="address_converter")
            location = geolocator.geocode(address)
            
            if location:
                latitude = location.latitude
                longitude = location.longitude
                return latitude, longitude
            else:
                return None
            
        def get_address_from_coordinates(latitude, longitude):
            geolocator = Nominatim(user_agent="address_converter")
            location = geolocator.reverse(f"{latitude}, {longitude}")
            
            address = location.raw['address']
            
            amenity = address.get('amenity', '')
            house_number = address.get('house_number', '')
            road = address.get('road', '')
            city = address.get('city', '')
            postcode = address.get('postcode', '')
            country = address.get('country', '')
            
            formatted_address = ''
            if amenity:
                formatted_address += f"{amenity}, "
            if house_number:
                formatted_address += house_number
                if road:
                    formatted_address += ' ' + road
            elif road:
                formatted_address += road
            
            if city:
                formatted_address += f", {city}"
            if postcode:
                formatted_address += f", {postcode}"
            if country:
                formatted_address += f", {country}"
            
            return formatted_address.strip(", ")
        
        def calculate_blocks_away(latitude, longitude):
            # Miles per degree
            mpd = (24901.92 / 360)

            # Blocks per degree
            bpd_n_mr = mpd * 12
            bpd_n_rc = mpd * 10
            bpd_n_ct = mpd * 9
            bpd_n = mpd * 8
            bpd_w = mpd * 8

            roosevelt = 41.8674224
            cermak = 41.8528516
            thirtyfirst = 41.8382902
            
            # Baseline
            b_latitude, b_longitude = 41.88205727768228, -87.62783047240069


            if latitude > b_latitude:
                blocks_away_latitude = (latitude - b_latitude) * bpd_n
                direction_latitude = "north"
            elif roosevelt <= latitude <= b_latitude:
                blocks_away_latitude = (b_latitude - latitude) * bpd_n_mr
                direction_latitude = "south"
            elif cermak <= latitude <= roosevelt:
                blocks_away_latitude = ((b_latitude - roosevelt) * bpd_n_mr + (roosevelt - latitude) * bpd_n_rc)
                direction_latitude = "south"
            elif thirtyfirst <= latitude <= cermak:
                blocks_away_latitude = ((b_latitude - roosevelt) * bpd_n_mr + (roosevelt - cermak) * bpd_n_rc + (cermak - latitude) * bpd_n_ct)
                direction_latitude = "south"
            elif latitude <= thirtyfirst:
                blocks_away_latitude = ((b_latitude - roosevelt) * bpd_n_mr + (roosevelt - cermak) * bpd_n_rc + (cermak - thirtyfirst) * bpd_n_ct + (thirtyfirst - latitude) * bpd_n)
                direction_latitude = "south"

            if longitude >= b_longitude:
                blocks_away_longitude = abs(b_longitude - longitude) * bpd_w
                direction_longitude = "east"
            elif longitude <= b_longitude:
                blocks_away_longitude = abs(longitude - b_longitude) * bpd_w
                direction_longitude = "west"

            return blocks_away_latitude, direction_latitude, blocks_away_longitude, direction_longitude

        self.question = input("Type \'blocks\' if you want to get the number of blocks from the center of Chicago, else type \'address\' to get the address given the number of blocks : ")
        if self.question == 'address':
            self.north = input('Number of blocks away to north : ')
            try:
                float(self.north)
            except ValueError:
                raise Exception("Please enter a valid positive number !!")
            self.south = input('Number of blocks away to south : ')
            try:
                float(self.south)
            except ValueError:
                raise Exception("Please enter a valid positive number !!")
            self.east = input('Number of blocks away to east : ')
            try:
                float(self.east)
            except ValueError:
                raise Exception("Please enter a valid positive number !!")
            self.west = input('Number of blocks away to west : ')
            try:
                float(self.west)
            except ValueError:
                raise Exception("Please enter a valid positive number !!")

            if self.north and self.south != '0' :
                raise Exception("The place cannot be both North and South at the same time !")
            
            if self.east and self.west != '0' :
                raise Exception("The place cannot be both East and West at the same time !")

        else:
            self.address = input('Give me the address: ')	## Here they should enter the address
            lat, long = get_coordinates(self.address)
            
            blocks_away_lat, direction_lat, blocks_away_lon, direction_lon = calculate_blocks_away(lat, long)
                
            print(f"{blocks_away_lat} blocks {direction_lat}")
            print(f"{blocks_away_lon} blocks {direction_lon}")

    

Chicagoify()
