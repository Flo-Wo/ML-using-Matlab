#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 29 10:36:35 2020

@author: florianwolf
"""

import torch
from torch.utils.data import Dataset, DataLoader, Subset, TensorDataset
from torchvision import datasets,transforms
import cv2
import numpy as np


# we use this file to laod the data into a torch dataloader, to efficiently
# store the data set and split it into train and test data

# override the Dataset class of pytorch to efficiently run the code
# https://stanford.edu/~shervine/blog/pytorch-how-to-generate-data-parallel
# using this technique

class Dataset(torch.utils.data.Dataset):
  'Characterizes a dataset for PyTorch'
  def __init__(self, list_IDs, labels):
        'Initialization with two dicts'
        self.labels = labels
        self.list_IDs = list_IDs

  def __len__(self):
        'Denotes the total number of samples'
        return len(self.list_IDs)

  def __getitem__(self, index):
        'Generates one sample of data'
        # Select sample
        ID = self.list_IDs[index]

        # Load data and get label
        X = torch.load('data/tensorData/of/' + str(ID) + '.pt')
        y = self.labels[ID]

        return X, y

class Dataset_of_frames(torch.utils.data.Dataset):
    # class to return mini batches to the siamese network
    # here X1 is the optical flow frame and X2 is the downsampled, but 
    # raw frame, y is the label
    # we can decide here, how we want to pass this into the network
    # (siamese or linear combination)
    'Characterizes a dataset for PyTorch'
    def __init__(self, list_IDs, labels):
          'Initialization with two dicts'
          self.labels = labels
          self.list_IDs = list_IDs
    
    def __len__(self):
          'Denotes the total number of samples'
          return len(self.list_IDs)
    
    def __getitem__(self, index):
          'Generates one sample of data'
          # Select sample
          ID = self.list_IDs[index]
    
          # Load data and get label
          X1 = torch.load('data/tensorData/of/' + str(ID) + '.pt')
          X2 = torch.load("data/tensorData/frames" + str(ID) + ".pt")
          y = self.labels[ID]
    
          return X1, X2, y

#### SAVE THE IMAGES AS TENSORS ####

def load_images_single():
    # only load the single images, to sample them down and save them as tensors
    # do it like 
    # https://www.geeksforgeeks.org/opencv-the-gunnar-farneback-optical-flow/
    video = cv2.VideoCapture("data/raw/train.mp4")
    success,prev_frame = video.read()
    while success:
        success, curr_frame = video.read()
        if success == False:
            break
        yield curr_frame
    video.release()
    cv2.destroyAllWindows()
    
def save_frames_as_tensors(save_path):
    print("saving single frames!")
    # load images, transform to tensors and add the label
    for i, frame in enumerate(load_images_single()):
        if i%100 == 0:
            print(i)
        frame = sample_down_half(frame[:-60,:,:])
        frame = sample_down_half_second(frame)
        frame = transforms.ToTensor()(frame)#.unsqueeze(0)
        #print(frame.shape)
        torch.save(frame, save_path + "{:05d}.pt".format(i+1))

#### CALCULATION AND SAVING OF THE OPTICAL FLOW #####

def generate_flow_all(save_path):
    print("saving of tensors!")
    # load images, transform to tensors and add the label
    for i, (prev_frame, curr_frame) in enumerate(load_images()):
        if i%100 == 0:
            print(i)
        #filepath = flow_dataset_path + "/{:05d}_of.png".format(i)
        rgb_flow = calc_of(curr_frame, prev_frame)
        #print(rgb_flow)
        # transform image to a tensor and concat them
        rgb_flow_tensor = transforms.ToTensor()(rgb_flow)#.unsqueeze(0)
        #print(rgb_flow_tensor.shape)
        torch.save(rgb_flow_tensor,save_path + "{:05d}.pt".format(i+1))

def generate_train_eval_dict(data_size, test_split_ratio):
    # we have 20399 images and of frames, we split them and create a dict
    data_size= 20399
    split_index = int(np.floor(data_size*test_split_ratio))
    all_indices = list(range(1,data_size+1))
    train_indices = ["{:05d}".format(x) for x in all_indices[:split_index]]
    test_indices = ["{:05d}".format(x) for x in all_indices[split_index:]]
    partition = {'train' : train_indices,\
                 'validation' : test_indices}
    return(partition)

def generate_label_dict(label_path,data_size):
    # these are all labels in a txt, we want to write them into a dict and
    # ignore the first value
    labels_np_array = np.loadtxt(label_path)
    labels = {}
    for index in range(1,data_size+1):
        labels["{:05d}".format(index)] = labels_np_array[index]
    return(labels)


def load_images():
    # do it like 
    # https://www.geeksforgeeks.org/opencv-the-gunnar-farneback-optical-flow/
    video = cv2.VideoCapture("data/raw/train.mp4")
    success,prev_frame = video.read()
    while success:
        success, curr_frame = video.read()
        if success == False:
            break
        yield prev_frame, curr_frame
        prev_frame = curr_frame
    video.release()
    cv2.destroyAllWindows()
    
def sample_down_half(frame):
    # sample to half size using bilinear interpolation
    return(cv2.resize(frame,(320,210)))

def sample_down_half_second(frame):
    # sample the image again down for half the size, after the of is calculated
    return(cv2.resize(frame,(160,105)))

def calc_of(curr_frame, prev_frame):
    # do it like 
    # https://www.geeksforgeeks.org/opencv-the-gunnar-farneback-optical-flow/
    curr_frame, prev_frame = sample_down_half(curr_frame[:-60,:,:]), sample_down_half(prev_frame[:-60,:,:])
    # Create mask 
    hsv_mask = np.zeros_like(prev_frame) 
    # Make image saturation to a maximum value 
    hsv_mask[:,:, 1] = 255
    
    prev_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)
    curr_gray = cv2.cvtColor(curr_frame, cv2.COLOR_BGR2GRAY)
    
    # Optical flow is now calculated 
    flow = cv2.calcOpticalFlowFarneback(prev_gray, curr_gray,
                                        None,\
                                        pyr_scale=0.5, levels=3, winsize=6,\
                                        iterations=3, poly_n=5, poly_sigma=1.1,\
                                        flags=0)
    # Compute magnitude and angle of 2D vector 
    mag, ang = cv2.cartToPolar(flow[..., 0], flow[..., 1]) 
    # Set image hue value according to the angle of optical flow 
    hsv_mask[:,:, 0] = ang * (180 / np.pi / 2)
    # Set value as per the normalized magnitude of optical flow 
    hsv_mask[:,:, 2] = cv2.normalize(mag, None, 0, 255, cv2.NORM_MINMAX) 
    # Convert to rgb 
    rgb_image = cv2.cvtColor(hsv_mask, cv2.COLOR_HSV2RGB) 
    rgb_image = sample_down_half_second(rgb_image)
    return(rgb_image)
    

# if __name__ == "__main__":
#     generate_flow_all("./data/tensorData/of/")
#     save_frames_as_tensors("./data/tensorData/frames/")


