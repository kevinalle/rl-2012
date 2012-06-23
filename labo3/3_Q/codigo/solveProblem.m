function [ ] = solveProblem(file_name, initial_state, Q)
    fileID = fopen(file_name,'w');
    steps = 0;
    
    s = initial_state;
    reward = 0;
    eoe = false;
    while ~eoe && steps < 100
        [val, a] = max(Q(s,:));
        [ s, r, eoe ] = SA(s, a );
        reward = reward + r;
        steps = steps + 1;
        fprintf(fileID, '%d', (a-1));
    end
    fclose(fileID);
    
    board = [1, 3, 2, 0];
    
    s = GetTaxiFactors(initial_state);
    
    x = num2str(s.x-1);
    y = num2str(s.y-1);
    
    d = num2str(board(s.dest));
    
    if s.pasajero == 5
        fprintf('No se puede graficar ya que empieza sobre el auto');
    else
        p = num2str(board(s.pasajero));        
        system(['python taxi-animate.py ' file_name ' ' x ' ' y ' ' p ' ' d ])
    end
    fprintf('Resuelto en %d pasos con un reward de %4.2f\n', steps, reward);
end