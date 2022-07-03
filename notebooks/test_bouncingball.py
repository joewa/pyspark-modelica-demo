# Versuche libOpenModelicaCompiler.so zu finden 
# (ist relocatable - siehe info/has_prefiix https://docs.conda.io/projects/conda-build/en/latest/resources/make-relocatable.html)
#  und dann den Path ermitteln
# libSimulationRuntimeC.so ist im gleichen Pfad
# Idee: - versuche in setup.py mit build zu finden und kopiere alle Dateien in das Modelica-Paket (ugly)
#   - kopiere sie in das lib path von modelicademo
#   - hoffe dass sie dann gefunden werden
import shutil
import os
omcpath = shutil.which('omc')
if omcpath.endswith('/bin/omc'):
    omcpath = omcpath[:-7]
print(omcpath)  # /home/joerg/miniforge3/envs/testpackage/bin/omc
# die libs sind in /home/joerg/miniforge3/envs/testpackage/lib/x86_64-linux-gnu/omc/


import sys
print(sys.prefix)
omc_lib_path = os.path.join(sys.prefix, 'lib', 'x86_64-linux-gnu', 'omc')
print(omc_lib_path)

print(omc_lib_files_list)

# sys.path.insert(0, '../src')
import TestBouncingBall


if __name__ == '__main__':
    # Execute when the module is not initialized from an import statement.
    result_df = TestBouncingBall.run_bouncingball_pandas()
    print(result_df)
