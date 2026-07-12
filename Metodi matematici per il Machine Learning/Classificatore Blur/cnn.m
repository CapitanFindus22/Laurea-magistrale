clear;
clc;
close all;

%% Riproducibilità
rng(42);

%% Immagini
path = fullfile('Dataset', 'Da usare');

imgs = imageDatastore(path, ...
    "IncludeSubfolders", true, ...
    "LabelSource", "foldernames");

%% Split dataset (60-20-20)
[imgsTrain, imgsTemp] = splitEachLabel(imgs, 0.6, "randomized");
[imgsVal, ~] = splitEachLabel(imgsTemp, 0.5, "randomized");

%% Architettura cnn
layers = [
    imageInputLayer([224 224 1], ...
    "Normalization", "rescale-zero-one")

    convolution2dLayer(3, 8, ...
        "WeightsInitializer","he", ...
        "Name","conv1")
    batchNormalizationLayer
    reluLayer
    maxPooling2dLayer(2, "Stride", 2)

    convolution2dLayer(3, 16, ...
        "WeightsInitializer","he", ...
        "Name","conv2")
    batchNormalizationLayer
    reluLayer
    maxPooling2dLayer(2, "Stride", 2)

    dropoutLayer(0.3)

    fullyConnectedLayer(numel(categories(imgs.Labels)))
    softmaxLayer
    classificationLayer
    ];

%% Opzioni
miniBatchSize = 32;
validationFrequency = ceil(numel(imgsTrain.Files)/miniBatchSize);

options = trainingOptions("sgdm", ...
    "ExecutionEnvironment", "cpu", ...
    "DispatchInBackground", true, ...
    "ValidationPatience", 3, ...
    "InitialLearnRate", 5e-4, ...
    "L2Regularization", 1e-4, ...
    "MaxEpochs", 30, ...
    "MiniBatchSize", miniBatchSize, ...
    "Shuffle", "every-epoch", ...
    "Plots", "training-progress", ...
    "ValidationData", imgsVal, ...
    "ValidationFrequency", validationFrequency, ...
    "Verbose", true);

%% Addestramento
net = trainNetwork(imgsTrain, layers, options);

%% Salvataggio
save('rete.mat', 'net', 'options', 'layers');