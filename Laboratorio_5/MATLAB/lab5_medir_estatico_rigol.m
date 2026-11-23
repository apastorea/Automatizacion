function outputFolder = lab5_medir_estatico_rigol(label,expectedVoltage)
%LAB5_MEDIR_ESTATICO_RIGOL Mide CH1/J8 durante diagnostico DAC estatico.
arguments
    label (1,1) string
    expectedVoltage (1,1) double
end

scriptFolder = fileparts(mfilename("fullpath"));
stamp = string(datetime("now",Format="yyyyMMdd_HHmmss"));
outputFolder = fullfile(scriptFolder,"datos_experimentales", ...
    "lab5_" + label + "_" + stamp);
mkdir(outputFolder);

devices = visadevlist;
row = contains(devices.ResourceName,"0x1AB1",IgnoreCase=true) & ...
    contains(devices.SerialNumber,"DS1ZE275014864",IgnoreCase=true);
assert(nnz(row)==1,"No se encontro exactamente un RIGOL DS1202Z-E.");
scope = visadev(devices.ResourceName(row));
scope.Timeout = 15;
scope.ByteOrder = "little-endian";

commands = [
    ":STOP"
    ":CHAN1:DISP ON"
    ":CHAN1:COUP DC"
    ":CHAN1:BWL 20M"
    ":CHAN1:PROB 10"
    ":CHAN1:SCAL 0.05"
    ":CHAN1:OFFS " + compose("%.6g",-expectedVoltage)
    ":TIM:SCAL 0.001"
    ":ACQ:TYPE HRES"
    ":TRIG:SWE AUTO"
    ":RUN"
    ];
for command = commands.'
    writeline(scope,command);
end
pause(0.2);
writeline(scope,":TFOR");
pause(0.8);
writeline(scope,":STOP");

writeline(scope,":WAV:SOUR CHAN1");
writeline(scope,":WAV:MODE NORM");
writeline(scope,":WAV:FORM BYTE");
preamble = str2double(split(strip(writeread(scope,":WAV:PRE?")),","));
writeline(scope,":WAV:DATA?");
raw = double(readbinblock(scope,"uint8"));
assert(~isempty(raw),"El RIGOL no devolvio muestras de CH1.");
sample = (0:numel(raw)-1).';
time_s = (sample-preamble(7)).*preamble(5)+preamble(6);
voltage_V = (raw(:)-preamble(9)-preamble(10)).*preamble(8);
waveform = table(sample,time_s,raw(:),voltage_V, ...
    VariableNames=["sample","time_s","raw","voltage_V"]);
writetable(waveform,fullfile(outputFolder,"chan1_J8.csv"));

writeline(scope,":DISP:DATA? ON,OFF,PNG");
imageBytes = readbinblock(scope,"uint8");
fid = fopen(fullfile(outputFolder,"pantalla.png"),"w");
assert(fid~=-1,"No se pudo crear la captura PNG.");
cleanupFile = onCleanup(@() fclose(fid));
fwrite(fid,imageBytes,"uint8");

summary = table(expectedVoltage,mean(voltage_V,"omitmissing"), ...
    std(voltage_V,0,"omitmissing"),min(voltage_V,[],"omitmissing"), ...
    max(voltage_V,[],"omitmissing"), ...
    VariableNames=["expected_V","mean_V","std_V","min_V","max_V"]);
writetable(summary,fullfile(outputFolder,"resumen.csv"));
disp(summary)
fprintf("MEDICION_ESTATICA_COMPLETA: %s\n",outputFolder);
end
