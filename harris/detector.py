import cv2 as cv
import numpy as np
import argparse


class HarrisCornerDetector:
    def __init__(self, sigma, k, threshold, kernel_size):
        self.sigma = sigma
        self.k = k
        self.threshold = threshold
        self.kernel_size = kernel_size

    def detect(self, image):
        image_gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)

        Ix, Iy = np.gradient(image_gray)
        R = self.compute_response(Ix, Iy)
        R = self.nms(R)
        y, x = np.nonzero(R)

        for corner_y, corner_x in zip(y, x):
            cv.circle(image, (corner_x, corner_y), 3, (0, 0, 255), -1)

        cv.imshow("Harris Corner Detector", image)
        cv.waitKey(0)

    def compute_response(self, Ix, Iy):
        Ix2 = Ix ** 2
        Iy2 = Iy ** 2
        IxIy = Ix * Iy

        kernel_shape = (self.kernel_size, self.kernel_size)
        Ix2 = cv.GaussianBlur(Ix2, kernel_shape, self.sigma)
        Iy2 = cv.GaussianBlur(Iy2, kernel_shape, self.sigma)
        IxIy = cv.GaussianBlur(IxIy, kernel_shape, self.sigma)

        detA = Ix2 * Iy2 - IxIy ** 2
        traceA = Ix2 + Iy2
        R = detA - self.k * traceA ** 2

        return R

    def nms(self, R):
        R_threshold = cv.threshold(R, self.threshold, 255, cv.THRESH_BINARY)[1]
        R_dilate = cv.dilate(R, np.ones((3, 3)))
        R = R_threshold * (R >= R_dilate)

        return R


if __name__ == "__main__" :
    arg_parser = argparse.ArgumentParser(description = "Harris Corner Detector")
    arg_parser.add_argument("-i", "--image_path", type = str,
                        help = "file path of the input color JPEG image", required=True)
    arg_parser.add_argument("-s", "--sigma", type = float, default = 1.0,
                        help = "sigma value for Gaussain filter (default = 1.0)")
    arg_parser.add_argument("-k", "--kappa", type = float, default = 0.04,
                        help = "kappa value for R matrix (default = 0.04)")
    arg_parser.add_argument("-t", "--threshold", type = float, default = 1e6,
                        help = "threshold value for corner detection (default = 1e6)")
    arg_parser.add_argument("-ks", "--kernel_size", type = int, default = 3,
                        help = "window size for Gaussian filter (default = 3)")
    args = arg_parser.parse_args()

    image = cv.imread(args.image_path)

    hcd = HarrisCornerDetector(args.sigma, args.kappa, args.threshold, args.kernel_size)
    hcd.detect(image)
