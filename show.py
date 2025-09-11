from PIL import Image
import numpy as np
import io
from .AC_FUN  import AC_FUN
class GetImageBinary(AC_FUN):
    @classmethod
    def INPUT_TYPES(s):
        return {"required": {"images": ("IMAGE", )}}
    
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("STRING",)
    FUNCTION = "get_binary"
    
    def get_binary(self, images):
        if not images.shape[0]:
            return (None,)
        
        # 只处理第一张图像
        image = images[0]
        i = 255. * image.cpu().numpy()
        img = Image.fromarray(np.clip(i, 0, 255).astype(np.uint8))
        
        # 将图像转换为二进制数据
        buffer = io.BytesIO()
        img.save(buffer, format="PNG")
        binary_data = buffer.getvalue()
        buffer.close()
        
        return (binary_data,)