within EDrives.Interfaces;
partial model LoadPort "Base model of the converter load port"
  extends LoadPins;
  Modelica.SIunits.Voltage vLoad "Voltage of the load port";
  Modelica.SIunits.Current iLoad "Current of the load port";
  Modelica.SIunits.Power powerLoad "Power of the load port";
equation
  vLoad = pLoad.v - nLoad.v;
  iLoad = pLoad.i;
  0 = nLoad.i + pLoad.i;
  // stoert vielleicht
  powerLoad = vLoad * iLoad;
end LoadPort;
