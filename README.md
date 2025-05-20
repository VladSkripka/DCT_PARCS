# DCT_PARCS
My DCT algorithm implementation using PARCS-Python

# Project structure
- solution.py, main file for PARCS
- Lineral_DCT.ipynb, linear DCT algorithm implementation (from Google Colab)
- input_matrix_example.txt, input example for PARCS
- input_matrix_large_example.txt, largre input example for PARCS (from 1000x1000 image)
- med.jpg, source image for input_matrix_example.txt
- large.jpg, source image for input_matrix_large_example.txt

# How to add numpy
-> gcloud compute ssh master (or worker<numer>)
-> docker ps
-> docker exec -it <container_id> /bin/bash
-> pip install numpy
To check version: python -c "import numpy; print(numpy.__version__)"
