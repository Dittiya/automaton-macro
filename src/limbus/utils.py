import numpy

def min_max(object: list) -> list:
    object = numpy.array(object)
    norm = (object - object.min()) / (object.max() - object.min())

    return norm.tolist()