# this is the main file where the functions exist

from geopy.geocoders import Nominatim

class Constants():
    def __init__(self):
        self.mpd = (24901.92 / 360)
        self.n_mr = self.mpd * 12
        self.n_rc = self.mpd * 10
        self.n_ct = self.mpd * 9
        self.n = self.mpd * 8
        self.c = self.mpd * 8

        self.roosevelt = 41.8674224
        self.cermak = 41.8528516
        self.thirtyfirst = 41.8382902

        self.b_lat = 41.88205727768228
        self.b.long = -87.62783047240069

c = Constants()

class Chicagoify:
    """
    This converts a given address into the number of blocks it is away from the center of Chicago, and vice versa!


    """

    def __init__(self):

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
            self.address = self.question

Chicagoify()
