import serial 
from datetime import datetime, timedelta, timezone 

gps = serial.Serial("COM3", baudrate=9600)

lat_data = []
lat_avg = 0
long_data = []
long_avg = 0

arr_len = 60


def save_data(current_time, lat_avg, long_avg):
    """Saves the average latitude and longitude to a file in decimal degrees"""
    with open("gps_data.txt", "a") as f:
        f.write(f"{current_time}, {lat_avg}, {long_avg}\n")

def save_geo_data(lat, long):
    """Saves the latitude and longitude to a file in decimal degrees"""
    with open("geo_data.txt", "a") as f:
        f.write(f"{lat}, {long}\n")
 
def convert_cordinates(lat, long):
    """Converts the latitude and longitude from degrees and minutes to decimal degrees"""
    # Converts the latitude and longitude to decimal degrees
    lat_degrees = lat[0:2]
    long_degrees = long[0:3]

    # Gets the decimal minutes from data, 
    lat_decimal_min = float(lat[2:])
    long_decimal_min = float(long[3:])

    # And then converts the decimal minutes to decimal degrees
    lat_decimal_degrees = lat_decimal_min/60
    long_decimal_degrees = long_decimal_min/60

    dec_lat = float(lat_degrees) + lat_decimal_degrees
    dec_long = float(long_degrees) + long_decimal_degrees

    return dec_lat, dec_long

init_program = True
running = True

while running:
    line = gps.readline().decode()
    data = line.split(",")
    if data[0] == "$GPRMC":
        if data[2] == "A":
            print(data)
            # If it is first time running loop, initializes the timestamp 
            if init_program:
                last_timestamp = datetime.strptime(data[1], "%H%M%S.%f")
                init_program = False

            # Get latitude and longitude
            decimal_degree_latitude, decimal_degree_longitude = convert_cordinates(data[3], data[5])

            save_geo_data(decimal_degree_latitude, decimal_degree_longitude)
            
            # Appends the latitude and longitude to the lists       
            lat_data.append(decimal_degree_latitude)
            long_data.append(decimal_degree_longitude)
            if len(lat_data) > arr_len:
                lat_data.pop(0)
                long_data.pop(0)

            # Calculates the average latitude and longitude
            MA60_lat = sum(lat_data) / len(lat_data)
            MA60_lon = sum(long_data) / len(long_data)

            current_time = datetime.strptime(data[1], "%H%M%S.%f")

            if current_time - last_timestamp >= timedelta(minutes=1):
                save_data(current_time, MA60_lat, MA60_lon)
                last_timestamp = current_time

            print(f'Latitude: {MA60_lat}, Longitude: {MA60_lon} n={len(lat_data)}')


        