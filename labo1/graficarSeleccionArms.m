function [] = graficarSeleccionArms(arms)
%     % Seleccion del mejor brazo
%     figure;
%     [~, maxArm]=max(bandit);
%     aa=(arms==maxArm);
%     seleccionMejorArm=cumsum(squeeze(mean(aa,2)),2);
%     bar(1:nparams,seleccionMejorArm(:,trials));
    
    % Distribucion brazos
    figure;
    nparams=size(arms,1);
    narms=length(unique(arms(:)));
    b=zeros(nparams,narms);
    for p=1:nparams
        auxA=squeeze(arms(p,:,:));
        b(p,:)=hist(auxA(:),narms);
    end
    bar(b);
end