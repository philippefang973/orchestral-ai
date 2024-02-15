mkdir datasets
curl "https://zenodo.org/records/1289786/files/Orchset_dataset_0.zip?download=1" --output "datasets/orchset.zip"
curl "https://qsdfo.github.io/LOP/database/LOP_database_06_09_17.zip" --output "datasets/lop.zip"
curl "https://storage.googleapis.com/magentadata/datasets/maestro/v3.0.0/maestro-v3.0.0-midi.zip" --output "datasets/maestro.zip"

unzip "datasets/orchset.zip"
unzip "datasets/lop.zip"
unzip "datasets/maestro.zip"