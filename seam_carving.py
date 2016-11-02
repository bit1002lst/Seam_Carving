import cv2
import numpy


def find_min_seam(src, line, dst):
    # calc grad
    x = cv2.Sobel(src, cv2.CV_16S, 0, 1)
    y = cv2.Sobel(src, cv2.CV_16S, 1, 0)
    abs_x = cv2.convertScaleAbs(x)
    abs_y = cv2.convertScaleAbs(y)
    dst1 = cv2.addWeighted(abs_x, 0.5, abs_y, 0.5, 0)
    # find_line
    dst = src.copy()
    min_energy_line = 0
    for i in range(dst1.shape[0]):
        i_org = i
        energy = int(dst1[i, 0])
        for j in range(1, dst1.shape[1]):
            if i == 0:
                tmp = [dst1[i, j], dst1[i+1, j]]
                i += tmp.index(min(tmp))
            elif i == dst1.shape[0] - 1:
                tmp = [dst1[i - 1, j], dst1[i, j]]
                i += tmp.index(min(tmp)) - 1
            else:
                tmp = [dst1[i-1, j], dst1[i, j], dst1[i+1, j]]
                i += tmp.index(min(tmp)) - 1
            energy = min(tmp) + energy
        if 'min_energy' in locals():
            if energy < min_energy:
                min_energy = energy
                min_energy_line = i
        else:
            min_energy = energy
    print min_energy_line

    if dst is not None:
        # draw line
        dst = src.copy()

        for j in range(src.shape[1]):
            if min_energy_line == 0:
                tmp = [src[min_energy_line, j], src[min_energy_line + 1, j]]
                min_energy_line += tmp.index(min(tmp))
            elif min_energy_line == src.shape[0] - 1:
                tmp = [src[min_energy_line - 1, j], src[min_energy_line, j]]
                min_energy_line += tmp.index(min(tmp)) - 1
            else:
                tmp = [src[min_energy_line - 1, j], src[min_energy_line, j], src[min_energy_line + 1, j]]
                min_energy_line += tmp.index(min(tmp)) - 1
            line.append([min_energy_line, j])
            dst[min_energy_line, j] = 255


def delete_seam_line(src, line, dst):
    for j in range(dst.shape[1]):
        for i in range(dst.shape[0]):
            if i < line[j][0]-1:
                dst[i][j] = src[i][j]
            elif i > line[j][0]:
                dst[i][j] = src[i+1][j]
            elif i == line[j][0]:
                dst[i][j] = (numpy.int16(src[i][j]) + src[i+1][j])/2.0
            else:
                dst[i][j] = (numpy.int16(src[i][j]) + src[i-1][j])/2.0


def main():
    img = cv2.imread("/home/lst/my_code/source/img/lena.jpg")
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    if gray.shape[0] > 2560:
        small = cv2.resize(gray, (0,0), fx=0.3, fy=0.3)
    else:
        small = gray.copy()
    cv2.namedWindow("src")
    cv2.imshow("src", small)

    seam_line = []
    dst2 = numpy.zeros([small.shape[0], small.shape[1], 1], numpy.uint8)
    find_min_seam(small, seam_line, dst2)
    print small.shape

    dst = small.copy()
    while dst.shape[0] > 505:
        print dst.shape[0]
        show_line = numpy.zeros([dst.shape[0], dst.shape[1], 1], numpy.int)
        find_min_seam(dst, seam_line, show_line)

        dst3 = numpy.zeros([dst.shape[0] - 1, dst.shape[1], 1], numpy.uint8)
        delete_seam_line(dst, seam_line, dst3)
        dst = dst3.copy()
    # dst2 = [[0 for i in range(dst1.shape[1])] for i in range(dst1.shape[0]-1)]

    cv2.namedWindow("delete_seam")
    cv2.imshow("delete_seam", dst)
    print dst.shape

    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
