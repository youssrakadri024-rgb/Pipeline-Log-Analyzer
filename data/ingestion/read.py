import gzip
import os
import os.path as pt
from pathlib import Path


"""
in : data
out : list of raws
"""
def ingest(path):
    try:
        files = os.listdir(path)
        raws = []

        for file in files:
            file_path = pt.join(path, file)

            if file.endswith('.gz'):
                opener = gzip.open(file_path, 'rt')
            else:
                opener = open(file_path, 'r')

            with opener as f:
                raws.extend(f.readlines())

        return raws

    except Exception as e:
        print(e)
        return []


if __name__ == '__main__':
    data = ingest('./data')

    if data:
        print(data[:10])