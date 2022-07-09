within EDrives.Examples.DCDC;

model HBridge_DC_Drive "H bridge DC/DC converter with DC drive"
  extends ExampleTemplates.HBridge(signalPWM(useConstantDutyCycle=false),
      constantVoltage(V=120));
  extends Modelica.Icons.Example;
  parameter Modelica.SIunits.Inductance Ld=3*dcpmData.La
    "Smoothing inductance";
  parameter Modelica.SIunits.Torque tauNominal=dcpmData.ViNominal
      *dcpmData.IaNominal/dcpmData.wNominal "Nominal torque";
  parameter Real dMin=0.2 "Minimum duty cycle";
  parameter Real dMax=1 - dMin "Maximum duty cycle";
  Modelica.Electrical.Machines.BasicMachines.DCMachines.DC_PermanentMagnet
    dcpm(
    VaNominal=dcpmData.VaNominal,
    IaNominal=dcpmData.IaNominal,
    wNominal=dcpmData.wNominal,
    TaNominal=dcpmData.TaNominal,
    Ra=dcpmData.Ra,
    TaRef=dcpmData.TaRef,
    La=dcpmData.La,
    Jr=dcpmData.Jr,
    useSupport=false,
    Js=dcpmData.Js,
    frictionParameters=dcpmData.frictionParameters,
    coreParameters=dcpmData.coreParameters,
    strayLoadParameters=dcpmData.strayLoadParameters,
    brushParameters=dcpmData.brushParameters,
    ia(start=0, fixed=true),
    TaOperational=293.15,
    alpha20a=dcpmData.alpha20a,
    phiMechanical(fixed=true, start=0),
    wMechanical(fixed=true, start=0)) annotation (Placement(
        transformation(extent={{20,-80},{40,-60}})));
  parameter
    Modelica.Electrical.Machines.Utilities.ParameterRecords.DcPermanentMagnetData
    dcpmData "Data record of PM excited DC machine"
    annotation (Placement(transformation(extent={{-10,-80},{10,-60}})));
  Modelica.Mechanics.Rotational.Sources.Torque torque
    annotation (Placement(transformation(extent={{70,-80},{50,-60}})));
  Modelica.Electrical.Analog.Basic.Inductor inductor(L=Ld) annotation (
      Placement(transformation(
        origin={40,30},
        extent={{10,-10},{-10,10}},
        rotation=90)));
  Modelica.Blocks.Interfaces.RealInput dutyCycle_series annotation(
    Placement(visible = true, transformation(origin = {-100, -60}, extent = {{-20, -20}, {20, 20}}, rotation = 0), iconTransformation(origin = {-80, -58}, extent = {{-20, -20}, {20, 20}}, rotation = 0)));
  Modelica.Blocks.Interfaces.RealInput loadTorque_Series annotation(
    Placement(visible = true, transformation(origin = {100, -70}, extent = {{20, -20}, {-20, 20}}, rotation = 0), iconTransformation(origin = {82, -60}, extent = {{20, -20}, {-20, 20}}, rotation = 0)));
equation
  connect(inductor.n, dcpm.pin_ap) annotation(
    Line(points = {{40, 20}, {40, -60}, {36, -60}}, color = {0, 0, 255}));
  connect(dcpm.pin_an, currentSensor.p) annotation(
    Line(points = {{24, -60}, {24, -6}, {0, -6}}, color = {0, 0, 255}));
  connect(dcpm.flange, torque.flange) annotation(
    Line(points = {{40, -70}, {50, -70}}));
  connect(inductor.p, hbridge.dc_p2) annotation(
    Line(points = {{40, 40}, {40, 70}, {-30, 70}, {-30, 6}, {-40, 6}}, color = {0, 0, 255}));
  connect(dutyCycle_series, signalPWM.dutyCycle) annotation(
    Line(points = {{-100, -60}, {-62, -60}}, color = {0, 0, 127}));
  connect(loadTorque_Series, torque.tau) annotation(
    Line(points = {{100, -70}, {72, -70}}, color = {0, 0, 127}));
  annotation (
    experiment(
      StopTime=24,
      Interval=0.0002,
      Tolerance=1e-06),
    Documentation(info="<html>
<p>This example of an H bridge with DC drive demonstrates the operation of the DC machine in four quadrants.
The DC output voltage is equal to <code>2 * (dutyCycle - 0.5)</code> times the input voltage.</p>

<table border=\"1\" cellspacing=\"0\" cellpadding=\"2\">
<tr>
<th><strong>start time (s)</strong></th>
<th><strong>machine speed</strong></th>
<th><strong>machine torque</strong></th>
<th><strong>mode</strong></th>
</tr>
<tr>
<td>0</td> <td>zero</td> <td>zero</td> <td></td>
</tr>
<tr>
<td>3</td> <td>positive</td> <td>zero</td> <td></td>
</tr>
<tr>
<td>6</td> <td>positive</td> <td>positive</td> <td>motor</td>
</tr>
<tr>
<td>9.5</td> <td>positive</td> <td>negative</td> <td>generator</td>
</tr>
<tr>
<td>12.5</td> <td>negative</td> <td>negative</td> <td>motor</td>
</tr>
<tr>
<td>15.5</td> <td>negative</td> <td>positive</td> <td>generator</td>
</tr>
<tr>
<td>19</td> <td>negative</td> <td>zero</td> <td></td>
</tr>
<tr>
<td>22</td> <td>zero</td> <td>zero</td> <td></td>
</tr>
</table>

<p>
Plot machine current <code>dcpm.ia</code>, averaged current <code>meanCurrent.y</code>, machine speed <code>dcpm.wMechanical</code>, averaged machine speed <code>dcpm.va</code> and torque <code>dcpm.tauElectrical</code>.</p>
</html>"));
end HBridge_DC_Drive;
