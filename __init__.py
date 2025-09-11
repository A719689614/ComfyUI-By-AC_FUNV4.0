from .AC_FUNV4 import PictureChannels,PictureMix,Image_channel,AC_Image_Remove_Color,AC_Image_Batch
from .AC_FUNV4 import AC_ImageContrast,AC_ImageBrightness,AC_Image_invert,AC_ImageCrop,AC_ImageDrow,AC_ImageBalance,AC_ImageCopy
from .AC_FUNV4 import InvertMask, IsMaskEmptyNode
from .AC_FUN_PATH import *
from .extend_nodes import *
from .AC_Image2Mask import AC_ImageToMask
from .install import *
from .AC_TRANS import AC_Trans
from .show import GetImageBinary



NODE_CLASS_MAPPINGS = {
    # 啊程V4.0
    "Image_批量图像加载":AC_Batch,
    "Image_批量保存保存":AC_Save,
    "Image_图像通道图":PictureChannels,
    "Image_图像混合Mix":PictureMix,
    "Image_图像去色RC":AC_Image_Remove_Color,
    "Image_图像合并MG":AC_Image_Batch,
    "Image_图像亮度BT":AC_ImageBrightness,
    "Image_图像对比度IC":AC_ImageContrast,
    "Image_图像反向":AC_Image_invert,
    "Image_图像裁切CP":AC_ImageCrop,
    "Image_图像叠加模式ID":AC_ImageDrow,
    "Image_图像色彩平衡":AC_ImageBalance,
    "Image_图像变换(翻转)":AC_Trans,
    "Image_图像复制CP":AC_ImageCopy,
    "Image_图像红绿蓝通道":Image_channel,
    "Image_图像裁切": CropImage,
    "Image_应用蒙版到图像": ApplyMaskToImage,
    "Image_图像转遮罩MTI":AC_ImageToMask,
    "Image_遮罩反转":InvertMask,
    "Image_空遮罩判断":IsMaskEmptyNode,
    "Image_二进制数据":GetImageBinary,
}
