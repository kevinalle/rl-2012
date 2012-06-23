function [ relaciones ] = analizar(met_err, k)
%


    [n, q1, q2] = size(met_err);    
    pads = combntns([1:n],k);

    %[a,b]=min(sum(squeeze(met_err(:,:,:,1)./met_err(:,:,:,2)),2));
    [a,b]=min(sum(met_err(:,:,8,1)./met_err(:,:,8,2),3),[],2)

    relaciones = pads(b,:);
end
