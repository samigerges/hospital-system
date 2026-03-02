# hospital_system/formats.py
"""
Custom date and number formats for the hospital system
"""

# English date formats
ENGLISH_DATE_FORMATS = {
    'DATE_FORMAT': 'F j, Y',           # December 15, 2024
    'DATETIME_FORMAT': 'F j, Y H:i',   # December 15, 2024 14:30
    'SHORT_DATE_FORMAT': 'm/d/Y',      # 12/15/2024
    'SHORT_DATETIME_FORMAT': 'm/d/Y H:i',  # 12/15/2024 14:30
    'TIME_FORMAT': 'H:i',              # 14:30
    'YEAR_MONTH_FORMAT': 'F Y',        # December 2024
    'MONTH_DAY_FORMAT': 'F j',         # December 15
}

# Arabic date formats
ARABIC_DATE_FORMATS = {
    'DATE_FORMAT': 'j F، Y',           # 15 ديسمبر، 2024
    'DATETIME_FORMAT': 'j F، Y H:i',   # 15 ديسمبر، 2024 14:30
    'SHORT_DATE_FORMAT': 'd/m/Y',      # 15/12/2024
    'SHORT_DATETIME_FORMAT': 'd/m/Y H:i',  # 15/12/2024 14:30
    'TIME_FORMAT': 'H:i',              # 14:30
    'YEAR_MONTH_FORMAT': 'F Y',        # ديسمبر 2024
    'MONTH_DAY_FORMAT': 'j F',         # 15 ديسمبر
}

# Number formats
NUMBER_FORMATS = {
    'USE_THOUSAND_SEPARATOR': True,
    'THOUSAND_SEPARATOR': ',',
    'DECIMAL_SEPARATOR': '.',
    'NUMBER_GROUPING': 3,
}