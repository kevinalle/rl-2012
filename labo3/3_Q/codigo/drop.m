function [ S_res, arribo ] = drop( S )
% parada 1: (1,1)
% parada 2: (5,1)
% parada 3: (4,5)
% parada 4: (1,5)
% subido -> 5
%Si hago drop fuera de una parada, no se baja
S_res = S;
arribo = false;
if S.pasajero == 5
    if S.dest == 1 && S.x == 1 && S.y == 1
        arribo = true;
        S_res.pasajero = 1;
    elseif S.dest == 2 && S.x == 5 && S.y == 1
        arribo = true;
        S_res.pasajero = 2;
    elseif S.dest == 3 && S.x == 4 && S.y == 5
        arribo = true;
        S_res.pasajero = 3;
    elseif S.dest == 4 && S.x == 1 && S.y == 5
        arribo = true;
        S_res.pasajero = 4;
    end
end


end

