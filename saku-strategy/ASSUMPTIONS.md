# ASSUMPTIONS & CONFIGURATION

This document lists assumptions made during development and how to modify them.

## 📋 Current Assumptions

### 1. Minimum Delegates Per Department
- **Default**: 3 delegates per department
- **Source**: Not explicitly found in Constitution, using reasonable default
- **Configurable**: Yes, in `rules/rules.yaml` under `min_per_department.value`
- **Citation**: TBD - needs Constitution review

### 2. Gender Balance Requirements
- **Default**: 33% female minimum per department
- **Tolerance**: 5% deviation allowed
- **Source**: Not explicitly found in Constitution, using reasonable default
- **Configurable**: Yes, in `rules/rules.yaml` under `gender_balance`
- **Citation**: TBD - needs Constitution review

### 3. Eligibility Requirements
- **Year of Study**: Minimum 2nd year (placeholder)
- **GPA**: Not tracked in current implementation
- **Disciplinary**: Not tracked in current implementation
- **Source**: Constitution parsing may have missed specific requirements
- **Configurable**: Yes, in `rules/rules.yaml` under `eligibility`

### 4. Win Score Weights
- **Minimum Gap Weight**: 5.0 (penalty for under-coverage)
- **Gender Gap Weight**: 20.0 (penalty for gender imbalance)
- **Buffer Weight**: 2.0 (bonus for over-coverage)
- **Configurable**: Yes, in `rules/rules.yaml` under `weights`

### 5. Database Configuration
- **Development**: SQLite (default)
- **Production**: PostgreSQL (recommended)
- **Configurable**: Yes, via `DATABASE_URL` environment variable

### 6. API Configuration
- **CORS**: Currently allows all origins (`*`)
- **Authentication**: Basic Django auth (no JWT)
- **Rate Limiting**: Not implemented
- **Configurable**: Yes, in Django settings

## 🔧 How to Modify Assumptions

### 1. Update Rules Configuration
Edit `rules/rules.yaml`:
```yaml
min_per_department:
  value: 5  # Change from 3 to 5
  citation: "Article X, Section Y"  # Add proper citation

gender_balance:
  target: { female_min: 0.4 }  # Change from 0.33 to 0.4
  tolerance: 0.1  # Change from 0.05 to 0.1

weights:
  w_min_gap: 10.0  # Increase penalty for under-coverage
  w_gender_gap: 15.0  # Decrease penalty for gender imbalance
```

### 2. Update Eligibility Rules
Add new eligibility checks in `rules_engine/validator.py`:
```python
def validate_delegate(delegate: Delegate, rules: Dict[str, Any]) -> Dict[str, Any]:
    # Add GPA check
    gpa = getattr(delegate, 'gpa', None)
    if gpa and gpa < 2.5:
        checks.append({
            'rule': 'gpa_min',
            'passed': False,
            'detail': f"GPA {gpa} below minimum 2.5",
            'citation': 'Article X, Section Y'
        })
```

### 3. Update Database Schema
Add new fields to `Delegate` model in `elections/models.py`:
```python
class Delegate(models.Model):
    # ... existing fields ...
    gpa = models.FloatField(null=True, blank=True)
    disciplinary_clear = models.BooleanField(default=True)
```

Then run migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. Update Frontend Display
Modify `frontend/src/ui/App.tsx` to show new fields:
```tsx
// Add GPA column to table
<th>GPA</th>
// ...
<td>{d.gpa || 'N/A'}</td>
```

## 📊 Validation Status

### ✅ Implemented
- [x] Department structure parsing
- [x] Basic eligibility validation
- [x] Win score calculation
- [x] What-if simulation
- [x] Risk assessment
- [x] API endpoints

### ⚠️ Needs Constitution Review
- [ ] Exact minimum delegates per department
- [ ] Gender balance requirements
- [ ] GPA requirements
- [ ] Disciplinary clearance requirements
- [ ] Year of study requirements
- [ ] Vetting process details

### 🔄 Pending Implementation
- [ ] Advanced eligibility checks
- [ ] Bulk import/export
- [ ] User authentication
- [ ] Role-based permissions
- [ ] Audit logging
- [ ] Email notifications

## 🎯 Next Steps

1. **Review Constitution**: Carefully read through the SAKU Constitution to extract exact requirements
2. **Update Rules**: Modify `rules/rules.yaml` with proper citations
3. **Test Scenarios**: Run simulations with real data
4. **Validate Assumptions**: Confirm all assumptions with SAKU officials
5. **Deploy**: Set up production environment

## 📞 Support

If you need to modify any assumptions or add new features:
1. Update the relevant configuration files
2. Run tests to ensure changes work
3. Update this document
4. Deploy changes

Remember: All changes should be traceable to the SAKU Constitution with proper citations.