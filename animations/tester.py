from datetime import datetime
from matplotlib.colors import get_named_colors_mapping

import numpy as np

from datetime import datetime

import numpy as np

from tree_animator import TreeAnimator
from utils.color import hsv_to_rgb
import requests
import json

serverURL ='http://172.20.10.6:8082/'

class NewAnimation(TreeAnimator):
    def __init__(self, coords_path=None):
        self.a=0
        super().__init__(coords_path=coords_path)

    def initialize_animation(self):
        self.angle = 0

        self.color_A = (255,0,0) # red
        self.color_B = (0,255,0) # green

    def _get_snake_coords_from_http(self):
        r = requests.get(serverURL)
    
        if r.encoding is None:
            r.encoding = 'utf-8'

        data = []
        for line in r.iter_lines(decode_unicode=True):
            if line:
                data = json.loads(line)
                print(data.get('Coords'))   
                self._snakeCoords = data.get('Coords')

    def calculate_colors(self, xyz_coords, start_time):

        self._get_snake_coords_from_http() #  => [[[x,y,z],[x,y,z],[x,y,z],[x,y,z],[x,y,z]]]

        colors = np.zeros((self.NUM_LIGHTS, 3), dtype=np.uint8)
        for i in range(self.NUM_LIGHTS):
            if self.a % 2 == 0:
                colors[i] = self.color_A
            else:
                colors[i] = self.color_B
        
        


            # capture lights data ((index, r,g,b) * 500lights) in object
            # Inject that into lights display script

        self.color_A = hsv_to_rgb(1,1,1)
        self.color_b = hsv_to_rgb(2,2,2)
        self.a +=1

        self.make_grid()
        return colors

    
    def make_grid(self):
        dataFile = open('coordinates/sample_coords.csv', 'r')

        coordinates = []
        for line in dataFile.readlines():
            coordMap = list(map(int, line.split(',')))
            coordinates.append(coordMap)
            
        
        snakeGameHeight = 20
        snakeGameWidth = 20
            
        maxYCoord = 0
        for c in coordinates:
            if c[2] > maxYCoord:
                maxYCoord = c[2]
                print(maxYCoord)
        
        minYCoord = 0
         
        maxXCoord = 0
        for c in coordinates:
            if c[1] > maxXCoord:
                maxXCoord = c[1]
                
        minXCoord = 0
        for c in coordinates:
            if c[1] > maxXCoord:
                maxXCoord = c[1]
            # if c[1] < minXCoord:
            #     minXCoord = c[1]
            if c[2] > maxYCoord:
                maxYCoord = c[2]
            # if c[2] > minYCoord:
            #     minYCoord = c[2]
        
        yRange = maxYCoord - minYCoord / snakeGameHeight
        xRange = maxXCoord - minXCoord / snakeGameWidth
        yRangeUpper = yRange
        xRangeUpper = xRange
        yRangeLower = 0
        xRangeLower = 0
        

        grid = []

        print(f'Y UPPER {yRangeUpper}')
        print(f'max Y Coord {maxYCoord}')
        print(f'min Y Coord {minYCoord}')
        print(f'Y Range {yRange}')
        while yRangeUpper <= maxYCoord:
            print('Here')
            for coord in coordinates:
                newRow =[]
                if (coord[2]) <= (yRangeUpper) and (coord[2]) >= (yRangeLower):
                    newRow.append(coord)
            grid.append(newRow)
            yRangeUpper += yRange
            yRangeLower += xRange
        
        finalGrid = []
        for row in grid:
            newRow =[]
            for coord in row:
                #print(coord)
                if (coord[1]) <= (xRangeUpper) and (coord[1]) >= (xRangeLower):
                    newRow.append(coord)
            finalGrid.append(newRow)
            xRangeUpper += xRange
            xRangeLower += xRange

            
        print(f'FINAL GRID: {finalGrid}')
            
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
