echo $(pwd);
for N in {1..8}; do ./align-dlib.py ./dataset  align outerEyesAndNose ./dataset_aligned --size 96 & done;
./batch-represent/main.lua -outDir ./models/trained/ -data ./dataset_aligned;
./classifier.py train ./models/trained/;

