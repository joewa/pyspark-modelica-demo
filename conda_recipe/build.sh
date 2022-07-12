mkdir $PREFIX/lib/omlibrary
cp -R $SRC_DIR/Complex.mo $PREFIX/"lib/omlibrary/Complex 4.0.0.mo"
cp -R $SRC_DIR/Modelica $PREFIX/"lib/omlibrary/Modelica 3.2.3"
cp -R $SRC_DIR/ModelicaServices $PREFIX/"lib/omlibrary/ModelicaServices 4.0.0"
python setup.py build
python setup.py install --single-version-externally-managed --record=record.txt
