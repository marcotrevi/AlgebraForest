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
  String printFormula(formula F) {
    String s = "";
    switch(F.type) {
    case 0:
      // constant
      s = str(F.value);
      break;
    case 1:
      // sum (has at least 2 children)
      s = "(" + printFormula(F.children.get(0));
      for (int i=1; i<F.children.size(); i++) {
        if (F.children.get(i).type == 0) {
          s = s + "+" + printFormula(F.children.get(i));
        } else {
          s = s + "+(" + printFormula(F.children.get(i)) + ")";
        }
      }
      s = s + ")";
      break;
    case 2:
      // product (has at least 2 children)
      s = "(" + printFormula(F.children.get(0));
      for (int i=1; i<F.children.size(); i++) {
        if (F.children.get(i).type == 0) {
          s = s + "*" + printFormula(F.children.get(i));
        } else {
          s = s + "*(" + printFormula(F.children.get(i)) + ")";
        }
      }
      s = s + ")";
      break;
    case 3:
      // opposite (has only 1 child)
      if (F.children.get(0).type == 0) {
        s = "-" + printFormula(F.children.get(0));
      } else {
        s = "-(" + printFormula(F.children.get(0)) + ")";
      }
      break;
    case 4:
      // reciprocal (has only 1 child)
      if (F.children.get(0).type == 0) {
        s = "1/" + printFormula(F.children.get(0));
      } else {
        s = "1/(" + printFormula(F.children.get(0)) + ")";
      }
      break;
    }
    return s;
  }
}
