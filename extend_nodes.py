from .AC_API import *
from .AC_CATEGORY import *
from .AC_FUN import AC_FUN
import torch

class CropImage(AC_FUN):
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                "x": (
                    "INT",
                    {"default": 0, "min": 0, "max": 8192, "step": 1},
                ),
                "y": (
                    "INT",
                    {"default": 0, "min": 0, "max": 8192, "step": 1},
                ),
                "width": (
                    "INT",
                    {"default": 512, "min": 1, "max": 8192, "step": 1},
                ),
                "height": (
                    "INT",
                    {"default": 512, "min": 1, "max": 8192, "step": 1},
                ),
            }
        }
    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "crop"

    def crop(self, image, x, y, width, height):
        out = image[:, y : y + height, x : x + width, :]
        return (out,)


class ApplyMaskToImage(AC_FUN):
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                "mask": ("MASK",),
            }
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "apply_mask"

    def apply_mask(self, image, mask):
        out = image.movedim(-1, 1)
        if out.shape[1] == 3:  # RGB
            out = torch.cat([out, torch.ones_like(out[:, :1, :, :])], dim=1)
        for i in range(out.shape[0]):
            out[i, 3, :, :] = mask
        out = out.movedim(1, -1)
        return (out,)
