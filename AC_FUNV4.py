from PIL import Image,ImageEnhance,ImageOps,ImageChops
import tensorflow as tf
import torch
from .AC_FUN import AC_FUN
from .AC_Factory import *
import random
# ==============================================
# TODO:
class AC_FUN_ImagePath_Dont_use(AC_FUN):
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
            "Image_path": ("STRING", {
                    "multiline": False,
                    })
        }}
    # 返回结果类型
    RETURN_TYPES = ('IMAGE',)
    
    # 返回节点命名
    RETURN_NAMES = ('list_item',)
    FUNCTION = "image_path" 
    image_list = []

    def image_path(self,Image_path):
            result = read_images_from_directory(Image_path)
            for x in result:
                tensors = tensor2pil(x)
                Image = pil2tensor(tensors)
                result = self.image_list.append(Image)
            return (result,)
  
# ============================================
class PictureChannels(AC_FUN):
  @classmethod
  def INPUT_TYPES(cls):
    return {
      "required": {
         "Source_Image":("IMAGE",),
      },
    }
  RETURN_TYPES = ("INT","INT","INT","STRING")
  RETURN_NAMES = ("height","width","channels","helper")
  FUNCTION = "picturechannels"


  def picturechannels(self,Source_Image):
    image_shape = tf.shape(Source_Image)
    height = int(image_shape[1])
    width = int(image_shape[2])
    channels = int(image_shape[0])
    result = "图像尺寸：{} x {} x {}".format(height, width, channels)
    return (height,width,channels,result)
# ============================================
class PictureMix(AC_FUN):
  @classmethod
  def INPUT_TYPES(cls):
    return {
      "required": {
         "image_1":("IMAGE",),
         "image_2":("IMAGE",),
         "Mix_percentage": ("FLOAT", {"default": 0.5, "min": 0.0, "max": 1.0, "step": 0.01}),
      },
    }
  RETURN_TYPES = ("IMAGE",)
  FUNCTION = "picturemix"


  def picturemix(self,image_1,image_2,Mix_percentage):
    # 转换图片为PIL格式
        img_a = tensor2pil(image_1)
        img_b = tensor2pil(image_2)

        # Blend image
        blend_mask = Image.new(mode="L", size=img_a.size,
                               color=(round(Mix_percentage * 255)))
        blend_mask = ImageOps.invert(blend_mask)
        img_result = Image.composite(img_a, img_b, blend_mask)

        del img_a, img_b, blend_mask
    
        return (pil2tensor(img_result), )

# ==============================================
# 图像去色
class AC_Image_Remove_Color(AC_FUN):
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                "target_red": ("INT", {"default": 255, "min": 0, "max": 255, "step": 1}),
                "target_green": ("INT", {"default": 255, "min": 0, "max": 255, "step": 1}),
                "target_blue": ("INT", {"default": 255, "min": 0, "max": 255, "step": 1}),
                "replace_red": ("INT", {"default": 255, "min": 0, "max": 255, "step": 1}),
                "replace_green": ("INT", {"default": 255, "min": 0, "max": 255, "step": 1}),
                "replace_blue": ("INT", {"default": 255, "min": 0, "max": 255, "step": 1}),
                "remove_threshold": ("INT", {"default": 10, "min": 0, "max": 255, "step": 1}),
            },
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "image_remove_color"


    def image_remove_color(self,image,target_red=255, remove_threshold=10, target_green=255, 
                           target_blue=255, replace_red=255, replace_green=255, replace_blue=255):
        return (pil2tensor(self.apply_remove_color(tensor2pil(image), remove_threshold, (target_red, target_green, target_blue), (replace_red, replace_green, replace_blue))),)

    def apply_remove_color(self, image, threshold=10, color=(255, 255, 255), rep_color=(0, 0, 0)):
        # Create a color image with the same size as the input image
        color_image = Image.new('RGB', image.size, color)

        # Calculate the difference between the input image and the color image
        diff_image = ImageChops.difference(image, color_image)

        # Convert the difference image to grayscale
        gray_image = diff_image.convert('L')

        # Apply a threshold to the grayscale difference image
        mask_image = gray_image.point(lambda x: 255 if x > threshold else 0)

        # Invert the mask image
        mask_image = ImageOps.invert(mask_image)

        # Apply the mask to the original image
        result_image = Image.composite(
            Image.new('RGB', image.size, rep_color), image, mask_image)

        return result_image
    
# ==============================================
class AC_Image_Batch(AC_FUN):
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "images_1": ("IMAGE",),
                "images_2": ("IMAGE",),
          
            },
        }

    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("image",)
    FUNCTION = "image_batch"


    def image_batch(self,images_1=None,images_2=None):
        try:
            result = images_1+images_2
        except:
            result = None
        return (result,)
# ==============================================
# TODO
class AC_ImageContrast(AC_FUN):
    def __init__(self):
        pass
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                "contrast": ("FLOAT",
                               {"min": -50.00, "max": 50.00, "step": 1.00}
                               )
            },
        }
    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("image",)
    FUNCTION = "image_Contrast"


    def image_Contrast(self,image=None,contrast=None,tips=None):
        image_pil = tensor2pil(image)
        enhanced_image_pil = ImageEnhance.Contrast(image_pil).enhance(contrast)
        enhanced_image_tensor = pil2tensor(enhanced_image_pil)

        return (enhanced_image_tensor,)
# ==============================================
class AC_ImageBrightness(AC_FUN):
    def __init__(self):
        pass
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                "brightness": ("FLOAT",
                               {"min": -50.00, "max": 50.00, "step": 1.00}
                               ),

            },
        }
    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("image",)
    FUNCTION = "image_brightness"


    def image_brightness(self,image=None,brightness=None):
        # 转换为 PIL 图像对象
        image_pil = tensor2pil(image)
        # 调整亮度
        enhanced_image_pil = ImageEnhance.Brightness(image_pil).enhance(brightness)
        # 转换回 Tensor 对象
        enhanced_image_tensor = pil2tensor(enhanced_image_pil)

        return (enhanced_image_tensor,)
# ==============================================
class AC_ImageDrow(AC_FUN):
    def __init__(self):
        pass
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image_1": ("IMAGE",),
                "image_2": ("IMAGE",),
                "alpha": ("FLOAT",
                               {"min": 0.00, "max": 1.00, "step": 0.01}
                               ),
            },
        }
    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("image",)
    FUNCTION = "image_drow"


    def image_drow(self,image_1,image_2,alpha):
        # 转换为 PIL 图像对象
        P1 = tensor2pil(image_1)
        P2 = tensor2pil(image_2)

        # 混合模式
        blended_image = Image.blend(P1, P2, alpha)
        
        # 转换回 Tensor 对象
        enhanced_image_tensor = pil2tensor(blended_image)

        return (enhanced_image_tensor,)
# ==============================================
class AC_ImageBalance(AC_FUN):
    def __init__(self):
        pass
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image_1": ("IMAGE",),
                "factor": ("FLOAT",
                               {"min": 0.00, "max": 1.00, "step": 0.01}
                               ),
            },
        }
    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("image",)
    FUNCTION = "image_balance"


    def image_balance(self,image_1,factor):
        # 转换为 PIL 图像对象
        P1 = tensor2pil(image_1)

        enhancer = ImageEnhance.Color(P1)
        balanced_image = enhancer.enhance(factor)

        enhanced_image_tensor = pil2tensor(balanced_image)

        return (enhanced_image_tensor,)
# ==============================================
class AC_ImageCopy(AC_FUN):
    def __init__(self):
        pass
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image_1": ("IMAGE",),
            },
        }
    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("image",)
    FUNCTION = "image_copy"


    def image_copy(self,image_1):

        P1 = tensor2pil(image_1)
        pil_image1 = P1.copy()
        enhanced_image_tensor_1 = pil2tensor(pil_image1)
        return (enhanced_image_tensor_1,)
# ==============================================
class AC_Image_invert(AC_FUN):
    def __init__(self):
        pass
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image_1": ("IMAGE",)
            },
        }
    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("image",)
    FUNCTION = "image_invert"


    def image_invert(self,image_1):
        # 转换为 PIL 图像对象
        P1 = tensor2pil(image_1)
        # 对图片进行复制
        pil_image1 = ImageOps.invert(P1)
        # 转换回 Tensor 对象
        enhanced_image_tensor_1 = pil2tensor(pil_image1)
        return (enhanced_image_tensor_1,)
# ==============================================
class AC_ImageCrop(AC_FUN):
    def __init__(self):
        pass
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                "left": ("INT",{"min": 0, "max": 9999, "step": 1}),
                "right": ("INT",{"min": 0, "max": 9999, "step": 1,"default":256}),
                "top": ("INT",{"min": 0, "max": 9999, "step": 1}),
                "bottom": ("INT",{"min": 0, "max": 9999, "step": 1,"default":256}),
                      }}
    RETURN_TYPES = ("IMAGE",)
    OUTPUT_NAMES = ("image",)
    FUNCTION = "image_crop"

    def image_crop(self,image,left=0,right=256,top=0,bottom=256):
        image = tensor2pil(image)
        img_width, img_height = image.size
        crop_top = max(top, 0)
        crop_left = max(left, 0)
        crop_bottom = min(bottom, img_height)
        crop_right = min(right, img_width)
        crop_width = crop_right - crop_left
        crop_height = crop_bottom - crop_top
        if crop_width <= 0 or crop_height <= 0:
            raise ValueError("Error: crop_width and crop_height")
        
        # Crop the image and resize
        crop = image.crop((crop_left, crop_top, crop_right, crop_bottom))
        crop = crop.resize((((crop.size[0] // 8) * 8), ((crop.size[1] // 8) * 8)))
        
        return (pil2tensor(crop),)
# ================================================================

Image_mode = ["red", "green", "blue"]
class Image_channel(AC_FUN):
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
            "image":("IMAGE",),
            "mode":(Image_mode,),
            "tips":("STRING",{"mutilin":False,"default":"图像的红绿蓝通道图"})
            },
        }
    RETURN_TYPES = ("IMAGE",)
    OUTPUT_NAMES = ("image",)
    FUNCTION = "image_channel"


    def image_channel(self,mode,image,tips=None):
        # tensor转换成pil
        image_pil = tensor2pil(image)
        # 分离通道
        r, g, b = image_pil.split()

        # 提取红色、绿色、蓝色通道
        red_image = Image.merge("RGB", (r, Image.new("L", image_pil.size, 0), Image.new("L", image_pil.size, 0)))
        green_image = Image.merge("RGB", (Image.new("L", image_pil.size, 0), g, Image.new("L", image_pil.size, 0)))
        blue_image = Image.merge("RGB", (Image.new("L", image_pil.size, 0), Image.new("L", image_pil.size, 0), b))
        # 判定条件
        if mode == "red":
            return (pil2tensor(red_image),)
        if mode == "green":
            return (pil2tensor(green_image),)
        if mode == "blue":
            return (pil2tensor(blue_image))


class InvertMask(AC_FUN):
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "mask": ("MASK",),
            }
        }
    FUNCTION = "main"
    RETURN_TYPES = ("MASK",)

    def main(self, mask):
        out = 1.0 - mask
        return (out,)

class IsMaskEmptyNode(AC_FUN):
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "mask": ("MASK",),
            },
        }
    RETURN_TYPES = ["NUMBER"]
    RETURN_NAMES = ["boolean_number"]

    FUNCTION = "main"

    def main(self, mask):
        return (torch.all(mask == 0).int().item(), )