
#!/usr/bin/env python3
import os
from pathlib import Path
from parsers.departments_parser import main as dept_main
from parsers.constitution_parser import main as const_main

ROOT = Path(__file__).resolve().parents[1]
UPLOADS = ROOT.parent / 'uploads'
DATA = ROOT.parent / 'data'
RULES = ROOT.parent / 'rules'
REPORTS = ROOT.parent / 'reports'

DEPT_FILE = None
CONST_FILE = None
for cand in UPLOADS.glob('*'):
    name = cand.name.lower()
    if 'department' in name and cand.suffix.lower() in {'.pdf', '.docx', '.csv'}:
        DEPT_FILE = cand
    if 'constitution' in name and cand.suffix.lower() in {'.pdf', '.docx'}:
        CONST_FILE = cand

assert DEPT_FILE, 'Departments file not found in uploads/'
assert CONST_FILE, 'Constitution file not found in uploads/'

print('Using:', DEPT_FILE)
print('Using:', CONST_FILE)

DATA.mkdir(exist_ok=True)
RULES.mkdir(exist_ok=True)
REPORTS.mkdir(exist_ok=True)

# Departments
dept_main(str(DEPT_FILE), str(DATA / 'departments.csv'), str(DATA / 'departments_raw.txt'))
print('Wrote data/departments.csv')

# Constitution
const_main(str(CONST_FILE), str(RULES / 'rules.yaml'), str(REPORTS / 'constitution_extract.md'), str(REPORTS / 'constitution_raw.txt'))
print('Wrote rules/rules.yaml and reports/constitution_extract.md')
