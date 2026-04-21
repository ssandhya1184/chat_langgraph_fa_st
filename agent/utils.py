import re

def mask_email(email: str) -> str:
    name,domain = email.split("@")
    return f"{name[0]}****@{domain}"

def mask_phone(phone: str) -> str:
    return "******" + phone[-4:]

def mask_credit_Card(credit_card: str) -> str:
    return "**** **** ****" + credit_card[-4:]

PII_PATTERNS = {
    "email": re.compile(r"\b[\w\.-]+@[\w\.-]+\.\w+\b"),
    "credit_card": re.compile(r"\b\d{13,16}\b"),
    "phone": re.compile(r"\b\d{10}\b"),
}

def sanitize_text(text: str):
    redacted = text
    detected = {}

    #Find email type of text in the input string
    emails = PII_PATTERNS['email'].findall(text)
    for e in emails:
        redacted_val = mask_email(e)
        redacted = redacted.replace(e,redacted_val)
        detected.setdefault("emails", []).append(
            {
                'original': "[REDACTED]",
                'masked':redacted_val
            }
        )
    
    #Find phone numbers in the input string
    phone = PII_PATTERNS["phone"].findall(text)
    for p in phone:
        redacted_val = mask_phone(p)
        redacted = redacted.replace(p,redacted_val)
        detected.setdefault("phone",[]).append(
            {
                'original': "[REDACTED]",
                'masked' : redacted_val
            }
        )
    
    #Find Credit Card number in input string
    credit_cards = PII_PATTERNS["credit_card"].findall(text)
    for cc in credit_cards:
        redacted_val = mask_credit_Card(text)
        redacted = redacted.replace(cc,redacted_val)
        detected.setdefault("credit_card",[]).append(
            {
                'original': "[REDACTED]",
                'masked' : redacted_val
            }
        )
    
    return redacted, detected


def format_response(response: str) -> str:
    final_text = ""
    last_message = response['messages'][-1].content
    if last_message:
        # This is a list of dict
        if isinstance(last_message, list):
            #last_messgae is of type dict
            for msg in last_message:
                if msg["type"] == "text":
                    final_text = msg["text"]
            
            return final_text
    else:
        return ""


