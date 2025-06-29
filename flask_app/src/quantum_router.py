# importing important dependencies
from quantum_prompts import *

def pick_quantum_template(question: str):
    q = question.lower()

    if "reason" in q or "benefit" in q:
        return tpl_list_reasons
    elif "purpose" in q or "why" in q:
        return tpl_purpose
    elif "define" in q or "what is" in q:
        if "equation" in q or "form of" in q or "state" in q:
            return tpl_equation
        return tpl_definition
    elif "equation" in q or "form of" in q or "state" in q:
        return tpl_equation
    elif "who" in q or "year" in q:
        return tpl_historical
    elif "how" in q or "function" in q or "role" in q or "do" in q:
        return tpl_functionality
    elif "difference" in q:
        return tpl_difference
    else:
        return tpl_definition
