function [ S_res, arribo ] = drop( S )
%Si hago drop fuera de una parada, no se baja
% parada 1: (1,1)
% parada 2: (5,1)
% parada 3: (4,5)
% parada 4: (1,5)
% subido -> 5
    S_res = S;
    arribo = false;
    
    if S.pasajero == 5
        if (isequal([S.x, S.y],[1,1]))
            S_res.pasajero = 1;
        end
        if (isequal([S.x, S.y],[5,1]))
                S_res.pasajero = 2;
        end
        if (isequal([S.x, S.y],[4,5]))
                S_res.pasajero = 3;
        end
        if (isequal([S.x, S.y],[1,5]))
                S_res.pasajero = 4;
        end
        if S_res.pasajero == S_res.dest
            arribo = true;
        end        
    end
end

