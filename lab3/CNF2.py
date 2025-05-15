class Clause:
    def __init__(self, p=None, n=None):
        """
        Initialize a clause with positive and negative literals.
        p: set of positive literals
        n: set of negative literals
        """
        self.p = set() if p is None else set(p)
        self.n = set() if n is None else set(n)
    
    def __eq__(self, other):
        """Check if two clauses are equal."""
        return self.p == other.p and self.n == other.n
    
    def __hash__(self):
        """Make clause hashable for use in sets."""
        return hash((frozenset(self.p), frozenset(self.n)))
    
    def __str__(self):
        """String representation of the clause."""
        terms = []
        for lit in sorted(self.p):
            terms.append(lit)
        for lit in sorted(self.n):
            terms.append(f"¬{lit}")
        if not terms:
            return "⊥"  # Empty clause (contradiction)
        return " ∨ ".join(terms)
    
    def __repr__(self):
        return self.__str__()
    
    def is_tautology(self):
        """Check if the clause is a tautology (contains both a and ¬a)."""
        return bool(self.p.intersection(self.n))
    
    def subsumes(self, other):
        """Check if this clause subsumes or equals other clause."""
        return self.p.issubset(other.p) and self.n.issubset(other.n)
    
    def strictly_subsumes(self, other):
        """Check if this clause strictly subsumes other clause."""
        return (self.subsumes(other) and 
                (self.p < other.p or self.n < other.n))


def resolution(A, B):
    """
    Apply one resolution step to clauses A and B.
    Returns the resolvent or False if no resolution is possible or result is a tautology.
    """
    # Make copies to avoid modifying the original clauses
    A_copy = Clause(A.p, A.n)
    B_copy = Clause(B.p, B.n)
    
    # Check if there's any complementary literal between A and B
    p_n_intersection = A_copy.p.intersection(B_copy.n)
    n_p_intersection = A_copy.n.intersection(B_copy.p)
    
    if not p_n_intersection and not n_p_intersection:
        return False
    
    # Apply resolution
    if p_n_intersection:
        a = next(iter(p_n_intersection))  # Pick random element
        A_copy.p.remove(a)
        B_copy.n.remove(a)
    else:
        a = next(iter(n_p_intersection))  # Pick random element
        A_copy.n.remove(a)
        B_copy.p.remove(a)
    
    # Create resolvent
    C = Clause(A_copy.p.union(B_copy.p), A_copy.n.union(B_copy.n))
    
    # Check if C is a tautology
    if C.is_tautology():
        return False
    
    return C


def incorporate_clause(A, KB):
    """
    Incorporate a single clause A into the knowledge base KB.
    Returns the updated KB.
    """
    # Check if A is subsumed by any clause in KB
    for B in KB:
        if B.subsumes(A):
            return KB
    
    # Remove all clauses that are subsumed by A
    new_KB = set()
    for B in KB:
        if not A.subsumes(B):
            new_KB.add(B)
    
    # Add A to KB
    new_KB.add(A)
    return new_KB


def incorporate(S, KB):
    """
    Incorporate a set of clauses S into the knowledge base KB.
    Returns the updated KB.
    """
    for A in S:
        KB = incorporate_clause(A, KB)
    return KB


def solver(KB):
    """
    Apply resolution to a set of clauses KB until no new clauses can be derived.
    Returns the final set of clauses.
    """
    KB = incorporate(KB, set())
    
    while True:
        KB_prime = KB.copy()
        S = set()
        
        # Apply resolution to each pair of clauses
        clauses = list(KB)
        for i in range(len(clauses)):
            for j in range(i+1, len(clauses)):
                C = resolution(clauses[i], clauses[j])
                if C:
                    S.add(C)
        
        # If no new resolvents, we're done
        if not S:
            return KB
        
        # Incorporate new resolvents
        KB = incorporate(S, KB)
        
        # If KB didn't change, we're done
        if KB == KB_prime:
            return KB


def parse_cnf_formula(formula):
    """
    Parse a CNF formula string into a Clause object.
    Example: "¬sun ∨ ¬money ∨ ice" -> Clause(p={"ice"}, n={"sun", "money"})
    """
    if not formula:
        return Clause()
        
    p = set()
    n = set()
    
    literals = formula.split(" ∨ ")
    for lit in literals:
        lit = lit.strip()
        if lit.startswith("¬"):
            n.add(lit[1:])  # Add the variable without negation to negative set
        else:
            p.add(lit)
            
    return Clause(p, n)


def main():
    # Example from the document
    KB_formulas = [
        "¬sun ∨ ¬money ∨ ice",
        "¬money ∨ ice ∨ movie",
        "¬movie ∨ money",
        "¬movie ∨ ¬ice",
        "movie",
        "sun ∨ money ∨ cry"
    ]

    # B.1 Robbery puzzle clauses
    # KB_formulas = [ 
    #     "A ∨ B ∨ C",    # At least one of A, B, or C is guilty
    #     "¬C ∨ A",       # C → A If not C, then A is guilty
    #     "¬B ∨ A ∨ C",   # B → A ∨ C , if B is guilty, then A or C is guilty too
    #     "¬A"            # Assume A is innocent
    # ]

    
    # Parse the formulas into clauses
    KB = set()
    for formula in KB_formulas:
        clause = parse_cnf_formula(formula)
        KB.add(clause)
    
    print("Initial KB:")
    for clause in KB:
        print(f"  {clause}")
    
    # Solve
    result = solver(KB)
    
    print("\nFinal KB after resolution:")
    for clause in result:
        print(f"  {clause}")
    
    # Check if a contradiction (empty clause) was derived
    # if Clause() in result:
    #     print("\nContradiction found: A is guilty.")
    # else:
    #     print("\nNo contradiction found: A is innocent.")


if __name__ == "__main__":
    main()