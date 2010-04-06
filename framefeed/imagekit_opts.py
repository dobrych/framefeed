from imagekit.specs import ImageSpec
from imagekit import processors


# default options are copied from flickr
class SquareThumbSize(processors.Resize):
    width = 75
    height = 75
    crop = True

class NormalThumbSize(processors.Resize):
    width = 100
    height = 100
    crop = False

class SmallSize(processors.Resize):
    width = 240
    height = 240
    crop = False

class MediumSize(processors.Resize):
    width = 500
    height = 500
    crop = False

class LargeSize(processors.Resize):
    width = 1024
    height = 1024
    crop = False

class EnchanceThumb(processors.Adjustment):
    contrast = 1.2
    sharpness = 1.1


class SquareThumb(ImageSpec):
    access_as = 'square_thumb'
    pre_cache = True
    processors = [SquareThumbSize, EnchanceThumb]

class NormalThumb(ImageSpec):
    access_as = 'normal_thumb'
    pre_cache = True
    processors = [NormalThumbSize, EnchanceThumb]

class SmallImg(ImageSpec):
    access_as = 'small_img'
    pre_cache = True
    processors = [SmallSize,]

class MediumImg(ImageSpec):
    quality = 85
    access_as = 'medium_img'
    pre_cache = True
    processors = [MediumSize,]

class LargeImg(ImageSpec):
    quality = 85
    access_as = 'large_img'
    pre_cache = True
    processors = [LargeSize,]
