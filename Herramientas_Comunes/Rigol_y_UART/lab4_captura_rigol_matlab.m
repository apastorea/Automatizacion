function outputFolder = lab4_captura_rigol_matlab(label, stopDelay, timeScale, ch1Scale, ch2Scale)
%LAB4_CAPTURA_RIGOL_MATLAB Captura sincronizada PSoC-RIGOL para el Lab. 4.
%   Espera el encabezado de una nueva ejecucion por COM4, inicia el RIGOL
%   en barrido automatico, lo detiene stopDelay segundos despues y guarda
%   la pantalla, ambas trazas y la telemetria completa del PSoC.

arguments
    label (1,1) string = "control_bode_escalon"
    stopDelay (1,1) double {mustBePositive} = 0.090
    timeScale (1,1) double {mustBePositive} = 0.010
    ch1Scale (1,1) double {mustBePositive} = 0.050
    ch2Scale (1,1) double {mustBePositive} = 0.020
end

projectRoot = fileparts(fileparts(mfilename("fullpath")));
dataRoot = fullfile(projectRoot,"Matlab","Laboratorio 4", ...
    "datos_experimentales");
stamp = string(datetime("now",Format="yyyyMMdd_HHmmss"));
outputFolder = fullfile(dataRoot,"lab4_" + label + "_" + stamp);
mkdir(outputFolder);

devices = visadevlist;
rigolRow = contains(devices.ResourceName,"0x1AB1",IgnoreCase=true) & ...
    contains(devices.SerialNumber,"DS1ZE275014864",IgnoreCase=true);
assert(nnz(rigolRow)==1,"No se encontro exactamente un RIGOL DS1202Z-E.");
resourceName = devices.ResourceName(rigolRow);

scope = visadev(resourceName);
scope.Timeout = 15;
scope.ByteOrder = "little-endian";

configureScope(scope,timeScale,ch1Scale,ch2Scale);
writeline(scope,":SING");

port = serialport("COM4",57600,Timeout=1);
configureTerminator(port,"LF");
flush(port);

fprintf("CAPTURA_LISTA: esperando reinicio del PSoC en COM4.\n");
lines = strings(0,1);
started = false;
finished = false;
deadline = tic;
while toc(deadline) < 600
    if port.NumBytesAvailable==0
        pause(0.02);
        continue
    end
    rawLine = readline(port);
    if ~(isstring(rawLine) || ischar(rawLine))
        continue
    end
    line = strip(string(rawLine));
    if strlength(line)==0
        continue
    end
    lines(end+1,1) = line;
    if ~started && startsWith(line,"# LAB4")
        started = true;
        fprintf("CAPTURA_INICIADA: encabezado LAB4 detectado; RIGOL armado en SINGLE.\n");
        pause(stopDelay);
        writeline(scope,":TFOR");
        fprintf("DISPARO_FORZADO: %.3f s despues del encabezado.\n",stopDelay);
    end
    if started && startsWith(line,"# END")
        finished = true;
        break
    end
end
assert(started,"No se detecto un nuevo encabezado LAB4 por COM4.");
assert(finished,"La telemetria del PSoC no termino antes del timeout.");
triggerState = string(strip(writeread(scope,":TRIG:STAT?")));
if triggerState~="STOP"
    writeline(scope,":STOP");
end
fprintf("RIGOL_ESTADO_FINAL: %s.\n",triggerState);

writeTextLines(fullfile(outputFolder,"psoc_uart.txt"),lines);
uartTable = parseUartTable(lines);
writetable(uartTable,fullfile(outputFolder,"psoc_uart.csv"));

captureScreen(scope,fullfile(outputFolder,"pantalla.png"));
captureWaveform(scope,"CHAN1",fullfile(outputFolder,"chan1.csv"));
captureWaveform(scope,"CHAN2",fullfile(outputFolder,"chan2.csv"));

metadata = struct;
metadata.capturedAt = string(datetime("now",TimeZone="local", ...
    Format="yyyy-MM-dd'T'HH:mm:ssXXX"));
metadata.resource = resourceName;
metadata.idn = strtrim(writeread(scope,"*IDN?"));
metadata.label = label;
metadata.stopDelay_s = stopDelay;
metadata.timeScale_s_div = timeScale;
metadata.ch1Scale_V_div = ch1Scale;
metadata.ch2Scale_V_div = ch2Scale;
metadata.channelMap = struct("CH1","J5: entrada fisica de planta u(t)", ...
    "CH2","J7: salida fisica de planta y(t)");
fid = fopen(fullfile(outputFolder,"metadata.json"),"w");
assert(fid~=-1,"No se pudo crear metadata.json.");
cleanupFile = onCleanup(@() fclose(fid));
fprintf(fid,"%s",jsonencode(metadata,PrettyPrint=true));

fprintf("CAPTURA_COMPLETA: %s\n",outputFolder);
end

function configureScope(scope,timeScale,ch1Scale,ch2Scale)
commands = [
    ":STOP"
    ":CHAN1:DISP ON"
    ":CHAN2:DISP ON"
    ":CHAN1:COUP DC"
    ":CHAN2:COUP DC"
    ":CHAN1:BWL 20M"
    ":CHAN2:BWL 20M"
    ":CHAN1:PROB 10"
    ":CHAN2:PROB 10"
    ":CHAN1:SCAL " + compose("%.9g",ch1Scale)
    ":CHAN2:SCAL " + compose("%.9g",ch2Scale)
    ":CHAN1:OFFS 0"
    ":CHAN2:OFFS 0"
    ":TIM:MODE MAIN"
    ":TIM:SCAL " + compose("%.9g",timeScale)
    ":TIM:OFFS 0"
    ":ACQ:TYPE HRES"
    ":TRIG:MODE EDGE"
    ":TRIG:EDGE:SOUR CHAN2"
    ":TRIG:EDGE:SLOP POS"
    ":TRIG:EDGE:LEV 0.5"
    ":TRIG:SWE NORM"
    ];
for command = commands.'
    writeline(scope,command);
end
end

function captureScreen(scope,fileName)
writeline(scope,":DISP:DATA? ON,OFF,PNG");
bytes = readbinblock(scope,"uint8");
fid = fopen(fileName,"w");
assert(fid~=-1,"No se pudo crear la captura PNG.");
cleanupFile = onCleanup(@() fclose(fid));
fwrite(fid,bytes,"uint8");
end

function captureWaveform(scope,channel,fileName)
writeline(scope,":WAV:SOUR " + channel);
writeline(scope,":WAV:MODE NORM");
writeline(scope,":WAV:FORM BYTE");
preamble = str2double(split(strip(writeread(scope,":WAV:PRE?")),","));
writeline(scope,":WAV:DATA?");
raw = double(readbinblock(scope,"uint8"));
assert(numel(preamble)>=10,"Preambulo de onda RIGOL incompleto.");
xIncrement = preamble(5);
xOrigin = preamble(6);
xReference = preamble(7);
yIncrement = preamble(8);
yOrigin = preamble(9);
yReference = preamble(10);
sample = (0:numel(raw)-1).';
time_s = (sample-xReference).*xIncrement+xOrigin;
voltage_V = (raw(:)-yOrigin-yReference).*yIncrement;
T = table(sample,time_s,raw(:),voltage_V, ...
    VariableNames=["sample","time_s","raw","voltage_V"]);
writetable(T,fileName);
end

function T = parseUartTable(lines)
headerIndex = find(startsWith(lines,"k,t_us,"),1,"first");
endIndex = find(startsWith(lines,"# END"),1,"first");
assert(~isempty(headerIndex) && ~isempty(endIndex) && endIndex>headerIndex, ...
    "No se encontro la tabla UART completa.");
body = lines(headerIndex:endIndex-1);
tmp = string(tempname) + ".csv";
cleanupTmp = onCleanup(@() deleteIfExists(tmp));
writeTextLines(tmp,body);
T = readtable(tmp,VariableNamingRule="preserve");
end

function writeTextLines(fileName,lines)
fid = fopen(fileName,"w");
assert(fid~=-1,"No se pudo crear %s.",fileName);
cleanupFile = onCleanup(@() fclose(fid));
for line = lines.'
    fprintf(fid,"%s\n",line);
end
end

function deleteIfExists(fileName)
if isfile(fileName)
    delete(fileName);
end
end
