import re

CASE_NUMBER_PATTERN = re.compile(r'(?:W\.P\.|WP|Case|Civil Appeal|Criminal Petition)\s*(?:No\.)?\s*\d+/\d{4}', re.IGNORECASE)
DATE_PATTERN = re.compile(r'\b(\d{1,2}[/-]\d{1,2}[/-]\d{4}|\d{1,2}\s+[A-Za-z]+\s+\d{4})\b')
