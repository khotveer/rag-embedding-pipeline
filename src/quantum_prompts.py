

BASE_HEADER = """You are a quantum computing assistant trained on academic lecture notes.

Answer the question strictly based on the provided context. Do not rely on prior knowledge or assumptions. If the answer is not explicitly present in the context, reply with "I don't know."

**Key instructions:**
- Use technical terms and examples exactly as presented in the context.
- When a definition includes a quantum state (like |00⟩ or entangled states), include it explicitly.
- Avoid vague language (like "a unit vector") if not supported by the context.
If the context contains an explicit quantum state definition (e.g., |00⟩ + |11⟩), that expression must be shown in the answer."""

def _assemble(extra_instruction: str, context: str, question: str) -> str:
    return (
        BASE_HEADER
        + f"\n- {extra_instruction}\n\n"
        + "Context:\n" + context
        + "\n\nQuestion:\n" + question
        + "\n\nAnswer (structured and accurate):"
    )

def tpl_definition(context: str, question: str) -> str:
    return _assemble("Give a concise, one-sentence definition or explanation.", context, question)

def tpl_purpose(context: str, question: str) -> str:
    return _assemble("State the purpose or motivation in ≤ 3 sentences.", context, question)

def tpl_equation(context: str, question: str) -> str:
    return _assemble(
        "Include the exact equation or quantum state from the context. "
        "If the state is written in Dirac form (like |ψ⟩ = 1/√2(|00⟩ + |11⟩)), copy it directly.",
        context, question
    )

def tpl_historical(context: str, question: str) -> str:
    return _assemble("Give the name(s) and year(s) requested, citing exactly as in the context.", context, question)

def tpl_functionality(context: str, question: str) -> str:
    return _assemble("Describe the function or mechanism clearly. Use steps or bullet points if needed.", context, question)

def tpl_difference(context: str, question: str) -> str:
    return _assemble("List the differences between the two concepts. Use a bullet list or comparison structure.", context, question)

def tpl_list_reasons(context: str, question: str) -> str:
    return _assemble("Extract and return the exact 3 reasons mentioned in the context, numbered 1–3. Preserve wording and order.", context, question)