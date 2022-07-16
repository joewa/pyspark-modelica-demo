within EDrives.Converters.SwitchingIdeal;
model PowerConverterVSk
  "Sets output voltage whilst keeping in- and output power equal"
  extends Modelica.Electrical.PowerConverters.Icons.Converter;
  extends EDrives.Interfaces.SupplyPins;
  extends EDrives.Interfaces.LoadPins;
  Modelica.Blocks.Interfaces.RealInput ref "Gain of input voltage" annotation(Placement(transformation(extent = {{-20,-20},{20,20}}, rotation = 180, origin = {106,0}), iconTransformation(extent = {{-20,-20},{20,20}}, rotation = 180, origin = {96,0})));
  parameter Modelica.SIunits.Frequency f=1000 "Switching frequency";
  Modelica.Electrical.PowerConverters.DCDC.HBridge hbridge(useHeatPort=
        false)
    annotation (Placement(transformation(extent={{-60,-10},{-40,10}})));
  Modelica.Electrical.PowerConverters.DCDC.Control.SignalPWM signalPWM(
      constantDutyCycle=0.6, f=f) annotation (Placement(visible = true, transformation(extent = {{-60, -40}, {-40, -20}}, rotation = 0)));
equation
  connect(hbridge.fire_p, signalPWM.fire) annotation(
    Line(points = {{-56, -12}, {-56, -19}}, color = {255, 0, 255}));
  connect(signalPWM.notFire, hbridge.fire_n) annotation(
    Line(points = {{-44, -19}, {-44, -12}}, color = {255, 0, 255}));
  connect(nSupply, hbridge.dc_n1) annotation(
    Line(points = {{-100, -60}, {-80, -60}, {-80, -6}, {-60, -6}}, color = {0, 0, 255}));
  connect(pSupply, hbridge.dc_p1) annotation(
    Line(points = {{-100, 60}, {-80, 60}, {-80, 6}, {-60, 6}}, color = {0, 0, 255}));
  connect(hbridge.dc_p2, pLoad) annotation(
    Line(points = {{-40, 6}, {20, 6}, {20, -80}, {60, -80}, {60, -100}}, color = {0, 0, 255}));
  connect(ref, signalPWM.dutyCycle) annotation(
    Line(points = {{106, 0}, {80, 0}, {80, -60}, {-70, -60}, {-70, -30}, {-62, -30}}, color = {0, 0, 127}));
  connect(hbridge.dc_n2, nLoad) annotation(
    Line(points = {{-40, -6}, {-20, -6}, {-20, -80}, {-60, -80}, {-60, -100}}, color = {0, 0, 255}));
  annotation (Documentation(
        info="<html>
<p>H bridge example template including supply and sensors; load is not yet included</p>
</html>"));

end PowerConverterVSk;
