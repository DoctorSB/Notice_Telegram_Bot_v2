import zipfile
import os


def zip_folder(folder_path, output_path):
    z = zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED, True)
    for root, dirs, files in os.walk(folder_path):
        for dir_name in dirs:
            z.write(os.path.join(root, dir_name))
        for file_name in files:
            z.write(os.path.join(root, file_name))
    z.close()
