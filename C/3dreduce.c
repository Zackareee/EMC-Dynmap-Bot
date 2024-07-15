#include <stdio.h>
#include <stdlib.h>

int min1d(int *array, int width) {
    int min = array[0];
    for (int i = 1; i < width; i++) {
        if (array[i] < min) {
            min = array[i];
        }
    }
    return min;
}

int min2d(int **array, int width, int height) {
    int min = array[0][0];
    int current;
    for (int i = 0; i < height; i++) {
        current = min1d(array[i], width);
        if (current < min) {
            min = current;
        }
    }
    return min;
}

int min3d(int ***array, int width, int height, int depth) {
    int min = array[0][0][0];
    int current;
    for (int i = 0; i < depth; i++) {
        current = min2d(array[i], width, height);
        if (current < min) {
            min = current;
        }
    }
    return min;
}




int max1d(int *array, int width) {
    int max = array[0];
    for (int i = 1; i < width; i++) {
        if (array[i] > max) {
            max = array[i];
        }
    }
    return max;
}

int max2d(int **array, int width, int height) {
    int max = array[0][0];
    int current;
    for (int i = 0; i < height; i++) {
        current = max1d(array[i], width);
        if (current > max) {
            max = current;
        }
    }
    return max;
}

int max3d(int ***array, int width, int height, int depth) {
    int max = array[0][0][0];
    int current;
    for (int i = 0; i < depth; i++) {
        current = max2d(array[i], width, height);
        if (current > max) {
            max = current;
        }
    }
    return max;
}


int main() {
    return 0;
}

