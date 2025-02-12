from util.libraries import os, cv2, plt, pd
from util.libraries import cv2
from util.img_util import readImageFile, saveImageFile, ImageDataLoader
from util.inpaint_util import removeHair

data_dir = './data'
save_dir = './result'
csv_path = './data-student.csv'
group_id = 'O'

# read CSV file to get the image data
df = pd.read_csv(csv_path, delimiter=';')

# filtering data according to group_id
image_paths = df[df['Group_ID'] == group_id]['File_ID'].head(15).values

resize = lambda img: cv2.resize(img, (256, 256))
image_loader = ImageDataLoader(image_paths=image_paths, directory=data_dir, transform=None)

for file_name, img_rgb, img_gray in image_loader:
    # apply hair removal
    blackhat, thresh, img_out = removeHair(img_rgb, img_gray)

    # Plotting
    fig, axes = plt.subplots(2, 2, figsize=(10, 8))

    # List of images and titles
    images = [img_rgb, blackhat, thresh, img_out]
    titles = ["Original Image", "BlackHat Image", "Thresholded Mask", "Inpainted Image"]
    
    for idx, (image, title) in enumerate(zip(images, titles)):
        ax = axes[idx // 2, idx % 2]
        ax.imshow(image, cmap="gray" if title != "Original Image" else None)
        ax.set_title(title)
        ax.axis("off")
    
    # adjust layout and show plot
    plt.tight_layout()
    plt.show()

    # save the processed image
    saveImageFile(img_out, os.path.join(save_dir, f"processed_{file_name}"))