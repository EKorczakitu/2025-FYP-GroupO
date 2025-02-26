from util import os, cv2, plt, pd
from util.img_util import readImageFile, saveImageFile, ImageDataLoader
from util.inpaint_util import removeHair

# change the following paths according to your setup
data_dir = './data'
save_dir = './result'
csv_path = './data-student.csv'

group_id = 'O'

# read CSV file to get the image data
df = pd.read_csv(csv_path, delimiter=',')

# filtering data according to group_id
image_paths = df[df['Group_ID'] == group_id]['File_ID'].values

# create the dataloader class and use it for iteration
for file_name, img_rgb, img_gray in ImageDataLoader(image_paths=image_paths, directory=data_dir, transform=None):
    # create a folder for each file_name inside save_dir
    image_save_dir = os.path.join(save_dir, file_name[:-4])
    if not os.path.exists(image_save_dir):
        os.makedirs(image_save_dir)

    # apply hair removal
    blackhat, thresh, img_out = removeHair(img_rgb, img_gray)

    # list of images and titles
    images = [img_rgb, img_gray, blackhat, thresh, img_out]
    titles = ["Original Image", "Grayscale Image", "BlackHat Image", "Thresholded Mask", "Inpainted Image"]

    for (image, title) in zip(images, titles):
        # save the processed image into its folder
        saveImageFile(image, os.path.join(image_save_dir, f"{title.replace(' ', '_').lower()}.png"))