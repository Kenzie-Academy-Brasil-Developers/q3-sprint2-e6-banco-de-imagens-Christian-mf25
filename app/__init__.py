from flask import Flask, request, send_from_directory
from dotenv import load_dotenv
import os.path

load_dotenv()
app = Flask(__name__)

###############################################


def create_files_directory():
    try:
        os.mkdir("./files")
    except:
        "Unable to create files folder"


def create_download_directory():
    try:
        os.mkdir("./download")
    except:
        "Unable to create files folder"


def check_directory(directory_name):
    try:
        return os.mkdir(f"./files/{directory_name}")
    except:
        f"Unable to create {directory_name} folder"


def check_file_exist(file_name, extension):
    if (os.path.isfile(f"./files/{extension}/{file_name}")):
        return False
    else:
        return True


def all_files():
    files = {}
    folders = os.listdir("./files")

    for dir in folders:
        files[dir] = os.listdir(f"./files/{dir}")

    return files

def check_folder_exist(extension):
	all_folders = os.listdir(f"./files")
	result = extension in all_folders
	return result

def create_zip(ratio, extension):
	os.system(f"zip -r -{ratio} /tmp/images_zip ./files/{extension}")
	return "/tmp/images_zip"

###############################################


allowed = app.config["ALLOWED_EXTENSIONS"] = {"png", "jpg", "gif"}
max_length = app.config["MAX_CONTENT_LENGTH"] = 1024 * 1024
save_at = app.config["FILES_DIRECTORY"] = "./files"

create_files_directory()


@app.errorhandler(413)
def large_file(e):
    return {"message": "File larger than 1mb"}, 413


@app.post("/upload")
def upload():
    file = request.files["file"]
    format_file_name = file.filename.split()
    file_name = "_".join(format_file_name)
    extension_name = file_name.split(".")[1]
    if extension_name in allowed:

        if check_file_exist(file_name, extension_name):
            check_directory(extension_name)
            file.save(os.path.join(f"{save_at}/{extension_name}/{file_name}"))
            return {"message": "Upload performed"}, 201
        else:
            return {"message": "Name of an existing file"}, 409
    else:
        return {"message": "Extension not supported"}, 415


@app.get("/files")
def list_files():
    return {"files": all_files()}, 200


@app.get("/files/<string:extension>")
def list_files_by_extension(extension):
    try:
        files = os.listdir(f"./files/{extension}")
        return {f"{extension}": files}, 200
    except:
        return {"message": "File not found"}, 404


@app.get("/download/<string:file_name>")
def download(file_name):
    extension_name = file_name.split(".")[1]
    try:
        return send_from_directory(
            directory=f"../files/{extension_name}",
            path=f"{file_name}",
            as_attachment=True
        )
    except:
        return {"message": "File not found"}, 404


@app.get("/download-zip")
def download_dir_as_zip():
	ratio = request.args.get("compression_ratio")
	extension = request.args.get("file_extension")
	exist_extension = check_folder_exist(extension)
	
	if not exist_extension:
		return {"message": "Missing folder "}, 404
	try:
		create_zip(ratio, extension)
		return send_from_directory(
			directory=f"/tmp",
			path="images_zip.zip",
			as_attachment=True
		)
		
	except:
		return {"mesage": "File not found"}, 404