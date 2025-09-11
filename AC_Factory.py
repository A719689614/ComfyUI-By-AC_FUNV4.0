import torch
import numpy as np
from PIL import Image
import os

def tensor2mask(t: torch.Tensor) -> torch.Tensor:
    size = t.size()
    if (len(size) < 4):
        return t
    if size[3] == 1:
        return t[:,:,:,0]
    elif size[3] == 4:
        if torch.min(t[:, :, :, 3]).item() != 1.:
            return t[:,:,:,3]


# Tensor to PIL
def tensor2pil(image):
    return Image.fromarray(np.clip(255. * image.cpu().numpy().squeeze(), 0, 255).astype(np.uint8))
    
# PIL to Tensor
def pil2tensor(image):
    return torch.from_numpy(np.array(image).astype(np.float32) / 255.0).unsqueeze(0)


def read_images_from_directory(directory):
    image_list = []
    extensions = ['.jpg', '.jpeg', '.png', '.gif']  # 可以根据需要添加其他图片格式的扩展名

    for filename in os.listdir(directory):
        if any(filename.lower().endswith(ext) for ext in extensions):
            image_path = os.path.join(directory, filename)
            image = Image.open(image_path)
            image_list.append(image)

    return image_list