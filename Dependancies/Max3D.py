import ctypes

soFile = './C/3dreducelib.so'
mainFile = ctypes.cdll.LoadLibrary(soFile)
max1d = mainFile.max1d
max2d = mainFile.max2d
max3d = mainFile.max2d

def max1d(array):
    array_type = ctypes.c_int * len(array)
    c_array = array_type(*array)
    return mainFile.max1d(c_array, len(array))


def max2d(array):
    height = len(array)
    width = len(array[0])
    
    row_pointers_type = ctypes.POINTER(ctypes.c_int) * height
    row_pointers = row_pointers_type()
    
    for i in range(height):
        row_array_type = ctypes.c_int * width
        row_array = row_array_type(*array[i])
        row_pointers[i] = row_array
    
    return mainFile.max2d(row_pointers, width, height)


def max3d(array):
    depth = len(array)
    height = len(array[0])
    width = len(array[0][0])
    
    plane_pointers_type = ctypes.POINTER(ctypes.POINTER(ctypes.c_int)) * depth
    plane_pointers = plane_pointers_type()
    
    for i in range(depth):
        row_pointers_type = ctypes.POINTER(ctypes.c_int) * height
        row_pointers = row_pointers_type()
        
        for j in range(height):
            row_array_type = ctypes.c_int * width
            row_array = row_array_type(*array[i][j])
            row_pointers[j] = row_array
        
        plane_pointers[i] = row_pointers
    
    return mainFile.max3d(plane_pointers, width, height, depth)

