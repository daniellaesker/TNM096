from itertools import combinations

def negate(literal):
    """Negate a literal."""
    return literal[1:] if literal.startswith('¬') else '¬' + literal

def resolve(clause1, clause2):
    """
    Resolve two clauses and return a set of resolvents (each a frozenset).
    """
    resolvents = set()
    for literal in clause1:
        negated = negate(literal)
        if negated in clause2:
            # Remove the complementary pair and union the rest
            new_clause = (clause1 - {literal}) | (clause2 - {negated})
            resolvents.add(frozenset(new_clause))
    return resolvents

def resolution(clauses):
    """
    :param clauses: list of sets, where each set is a clause (set of literals)
    :return: True if a contradiction (empty clause) is derived, False otherwise
    """
    clauses = set(frozenset(c) for c in clauses)
    new = set()

    while True:
        pairs = list(combinations(clauses, 2))
        for (ci, cj) in pairs:
            resolvents = resolve(ci, cj)
            if frozenset() in resolvents:
                print(f"Derived empty clause from {ci} and {cj}.")
                print(f"Final clauses: {clauses}")
                return True
            new |= resolvents
        if new.issubset(clauses):
        # Collect all unit clauses and their implications
            assumptions = set()
            for clause in clauses:
                if len(clause) == 1:
                    literal = next(iter(clause))
                    assumptions.add(literal.strip(','))  # Add strip to remove any stray commas
                    # If we have a literal, its negation must be false
                    for other_clause in clauses:
                        if len(other_clause) == 2 and literal in other_clause:
                            other_literal = next(l for l in other_clause if l != literal)
                            assumptions.add(negate(other_literal).strip(','))  # Add strip here too
            print(f"Final assumptions: {sorted(assumptions)}")  # Sort for consistent output
            return False
        clauses |= new

def parse_clause(clause_str):
    """Parses a string like 'A ∨ ¬B ∨ C' into a set of literals {'A', '¬B', 'C'}"""
    return set(literal.strip() for literal in clause_str.split('∨'))

def main():
    # Predefined set of clauses
    predefined_clauses = [
        {'¬sun', '¬money', 'ice'},
        {'¬money', 'ice', 'movie'},
        {'¬movie', 'money'},
        {'¬movie', '¬ice'},
        {'movie'},
        {'sun', 'money', 'cry'}
    ]

    print("Using predefined clauses in CNF:")
    for clause in predefined_clauses:
        print(f"  {clause}")

    result = resolution(predefined_clauses)
    print("\nResult:")
    if result:
        print("Contradiction found: the set of clauses is UNSAT (unsatisfiable).")
    else:
        print("No contradiction found: the set of clauses is SAT (satisfiable).")

if __name__ == "__main__":
    main()
