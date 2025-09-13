
import re
import yaml
from typing import Dict, Any, List, Tuple


def extract_text_from_pdf(pdf_path: str) -> str:
    import pdfplumber
    parts = []
    with pdfplumber.open(pdf_path) as pdf:
        for p in pdf.pages:
            parts.append(p.extract_text(x_tolerance=1, y_tolerance=1) or '')
    return "\n".join(parts)


def split_clauses(text: str) -> List[Tuple[str,str]]:
    # Simple splitter by Article/Section headings
    pattern = re.compile(r"^(Article\s+[IVXLC]+\b[^\n]*|Section\s+\d+[^\n]*)$", re.I | re.M)
    segments = []
    last = 0
    for m in pattern.finditer(text):
        start = m.start()
        if last < start:
            head = 'Preamble' if not segments else segments[-1][0]
            segments.append((head, text[last:start].strip()))
        segments.append((m.group(1).strip(), ''))
        last = m.end()
    if last < len(text):
        head = segments[-1][0] if segments else 'Preamble'
        segments.append((head, text[last:].strip()))
    # Merge consecutive heading+body pairs
    merged: List[Tuple[str,str]] = []
    i = 0
    while i < len(segments):
        head = segments[i][0]
        body = segments[i+1][1] if i+1 < len(segments) else ''
        merged.append((head, body))
        i += 2
    return merged


def find_rule_candidates(clauses: List[Tuple[str,str]]) -> Dict[str, Any]:
    rules: Dict[str, Any] = {}
    citations: Dict[str, str] = {}

    # Defaults (will be marked editable)
    rules['min_per_department'] = { 'value': 3, 'scope': 'department', 'citation': '', 'editable': True }
    rules['gender_balance'] = { 'metric': 'ratio', 'target': { 'female_min': 0.33 }, 'tolerance': 0.05, 'scope': 'department', 'citation': '', 'editable': True }
    rules['eligibility'] = {}

    for head, body in clauses:
        text = (head + "\n" + body).lower()
        if any(k in text for k in ['delegate', 'representation', 'representative']):
            m = re.search(r"minimum\s+(?:of\s+)?(\d+)\s+delegate", text)
            if m:
                rules['min_per_department']['value'] = int(m.group(1))
                rules['min_per_department']['citation'] = head
        if any(k in text for k in ['gender', 'balance', 'equity', 'equality']):
            m = re.search(r"(\d{1,2})\s*%\s+(?:female|women)", text)
            if m:
                rules['gender_balance']['target']['female_min'] = int(m.group(1)) / 100.0
                rules['gender_balance']['citation'] = head
        if 'year' in text and any(k in text for k in ['eligib', 'candidate', 'delegate']):
            m = re.search(r"year\s*(?:of\s*study)?\s*(\d)", text)
            if m:
                rules['eligibility']['year_min'] = { 'value': int(m.group(1)), 'citation': head }
        if 'gpa' in text or 'grade point' in text:
            m = re.search(r"gpa\s*(?:of\s*at\s*least\s*)?(\d(?:\.\d)?)", text)
            if m:
                rules['eligibility']['gpa_min'] = { 'value': float(m.group(1)), 'citation': head }
        if 'disciplinary' in text or 'integrity' in text:
            rules['eligibility']['disciplinary_clear'] = { 'value': True, 'citation': head }

    return rules


def write_rules_yaml(rules: Dict[str, Any], path: str) -> None:
    with open(path, 'w') as f:
        yaml.safe_dump(rules, f, sort_keys=False)


def write_extract(clauses: List[Tuple[str,str]], path: str) -> None:
    with open(path, 'w') as f:
        f.write('# Constitution Extract (auto-generated)\n\n')
        for head, body in clauses:
            if not body.strip():
                continue
            f.write(f'## {head}\n\n')
            f.write(body.strip() + '\n\n')


def main(pdf_path: str, rules_yaml: str, extract_md: str, raw_txt_path: str) -> None:
    text = extract_text_from_pdf(pdf_path)
    with open(raw_txt_path, 'w') as f:
        f.write(text)
    clauses = split_clauses(text)
    rules = find_rule_candidates(clauses)
    write_rules_yaml(rules, rules_yaml)
    write_extract(clauses, extract_md)

if __name__ == '__main__':
    import sys
    main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
