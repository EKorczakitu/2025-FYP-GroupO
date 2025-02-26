from util import cv2

def removeHair(img_org, img_gray, kernel_size=25, threshold=10, radius=4):
    """
    Removes hair from the image using morphological filtering and inpainting.

    Args:
        img_org (ndarray): The original RGB image.
        img_gray (ndarray): The grayscale version of the original image.
        kernel_size (int): The size of the kernel used for the morphological operation (default is 25)
        threshold (int): The threshold value used for binarizing the hair contours (default is 10)
        radius (int): The radius used for inpainting the image (default is 4)
    
    Returns:
        tuple: A tuple containing:
            - blackhat (ndarray): The result of the blackHat morphological operation.
            - thresh (ndarray): The thresholded mask used for inpainting.
            - img_out (ndarray): The inpainted image with hair removed.
    """
    # the kernel is used to define the size and shape of the area over which the 'cv2.MORPH_BLACKHAT' is applied
    # larger kernel will affect a larger portion of the image, while a smaller kernel focuses on finer details
    kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (kernel_size, kernel_size))

    # grayscaling the image using the kernel to detect the contours of the hair
    # the result is an image where dark hair stands out in white on a mostly black background
    blackhat = cv2.morphologyEx(img_gray, cv2.MORPH_BLACKHAT, kernel)

    # after the BlackHat operation, the contours of the hair are intensified, but we need to separate them clearly from the background
    # thresholding is used to create a mask that highlights the hair as a binary image (hair = white, background = black)
    _, thresh = cv2.threshold(blackhat, threshold, 255, cv2.THRESH_BINARY)

    # inpainting is used to fill in the removed hair regions
    # the cv2.inpaint() function fills in the detected hair regions using neighboring pixels to make the inpainting as seamless as possible
    img_out = cv2.inpaint(img_org, thresh, radius, cv2.INPAINT_TELEA)

    return blackhat, thresh, img_out