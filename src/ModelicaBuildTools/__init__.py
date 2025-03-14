import pkg_resources
import os
import sys
import shutil
import errno


SETUP_DIR = pkg_resources.resource_filename(__name__, "../")


def build_script(modelwrapper, modelName, cwd=None, cleanup=False, copy_files=True):
    info_str = str("IN: build_screipt...\n")
    if cwd is None:
        setup_dir = SETUP_DIR
        cwd = SETUP_DIR
    else:
        setup_dir = SETUP_DIR
        cwd = cwd  # os.getcwd()
    destination_folder = os.path.join(setup_dir, 'MM', 'build')
    if copy_files:
        try:
            info_str += "Try creating directory " + str(destination_folder) + "\n"
            os.makedirs(destination_folder)
            info_str += "Directory " + str(destination_folder) + "created!\n"
            files2delete = [f for f in os.listdir(destination_folder) if os.path.isfile(f)]
            for f in files2delete:
                info_str += "Deleting file " + str(f) + ".\n"
                os.remove(os.path.join(destination_folder, f))
        except FileExistsError as e:
            info_str += "Catched FileExistsErr: " + str(e) + ".\n"
            # directory already exists
            pass
        files_before_build = set([f for f in os.listdir(cwd) if os.path.isfile(f)])
    mod = modelwrapper.buildmodel(modelName)
    info_str += str(mod)
    if copy_files:
        files_after_build = set([f for f in os.listdir(cwd) if os.path.isfile(f)])
        # raise ValueError('omc stdout:' + str(mod) + '\nFiles' + str(files_after_build))
        files_new = files_after_build.difference(files_before_build)
        # print(files_new)
        for f in files_new:
            #print(f)
            if cleanup & os.path.isfile(os.path.join(destination_folder, f)):
                os.remove(os.path.join(destination_folder, f))
            if not os.path.isfile(os.path.join(destination_folder, f)):
                # shutil.move(f, destination_folder)
                copyinfo = "Copy " + str(f) + " -> " + destination_folder + "\n"
                info_str += copyinfo
                shutil.copy(f, destination_folder)
                os.remove(os.path.join(cwd, f))

        # Copy omc runtime
        omc_lib_path_list = [
            os.path.join(sys.prefix, 'lib', 'omc'),
            os.path.join(sys.prefix, 'lib', 'x86_64-linux-gnu', 'omc')]
        for omc_lib_path in omc_lib_path_list:
            omc_lib_files_list = os.listdir(omc_lib_path)
            if 'libSimulationRuntimeC' in str(omc_lib_files_list):
                break
        omc_lib_files_list = [os.path.join(omc_lib_path, f) for f in os.listdir(omc_lib_path)]
        omc_lib_files_list = [f for f in omc_lib_files_list if os.path.isfile(f)]
        if len(omc_lib_files_list) == 0:
            raise FileNotFoundError('Openmodelica runtime libs not found in ' + omc_lib_path)
        build_lib_path = os.path.join(sys.prefix, 'lib')
        if 'libopenblas' in str(os.listdir(build_lib_path)):
            lib_files_list = [os.path.join(build_lib_path, f) for f in os.listdir(build_lib_path)]
            lib_files_list = [f for f in lib_files_list if (os.path.isfile(f) and (('libstdc++' in f) or ('libopenblas' in f) or ('libnghttp' in f) or ('libquadmath' in f) or ('libgfortran' in f) or ('libss' in f) or ('crypto' in f) or ('libcurl' in f) or ('liblapack' in f)))]
            omc_lib_files_list += lib_files_list
        omc_lib_dest_dir = destination_folder
        for f in omc_lib_files_list:
            #print(f)
            #if os.path.islink(f):
            #    linkto = os.readlink(f)
            #    os.symlink(linkto, omc_lib_dest_dir)
            #else:
            copyinfo = "Copy " +str(f) + " -> " + omc_lib_dest_dir + "\n"
            info_str += copyinfo
            shutil.copy(f, omc_lib_dest_dir)

    # return mod
    return info_str
