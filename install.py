#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2023 Huawei Device Co., Ltd.
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import argparse
import os
import subprocess
import sys


def untar_file(tar_file_path, extract_path, args):
    try:
        if os.path.exists(extract_path):
            rm_cmd = ['rm', '-rf', extract_path]
            subprocess.run(rm_cmd, check=True)

        tar_cmd = ['tar', '-zxvf', tar_file_path, '-C', args.gen_dir]
        subprocess.run(tar_cmd, check=True)

    except Exception as e:
        print("tar error!")
        return


def apply_patch(patch_file, target_dir):
    try:
        if not os.path.exists(target_dir):
            return

        patch_cmd = ['patch', '-p1', "--fuzz=0", "--no-backup-if-mismatch", '-i', patch_file, '-d', target_dir]
        subprocess.run(patch_cmd, check=True)

    except Exception as e:
        print("apply_patch error!")
        return


def do_patch(args, target_dir):
    patch_file = [
        "Fix error whenparses the value of 5E-324 with libc++.patch",
        "0001-Parse-large-floats-as-infinity-1349-1353.patch",
        "0001-Use-default-rather-than-hard-coded-8-for-maximum-agg.patch",
        "Fix.patch"
    ]

    for patch in patch_file:
        file_path = os.path.join(args.source_file, patch)
        apply_patch(file_path, target_dir)


def main():
    libpng_path = argparse.ArgumentParser()
    libpng_path.add_argument('--gen-dir', help='generate path of jsoncpp')
    libpng_path.add_argument('--source-file', help='jsoncpp source compressed dir')
    args = libpng_path.parse_args()
    tar_file_path = os.path.join(args.source_file, "jsoncpp-1.9.5.tar.gz")
    target_dir = os.path.join(args.gen_dir, "jsoncpp-1.9.5")
    untar_file(tar_file_path, target_dir, args)
    do_patch(args, target_dir)
    return 0


if __name__ == '__main__':
    sys.exit(main())
