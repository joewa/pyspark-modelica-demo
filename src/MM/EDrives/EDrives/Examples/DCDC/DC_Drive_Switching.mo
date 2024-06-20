within EDrives.Examples.DCDC;

model DC_Drive_Switching
  extends Modelica.Icons.Example;
  extends EDrives.Assemblies.DC_Drive(
    hBridge.signalPWM(useConstantDutyCycle = false),
    constantVoltage(V = 120)
  );
equation

end DC_Drive_Switching;
