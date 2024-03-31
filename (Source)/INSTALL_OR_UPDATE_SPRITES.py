import os
import subprocess
import time
import shutil
import stat

def ignore_git(dir_name, filenames):
    return ['.git']

def masscopy(src_dir, dst_dir):
    # Copy the directory and its contents, ignoring .git
    shutil.copytree(src_dir, dst_dir, dirs_exist_ok=True, ignore=ignore_git)
    return

print("This will make your game preloaded by installing/updating all the sprites.")
print("Using this tool requires a stable internet connection.")
time.sleep(6)
input("If you wish to proceed, press Enter. Otherwise, close this window.")
time.sleep(4)
input("Last warning! Press Enter again to proceed.")


def remove_readonly(func, path, _):
    "Clear the readonly bit and reattempt the removal"
    os.chmod(path, stat.S_IWRITE)
    func(path)

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

# Define the repositories to clone or update
repos = [
    "https://gitlab.com/pokemoninfinitefusion/autogen-fusion-sprites.git",
    "https://gitlab.com/pokemoninfinitefusion/customsprites.git"
]


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