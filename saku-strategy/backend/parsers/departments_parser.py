
import re
from typing import List, Dict, Tuple


def extract_text_from_pdf(pdf_path: str) -> str:
    import pdfplumber
    text_parts = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text_parts.append(page.extract_text(x_tolerance=1, y_tolerance=1) or '')
    return '\n'.join(text_parts)


def parse_departments(text: str) -> List[Tuple[str, List[str]]]:
    lines = [ln.strip() for ln in text.splitlines() if ln and ln.strip()]
    sections: List[Tuple[str, List[str]]] = []
    current_dept = None
    courses: List[str] = []

    dept_header = re.compile(r"^(?:school|faculty|department)[:\s-]+(.+)$", re.I)
    all_caps = re.compile(r"^[A-Z &/\-]{4,}$")
    bullet = re.compile(r"^(?:[-•*•]|\d+[.)])\s+(.*)$")

    for ln in lines:
        m = dept_header.search(ln)
        if m:
            if current_dept:
                sections.append((current_dept, courses))
            current_dept = m.group(1).strip()
            courses = []
            continue
        if all_caps.match(ln) and len(ln.split()) <= 8:
            if current_dept:
                sections.append((current_dept, courses))
            current_dept = ln.strip().title()
            courses = []
            continue
        b = bullet.match(ln)
        if b and current_dept:
            courses.append(b.group(1).strip())
            continue
        if current_dept and (ln.lower().startswith('bachelor') or ln.lower().startswith('diploma') or ln.lower().startswith('certificate')):
            courses.append(ln.strip())
            continue
    if current_dept:
        sections.append((current_dept, courses))
    return sections


def write_csv(sections: List[Tuple[str, List[str]]], csv_path: str) -> None:
    import csv
    with open(csv_path, 'w', newline='') as f:
        w = csv.writer(f)
        w.writerow(['department_code','department_name','course_name'])
        for dept_name, course_list in sections:
            code = re.sub(r"[^a-z0-9]+","-", dept_name.lower()).strip('-')[:20]
            if not course_list:
                w.writerow([code, dept_name, ''])
            else:
                for c in course_list:
                    w.writerow([code, dept_name, c])


def main(pdf_path: str, out_csv: str, raw_txt_path: str) -> None:
    text = extract_text_from_pdf(pdf_path)
    with open(raw_txt_path, 'w') as f:
        f.write(text)
    sections = parse_departments(text)
    write_csv(sections, out_csv)

if __name__ == '__main__':
    import sys
    main(sys.argv[1], sys.argv[2], sys.argv[3])
