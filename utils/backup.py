import os
import shutil


def backup_file(backup_path, folder, file, dry_mode=False, pbar=None):
    file_path = os.path.join(folder, file)
    root_path = os.path.commonpath([backup_path, folder])
    backup_file_path = os.path.join(root_path, os.path.relpath(backup_path, root_path), os.path.relpath(file_path, root_path))
    previous_path = str()

    if not dry_mode:
        for path in os.path.dirname(backup_file_path).split(os.sep):
            # ensure that the folders already exist prior to backup the files
            path = os.path.join(previous_path, path)
            if not os.path.isdir(path):
                os.mkdir(os.path.abspath(path))
            previous_path = path + os.sep

    if os.path.isfile(file_path):
        if not os.path.isfile(backup_file_path):
            if not dry_mode:
                shutil.copyfile(file_path, backup_file_path)
            if not pbar is None:
                if dry_mode:
                    pbar.range+=1
                else:
                    pbar.update("%s" % file)
