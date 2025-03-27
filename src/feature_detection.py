import cv2 as cv
from cv2.typing import MatLike

def detect_feature(img: MatLike, edge_threshold=31):
    detector = cv.ORB_create(edgeThreshold=edge_threshold)
    keypoints, descriptor = detector.detectAndCompute(img, None)

    return keypoints, descriptor

def match_feature(descriptor_query, descriptor_train, sort=False):
    matcher = cv.BFMatcher(cv.NORM_HAMMING, crossCheck=True)
    matches = matcher.match(descriptor_query, descriptor_train)

    if sort == True:
        matches = sorted(matches, key=lambda x:x.distance)
    
    return matches
