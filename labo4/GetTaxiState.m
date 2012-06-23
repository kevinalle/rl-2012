function [res] = GetTaxiState(S)
    res = 0;
    res = res+ S.x-1;
    res = res+ (S.y-1)*5;
    res = res+ (S.pasajero-1)*25;
    res = res+ (S.dest-1)*125;   
    res = res+1;
end