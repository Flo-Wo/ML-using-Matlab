#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 03.01.2021
@author: Franz Herbst
"""

import torch
<<<<<<< HEAD
#from torch.utils.data import Dataset, DataLoader, Subset, TensorDataset
=======
>>>>>>> net_trainer_approach
from torchvision import transforms
import cv2
import numpy as np
from tqdm import tqdm

# we use this file to load the data into a torch data loader, to efficiently
# store the data set and split it into train and test data

# override the Dataset class of pytorch to efficiently run the code
# https://stanford.edu/~shervine/blog/pytorch-how-to-generate-data-parallel
# using this technique

# #############################################################
# IMPORTANT CONSTANTS
# #############################################################

path_tensor_opt_fl = "./data/tensorData/of/"
path_tensor_frames = "./data/tensorData/frames/"
path_image_opt_fl = "data/opticalFlow/"
path_image_frames = "data/frames/"
path_raw_video = "data/raw/train.mp4"
path_labels = "./data/raw/train_label.txt"
path_labels_test = "./data/raw/new_train_label.txt"
test_path = "new/"

picture_bottom_offset = 60
picture_opt_fl_size = (320, 210)
picture_final_size = (160, 105)


# #############################################################
# DATASET CLASSES
# #############################################################

class DatasetOptFlo(torch.utils.data.Dataset):
    """Characterizes a dataset for PyTorch"""

    def __init__(self, list_ids, labels, test=False):
        """Initialization with two dicts"""
        self.list_IDs = list_ids
        self.labels = labels
        self.test = test

    def __len__(self):
        """Denotes the total number of samples"""
        return len(self.list_IDs)

    def __getitem__(self, index):
        """Generates one sample of data"""
        #Select sample
        element_id = self.list_IDs[index]
        element_id = (element_id % 20400)
        # print(element_id)
        # Load data and get label
        if self.test:
            x = torch.load(path_tensor_opt_fl + test_path + "{:05d}.pt".format(element_id))
        else:
            x = torch.load(path_tensor_opt_fl + "{:05d}.pt".format(element_id))
        # y = (self.labels[element_id] + self.labels[element_id - 1]) / 2
        y = self.labels[element_id]

        return x, y, element_id

    @classmethod
    def get_images(cls, prev_frame, curr_frame, opt_flow):
        return [opt_flow]


class DatasetFrames(torch.utils.data.Dataset):
    """Characterizes a dataset for PyTorch"""

    def __init__(self, list_ids, labels, test=False):
        """Initialization with two dicts"""
        self.list_IDs = list_ids
        self.labels = labels
        self.test = test

    def __len__(self):
        """Denotes the total number of samples"""
        return len(self.list_IDs)

    def __getitem__(self, index):
        """Generates one sample of data"""
        # Select sample
        ID = self.list_IDs[index]

        if ID < 0:
            X1 = torch.load(path_tensor_frames + test_path + "{:05d}.pt".format((-ID) - 1))
            X2 = torch.load(path_tensor_frames + test_path + "{:05d}.pt".format(-ID))
            y = self.labels[-ID]
        else:
            # Load data and get label
            X1 = torch.load(path_tensor_frames + "{:05d}.pt".format(ID - 1))
            X2 = torch.load(path_tensor_frames + "{:05d}.pt".format(ID))
            y = self.labels[ID]

        return X1, X2, y, ID

    @classmethod
    def get_images(cls, prev_frame, curr_frame, opt_flow):
        return [prev_frame, curr_frame]


class DatasetOptFlo1Frames(torch.utils.data.Dataset):
    # class to return mini batches to the siamese network
    # here X1 is the optical flow frame and X2 is the one sampled down, but
    # raw frame, y is the label
    # we can decide here, how we want to pass this into the network
    # (siamese or linear combination)
    """Characterizes a dataset for PyTorch"""

    def __init__(self, list_ids, labels, labelsT=[]):
        """Initialization with two dicts"""
        self.labels = labels
        self.labelsT = labelsT
        self.list_IDs = list_ids

    def __len__(self):
        """Denotes the total number of samples"""
        return len(self.list_IDs)

    def __getitem__(self, index):
        """Generates one sample of data"""
        # Select sample
        ID = self.list_IDs[index]

        # Load data and get label
<<<<<<< HEAD
<<<<<<< HEAD
        F = torch.load(path_tensor_frames + "{:05d}.pt".format(ID))
        X = torch.load(path_tensor_opt_fl + "{:05d}.pt".format(ID))
        y = (self.labels[ID] + self.labels[ID - 1]) / 2
        # y = self.labels[ID]
=======
        if self.test:
            X1 = torch.load(path_tensor_opt_fl + test_path + "{:05d}.pt".format(ID))
            X2 = torch.load(path_tensor_frames + test_path + "{:05d}.pt".format(ID))
        else:
            X1 = torch.load(path_tensor_opt_fl + "{:05d}.pt".format(ID))
            X2 = torch.load(path_tensor_frames + "{:05d}.pt".format(ID))
        y = self.labels[ID]
>>>>>>> net_trainer_approach
=======
        if ID < 0:
            X1 = torch.load(path_tensor_opt_fl + test_path + "{:05d}.pt".format(-ID))
            X2 = torch.load(path_tensor_frames + test_path + "{:05d}.pt".format(-ID))
            y = self.labelsT[-ID]
        else:
            X1 = torch.load(path_tensor_opt_fl + "{:05d}.pt".format(ID))
            X2 = torch.load(path_tensor_frames + "{:05d}.pt".format(ID))
            y = self.labels[ID]
>>>>>>> net_trainer_approach

        return X1, X2, y, ID

    @classmethod
    def get_images(cls, prev_frame, curr_frame, opt_flow):
        return [opt_flow, curr_frame]


class DatasetOptFlo2Frames(torch.utils.data.Dataset):
    """Characterizes a dataset for PyTorch"""

    def __init__(self, list_ids, labels, test=False):
        """Initialization with two dicts"""
        self.list_IDs = list_ids
        self.labels = labels
        self.test = test

    def __len__(self):
        """Denotes the total number of samples"""
        return len(self.list_IDs)

    def __getitem__(self, index):
        """Generates one sample of data"""
        # Select sample
        ID = self.list_IDs[index]

        # Load data and get label
        if self.test:
            F1 = torch.load(path_tensor_frames + test_path + "{:05d}.pt".format(ID - 1))
            F2 = torch.load(path_tensor_frames + test_path + "{:05d}.pt".format(ID))
            X = torch.load(path_tensor_opt_fl + test_path + "{:05d}.pt".format(ID))
        else:
            F1 = torch.load(path_tensor_frames + "{:05d}.pt".format(ID - 1))
            F2 = torch.load(path_tensor_frames + "{:05d}.pt".format(ID))
            X = torch.load(path_tensor_opt_fl + "{:05d}.pt".format(ID))
        y = self.labels[ID]

        return F1, F2, X, y, ID

    @classmethod
    def get_images(cls, prev_frame, curr_frame, opt_flow):
        return [prev_frame, curr_frame, opt_flow]


# #############################################################
# IMAGE LOADERS
# #############################################################

def load_single_images(video_path):
    """
    Loading the single images out of the video to sample them down and save them as tensors
    Source: https://www.geeksforgeeks.org/opencv-the-gunnar-farneback-optical-flow/
    """
    video = cv2.VideoCapture(video_path)

    success, curr_frame = video.read()
    while success:
        yield curr_frame
        success, curr_frame = video.read()

    video.release()
    cv2.destroyAllWindows()


def load_double_images(video_path):
    """
    Loading two images out of the video to sample them down and calculate the optical flow
    Source: https://www.geeksforgeeks.org/opencv-the-gunnar-farneback-optical-flow/
    """
    video = cv2.VideoCapture(video_path)

    success, prev_frame = video.read()
    if success:
        success, curr_frame = video.read()

        while success:
            yield prev_frame, curr_frame
            prev_frame = curr_frame
            success, curr_frame = video.read()

    video.release()
    cv2.destroyAllWindows()


# #############################################################
# SAMPLE DOWN IMAGES
# #############################################################

def sample_down(frame, size):
    """Sample down the frame to special height"""
    return cv2.resize(frame, size)


def cut_bottom(frame, height):
    """Cuts off the bottom of the image"""
    return frame[:-height, :, :]


# #############################################################
# SAVE TENSORS
# #############################################################

def save_both(save_path_frames, save_path_of, video_path,
              save_as_png=False, save_png_fr=path_image_frames, save_png_of=path_image_opt_fl):
    """Iterate through video and save images and optical flow as tensors"""
    for i, (prev_frame, curr_frame) in enumerate(tqdm(load_double_images(video_path), "Save Flow and Frame Tensors")):
        curr_frame = sample_down(cut_bottom(curr_frame, picture_bottom_offset), picture_opt_fl_size)
        prev_frame = sample_down(cut_bottom(prev_frame, picture_bottom_offset), picture_opt_fl_size)

        # SAVE FRAME

        if i == 0:
            frame = sample_down(prev_frame, picture_final_size)
            if save_as_png:
                cv2.imwrite(save_png_fr + "{:05d}.png".format(i), frame)

            frame = transforms.ToTensor()(frame)
            torch.save(frame, save_path_frames + "{:05d}.pt".format(i))

        frame = sample_down(curr_frame, picture_final_size)
        if save_as_png:
            cv2.imwrite(save_png_fr + "{:05d}.png".format(i), frame)

        frame = transforms.ToTensor()(frame)
        torch.save(frame, save_path_frames + "{:05d}.pt".format(i))

        # SAVE FLOW

        rgb_flow = calculate_opt_flow(curr_frame, prev_frame)

        if save_as_png:
            cv2.imwrite(save_png_of + "{:05d}.png".format(i + 1), rgb_flow)
        # transform image to a tensor and concat them
        rgb_flow_tensor = transforms.ToTensor()(rgb_flow)
        torch.save(rgb_flow_tensor, save_path_of + "{:05d}.pt".format(i + 1))


def save_frames_as_tensors(save_path, video_path, save_as_png=False,
                           save_png_path=path_image_frames):
    """load images, transform to tensors and add the label"""
    for i, frame in enumerate(tqdm(load_single_images(video_path), "Save Frames as Tensors")):
        frame = cut_bottom(frame, picture_bottom_offset)
        frame = sample_down(frame, picture_final_size)

        if save_as_png:
            cv2.imwrite(save_png_path + "{:05d}.png".format(i), frame)

        frame = transforms.ToTensor()(frame)
        torch.save(frame, save_path + "{:05d}.pt".format(i))


def save_flow_as_tensors(save_path, video_path, save_as_png=False,
                         save_png_path=path_image_opt_fl, augmentation=False):
    # load images, transform to tensors and add the label
    for i, (prev_frame, curr_frame) in enumerate(tqdm(load_double_images(video_path), "Save Opt. Flow as Tensors")):
        curr_frame = sample_down(cut_bottom(curr_frame, picture_bottom_offset), picture_opt_fl_size)
        prev_frame = sample_down(cut_bottom(prev_frame, picture_bottom_offset), picture_opt_fl_size)
        # if brightness and augmentation flag is true, run the augmentation
        # function
        if augmentation:
            contrast_factor = 0.35 + np.random.uniform()
            bright_factor = np.random.uniform(-5, 35)
            curr_frame = augment_brightness(curr_frame, contrast_factor, bright_factor)
            
            contrast_factor = 0.35 + np.random.uniform()
            bright_factor = np.random.uniform(-5, 35)
            prev_frame = augment_brightness(prev_frame, contrast_factor, bright_factor)

        rgb_flow = calculate_opt_flow(curr_frame, prev_frame)
        # print(rgb_flow)
        if save_as_png:
            cv2.imwrite(save_png_path + "{:05d}.png".format(i + 1), rgb_flow)
        # transform image to a tensor and concat them
        rgb_flow_tensor = transforms.ToTensor()(rgb_flow)
        if not augmentation:
            torch.save(rgb_flow_tensor, save_path + "{:05d}.pt".format(i + 1))
        else:
            # choose 20400 as offset, so in the dataloader, we can do modulo
            # 20400, to get the label of the frame
            offset = 20400
            torch.save(rgb_flow_tensor, save_path + "{:05d}.pt".format(i + 1 + offset))
            pass

# #############################################################
# CALCULATE OPTICAL FLOW
# #############################################################

def calculate_opt_flow(curr_frame, prev_frame):
    """
    Calculates the optical Flow of two images
    Source: https://www.geeksforgeeks.org/opencv-the-gunnar-farneback-optical-flow/
    """
    # Create mask
    hsv_mask = np.zeros_like(prev_frame)
    # Make image saturation to a maximum value
    hsv_mask[:, :, 1] = 255

    prev_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)
    curr_gray = cv2.cvtColor(curr_frame, cv2.COLOR_BGR2GRAY)

    # Optical flow is now calculated
    flow = cv2.calcOpticalFlowFarneback(prev_gray, curr_gray, None, pyr_scale=0.5, levels=3, winsize=6,
                                        iterations=3, poly_n=5, poly_sigma=1.1, flags=0)
    # Compute magnitude and angle of 2D vector
    mag, ang = cv2.cartToPolar(flow[..., 0], flow[..., 1])
    # Set image hue value according to the angle of optical flow
    hsv_mask[:, :, 0] = ang * (90 / np.pi)
    # Set value as per the normalized magnitude of optical flow
    hsv_mask[:, :, 2] = cv2.normalize(mag, None, 0, 255, cv2.NORM_MINMAX)
    # Convert to rgb
    rgb_image = cv2.cvtColor(hsv_mask, cv2.COLOR_HSV2RGB)
    rgb_image = sample_down(rgb_image, picture_final_size)
    return rgb_image


# #############################################################
# TRAIN EVALUATION DICTIONARIES
# #############################################################
<<<<<<< HEAD
def generate_train_eval_dict(data_size, test_split_ratio, new_split=True, \
                             block_size=100, offset=None):
    if new_split:
        return(generate_train_eval_dict_original(data_size, test_split_ratio))
        #return(generate_train_eval_dict_new_splitting(data_size, test_split_ratio))
    else:
        return(generate_train_eval_dict_old(data_size, test_split_ratio, block_size))
=======
>>>>>>> net_trainer_approach



def generate_test_splitting_new(data_size, test_split_ratio=0.4):
    test_block = data_size * test_split_ratio
    all_indices = np.linspace(1, data_size, data_size, dtype=int)
    train_index = all_indices < test_block
    train_indices = [*(-all_indices[train_index])]
    test_indices = [*(-all_indices[~train_index])]

    partition = {'train': train_indices, 'test': test_indices}
    return partition


def generate_test_splitting(data_size):
    return np.linspace(1, data_size, data_size, dtype=int)


def generate_block_splitting(data_size, test_split_ratio, block_size):
    test_block = block_size * test_split_ratio

    all_indices = np.linspace(1, data_size, data_size, dtype=int)
    train_index = (all_indices % block_size) < test_block
    train_indices = [*all_indices[train_index]]
    test_indices = [*all_indices[~train_index]]

    partition = {'train': train_indices, 'validation': test_indices}
    return partition


situation_params = [("highway", 0, 8400), ("traffic jam", 8400, 15000), ("city", 15000, 20399)]

<<<<<<< HEAD
    # constants:
    # Scene       | from minute to minute | frame to frame
    # ------------------------------------------------------
    # highway     | 0:00 to 7:00          | 0 to 8400
    # stop&go     | 7:00 to 12:30         | 8401 to 15000
    # city        | 12:30 to end          | 15001 to end
    
    # highway_end = int(np.floor(test_split_ratio*8400))
    # trafficjam_end = int(np.floor(test_split_ratio*15000))
    # last_split = int(np.floor(test_split_ratio*data_size))
    
    all_indices = np.linspace(1, data_size, data_size, dtype=int)
    
    # highway scenes
    
    highway_indices = all_indices[:8400]
    np.random.shuffle(highway_indices)
    
    highway_end = int(np.size(highway_indices)*test_split_ratio)
    
    highway_train = highway_indices[:highway_end]
    highway_test = highway_indices[highway_end:]
    
    # traffic jam scenes
    trafficjam_indices = all_indices[8400:15000]
    np.random.shuffle(trafficjam_indices)
    
    trafficjam_end = int(np.size(trafficjam_indices)*test_split_ratio)
    
    trafficjam_train = trafficjam_indices[:trafficjam_end]
    trafficjam_test = trafficjam_indices[trafficjam_end:]

    # city scenes
    city_indices = all_indices[15000:]
    np.random.shuffle(city_indices)
    
    city_end = int(np.size(city_indices)*test_split_ratio)
=======

def generate_situation_splitting(test_split_ratio, params=situation_params,
                                 shuffle=True, augmentation=False):
    train_indices = []
    test_indices = []
>>>>>>> net_trainer_approach

    for situation, start, stop in params:
        indices = np.linspace(start+1, stop, stop-start, dtype=int)
        if shuffle:
            np.random.shuffle(indices)
        
        if augmentation:
            train_additional = indices[0:int(test_split_ratio*len(indices))]+20400
            train_indices = [*train_indices, 
                             *indices[0:int(test_split_ratio*len(indices))],
                             *train_additional]
        else:
            train_indices = [*train_indices, 
                             *indices[0:int(test_split_ratio*len(indices))]]
        test_indices = [*test_indices, *indices[int(test_split_ratio*len(indices)):]]

    partition = {'train': train_indices, 'validation': test_indices}
    return partition


def generate_hard_cut_off_splitting(test_split_ratio):
    all_indices = np.arange(1,20400)
    point = int(len(all_indices)*test_split_ratio)
    train_indices = [*all_indices[:point]]
    test_indices = [*all_indices[point:]]
    partition = {'train': train_indices, 'validation': test_indices}
    return partition

def generate_train_eval_dict_original(data_size, test_split_ratio):
    # we have 20399 images and of frames, we split them and create a dict
    # data_size= 20399
    split_index = int(np.floor(data_size*test_split_ratio))
    all_indices = list(range(1,data_size+1))
    train_indices = [*all_indices[:split_index]]
    test_indices = [*all_indices[split_index:]]
    partition = {'train': train_indices, 'validation': test_indices}
    return(partition)


def generate_label_dict(label_path, data_size):
    # these are all labels in a txt, we want to write them into a dict and
    # ignore the first value
    labels_np_array = np.loadtxt(label_path)
    labels = {}
    for index in range(1, data_size+1):
        labels[index] = labels_np_array[index]
    return labels

## #############################################################
# Brightness augmentation
# #############################################################

def augment_brightness(frame,contrast_factor,brigth_factor=0):
    return cv2.addWeighted(frame, contrast_factor,
                           frame,0,
                           brigth_factor)
    # function to add some noise into the image
    hsv_image = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    # bright_factor = 0.2 + np.random.uniform()
    hsv_image[:,:,2] = hsv_image[:,:,2] * contrast_factor
    frame_rgb = cv2.cvtColor(hsv_image, cv2.COLOR_HSV2BGR)
    return frame_rgb

<<<<<<< HEAD
if __name__ == "__main__":
    # i1 = cv2.imread("./data/frames/frame1.png")
    # i2 = cv2.imread("./data/frames/frame2.png")
    # i2_cut_down = sample_down_half(i2[:-60,:,:])
    # flow_field = calc_of(i1, i2)
    # cv2.imwrite("../report/imgs/frame2_original.png",i2)
    # cv2.imwrite("../report/imgs/frame2_cut_sampled.png",i2_cut_down)
    # cv2.imwrite("../report/imgs/frame2_flow_field.png",flow_field)
    # save_flow_as_tensors(path_tensor_opt_fl, path_raw_video)
    # save_frames_as_tensors(path_tensor_frames, path_raw_video)
    # save_both(path_tensor_frames, path_tensor_opt_fl, path_raw_video)
    # partition = generate_train_eval_dict_new_splitting(20399,0.8)
    frame = cv2.imread("./data/frames/frame1.png")
    # in expectation we decrease the contrast
    contrast_factor = 0.5 + np.random.uniform()
    bright_factor = np.random.uniform(-30,30)
    frame_changed = augment_brightness(frame, contrast_factor,bright_factor)
    cv2.imwrite("../augmentation9.png",frame_changed)
    pass
=======
# #############################################################
# Brightness augmentation
# #############################################################

def augment_brightness(frame, contrast_factor, bright_factor=0):
    return cv2.addWeighted(frame, contrast_factor,
                           frame, 0,
                           bright_factor)
    # function to add some noise into the image
    hsv_image = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    # bright_factor = 0.2 + np.random.uniform()
    hsv_image[:, :, 2] = hsv_image[:, :, 2] * contrast_factor
    frame_rgb = cv2.cvtColor(hsv_image, cv2.COLOR_HSV2BGR)
    return frame_rgb



# if __name__ == "__main__":
#     # i1 = cv2.imread("./data/frames/frame1.png")
#     # i2 = cv2.imread("./data/frames/frame2.png")
#     # i2_cut_down = sample_down_half(i2[:-60,:,:])
#     # flow_field = calc_of(i1, i2)
#     # cv2.imwrite("../report/imgs/frame2_original.png",i2)
#     # cv2.imwrite("../report/imgs/frame2_cut_sampled.png",i2_cut_down)
#     # cv2.imwrite("../report/imgs/frame2_flow_field.png",flow_field)
#     # save_flow_as_tensors(path_tensor_opt_fl, path_raw_video)
#     # save_frames_as_tensors(path_tensor_frames, path_raw_video)
#     # save_both(path_tensor_frames, path_tensor_opt_fl, path_raw_video)
#     # partition = generate_train_eval_dict_new_splitting(20399,0.8)
#     frame = cv2.imread("./data/frames/frame1.png")
    
#     cv2.imwrite("../original.png",frame)
#     for i in range(0,10):
#         contrast_factor = 0.35 + np.random.uniform()
#         bright_factor = np.random.uniform(-5, 35)
#         frame_changed = augment_brightness(frame, contrast_factor, bright_factor)
#         cv2.imwrite("../augmentation{}.png".format(i), frame_changed)
    
#     pass

#if __name__ == "__main__":
    # save_flow_as_tensors(path_tensor_opt_fl, path_raw_video, save_as_png=False,
    #                      augmentation=True)
    #test = generate_hard_cut_off_splitting(0.8)
>>>>>>> net_trainer_approach
