import pkg_resources
import os
import sys
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
    # raise ValueError('omc stdout:' + str(mod) + '\nFiles' + str(files_after_build))
    files_new = files_after_build.difference(files_before_build)
    for f in files_new:
        #print(f)
        if not os.path.isfile(os.path.join(destination_folder, f)) :
            # shutil.move(f, destination_folder)
            shutil.copy(f, destination_folder)
            os.remove(os.path.join(cwd, f))

    # Copy omc runtime
    omc_lib_path = os.path.join(sys.prefix, 'lib', 'x86_64-linux-gnu', 'omc')
    omc_lib_files_list = os.listdir(omc_lib_path)
    omc_lib_files_list = [os.path.join(omc_lib_path, f) for f in os.listdir(omc_lib_path)]
    omc_lib_files_list = [f for f in omc_lib_files_list if os.path.isfile(f)]
    if len(omc_lib_files_list) == 0:
        raise FileNotFoundError('Openmodelica runtime libs not found in ' + omc_lib_path)
    omc_lib_dest_dir = os.path.join(setup_dir, 'omcsimruntime')
    try:
        os.makedirs(omc_lib_dest_dir)
        files2delete = [f for f in os.listdir(omc_lib_dest_dir) if os.path.isfile(f)]
        for f in files2delete:
            os.remove(os.path.join(omc_lib_dest_dir, f))
    except FileExistsError:
        # directory already exists
        pass
    for f in omc_lib_files_list:
        #print(f)
        #if os.path.islink(f):
        #    linkto = os.readlink(f)
        #    os.symlink(linkto, omc_lib_dest_dir)
        #else:
        shutil.copy(f, omc_lib_dest_dir)

    pass
