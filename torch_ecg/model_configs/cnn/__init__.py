"""
configs for the basic cnn layers and blocks
"""

from .vgg import (
    vgg_block_basic, vgg_block_mish, vgg_block_swish,
    vgg16, vgg16_leadwise,
)
from .resnet import (
    # building blocks
    resnet_block_basic, resnet_bottle_neck,
    resnet_bottle_neck_B, resnet_bottle_neck_D,
    resnet_block_basic_se, resnet_bottle_neck_se,
    resnet_block_basic_nl, resnet_bottle_neck_nl,
    resnet_block_basic_gc, resnet_bottle_neck_gc,
    # vanilla resnet
    resnet_vanilla_18, resnet_vanilla_34, resnet_vanilla_50,
    resnet_vanilla_101, resnet_vanilla_152,
    resnext_vanilla_50_32x4d, resnext_vanilla_101_32x8d,
    resnet_vanilla_wide_50_2, resnet_vanilla_wide_101_2,
    # custom resnet
    resnet_cpsc2018, resnet_cpsc2018_leadwise,
    # stanford resnet
    resnet_block_stanford, resnet_stanford,
    # ResNet Nature Communications
    resnet_nature_comm,
    resnet_nature_comm_se, resnet_block_basic_nl, resnet_block_basic_gc,
    # TResNet
    tresnetM, tresnetL, tresnetXL,
)
from .cpsc import (
    # cpsc2018 SOTA
    cpsc_block_basic, cpsc_block_mish, cpsc_block_swish,
    cpsc_2018, cpsc_2018_leadwise,
)
from .multi_scopic import (
    multi_scopic_block,
    multi_scopic, multi_scopic_leadwise,
)
from .densenet import (
    # vanilla densenet
    densenet_vanilla,
    # custom densenet
    densenet_leadwise,
)
from .xception import (
    # vanilla xception
    xception_vanilla,
    # custom xception
    xception_leadwise,
)
from .mobilenet import (
    # vanilla mobilenets
    mobilenet_v1_vanilla,
    mobilenet_v2_vanilla,
)


__all__ = [
    # vgg
    "vgg_block_basic", "vgg_block_mish", "vgg_block_swish",
    "vgg16", "vgg16_leadwise",
    # resnet building blocks
    "resnet_block_basic", "resnet_bottle_neck",
    "resnet_bottle_neck_B", "resnet_bottle_neck_D",
    "resnet_block_basic_se", "resnet_bottle_neck_se",
    "resnet_block_basic_nl", "resnet_bottle_neck_nl",
    "resnet_block_basic_gc", "resnet_bottle_neck_gc",
    # vanilla resnet
    "resnet_vanilla_18", "resnet_vanilla_34",
    "resnet_vanilla_50", "resnet_vanilla_101", "resnet_vanilla_152",
    "resnext_vanilla_50_32x4d", "resnext_vanilla_101_32x8d",
    "resnet_vanilla_wide_50_2", "resnet_vanilla_wide_101_2",
    # custom resnet
    "resnet_cpsc2018", "resnet_cpsc2018_leadwise",
    # stanford resnet
    "resnet_block_stanford", "resnet_stanford",
    # ResNet Nature Communications
    "resnet_nature_comm",
    "resnet_nature_comm_se", "resnet_nature_comm_nl", "resnet_nature_comm_gc",
    # TresNet
    "tresnetM", "tresnetL", "tresnetXL",
    # cpsc2018 SOTA
    "cpsc_block_basic", "cpsc_block_mish", "cpsc_block_swish",
    "cpsc_2018", "cpsc_2018_leadwise",
    # multi_scopic
    "multi_scopic_block",
    "multi_scopic", "multi_scopic_leadwise",
    # vanilla densenet
    "densenet_vanilla",
    # custom densenet
    "densenet_leadwise",
    # vanilla xception
    "xception_vanilla",
    # custom xception
    "xception_leadwise",
    # vanilla mobilenets
    "mobilenet_v1_vanilla",
    "mobilenet_v2_vanilla",
]