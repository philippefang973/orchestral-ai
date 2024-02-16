mkdir datasets
cd datasets
curl "https://zenodo.org/records/1289786/files/Orchset_dataset_0.zip?download=1" -O "orchset.zip"
curl "https://qsdfo.github.io/LOP/database/LOP_database_06_09_17.zip" -O "lop.zip"
curl "https://storage.googleapis.com/magentadata/datasets/maestro/v3.0.0/maestro-v3.0.0-midi.zip" -O "maestro.zip"

unzip "orchset.zip"
unzip "lop.zip"
unzip "maestro.zip"
cd ..
