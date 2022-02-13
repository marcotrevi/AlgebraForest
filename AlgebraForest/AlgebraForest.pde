// the AlgebraForest project aims to create a mathematical formula database.
// formulas are n-ary trees with mathematical operators as nodes and constants or variables as leaves.
// allowed operators are the sum (+), the product (*), the opposite (op), the reciprocal (rec).

constants C = new constants();
utilities U = new utilities();

void setup() {
  formula f1 = new formula();
  f1.type = 0;
  f1.value = 1;
  formula f2 = new formula();
  f2.type = 0;
  f2.value = 2;
  formula f3 = new formula();
  f3.type = 0;
  f3.value = 3;
  f3 = U.opposite(f3);
  ArrayList<formula> formulas = new ArrayList<formula>();
  formulas.add(f1);
  formulas.add(f2);
  
  formula sum = U.sum(formulas);
  ArrayList<formula> formulas2 = new ArrayList<formula>();
  formulas2.add(sum);
  formulas2.add(f3);
  
  formula prod = U.product(formulas2);
  
  String s = U.printFormula(prod);
  println(s);
}
