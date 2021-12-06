from datetime import datetime
from matplotlib.colors import get_named_colors_mapping

import numpy as np

from datetime import datetime

import numpy as np

from tree_animator import TreeAnimator
from utils.color import hsv_to_rgb
import requests
import json
import ast

IP_ADDRESS = '192.168.1.72'
PORT = 8080
serverURL =f'http://{IP_ADDRESS}:{PORT}/'

class NewAnimation(TreeAnimator):
    def __init__(self, coords_path=None):
        self.coordinates=[]
        self.get_tree_coordinates_as_list() # populates self.coordinates
        self.snakeCoordinates = [] # populated by get_snake_coords_from_http() every frame
        super().__init__(coords_path=coords_path)

    def initialize_animation(self):
        self.angle = 0

        self.color_A = (255,0,0) # red
        self.color_B = (0,255,0) # green

    def get_snake_coords_from_http(self):
        r = requests.get(serverURL)
    
        if r.encoding is None:
            r.encoding = 'utf-8'

        data = []

        for line in r.iter_lines(decode_unicode=True):
            if line:
                data = json.loads(line)
                print(f'HERE IS THE DATA: {data}')   
                print(data.get('coords'))
                print(type(data.get('coords')))
                coordsMap = ast.literal_eval(data.get('coords'))
                snakeCoordinates = coordsMap['coordinates']
                self.snakeCoords = snakeCoordinates

    def calculate_colors(self, xyz_coords, start_time):

        self.get_snake_coords_from_http() #  => [[[x,y,z],[x,y,z],[x,y,z],[x,y,z],[x,y,z]]]

        colors = np.zeros((self.NUM_LIGHTS, 3), dtype=np.uint8)
        for i in range(self.NUM_LIGHTS):
            if 0 % 2 == 0:
                colors[i] = self.color_A
            else:
                colors[i] = self.color_B
        

        self.color_A = hsv_to_rgb(1,1,1)
        self.color_b = hsv_to_rgb(2,2,2)

        return colors

    
    def get_tree_coordinates_as_list(self):

        dataFile = open('coordinates/sample_coords.csv', 'r')
        
        for line in dataFile.readlines():
            coordMap = list(map(int, line.split(',')))
            self.coordinates.append(coordMap)
            
        
            
    def snake_coords_to_light_index(self, snakeCoords):  # => list[lightIndexes]
                
        # Which snake coord corresponds to which light index
        # coords max, min for x, y,
        # width is (max - min) / 20 = box width
        # Width for each horizontal band

        maxXCoord = 0
        maxYCoord = 0
        minXCoord = 0
        minYCoord = 0

        for c in snakeCoords:
           # print(c[2])
            if int(c[1]) > maxXCoord:
                maxXCoord = int(c[1])
            # if int(c[1]) < minXCoord:
            #     minXCoord = int(c[1])
            if int(c[2]) > maxYCoord:
                maxYCoord = int(c[2])
            # if int(c[2]) < minYCoord:
            #     print(f'HEREHERHE {c[2]}')
            #     minYCoord = int(c[2])
            

if __name__ == "__main__":
    anim = NewAnimation()

    anim.animation_loop()
