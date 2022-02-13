class utilities {
  utilities() {
  }

  boolean areEquivalent(formula F, formula G) {
    boolean check = false;
    return check;
  }

  formula sum(ArrayList<formula> formulas) {
    // combines formulas f1...fn into a sum
    formula S = new formula();
    S.type = 1;
    for (int i=0; i<formulas.size(); i++) {
      S.children.add(formulas.get(i));
    }
    return S;
  }

  formula product(ArrayList<formula> formulas) {
    // combines formulas f1...fn into a product
    formula P = new formula();
    P.type = 2;
    for (int i=0; i<formulas.size(); i++) {
      P.children.add(formulas.get(i));
    }
    return P;
  }

  formula opposite(formula F) {
    // returns the opposite of formula F
    formula OP = new formula();
    OP.type = 3;
    OP.children.add(F);
    return OP;
  }

  formula reciprocal(formula F) {
    // returns the reciprocal of formula F
    formula REC = new formula();
    REC.type = 4;
    REC.children.add(F);
    return REC;
  }

}
