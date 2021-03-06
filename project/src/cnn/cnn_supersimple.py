#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 29 09:01:23 2020

@author: florianwolf
"""

import torch
import torch.nn as nn

# this way we can easily change the activation function for the whole network
def activ_func():
    return(nn.LeakyReLU())
    #return(nn.ReLU())
# additional arguments default values are taken directly from pytorch
def conv_layer(num_in_channels, num_out_channels,kernel_size,stride=1,padding=0,dilation=1):
    return nn.Sequential(\
        nn.Conv2d(num_in_channels, num_out_channels, kernel_size=kernel_size, stride=stride,
                        padding=padding, dilation=dilation, bias=True),\
        activ_func())
def fc_layer(num_input_channels, num_output_channels):
    return nn.Sequential(\
        nn.Linear(num_input_channels,num_output_channels),
        activ_func())

def pooling(kernel_size_own,stride_own,padding_own):
    return(nn.MaxPool2d(kernel_size=kernel_size_own,stride=stride_own,padding=padding_own))
    # return(nn.AvgPool2d(kernel_size=kernel_size_own,stride=stride_own,padding=padding_own))


class CnnSuperSimple(nn.Module):
    def __init__(self,num_input_channels, last_layer=False):
        # call super method to create instance of the network class
        super(CnnSuperSimple, self).__init__()
        self.bn1 = nn.BatchNorm2d(num_input_channels)
        self.conv1 = conv_layer(num_input_channels, 24, kernel_size=3, stride=2)
        #self.conv2 = conv_layer(24, 24, kernel_size=3, stride=2)
        #self.conv2 = conv_layer(24, 32, kernel_size=5, stride=2)
        
        # first pooling layer after second convolution layer, conv_layer
        # already includes the activation function
        #self.pool1 = pooling(kernel_size_own=2,stride_own=2,padding_own=1)

        # now fully connected layers
        self.fc1 = fc_layer(24*52*79, 100)
        self.fc2 = fc_layer(100, 50)
        self.fc3 = fc_layer(50,1)
        # no activation function in the last layer
        #self.fc4 = nn.Linear(10,1)

        self.last_layer = last_layer
        if last_layer:
            # linear last layer
            self.fc5 = nn.Linear(1, 1)

        # init weights and bias' for the convolution layer
        # for the linear layers, pytorch chooses a uniform distribution for
        # w and b, which should be fine
        for layer in self.modules():
            if isinstance(layer, nn.Conv2d):
                # add nonlinearity to the layer, as we are using the relu function
                # this should also be the way how matlab chooses weights
                nn.init.kaiming_uniform_(layer.weight.data, mode='fan_in',\
                                         nonlinearity='relu')
                if layer.bias is not None:
                    # init bias with all zeros, as we usually did in the lecture
                    layer.bias.data.zero_()
            
        # print(self.modules)
    
    # implement forward function for the network
    def forward(self,x):
#        print("shape = ",x.shape)
        x = self.bn1(x)
        x = self.conv1(x)
        #x = self.conv2(x)
        #x = self.pool1(x)

        #print(x.shape)

        x = x.view(-1, 24*52*79)
        x = self.fc1(x)
        x = self.fc2(x)
        x = self.fc3(x)
        #x = self.fc4(x)

        if self.last_layer:
            x = self.fc5(x)
        # remove all dimensions with size 1, so we get a tensor of the form
        # batchSize x 1 (in particular a scalar for each input image, which
        # is, what we want)
        return(x.squeeze(1))
        
# if __name__ == '__main__':
#     model = CNNFlowOnlyWithPooling(3)
#     from torchsummary import summary
#     summary(model, (3,105,160))
#     # x = torch.rand(10,3,105,160)
#     # #x = torch.load("../data/tensorData/frames/00001.pt")
#     # res = model.forward(x)
#     # print(res)
        