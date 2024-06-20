within EDrives.Assemblies;

partial model HBridge "H bridge DC/DC converter"
  extends Icons.ExampleTemplate;
  parameter Modelica.SIunits.Frequency f=1000 "Switching frequency";
  Modelica.Electrical.Analog.Sources.ConstantVoltage constantVoltage(V=
        100) annotation (Placement(transformation(
        extent={{-10,-10},{10,10}},
        rotation=270,
        origin={-80,0})));
  Modelica.Electrical.Analog.Basic.Ground ground annotation (Placement(
        visible = true, transformation(extent = {{-90, -40}, {-70, -20}}, rotation = 0)));
  replaceable EDrives.Converters.SwitchingIdeal.PowerConverterVSk hBridge annotation(
    Placement(visible = true, transformation(origin = {-50, 0}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
equation
  connect(ground.p, constantVoltage.n) annotation(
    Line(points = {{-80, -20}, {-80, -10}}, color = {0, 0, 255}));
  connect(constantVoltage.p, hBridge.pSupply) annotation(
    Line(points = {{-80, 10}, {-68, 10}, {-68, 6}, {-60, 6}}, color = {0, 0, 255}));
  connect(constantVoltage.n, hBridge.nSupply) annotation(
    Line(points = {{-80, -10}, {-68, -10}, {-68, -6}, {-60, -6}}, color = {0, 0, 255}));
  annotation (Documentation(
        info="<html>
<p>H bridge example template including supply and sensors; load is not yet included</p>
</html>"));
end HBridge;
