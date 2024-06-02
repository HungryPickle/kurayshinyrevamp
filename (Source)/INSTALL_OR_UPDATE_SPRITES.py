import os
import subprocess
import time
import shutil
import stat
import concurrent.futures

def ignore_git(dir_name, filenames):
    return ['.git']

# def masscopy(src_dir, dst_dir):
#     # Copy the directory and its contents, ignoring .git
#     shutil.copytree(src_dir, dst_dir, dirs_exist_ok=True, ignore=ignore_git)
#     return

def masscopy(src_dir, dst_dir):
    # Call robocopy
    result = subprocess.run(['robocopy', src_dir, dst_dir, '/E', '/IS'])

    # Check the return code
    if result.returncode > 3:
        raise subprocess.CalledProcessError(result.returncode, result.args)

# def copy_file(src_file, dst_dir_path):
#     dst_file = os.path.join(dst_dir_path, os.path.basename(src_file))
#     if os.path.exists(dst_file):
#         os.chmod(dst_file, stat.S_IWRITE)  # Change the permission of destination file
#         os.remove(dst_file)
#     shutil.copy2(src_file, dst_dir_path)

# def masscopy(src_dir, dst_dir):
#     # Copy the directory and its contents, ignoring .git
#     with concurrent.futures.ThreadPoolExecutor() as executor:
#         for dirpath, dirs, files in os.walk(src_dir):
#             dst_dir_path = dirpath.replace(src_dir, dst_dir, 1)
#             if not os.path.exists(dst_dir_path):
#                 os.makedirs(dst_dir_path)
#             for file_ in files:
#                 src_file = os.path.join(dirpath, file_)
#                 executor.submit(copy_file, src_file, dst_dir_path)

# def masscopy(src_dir, dst_dir):
#     # Copy the directory and its contents, ignoring .git
#     for dirpath, dirs, files in os.walk(src_dir):
#         dst_dir_path = dirpath.replace(src_dir, dst_dir, 1)
#         if not os.path.exists(dst_dir_path):
#             os.makedirs(dst_dir_path)
#         for file_ in files:
#             src_file = os.path.join(dirpath, file_)
#             dst_file = os.path.join(dst_dir_path, file_)
#             if os.path.exists(dst_file):
#                 os.chmod(dst_file, stat.S_IWRITE)  # Change the permission of destination file
#                 os.remove(dst_file)
#             shutil.copy2(src_file, dst_dir_path)
#     return

print("This will make your game preloaded by installing/updating all the sprites.")
print("Using this tool requires a stable internet connection.")
print("Close the program without choosing an option if you want to cancel the process.")
time.sleep(6)
print("Please choose an option:")
print("1. Download autogen-fusion-sprites only")
print("2. Download customsprites only")
print("3. Download both")

choice = ''
while choice not in ['1', '2', '3']:
    choice = input("Enter your choice (1, 2, or 3): ")
    if choice not in ['1', '2', '3']:
        print("Wrong choice. Please enter 1, 2, or 3.")

# Define the repositories to clone or update
repos = [
    "https://gitlab.com/pokemoninfinitefusion/autogen-fusion-sprites.git",
    "https://gitlab.com/pokemoninfinitefusion/customsprites.git"
]

if choice == '1':
    repos = [repos[0]]  # Keep only autogen-fusion-sprites
elif choice == '2':
    repos = [repos[1]]  # Keep only customsprites
# No need for an elif for choice '3' because it means we keep both repos


def remove_readonly(func, path, _):
    "Clear the readonly bit and reattempt the removal"
    os.chmod(path, stat.S_IWRITE)
    func(path)

try:
    if os.path.isdir("autogen-fusion-sprites"):
        shutil.rmtree("autogen-fusion-sprites", onerror=remove_readonly)
    if os.path.isdir("customsprites"):
        shutil.rmtree("customsprites", onerror=remove_readonly)

    # Define the path to the 7z executable and the MinGit archive
    exe_path = ".\\REQUIRED_BY_INSTALLER_UPDATER\\7z.exe"
    archive_path = "REQUIRED_BY_INSTALLER_UPDATER\\MinGit.7z"

    # Extract the MinGit archive
    subprocess.check_call([exe_path, "e", "-spf", "-aoa", archive_path])

    # Define the path to the git executable
    git_path = ".\\REQUIRED_BY_INSTALLER_UPDATER\\cmd\\git.exe"

    # Iterate over the repositories
    for repo in repos:
        # Extract the name of the repository from the URL
        name = repo.split("/")[-1].replace(".git", "")
        # Check if the repository already exists
        if not os.path.exists(name):
            # Clone the repository
            subprocess.check_call([git_path, "clone", repo])
        else:
            # Update the repository
            subprocess.check_call([git_path, "-C", name, "pull"])

        # If the repository is autogen-fusion-sprites, copy the Battlers directory
        if name == "autogen-fusion-sprites":
            print("Moving all the autogenerated sprites in their respective folders... (This may take a while)")
            if os.path.isdir(name + "/.git"):
                shutil.rmtree(name + "/.git", onerror=remove_readonly)
            # shutil.rmtree(name + "/.git", ignore_errors=True)
            src_dir = os.path.join(name, "Battlers")
            dst_dir = "Graphics/Battlers"
            masscopy(src_dir, dst_dir)
            # Delete the autogen-fusion-sprites directory
            if os.path.isdir(name):
                shutil.rmtree(name, onerror=remove_readonly)
            print("Moving all the autogenerated sprites done!")

        if name == "customsprites":
            print("Moving all the custom sprites in their respective folders... (This may take a while)")
            if os.path.isdir(name + "/.git"):
                shutil.rmtree(name + "/.git", onerror=remove_readonly)
            # shutil.rmtree(name + "/.git", ignore_errors=True)
            src_dir = os.path.join(name, "CustomBattlers")
            dst_dir = "Graphics/CustomBattlers"
            masscopy(src_dir, dst_dir)
            src_dir = os.path.join(name, "Other")
            dst_dir = "Graphics"
            masscopy(src_dir, dst_dir)
            # src_dir = os.path.join(name, "Other/BaseSprites")
            # dst_dir = "Graphics/BaseSprites"
            # masscopy(src_dir, dst_dir)
            # src_dir = os.path.join(name, "Other/Triples")
            # dst_dir = "Graphics/Triples"
            # masscopy(src_dir, dst_dir)
            # Delete the autogen-fusion-sprites directory
            if os.path.isdir(name):
                shutil.rmtree(name, onerror=remove_readonly)
            print("Moving all the custom sprites done!")


    print("\nInstaller/Updater made by Hungry Pickle")
    print("\nThank you for installing or updating the spritepacks! You can close this window now.")
    input("Press Enter to exit.")
except Exception as e:
    print(f"An error occurred: {e}")
    print("Please report this error on the Discord server or on our Github repository.")
    print("If this is a connection issue, please check your internet connection and try again.")
    input("Press Enter to exit.")