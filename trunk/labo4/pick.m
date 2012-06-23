function [ S_res ] = pick( S )
% parada 1: (1,1)
% parada 2: (5,1)
% parada 3: (4,5)
% parada 4: (1,5)
% subido -> 5
    S_res = S;
    if (isequal([S.x, S.y],[1,1]) && S.pasajero == 1)
            S_res.pasajero = 5;
    end
    if (isequal([S.x, S.y],[5,1]) && S.pasajero == 2)
            S_res.pasajero = 5;
    end
    if (isequal([S.x, S.y],[4,5]) && S.pasajero == 3)
            S_res.pasajero = 5;
    end
    if (isequal([S.x, S.y],[1,5]) && S.pasajero == 4)
            S_res.pasajero = 5;
    end
end

