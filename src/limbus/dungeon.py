from cv2.typing import MatLike
from feature_detection import match_feature, detect_feature
from limbus.data import Config, Encounter, Encounters, Node
from math import dist
import cv2 as cv
import os
import numpy as np

def check_duplicate(index: int, lines: list, min_distance: int=50) -> bool:
    """
    Check duplicate lines
    """
    has_duplicate = False
    query = lines[index]

    min_dst = float("inf")
    for i in range(0, index):
        dst = dist(query.reshape(-1), lines[i].reshape(-1))

        if dst < min_dst:
            min_dst = dst
    
    if min_dst < min_distance:
        has_duplicate = True

    return has_duplicate

def get_lines_roi(dungeon, nodes):
    anchor_y_start, anchor_y_end = 0, 2
    h, h1 = nodes[anchor_y_start].y, nodes[anchor_y_end].y+nodes[anchor_y_end].height

    roi = []
    for i in range(0, 7, 3):
        w, w1 = nodes[i].x+nodes[i].width, nodes[i+3].x
        roi.append(dungeon[h:h1, w:w1])

    return roi

def translate_line(line: list, node: Node):
    for x1, y1, x2, y2 in line:
        x = node.x + node.width + x1
        y = node.y + y1
        xt = node.x + node.width + x2
        yt = node.y + y2

        return [[x, y, xt, yt]]

class Dungeon:
    def __init__(self, dungeon: MatLike, col: int=4, row: int=3, config: Config=None, encounters_dir: str="", edge_threshold: int=10):
        self.dungeon: MatLike = dungeon
        self.col: int = col
        self.row: int = row
        self.config: Config = config
        self.encounters_dir = encounters_dir
        self.edge_threshold = edge_threshold
        self.nodes: list = []
        self.encounters: list = [0 for _ in range(len(Encounters))]

        self.map_encounters(self.encounters_dir)

    def map_encounters(self, dir: str):
        for file in os.listdir(dir):
            image = cv.imread(f"{dir}\\{file}", cv.IMREAD_GRAYSCALE)
            _, descriptor = detect_feature(image, self.edge_threshold)

            name = file.split(".")[0]
            encounter = Encounter(name, Encounters[name.upper()].value, descriptor)

            self.encounters[Encounters[name.upper()].value] = encounter

        return self.encounters

    def map(self):
        if self.config is not None:
            x_start = self.config.x_start
            y_start = self.config.y_start
            width = self.config.width
            height = self.config.height
            x_stride = self.config.x_stride
            y_stride = self.config.y_stride
            index = 1

            for _ in range(self.col):
                for _ in range(self.row):
                    name = f"Node_{index}"
                    node = Node(name, -1, x_start, y_start, width, height, connection=[])
                    self.nodes.append(node)

                    y_start += y_stride
                    index += 1
                y_start = self.config.y_start
                x_start += x_stride

        for node in self.nodes:
            img = self.dungeon[node.y:node.y+node.height, node.x:node.x+node.width]
            _, descriptor = detect_feature(img, self.edge_threshold)

            if descriptor is None:
                continue

            candidates = []
            for encounter in self.encounters:
                matches = match_feature(encounter.descriptor, descriptor, True)
                distances = [match.distance for match in matches[:10]]
                candidates.append(np.mean(distances))
            
            event = np.argmin(candidates)
            node.type = event

        return self.nodes
    
    def map_connections(self):
        img = self.dungeon
        img = cv.GaussianBlur(img, (3,3), 0)
        img = cv.Canny(img, 15, 75)

        lines_roi = get_lines_roi(img, self.nodes)

        kwargs = {
            "rho": 1,
            "theta": np.pi / 180,
            "threshold": 35,
            "minLineLength": 25,
            "maxLineGap": 60
        }

        connections = []
        index = 0
        for roi in lines_roi:
            lines = cv.HoughLinesP(roi, **kwargs)

            for i, line in enumerate(lines):
                has_dupe = check_duplicate(i, lines, 50)

                if has_dupe is False:
                    connections.append(translate_line(line, self.nodes[index]))

            index += 3

        return connections

    def crawl(self):
        pass
