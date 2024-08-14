import cv2 
from helper_func import encode, decode_image

img = cv2.imread(r"Stenography\L._Hamway_Recommendation.tiff", 0)

hidden_message = r"Hidden link https://www.google.com/"

encoded_image = encode(img, hidden_message)

cv2.imwrite("coded_image.png", encoded_image)

image_encoded = cv2.imread("coded_image.png")
decoded_message = decode_image(image_encoded)

print("Decoded message - ", decoded_message)
cv2.imshow("Original Image", img)
cv2.imshow("Encoded image", encoded_image)
cv2.waitKey(0)
cv2.destroyAllWindows()