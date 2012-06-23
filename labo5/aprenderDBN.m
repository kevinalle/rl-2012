function [meteorologos, met_error, relaciones] = aprenderDBN(n, k)
% Recibe n=nro factores, k=max in-degree (max nro de padres). n=6, k=3 en
% el ejemplito implementado en doEsperar.

% Para cada factor n, genera (n choose k) meteorologos, donde cada
% meteorologo le va a prestar atencion a una combinacion posible de padres.
% choose k from n filas y k columnas.
dominio_meteorologos = combntns(1:n,k);

% cada meteorologo mira para el factor i como depende de cada
% posible combinación de los 3 factores que mira y además cuenta cuantas
% veces sucedio
meteorologos = zeros(n,length(dominio_meteorologos),2^k,2);
num_pedidos = 10000;
T=200;
met_error = zeros(n,length(dominio_meteorologos),2^k,2);
s = randi([0 1],1,n);


for e=1:num_pedidos
    s_next = doEsperar(s);
    for i=1:n
        for m=1:length(dominio_meteorologos) %para cada meteorologo del factor i
            % Para cada observacion de doEsperar:
            %   Mandarsela a los meteorologos para que actualicen sus estimaciones.
            
            %   Calcular la probabilidad de que s_next(i) == 1, dado s(dominio_meteorologs(m,:))
            caso = bi2de(s(dominio_meteorologos(m,:))) + 1;
            
            
            %   Los meteorologos deberian contar nro de ejemplos que tienen para cada
            %   entradita.
            %   Si tienen mas de M, que empiecen a predecir y estimar su error:
            if meteorologos(i, m, caso, 2) > T
                prob = meteorologos(i, m, caso, 1)/meteorologos(i, m, caso, 2);
                met_error(i,m,caso, :) = squeeze(met_error(i,m,caso, :)) + [sqrt(prob^2 - s_next(i)) 1]';
            else
                meteorologos(i, m, caso, :) = squeeze(meteorologos(i, m, caso, :)) + [s_next(1) 1]';
            end
            %   diferencia cuadrada entre estimacion y observacion. Se van sumando.
            
            % AYUDA: usar funcion bi2de para mapear un vector de 0s y 1s a
            % un entero. Sirve para indexar sobre asignaciones de los
            % padres:
            % ind_asignacion=bi2de(s(dominio_meteorologos(m,:))) + 1;
            
        end
    end
    s = s_next;
end

% Despues de un rato de estimar error, podes pedir, para cada factor, cual
% es el meteorologo con menor error. O sea, cuales son los padres. Usar
% analizar.m
relaciones = analizar(met_error, k);

end
