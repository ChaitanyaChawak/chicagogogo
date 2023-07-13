# this is the main file where the functions exist

from geopy.geocoders import Nominatim


class Chicagoify:
    """
    This converts a given address into the number of blocks it is away from the center of Chicago, and vice versa!


    """

    def __init__(self):

        #Miles per degree
        mpd = (24901.92 / 360)

        # Blocks per degree
        bpd_n_mr = mpd * 12
        bpd_n_rc = mpd * 10
        bpd_n_ct = mpd * 9
        bpd_n = mpd * 8
        bpd_w = mpd * 6

        roosevelt = 41.8674224
        cermak = 41.8528516
        thirtyfirst = 41.8382902

        b_latitude, b_longitude = 41.88205727768228, -87.62783047240069

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
            """
            Inputs: latitude, longitude
                - latitude: float, value from -90 to 90
                - longitude: float, value from -180 to 180
            Outputs: formatted address, which includes the latitude and longitude if no house number is given in the output

            Ex. get_address_from_coordinates(38, -86)
            Outputs: The precise location can also be found as: [38, -86]. 
            'OLD HWY 111 SE, 47117, United States'

            """
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

            precise_location = f"[{latitude}, {longitude}]"

            if not house_number:
                print("The precise location can also be found as:", precise_location)
            
            return formatted_address.strip(", ")
        
        def calculate_blocks_away(latitude, longitude):
            """
            Inputs: latitude, longitude
                - latitude: float, value from -90 to 90
                - longitude: float, value from -180 to 180
            Outputs: array of blocks away (north/south, east/west) from the intersection of State St and Madison St in Chicago
                - blocks_away_latitude: float, value >= 0
                - direction_latitude: string, either 'north' or 'south'
                - blocks_away_longitude: float, value >= 0
                - direction_longitude: string, either 'east' or 'west'

            Ex. calculate_blocks_away(38, -86)
            Outputs: (2155.309647046862, 'south', 900.8023154952035, 'east')
            """
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
        
        def calculate_latitude_longitude(blocks_away_latitude, direction_latitude, blocks_away_longitude, direction_longitude):
            """
            Inputs: blocks_away_latitude, direction_latitude, blocks_away_longitude, direction_longitude
                - blocks_away_latitude: float, value >= 0
                - direction_latitude: string, either 'north' or 'south'
                - blocks_away_longitude: float, value >= 0
                - direction_longitude: string, either 'east' or 'west'

            Outputs: array of blocks away (north/south, east/west) from the intersection of State St and Madison St in Chicago
                - blocks_away_latitude: float, value >= 0
                - direction_latitude: string, either 'north' or 'south'
                - blocks_away_longitude: float, value >= 0
                - direction_longitude: string, either 'east' or 'west'

            Ex. calculate_latitude_longitude(72.14, 'north', 64.84, 'west')
            Outputs: 6300 West Touhy Avenue, 60714, United States
            """
            latitude = longitude = None

            if direction_latitude == "north":
                latitude = b_latitude + (blocks_away_latitude / bpd_n)
            elif direction_latitude == "south":
                if blocks_away_latitude <= (b_latitude - roosevelt) * bpd_n_mr:
                    latitude = b_latitude - (blocks_away_latitude / bpd_n_mr)
                elif blocks_away_latitude <= (b_latitude - roosevelt) * bpd_n_mr + (roosevelt - cermak) * bpd_n_rc:
                    latitude = roosevelt - (blocks_away_latitude - (b_latitude - roosevelt) * bpd_n_mr) / bpd_n_rc
                elif blocks_away_latitude <= (b_latitude - roosevelt) * bpd_n_mr + (roosevelt - cermak) * bpd_n_rc + (cermak - thirtyfirst) * bpd_n_ct:
                    latitude = cermak - (blocks_away_latitude - (b_latitude - roosevelt) * bpd_n_mr - (roosevelt - cermak) * bpd_n_rc) / bpd_n_ct
                else:
                    latitude = thirtyfirst - (blocks_away_latitude - (b_latitude - roosevelt) * bpd_n_mr - (roosevelt - cermak) * bpd_n_rc - (cermak - thirtyfirst) * bpd_n) / bpd_n

            if direction_longitude == "east":
                longitude = b_longitude + (blocks_away_longitude / bpd_w)
            elif direction_longitude == "west":
                longitude = b_longitude - (blocks_away_longitude / bpd_w)

            return latitude, longitude


        ## this part asks the user for their input and then uses the above functions to carry the required actions
        self.question = input("Type \'blocks\' if you want to get the number of blocks from the center of Chicago, else type \'address\' to get the address given the number of blocks : ")
        if self.question == 'address':
            self.north = input('Number of blocks away to north : ')

            blocks_away_latitude, blocks_away_longitude = 0, 0
            direction_latitude, direction_longitude = 'north', 'east'
            try:
                float(self.north)
                if float(self.north) > 22000 : raise Exception("Too far north :P")
                if self.north != '0' : direction_latitude, blocks_away_latitude = 'north', float(self.north)
            except ValueError:
                raise Exception("Please enter a valid positive number !!")
            self.south = input('Number of blocks away to south : ')
            try:
                float(self.south)
                if float(self.south) > 67000 : raise Exception("Too far south :P")
                if self.south != '0' : direction_latitude, blocks_away_latitude = 'south', float(self.south)
            except ValueError:
                raise Exception("Please enter a valid positive number !!")
            self.east = input('Number of blocks away to east : ')
            try:
                float(self.east)
                if float(self.east) > 95000 : raise Exception("Too far east :P")
                if self.east != '0' : direction_longitude, blocks_away_longitude = 'east', float(self.east)
            except ValueError:
                raise Exception("Please enter a valid positive number !!")
            self.west = input('Number of blocks away to west : ')
            try:
                float(self.west)
                if float(self.east) > 95000 : raise Exception("Too far west :P")
                if self.west != '0' : direction_longitude, blocks_away_longitude = 'west', float(self.west)
            except ValueError:
                raise Exception("Please enter a valid positive number !!")

            if self.north != '0' and self.south != '0' :
                raise Exception("The place cannot be both North and South at the same time !")
            
            if self.east != '0' and self.west != '0' :
                raise Exception("The place cannot be both East and West at the same time !")
            
            lat, long = calculate_latitude_longitude(blocks_away_latitude, direction_latitude, blocks_away_longitude, direction_longitude)
            address = get_address_from_coordinates(lat, long)
            print(address)
            
        elif self.question == 'blocks':
            self.address = input('Give me the address: ')	## Here they should enter the address
            lat, long = get_coordinates(self.address)
            
            blocks_away_lat, direction_lat, blocks_away_lon, direction_lon = calculate_blocks_away(lat, long)
                
            print(f"{blocks_away_lat:.2f} blocks {direction_lat}")
            print(f"{blocks_away_lon:.2f} blocks {direction_lon}")
    
        else :
            raise Exception("IDK what you're saying lol")

    
Chicagoify()