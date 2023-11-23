import cv2


def detect_contours(img):
    blurred_img = cv2.GaussianBlur(img, (5, 5), 0)
    edges = cv2.Canny(blurred_img, 50, 150)
    return edges


model = cv2.imread('images/1.png', 0)
model = cv2.resize(model, (600, 800))
cv2.imshow('Edges', detect_contours(model))
cv2.waitKey(0)
cv2.destroyAllWindows()
