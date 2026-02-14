# RK 2023 Scripts

## rk23_parliament.py
Deterministic reconstruction of the 101 elected members for RK elections.

### Requirements
- Python 3.x
- `matplotlib` only if you use `--pie`

### Run (any shell)
```bash
cd /path/to/evoting
python rk23_parliament.py --out print
```

If `python` is not found, try:
```bash
python3 rk23_parliament.py --out print
```

### Options
- `--voting <path>`  
  Path to `VOTING_RESULT_IN_COUNTIES.xml` (default: `VOTING_RESULT_IN_COUNTIES.xml`)
- `--candidates <path>`  
  Path to `ELECTION_CANDIDATES.xml` (default: `ELECTION_CANDIDATES.xml`)
- `--out print|csv|txt`  
  Output mode (default: `print`)
- `--pie [file]`  
  Write 3 pie charts (paper / actual / e-votes) to PNG.  
  Default filename: `seats_pies.png`
- `--base <path>`  
  Base path for default input/output files.
- `[output]` (positional)  
  Output file path for `--out csv/txt` (default: `elected_101.csv` / `elected_101.txt`)

### Examples
Print to console:
```bash
python rk23_parliament.py --out print
```

Write CSV:
```bash
python rk23_parliament.py --out csv elected_101.csv
```

Write TXT (same content as CSV):
```bash
python rk23_parliament.py --out txt
```

Write pie charts (PNG):
```bash
python rk23_parliament.py --pie
```

Custom files:
```bash
python rk23_parliament.py --voting VOTING_RESULT_IN_COUNTIES.xml --candidates ELECTION_CANDIDATES.xml --out csv out.csv
```

Use base path:
```bash
python rk23_parliament.py --base /data/rk23 --out txt
```

### Notes
- The CSV is semicolon-delimited and written with `utf-8-sig` for Excel compatibility.
- `--pie` requires `matplotlib`:
```bash
python -m pip install matplotlib
```
