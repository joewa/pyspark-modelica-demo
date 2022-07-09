within EDrives.Examples.DCDC;

model HBridge_DC_Drive_Test
  extends Modelica.Icons.Example;

  EDrives.Examples.DCDC.HBridge_DC_Drive hBridge_DC_Drive annotation(
    Placement(visible = true, transformation(origin = {10, -2}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Modelica.Blocks.Sources.TimeTable dutyCycleTable(table = [0, 0.5; 3, 0.5; 4, dMax; 12, dMax; 13, dMin; 21, dMin; 22, 0.5; 24, 0.5]) annotation(
    Placement(visible = true, transformation(extent = {{-40, -18}, {-20, 2}}, rotation = 0)));
  Modelica.Blocks.Sources.TimeTable torqueTable(table = [0, 0; 6, 0; 7, -tauNominal; 9, -tauNominal; 10, +tauNominal; 15, tauNominal; 16, -tauNominal; 18, -tauNominal; 19, 0; 24, 0]) annotation(
    Placement(visible = true, transformation(extent = {{60, -18}, {40, 2}}, rotation = 0)));
  parameter Modelica.Electrical.Machines.Utilities.ParameterRecords.DcPermanentMagnetData dcpmData annotation(
    Placement(visible = true, transformation(extent = {{-10, -80}, {10, -60}}, rotation = 0)));
  parameter Modelica.SIunits.Torque tauNominal=dcpmData.ViNominal
      *dcpmData.IaNominal/dcpmData.wNominal "Nominal torque";
  parameter Real dMin=0.2 "Minimum duty cycle";
  parameter Real dMax=1 - dMin "Maximum duty cycle";

equation
  connect(dutyCycleTable.y, hBridge_DC_Drive.dutyCycle_series) annotation(
    Line(points = {{-18, -8}, {2, -8}}, color = {0, 0, 127}));
  connect(torqueTable.y, hBridge_DC_Drive.loadTorque_Series) annotation(
    Line(points = {{39, -8}, {18, -8}}, color = {0, 0, 127}));
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
end HBridge_DC_Drive_Test;
