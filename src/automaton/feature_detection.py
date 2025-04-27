import cv2 as cv
from cv2.typing import MatLike

def detect_feature(img: MatLike, edge_threshold=31):
    detector = cv.ORB_create(edgeThreshold=edge_threshold)
    keypoints, descriptor = detector.detectAndCompute(img, None)

    return keypoints, descriptor

def match_feature(descriptor_query, descriptor_train, cross_check: bool=True, sort: bool=False):
    matcher = cv.BFMatcher(cv.NORM_HAMMING, crossCheck=cross_check)
    matches = matcher.match(descriptor_query, descriptor_train)

    if sort == True:
        matches = sorted(matches, key=lambda x:x.distance)
    
    return matches

def detect_object(target_descriptor, train_descriptor, ratio: float=0.75, min: int=10) -> bool:
    matcher = cv.BFMatcher(cv.NORM_HAMMING)
    matches = matcher.knnMatch(target_descriptor, train_descriptor, k=2)

    candidates = []
    for m, n in matches:
        if m.distance < ratio*n.distance:
            candidates.append([m])

    return len(candidates) > min

def match_feature_knn(target_descriptor, train_descriptor, ratio: float=0.75) -> bool:
    matcher = cv.BFMatcher(cv.NORM_HAMMING)
    matches = matcher.knnMatch(target_descriptor, train_descriptor, k=2)

    candidates = []
    for m, n in matches:
        if m.distance < ratio*n.distance:
            candidates.append([m])

    return len(candidates)
