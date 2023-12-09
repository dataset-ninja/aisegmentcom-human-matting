# https://www.kaggle.com/datasets/laurentmih/aisegmentcom-matting-human-datasets

import glob
import os
import shutil
from urllib.parse import unquote, urlparse

import cv2
import numpy as np
import supervisely as sly
from dataset_tools.convert import unpack_if_archive
from dotenv import load_dotenv
from supervisely.io.fs import (
    dir_exists,
    file_exists,
    get_file_name,
    get_file_name_with_ext,
    get_file_size,
)
from tqdm import tqdm

import src.settings as s


def count_files(path, extension):
    count = 0
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(extension):
                count += 1
    return count


def convert_and_upload_supervisely_project(
    api: sly.Api, workspace_id: int, project_name: str
) -> sly.ProjectInfo:
    # project_name = "Matting Human"
    dataset_path = "/home/grokhi/rawdata/aisegmentation-human-matting"
    images_folder = "clip_img"
    anns_folder = "matting"
    images_subfolder = "clip_"
    anns_subfolder = "matting_"
    images_ext = ".jpg"
    anns_ext = ".png"
    ds_name = "ds"
    batch_size = 30

    def create_ann(image_path):
        labels = []

        # image_np = sly.imaging.image.read(image_path)[:, :, 0]
        img_height = 800  # image_np.shape[0]
        img_wight = 600  # image_np.shape[1]

        subfolder_value = image_path.split("/")[-3]
        subfolder = sly.Tag(subfolder_meta, value=subfolder_value)

        clip_folder = image_path.split("/")[-2]
        clip_value = int(clip_folder.split("_")[-1])
        clip = sly.Tag(clip_meta, value=clip_value)

        mask_path = (
            image_path.replace(images_folder, anns_folder)
            .replace(images_subfolder, anns_subfolder)
            .replace(images_ext, anns_ext)
        )

        if file_exists(mask_path):
            mask_np = cv2.imread(mask_path, cv2.IMREAD_UNCHANGED)[:, :, 3]
            mask = mask_np != 0
            curr_bitmap = sly.Bitmap(mask)
            curr_label = sly.Label(curr_bitmap, obj_class)
            labels.append(curr_label)

        return sly.Annotation(
            img_size=(img_height, img_wight), labels=labels, img_tags=[subfolder, clip]
        )

    obj_class = sly.ObjClass("human", sly.Bitmap)
    subfolder_meta = sly.TagMeta("group", sly.TagValueType.ANY_STRING)

    clip_meta = sly.TagMeta("clip", sly.TagValueType.ANY_NUMBER)

    project = api.project.create(workspace_id, project_name, change_name_if_conflict=True)
    meta = sly.ProjectMeta(obj_classes=[obj_class], tag_metas=[subfolder_meta, clip_meta])
    api.project.update_meta(project.id, meta.to_json())

    dataset = api.dataset.create(project.id, ds_name, change_name_if_conflict=True)

    images_pathes = glob.glob(dataset_path + "/clip_img/*/*/*.jpg")

    progress = sly.Progress("Create dataset {}".format(ds_name), len(images_pathes))

    for img_pathes_batch in sly.batched(images_pathes, batch_size=batch_size):
        img_names_batch = [get_file_name_with_ext(im_path) for im_path in img_pathes_batch]

        img_infos = api.image.upload_paths(dataset.id, img_names_batch, img_pathes_batch)
        img_ids = [im_info.id for im_info in img_infos]

        anns = [create_ann(image_path) for image_path in img_pathes_batch]
        api.annotation.upload_anns(img_ids, anns)

        progress.iters_done_report(len(img_names_batch))
    return project
