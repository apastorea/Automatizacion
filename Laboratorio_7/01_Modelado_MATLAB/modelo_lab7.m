function p = modelo_lab7()
%MODELO_LAB7 Parametros fisicos y decisiones trazables del Laboratorio 7.
% IMPORTANTE: El archivo se entrega DELIBERADAMENTE sin modelo validado.
% Nunca sustituir la planta de Lab7 por el modelo de Lab5 sin comprobar
% esquema, componentes, polaridades y definicion de estados.

p.validado = false;  % Cambiar a true SOLO despues de revisar el montaje.
p.revision_modelo = 'PENDIENTE_MEDICION_LAB7';

% x_punto = F*x + G*u ; y = H*x + J*u.
p.F = [NaN NaN; NaN NaN];
p.G = [NaN; NaN];
p.H = [NaN NaN];
p.J = 0;

% Parametros de DISEÑO PRELIMINARES, sujetos a justificación:
p.Ts_s = 0.002;   % 2 ms es antecedente de un informe, NO valor medido.
p.polos_control = [0.80+0.25i, 0.80-0.25i];
p.polos_estimador = { [0.40+0.25i, 0.40-0.25i], ...
                      [0.20+0.10i, 0.20-0.10i] };

% Entradas y condiciones iniciales de simulacion; son parametros editables.
p.referencia_V = 0.05;
p.t_sim_s = 0.20;
p.x0 = [0;0];
p.xestimado0 = [0.02;-0.01];
p.u_min_V = -1.0;   % limite HISTORICO; revisar fisicamente.
p.u_max_V =  1.0;
end
