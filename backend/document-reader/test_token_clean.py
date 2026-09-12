import re

SERVICE_TABLE_TERMINATORS = [
    "project /", "lumpsum", "based", "monthly", "package", "estimated cost",
    "delivery days", "डिलीवरी", "मात्रा", "quantity", "s.no", "सं.", "परेषिती",
    "consignee", "reporting", "officer", "अिधकार", "अतिरिक्त आवश्यकता", "additional requirement",
    "buyer added", "special terms", "specification", "technical specifications", "advisory", "clause"
]

def clean_address_tokens(raw_tokens):
    cleaned = []
    for token in raw_tokens:
        tok_lower = token.lower().strip()
        # Check if this token is a service table column or terminator
        if any(term in tok_lower for term in [
            "project /", "lumpsum", "based", "monthly basis", "delivery days",
            "s.no", "सं.", "additional requirement", "अतिरिक्त आवश्यकता", "buyer added", "special terms"
        ]):
            break
        
        # Remove single junk tokens like "N/A" or isolated punctuation
        if tok_lower in ["n/a", "na", "-", "/", "\\", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]:
            continue
        
        # Clean token
        clean_tok = re.sub(r'\*+', '', token).strip()
        if len(clean_tok) > 1:
            cleaned.append(clean_tok)
            
    res = ", ".join(cleaned)
    res = re.sub(r'^[,\s]+|[,\s]+$', '', res)
    res = re.sub(r',\s*,', ',', res)
    return res

# Test token cleaning
sample = [
    "IOCL, Marketing", "Division Head Office. IndianOIl", "Bhavan,.", "G-9, Ali Yavar Jung",
    "Marg, Bandra (East). Mumbai", "400051", "Project /", "Lumpsum", "Based", "N/A", "5.सं./S.N"
]
print("Cleaned address:", clean_address_tokens(sample))
