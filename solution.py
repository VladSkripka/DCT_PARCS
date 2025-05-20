from Pyro4 import expose
import numpy as np
import math

class Solver:

    def __init__(self, workers=None, input_file_name=None, output_file_name=None):
        self.input_file = input_file_name
        self.output_file = output_file_name
        self.workers = workers
        print("Solver Inited")

    def solve(self):
        print("Job Started")

        matrix = self.read_input_matrix()
        rows = len(matrix)
        cols = len(matrix[0])
        chunk_size_rows = rows // len(self.workers)

        
        print("Starting parallel row-wise DCT...")
        mapped_row_dct_results = []
        for i in range(len(self.workers)):
            start = i * chunk_size_rows
            end = rows if i == len(self.workers) - 1 else start + chunk_size_rows
            mapped_row_dct_results.append(self.workers[i].mymap_row_dct(matrix[start:end].tolist()))
        intermediate_matrix_list = self.myreduce_collect_rows(mapped_row_dct_results)
        intermediate_matrix = np.array(intermediate_matrix_list)
        print("Row-wise DCT finished.")

        transposed_matrix = intermediate_matrix.T
        chunk_size_cols = cols // len(self.workers)

        print("Starting parallel column-wise DCT...")
        mapped_col_dct_results = []
        for i in range(len(self.workers)):
            start = i * chunk_size_cols
            end = cols if i == len(self.workers) - 1 else start + chunk_size_cols

            mapped_col_dct_results.append(self.workers[i].mymap_col_dct(transposed_matrix[start:end].tolist()))


        final_transposed_matrix_list = self.myreduce_collect_rows(mapped_col_dct_results)
        final_transposed_matrix = np.array(final_transposed_matrix_list)

        final_result_matrix = final_transposed_matrix.T
        print("Column-wise DCT finished.")

        self.write_output(final_result_matrix)
        print("Job Finished")

    def read_input_matrix(self):
        with open(self.input_file, 'r') as f:

            return np.array([[float(val) for val in line.strip().split()] for line in f])

    @staticmethod
    def dct_1d(vector):
        N = len(vector)
        result = np.zeros(N)
        factor = math.pi / (2 * N)
        for k in range(N):

            sum_val = sum(vector[n] * math.cos((2*n + 1) * k * factor) for n in range(N))
            c = math.sqrt(1.0 / N) if k == 0 else math.sqrt(2.0 / N)
            result[k] = c * sum_val
        return result

    @staticmethod
    @expose
    def mymap_row_dct(rows_list):

        rows = np.array(rows_list)

        return [Solver.dct_1d(row).tolist() for row in rows]

    @staticmethod
    @expose
    def mymap_col_dct(cols_list):

        cols = np.array(cols_list)

        return [Solver.dct_1d(col).tolist() for col in cols]


    @staticmethod
    @expose
    def myreduce_collect_rows(mapped_parts):

        output = []
        for part in mapped_parts:

            output.extend(part.value)
        return output

    def write_output(self, matrix):
        with open(self.output_file, 'w') as f:
            for row in matrix:

                f.write(' '.join(map(str, row)) + '\n')