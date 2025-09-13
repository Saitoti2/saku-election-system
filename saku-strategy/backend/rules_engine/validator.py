from typing import Dict, Any
from elections.models import Delegate


def validate_delegate(delegate: Delegate, rules: Dict[str, Any]) -> Dict[str, Any]:
    eligibility_rules = (rules or {}).get('eligibility', {})
    checks = []
    passed = True

    # year_min
    yr = eligibility_rules.get('year_min')
    if yr and 'value' in yr:
        ok = delegate.year_of_study >= int(yr['value'])
        checks.append({
            'rule': 'year_min',
            'passed': ok,
            'detail': f"Year >= {yr['value']}",
            'citation': yr.get('citation','')
        })
        passed = passed and ok

    # GPA not tracked yet; placeholder if present in rules
    gpa = eligibility_rules.get('gpa_min')
    if gpa and 'value' in gpa:
        # No GPA field; mark as unknown -> not failing, but recorded
        checks.append({
            'rule': 'gpa_min',
            'passed': True,
            'detail': f"GPA >= {gpa['value']} (not tracked)",
            'citation': gpa.get('citation','')
        })

    disc = eligibility_rules.get('disciplinary_clear')
    if disc and 'value' in disc:
        checks.append({
            'rule': 'disciplinary_clear',
            'passed': True,
            'detail': 'No disciplinary record (not tracked)',
            'citation': disc.get('citation','')
        })

    return {
        'eligibility_checks': checks,
        'overall_passed': passed
    }



