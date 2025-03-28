from cv2.typing import MatLike
from feature_detection import match_feature, detect_feature
from limbus.data import Config, Encounter, Encounters, Node
import cv2 as cv
import os
import numpy as np

class Dungeon:
    def __init__(self, col: int=4, row: int=3, config: Config=None, encounters_dir: str=""):
        self.col: int = col
        self.row: int = row
        self.config: Config = config
        self.encounters_dir = encounters_dir
        self.edge_threshold = 10
        self.nodes: list = []
        self.encounters: list = [0 for _ in range(len(Encounters))]

        self.build_encounters(self.encounters_dir)

    def build_encounters(self, dir: str):
        for file in os.listdir(dir):
            image = cv.imread(f"{dir}\\{file}", cv.IMREAD_GRAYSCALE)
            _, descriptor = detect_feature(image, self.edge_threshold)

            name = file.split(".")[0]
            encounter = Encounter(name, Encounters[name.upper()].value, descriptor)

            self.encounters[Encounters[name.upper()].value] = encounter

        return self.encounters

    def map(self, image: MatLike):
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
            img = image[node.y:node.y+node.height, node.x:node.x+node.width]
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

    def crawl(self):
        pass
