import pkg_resources
import os
import shutil


SETUP_DIR = pkg_resources.resource_filename(__name__, "../")


def build_script(setup_dir=None):
    if setup_dir is None:
        setup_dir = SETUP_DIR
        cwd = SETUP_DIR
    else:
        cwd = os.getcwd()
    destination_folder = os.path.join(setup_dir, 'ModelicaModels', 'build', "BouncingBall")
    #print(cwd)
    #print(setup_dir)
    #print(destination_folder)
    from ModelicaModels.BouncingBall import buildmodel
    try:
        os.makedirs(destination_folder)
        files2delete = [f for f in os.listdir(destination_folder) if os.path.isfile(f)]
        for f in files2delete:
            os.remove(os.path.join(destination_folder, f))
    except FileExistsError:
        # directory already exists
        pass
    files_before_build = set([f for f in os.listdir(cwd) if os.path.isfile(f)])
    mod = buildmodel()
    files_after_build = set([f for f in os.listdir(cwd) if os.path.isfile(f)])
    files_new = files_after_build.difference(files_before_build)
    for f in files_new:
        #print(f)
        if not os.path.isfile(os.path.join(destination_folder, f)) :
            shutil.move(f, destination_folder)
    pass