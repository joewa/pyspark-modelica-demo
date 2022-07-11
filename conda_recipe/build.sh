mkdir $PREFIX/lib/omlibrary
ln $SRC_DIR/Complex.mo $PREFIX/"lib/omlibrary/Complex 4.0.0.mo"
ln $SRC_DIR/Modelica $PREFIX/"lib/omlibrary/Modelica 3.2.3"
ln $SRC_DIR/ModelicaServices $PREFIX/"lib/omlibrary/ModelicaServices 4.0.0"
python setup.py build
python setup.py install --single-version-externally-managed --record=record.txt
