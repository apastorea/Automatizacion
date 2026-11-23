function results = lab5_analizar_calibracion_final(dataFolder)
%LAB5_ANALIZAR_CALIBRACION_FINAL Valida la calibracion bipolar de Lab. 5.
% Conserva los valores crudos y agrega columnas corregidas por el offset
% medido. La alineacion temporal se obtiene de los cambios fisicos de J5.

arguments
    dataFolder (1,1) string {mustBeFolder}
end

ch1 = readtable(fullfile(dataFolder,"chan1_J5.csv"));
ch2 = readtable(fullfile(dataFolder,"chan2_J7.csv"));
uart = readtable(fullfile(dataFolder,"psoc_uart.csv"));

assert(height(ch1)==height(ch2),"Las trazas del RIGOL tienen distinta longitud.");
assert(height(uart)>=224,"La telemetria no contiene la secuencia completa.");
assert(all(uart.flags==0),"La telemetria contiene banderas de fallo.");

Ts = median(diff(uart.t_us))*1e-6;
plateauDuration = 32*Ts;
filteredJ5 = smoothdata(ch1.voltage_V,"movmedian",5);
deltaJ5 = abs([0;diff(filteredJ5)]);
candidateIndex = find(deltaJ5>0.015);
candidateIndex = candidateIndex([true;diff(candidateIndex)>2]);
candidateTimes = ch1.time_s(candidateIndex);
assert(numel(candidateTimes)>=6,"No se detectaron los seis cambios de J5.");

spacingError = inf(numel(candidateTimes)-5,1);
for first = 1:numel(spacingError)
    spacingError(first) = sum(abs(diff(candidateTimes(first:first+5))-plateauDuration));
end
[~,bestFirst] = min(spacingError);
edgeTimes = candidateTimes(bestFirst:bestFirst+5);
t0 = edgeTimes(1);
assert(max(abs(diff(edgeTimes)-plateauDuration))<0.03, ...
    "Los cambios fisicos no coinciden con el periodo programado.");

labels = ["cero_pre";"mas_50mV";"mas_100mV";"cero_medio"; ...
    "menos_50mV";"menos_100mV";"cero_post"];
requested_V = [0;0.050;0.100;0;-0.050;-0.100;0];
segmentStart_k = (0:32:192).';
scopeStart_s = t0 + (-1:5).'*plateauDuration;

n = numel(labels);
j5_raw_V = zeros(n,1);
j5_std_V = zeros(n,1);
j7_raw_V = zeros(n,1);
j7_std_V = zeros(n,1);
uart_requested_V = zeros(n,1);
uart_applied_V = zeros(n,1);
uart_y_V = zeros(n,1);
dac_p = zeros(n,1);
dac_n = zeros(n,1);

for i = 1:n
    scopeFirst = scopeStart_s(i) + 0.25*plateauDuration;
    scopeLast = scopeStart_s(i) + 0.75*plateauDuration;
    scopeRows = ch1.time_s>=scopeFirst & ch1.time_s<scopeLast;
    assert(nnz(scopeRows)>=10,"Muy pocas muestras del RIGOL en la meseta %s.",labels(i));
    j5_raw_V(i) = mean(ch1.voltage_V(scopeRows),"omitmissing");
    j5_std_V(i) = std(ch1.voltage_V(scopeRows),0,"omitmissing");
    j7_raw_V(i) = mean(ch2.voltage_V(scopeRows),"omitmissing");
    j7_std_V(i) = std(ch2.voltage_V(scopeRows),0,"omitmissing");

    uartRows = uart.k>=segmentStart_k(i) & uart.k<segmentStart_k(i)+32;
    uart_requested_V(i) = mean(uart.u_requested_mV(uartRows),"omitmissing")/1000;
    uart_applied_V(i) = mean(uart.u_applied_mV(uartRows),"omitmissing")/1000;
    uart_y_V(i) = mean(uart.y_mV(uartRows),"omitmissing")/1000;
    dac_p(i) = mean(uart.dac_p(uartRows),"omitmissing");
    dac_n(i) = mean(uart.dac_n(uartRows),"omitmissing");
end

zeroRows = requested_V==0;
j5_offset_V = mean(j5_raw_V(zeroRows));
j7_offset_V = mean(j7_raw_V(zeroRows));
j5_corrected_V = j5_raw_V-j5_offset_V;
j7_corrected_V = j7_raw_V-j7_offset_V;
j5_error_vs_applied_V = j5_corrected_V-uart_applied_V;

actuatorFit = polyfit(uart_applied_V,j5_raw_V,1);
adcFit = polyfit(uart_y_V,j7_raw_V,1);
actuatorResidual = j5_raw_V-polyval(actuatorFit,uart_applied_V);
adcResidual = j7_raw_V-polyval(adcFit,uart_y_V);

levels = table(labels,requested_V,uart_requested_V,uart_applied_V,dac_p,dac_n, ...
    j5_raw_V,j5_std_V,j5_corrected_V,j5_error_vs_applied_V, ...
    uart_y_V,j7_raw_V,j7_std_V,j7_corrected_V, ...
    VariableNames=["level","requested_V","uart_requested_V","uart_applied_V", ...
    "dac_p","dac_n","j5_raw_V","j5_std_V","j5_corrected_V", ...
    "j5_error_vs_applied_V","uart_y_V","j7_raw_V","j7_std_V", ...
    "j7_corrected_V"]);

metric = ["sample_period";"first_physical_edge";"j5_zero_offset"; ...
    "j5_per_applied_slope";"j5_fit_intercept";"j5_fit_rmse"; ...
    "j7_zero_offset";"j7_per_uart_y_slope";"j7_fit_intercept";"j7_fit_rmse"];
value = [Ts;t0;j5_offset_V;actuatorFit(1);actuatorFit(2); ...
    sqrt(mean(actuatorResidual.^2));j7_offset_V;adcFit(1);adcFit(2); ...
    sqrt(mean(adcResidual.^2))];
unit = ["s";"s";"V";"V/V";"V";"V";"V";"V/V";"V";"V"];
fitSummary = table(metric,value,unit);

writetable(levels,fullfile(dataFolder,"resumen_niveles.csv"));
writetable(fitSummary,fullfile(dataFolder,"ajustes_calibracion.csv"));

fig = figure(Color="w",Position=[80 80 1250 760]);
layout = tiledlayout(fig,2,2,TileSpacing="compact",Padding="compact");
nexttile(layout,[1 2]);
plot(ch1.time_s,ch1.voltage_V,LineWidth=1.2,DisplayName="J5: mando"); hold on
plot(ch2.time_s,ch2.voltage_V,LineWidth=1.2,DisplayName="J7: salida");
for edge = edgeTimes.'
    xline(edge,":",Color=[0.25 0.25 0.25],HandleVisibility="off");
end
grid on; xlabel("Tiempo (s)"); ylabel("Tension (V)");
title("Calibracion bipolar: valores crudos medidos"); legend(Location="best");

nexttile;
scatter(uart_applied_V,j5_raw_V,55,"filled",DisplayName="Mesetas"); hold on
xFit = linspace(min(uart_applied_V),max(uart_applied_V),100);
plot(xFit,polyval(actuatorFit,xFit),LineWidth=1.3,DisplayName="Ajuste lineal");
grid on; axis equal; xlabel("u aplicada por firmware (V)"); ylabel("J5 crudo (V)");
title(sprintf("Actuador: offset %.2f mV, pendiente %.4f", ...
    1000*actuatorFit(2),actuatorFit(1))); legend(Location="best");

nexttile;
scatter(uart_y_V,j7_raw_V,55,"filled",DisplayName="Mesetas"); hold on
yFit = linspace(min(uart_y_V),max(uart_y_V),100);
plot(yFit,polyval(adcFit,yFit),LineWidth=1.3,DisplayName="Ajuste lineal");
grid on; axis equal; xlabel("y calculada desde ADC (V)"); ylabel("J7 crudo (V)");
title(sprintf("Lectura: offset %.2f mV, pendiente %.4f", ...
    1000*adcFit(2),adcFit(1))); legend(Location="best");
exportgraphics(fig,fullfile(dataFolder,"calibracion_bipolar.png"),Resolution=300);
close(fig);

results = struct("levels",levels,"fitSummary",fitSummary, ...
    "edgeTimes_s",edgeTimes,"dataFolder",dataFolder);
disp(levels)
disp(fitSummary)
fprintf("CALIBRACION_ANALIZADA: %s\n",dataFolder);
end
