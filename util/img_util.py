from util.libraries import cv2, os, random

def readImageFile(file_path):
    """
    Reads an image from the specified file path and converts it to RGB and grayscale.

    Args:
        file_path (str): The path to the image file to be read.

    Returns:
        tuple: A tuple containing:
            - img_rgb (ndarray): The image in RGB format.
            - img_gray (ndarray): The image in grayscale format.
    
    Raises:
        ValueError: If the image cannot be loaded from the file path.
    """
    # the function reads the image and returns it as a NumPy array in BGR
    img_bgr = cv2.imread(file_path)
    
    # if the file doesn't exist/the file is corrupted/the file is not a valid image, it will return None
    if img_bgr is None:
        raise ValueError(f"Unable to load image at {file_path}")
    
    # the function returns the image in RGB format
    img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)

    # the function returns the grayscale version of the image
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2GRAY)

    return img_rgb, img_gray


def saveImageFile(img_rgb, file_path):
    """
    Saves the provided image in RGB format to the specified file path.

    Args:
        img_rgb (ndarray): The image in RGB format to be saved.
        file_path (str): The path where the image will be saved.
    
    Returns:
        bool: True if the image was saved successfully, false otherwise.
    
    Raises:
        Exception: If an error occurs during the saving process.
    """
    try:
        # The first argument to cv2.imwrite() is the file path (file_path), where the image should be saved
        # The second argument is the image, where the it's being converted from RGB to BGR color format because OpenCV uses BGR by default
        # It also returns a True of False value to verify that the image was saved properly
        success = cv2.imwrite(file_path, cv2.cvtColor(img_rgb, cv2.COLOR_RGB2BGR))
        if not success:
            print(f"Failed to save the image to {file_path}")
        return success

    except Exception as e:
        print(f"Error saving the image: {e}")
        return False

class ImageDataLoader:
    def __init__(self, image_paths, directory, transform=None):
        self.directory = directory
        self.transform = transform # this could be for data augmentation, resizing, or normalizing the image before using it in a machine learning model
        self.image_paths = image_paths
        self.file_dict = {}

        for file in os.listdir(directory): # this function returns a list of all files and directories in the specified directory
            if file in self.image_paths: # to filter out not needed images
                img_rgb, img_gray = readImageFile(os.path.join(self.directory, file)) # read image
                
                # apply transformation if needed
                if self.transform:
                    img_rgb = self.transform(img_rgb)
                    img_gray = self.transform(img_gray)
                
                # store images
                self.file_dict[file] = [img_rgb, img_gray]

        # if no images were found in the directory, it raises an error
        if not self.file_dict:
            raise ValueError("No image files found in the directory.")

        # stores the total number of image
        self.num_batches = len(self.file_dict)

    def __len__(self):
        # a special method that allows to use the len() function on an instance of the ImageDataLoader class
        return self.num_batches

    def __iter__(self):
        # this makes the ImageDataLoader class an iterable object
        for file_name, (img_rgb, img_gray) in self.file_dict.items():
            yield file_name, img_rgb, img_gray