% Calcola la varianza del Laplaciano per ogni immagine e salva i risultati in un file CSV.

clear; clc;

% Immagini
path = fullfile('Dataset','Da usare');
imgs = imageDatastore(path,...
    'IncludeSubfolders',true,...
    'LabelSource','foldernames');

numImages = numel(imgs.Files);

lapVariance = zeros(numImages,1);

fileNames = strings(numImages,1);

for i = 1:numImages

    img = readimage(imgs,i);

    if size(img,3) == 3
        img = rgb2gray(img);
    end

    img = double(img);

    lap = imfilter(img, fspecial('laplacian',0), 'replicate');

    lapVariance(i) = var(lap(:));

    [~, name, ext] = fileparts(imgs.Files{i});
    fileNames(i) = string(name) + string(ext);

end

T = table( ...
    fileNames, ...
    string(imgs.Labels), ...
    lapVariance, ...
    'VariableNames', {'File','Label','LapVariance'});

writetable(T,'laplacian_values.csv');