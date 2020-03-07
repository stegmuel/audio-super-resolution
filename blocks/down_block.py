from layers.superpixel import *
from blocks.base_block import *


class DownBlock(BaseBlock):
    def __init__(self, in_channels, kernel_sizes, channel_sizes, bottleneck_channels):
        super(DownBlock, self).__init__(in_channels, kernel_sizes, channel_sizes, bottleneck_channels)
        self.superpixel = SuperPixel1D(downscale_factor=2)
        self.activation = nn.PReLU(sum(channel_sizes))

    def forward(self, x):
        x = self.forward_base(x)
        x = self.superpixel(self.activation(x))
        return x