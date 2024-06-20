within EDrives.Examples.DCDC;

model DC_Drive_Continuous
  extends Modelica.Icons.Example;
  extends EDrives.Assemblies.DC_Drive(
    redeclare Converters.Continuous.PowerConverterVSk hBridge,
    constantVoltage(V = 120)
  );
equation
  connect(ground.p, hBridge.nLoad) annotation(
    Line(points = {{-80, -20}, {-56, -20}, {-56, -10}}, color = {0, 0, 255}));
end DC_Drive_Continuous;
