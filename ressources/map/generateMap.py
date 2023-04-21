import numpy as np
import cv2 as cv

if (__name__ == "__main__"):
    map = np.ones((20, 20))
    map[11:14, 4:14] = 0
    map[4:14, 11:14] = 0
    map = map * 255
    print(map)
    cv.imwrite("./map1.bmp", map)

    # scale the map to 50x50 pixels for display
    scale_ratio = 50
    resizedMap = cv.resize(map, None, fx=scale_ratio, fy=scale_ratio, interpolation=cv.INTER_NEAREST)
    cv.imshow("map", resizedMap)
    cv.waitKey(0)
    cv.destroyAllWindows()