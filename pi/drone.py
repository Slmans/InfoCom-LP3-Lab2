from flask import Flask, request
from flask_cors import CORS
import subprocess
import  requests


app = Flask(__name__)
CORS(app, supports_credentials=True)
app.secret_key = 'dljsaklqk24e21cjn!Ew@@dsa5'


#Give a unique ID for the drone !!DONE!!
#===================================================================
myID = "DRONE_1"
#===================================================================

# Get initial longitude and latitude the drone
#===================================================================
init_longitude = 13.21008
init_latitude = 55.71106
try:
    f = open("kordinatlar.txt", "x")
    f.write(init_longitude +"," + init_latitude)
    f.close()
    current_latitude = init_latitude
    current_longitude = init_longitude
except:
    with open("kordinatlar.txt", "r") as data_file:
        for line in data_file:
            data = line.split(",")
            current_longitude = data[0]
            current_latitude = data[1]
#===================================================================

drone_info = {'id': myID,
                'longitude': current_longitude,
                'latitude': current_latitude,
                'status': 'idle'
            }

# Fill in the IP address of server !!DONE!! , and send the initial location of the drone to the SERVER
#===================================================================
SERVER="http://192.168.0.2:5001/drone"
with requests.Session() as session:
    resp = session.post(SERVER, json=drone_info)
#===================================================================

@app.route('/', methods=['POST'])
def main():
    coords = request.json
    # Get current longitude and latitude of the drone 
    #===================================================================
    with open("kordinatlar.txt", "r") as data_file:
        for line in data_file:
            data = line.split(",")
            current_longitude = data[0]
            current_latitude = data[1]
    #===================================================================
    from_coord = coords['from']
    to_coord = coords['to']
    subprocess.Popen(["python3", "simulator.py", '--clong', str(current_longitude), '--clat', str(current_latitude),
                                                 '--flong', str(from_coord[0]), '--flat', str(from_coord[1]),
                                                 '--tlong', str(to_coord[0]), '--tlat', str(to_coord[1]),
                                                 '--id', myID
                    ])
    return 'New route received'

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
