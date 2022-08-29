import wandb

run = wandb.init(project = 'Openmmpose-3d-pose-estimation', tags = ['log video inference'])

run.name = 'log video inference'

# infer_old = wandb.Artifact('detect_v2_reid_v2', type='Inference_videos')

# infer_old.add_dir('/data.local/all/hainp/yolov5_deep_sort/deep_sort_copy/inference/detect_v2_reid_v2')

# run.log_artifact(infer_old)


infer_new = wandb.Artifact('2d_results', type='3D Pose Inferences')

infer_new.add_file('/home/ducanh/hain/code/deep-high-resolution-net-pytorch/output/175_30s_pose.avi')

run.log_artifact(infer_new)