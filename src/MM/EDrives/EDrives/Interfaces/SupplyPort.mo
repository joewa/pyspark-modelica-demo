within EDrives.Interfaces;
partial model SupplyPort "Base model of the converter (DC)-supply port"
  extends SupplyPins;
  // parameter Modelica.SIunits.Current IConverterMax(min = 0) "Maximum admissible converter DC supply current"                                                         annotation(Dialog(tab = "Reference values and limits"));
  Modelica.SIunits.Voltage vSupply "Voltage of the supply port";
  Modelica.SIunits.Current iSupply "Current of the supply port";
  Modelica.SIunits.Power powerSupply "Power of the supply port";
equation
  vSupply = pSupply.v - nSupply.v;
  iSupply = pSupply.i;
  0 = nSupply.i + pSupply.i;
  // stoert vielleicht
  powerSupply = iSupply * vSupply;
  assert(vSupply >= 0, "The voltage of the supply port must be greater than zero! (vSupply = " + String(vSupply) + "V)");
end SupplyPort;
