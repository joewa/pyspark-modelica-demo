within EDrives.Converters.Continuous;
model PowerConverterCS
  "Sets output current whilst keeping in- and output power equal"
  extends Modelica.Electrical.PowerConverters.Icons.Converter;
  extends EDrives.Interfaces.SupplyPort;
  extends EDrives.Interfaces.LoadPort;
  Modelica.Blocks.Interfaces.RealInput ref "Reference output current" annotation(Placement(transformation(extent = {{-20,-20},{20,20}}, rotation = 180, origin = {106,0}), iconTransformation(extent = {{-20,-20},{20,20}}, rotation = 180, origin = {96,0})));
  constant Modelica.SIunits.Current iUnit = 1;
equation
  iLoad = ref * iUnit;
  powerSupply = powerLoad;
  annotation(Icon(graphics), Diagram(coordinateSystem(preserveAspectRatio = false, extent = {{-100,-100},{100,100}}), graphics));
end PowerConverterCS;
