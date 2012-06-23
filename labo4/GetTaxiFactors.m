function [s] = GetTaxiFactors(n)
    n=n-1;
    s.dest = floor(n/125) + 1;
    remainder = mod(n,125);

    s.pasajero = floor(remainder/25) + 1;
    remainder = mod(remainder,25);
    
    s.y = floor(remainder/5) + 1;
    remainder = mod(remainder,5);

    s.x = remainder + 1;
end

