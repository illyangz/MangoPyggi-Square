import shlex
import subprocess
import math

MEASURE = "coverage run square.py {} {} {} {}"
REPORT = "coverage report -m"
NUM_LINES = 26

squares = [
    (1, 2, 3, 4), (1, 2, 4, 3), (2, 1, 3, 4), (2, 1, 4, 3), (3, 1, 2, 4),
    (3, 1, 4, 2), (1, 1, 1, -1), (1, 1, -1, 1), (1, -1, 1, 1),
    (1, 1, 1, 1), (100, 100, 100, 100), (99, 99, 99, 99),
    (100, 90, 100, 90), (90, 100, 90, 100), (90, 90, 90, 90), (3, 3, 2, 2),
    (5, 4, 3, 5), (5, 3, 4, 5), (4, 5, 3, 4), (4, 3, 5, 4), (3, 5, 4, 3)
]

failing = [(2, 9, 1, 1), (5, 4, 3, 5), (9, 2, 1, 1), (4, 5, 3, 4)]

missing_lines = {}
for square in squares:
    args = shlex.split(MEASURE.format(*square))
    proc = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = proc.communicate()
    proc = subprocess.Popen(shlex.split(REPORT), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    results = stdout.decode("ascii")
    for line in results.split('\n'):
        if line.strip().startswith("square.py"):
            missing_lines[square] = []
            for rng in line.split()[4:]:
                rng = rng.split(',')[0]
                if '-' in rng:
                    start, end = map(int, rng.split('-'))
                    missing_lines[square].extend(range(start, end + 1))
                else:
                    missing_lines[square].append(int(rng))

spectrum = {}
for line in range(1, NUM_LINES + 1):
    spectrum[line] = {'e_f': 0, 'n_f': 0, 'e_p': 0, 'n_p': 0}

for square in squares:
    if square in failing:
        for line in range(1, NUM_LINES + 1):
            if line in missing_lines[square]:
                spectrum[line]['n_f'] += 1
            else:
                spectrum[line]['e_f'] += 1
    else:
        for line in range(1, NUM_LINES + 1):
            if line in missing_lines[square]:
                spectrum[line]['n_p'] += 1
            else:
                spectrum[line]['e_p'] += 1

print("line #\te_f\tn_f\te_p\tn_p\tsusp")
for line in spectrum:
    spectra = spectrum[line]
    susp = float(spectra['e_f']) / math.sqrt((spectra['e_f'] + spectra['n_f']) * (spectra['e_f'] + spectra['e_p']))
    print("{}\t{}\t{}\t{}\t{}\t{}".format(
        line,
        spectra['e_f'],
        spectra['n_f'],
        spectra['e_p'],
        spectra['n_p'],
        susp
    ))
