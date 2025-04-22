from cv2.typing import MatLike
from automaton.feature_detection import match_feature, detect_feature
from limbus.data import Config, Encounter, Encounters, Node, Deviations
from limbus.utils import min_max
from limbus.image import read_image, process_image
from math import dist
from collections import defaultdict
import cv2
import os
import numpy

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

def get_lines_roi(dungeon, nodes) -> list:
    anchor_y_start, anchor_y_end = 0, 2
    h, h1 = nodes[anchor_y_start].y, nodes[anchor_y_end].y+nodes[anchor_y_end].height

    roi = []
    for i in range(0, 7, 3):
        w, w1 = nodes[i].x+nodes[i].width, nodes[i+3].x
        roi.append(dungeon[h:h1, w:w1])

    return roi

def min_distance_lines(node: Node, lines: list, threshold: int=0.1) -> list:
    # works under the assumption that there will always be a line closest to a node
    # else will cause a bug where lines from another area is categorized as the closest line

    distances = []
    for line in lines:
        x1, y1, _, _ = line[0]
        distance = dist(node.get_center(), [x1, y1])
        distances.append(int(distance))

    norm_dist = min_max(distances)
        
    return [i for i,x in enumerate(norm_dist) if x < threshold]

# janky but it works
def find_paths(node: Node, crawler: dict, point: int=0, path: list=[]) -> None:
    point += -1 if node.type == 0 else node.type
    path.append(node.id)

    if len(node.connection) == 0:
        if 0 in path:
            path.remove(0)

        if point < 0:
            point = 0

        crawler[point].append(path.copy())
        
        return None
    
    for i, _ in enumerate(node.connection):
        find_paths(node.connection[i], crawler, point)
        path.pop()

    return None

def translate_line(line: list, node: Node):
    for x1, y1, x2, y2 in line:
        x = node.x + node.width + x1
        y = node.y + y1
        xt = node.x + node.width + x2
        yt = node.y + y2

        return [[x, y, xt, yt]]
    
def find_deviation(line, threshold=15) -> Deviations:
    _, y1, _, y2 = line[0]

    deviation = y1 - y2
    
    if abs(deviation) <= threshold:
        return Deviations.MIDDLE
    elif deviation > 0:
        return Deviations.TOP
    elif deviation < 0:
        return Deviations.BOTTOM
    
    return None

class Dungeon:
    def __init__(self, dungeon: MatLike, col: int=4, row: int=3, config: Config=None, encounters_dir: str="", edge_threshold: int=10):
        self.dungeon: MatLike = dungeon
        self.col: int = col
        self.row: int = row
        self.config: Config = config
        self.encounters_dir = encounters_dir
        self.edge_threshold = edge_threshold
        self.nodes: list = []
        self.lines: list = []
        self.encounters: list = [0 for _ in range(len(Encounters))]

        self.map_encounters(self.encounters_dir)

    def map_encounters(self, dir: str):
        for file in os.listdir(dir):
            image = read_image(f"{dir}\{file}")
            image = process_image(image, ["gray"])
            _, descriptor = detect_feature(image, self.edge_threshold)

            name = file.split(".")[0]
            encounter = Encounter(name, Encounters[name.upper()].value, descriptor)

            self.encounters[Encounters[name.upper()].value] = encounter

        return self.encounters
    
    def map_connections(self, stride: int=3) -> list:
        for i, node in enumerate(self.nodes):
            if node.type == -1: 
                continue
            if i+stride >= len(self.nodes): 
                break

            connections = min_distance_lines(node, self.lines)

            for c in connections:
                direction = find_deviation(self.lines[c])
                node.add_connection(self.nodes[node.id+direction.value+2])

        return self.nodes

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
                    node = Node(index, name, -1, x_start, y_start, width, height, connection=[])
                    self.nodes.append(node)

                    y_start += y_stride
                    index += 1
                y_start = self.config.y_start
                x_start += x_stride

        dungeon = process_image(self.dungeon, ["gray"])
        for node in self.nodes:
            img = dungeon[node.y:node.y+node.height, node.x:node.x+node.width]
            _, descriptor = detect_feature(img, self.edge_threshold)

            if descriptor is None or len(descriptor) < 20:
                continue

            candidates = []
            for encounter in self.encounters:
                matches = match_feature(encounter.descriptor, descriptor, sort=True)
                distances = [match.distance for match in matches[:10]]
                candidates.append(numpy.mean(distances))
            
            event = numpy.argmin(candidates)
            node.type = event

        return self.nodes
    
    def find_lines(self):
        img = process_image(self.dungeon, ["gray", "thresh", "canny"])

        lines_roi = get_lines_roi(img, self.nodes)

        kwargs = {
            "rho": 1,
            "theta": numpy.pi / 180,
            "threshold": 50,
            "minLineLength": 25,
            "maxLineGap": 50
        }

        index = 0
        for roi in lines_roi:
            hough_lines = cv2.HoughLinesP(roi, **kwargs)

            for i, line in enumerate(hough_lines):
                has_dupe = check_duplicate(i, hough_lines, 50)

                if has_dupe is False:
                    self.lines.append(translate_line(line, self.nodes[index]))

            index += 3

        return self.lines

    def crawl(self) -> list:
        """
        Returns the id of nodes with shortest path
        """
        nodes = [node for node in self.nodes if node.id <= 3]
        temp = Node(0, "node_0", 0, 0, 0, 0, 0, nodes)
        crawler = defaultdict(list)

        find_paths(temp, crawler)

        return crawler[sorted(crawler)[0]][0]
