# Supplementary verification artifacts

These finite calculations supplement the mathematical review; they do not constitute general proofs or formal correctness certificates. The corresponding paper review identifies the exact checked claims and remaining obligations.

Public copies of Python scripts use output filenames relative to the working directory instead of the original temporary directory. Run them from this `audits` directory. They use Python's standard library or NumPy. `audit1471.cpp` requires C++17. Result JSON and `metric-certificate.log` preserve the recorded numerical verification evidence.

`audit286.py` additionally reads `286.txt`: obtain the public submission from https://stoc2027.sigact-ec.workers.dev/submissions/286.pdf and extract it with `pdftotext -layout 286.pdf 286.txt` in this directory before running that script. The PDF itself is not redistributed here. Some scripts only print their results.
