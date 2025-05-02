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
    Main resolution algorithm.
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
                return True
            new |= resolvents
        if new.issubset(clauses):
            return False
        clauses |= new

def parse_clause(clause_str):
    """
    Parses a string like 'A ∨ ¬B ∨ C' into a set of literals {'A', '¬B', 'C'}
    """
    return set(literal.strip() for literal in clause_str.split('∨'))

def main():
    print("Enter clauses in CNF (one per line, e.g., A ∨ ¬B). Type 'END' to finish input.\n")
    clauses = []
    while True:
        line = input("Clause: ")
        if line.strip().upper() == 'END':
            break
        clause = parse_clause(line)
        clauses.append(clause)

    result = resolution(clauses)
    print("\nResult:")
    if result:
        print("Contradiction found: the set of clauses is UNSAT (unsatisfiable).")
    else:
        print("No contradiction found: the set of clauses is SAT (satisfiable).")

if __name__ == "__main__":
    main()
