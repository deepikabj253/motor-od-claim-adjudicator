from app.agent.prompt import build_adjudication_prompt


claim = """
The insured vehicle was damaged in a road accident.
The vehicle collided with another vehicle.
"""

policy = """
Accidental Damage:
The policy covers damage to the insured vehicle caused by
accidents, including collision, overturning, and impact with
another vehicle or object.

Exclusions:
Damage caused intentionally by the insured is not covered.
"""

prompt = build_adjudication_prompt(claim, policy)

print(prompt)