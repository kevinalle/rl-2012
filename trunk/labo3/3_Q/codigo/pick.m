function [ S_res ] = pick( S )
S_res = S;
% parada 1: (1,1)
% parada 2: (5,1)
% parada 3: (4,5)
% parada 4: (1,5)
% subido -> 5
if (S.pasajero == 1 && S.x == 1 && S.y == 1) || (S.pasajero == 2 && S.x == 5 && S.y == 1) || (S.pasajero == 3 && S.x == 4 && S.y == 5) || (S.pasajero == 4 && S.x == 1 && S.y == 5) 
    S_res.pasajero = 5;
end

% El taxi tiene que estar donde esta el pasajero.

end

