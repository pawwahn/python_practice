import os
folder_path = r"C:\Users\56007\PycharmProjects\python_practice"
file_path = folder_path + "\\delete_this_file.docx"
if os.path.exists(folder_path):
    if os.path.isfile(file_path):
        print("File exists")
        os.remove(file_path)