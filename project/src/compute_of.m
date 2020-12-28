%% method to compute the optical flow of the saved frames
addpath("data/frames");
addpath("data/raw");

%% test how the opticalflow function is working and how the output looks like
% i1 = imread("frame100.png");
% i2 = ir("frame101.png");
% 
% 
% flow_func = opticalFlowFarneback("PyramidScale",0.5, "FilterSize", 15,"NeighborhoodSize",7);
% 
% r_flow = estimateFlow(flow_func,i2(:,:,1));
% g_flow = estimateFlow(flow_func,i2(:,:,2));
% b_flow = estimateFlow(flow_func,i2(:,:,3));
% imshow(i1)
% hold on
% plot(r_flow,'DecimationFactor',[5 5],'ScaleFactor',5);
% hold off
% fi(r_flow.Magnitude);
% % fi(g_flow.Magnitude);
% % fi(b_flow.Magnitude);

%% compute the optical flow of the first 100 frames, to test the cnn
% structure in matlab
vid_read = VideoReader("train.mp4");
flow_func = opticalFlowFarneback("NeighborhoodSize",7);
count = 1;
while hasFrame(vid_read) && count < 100
    frame = readFrame(vid_read);
    r_flow = estimateFlow(flow_func,frame(:,:,1));
    g_flow = estimateFlow(flow_func,frame(:,:,2));
    b_flow = estimateFlow(flow_func,frame(:,:,3));
    temp = zeros(480,640,3);
    temp(:,:,1) = r_flow.Magnitude;
    temp(:,:,2) = g_flow.Magnitude;
    temp(:,:,3) = b_flow.Magnitude;
    imwrite(temp, sprintf("data/optical_flow/of_frame%i.png",count));
    count = count + 1
end

