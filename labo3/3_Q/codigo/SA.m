function [ S_next, reward, eoe ] = SA( S, a )
% 'a' de 1 a 4 vale por direcciones, 5 por pick, 6 por drop 
    reward = -1;
    eoe = false;
    directions = ['N','S','O','E'];

    state = GetTaxiFactors(S);
    if a <= 4
        S_next = move(state, directions(a));
    elseif a == 5
        S_next = pick(state);
    elseif a == 6
        [S_next, eoe] = drop(state);
        if eoe
            reward = 10;
        else
            reward = -10;
        end
    end
    S_next = GetTaxiState(S_next);
end

