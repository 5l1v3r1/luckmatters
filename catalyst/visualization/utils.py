import pickle
import torch
import os
import sys
import glob
import yaml

def find_params(data, cond):
    for d in data:
        found = True
        for k, v in cond.items():
            if d["args"][k] != v:
                found = False
        if found:
            return d
    return None

def find_all_params(data, cond):
    all_d = []
    for d in data:
        found = True
        for k, v in cond.items():
            if d["args"][k] != v:
                found = False
        if found:
            all_d.append(d)
    return all_d

def load_data(root):
    data = []
    total = 0
    folders = sorted(glob.glob(os.path.join(root, "*")))
    last_prefix = None

    for folder in folders:
        path, folder_name = os.path.split(folder)
        prefix, job_id = folder_name.split("_")
        if prefix == last_prefix:
            continue

        args = yaml.load(open(os.path.join(folder, "config.yaml"), "r"))
        filename = os.path.join(folder, "stats.pickle")
        if os.path.exists(filename):
            print(f"{len(data)}: {folder}")
            stats = torch.load(filename)
            data.append(dict(args=args,stats=stats))
            last_prefix = prefix
            
    return data