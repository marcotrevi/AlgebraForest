class formula {
  // a formula is a n-ary tree.
  // nodes are mathematical operators; leaves are scalars or variables.

  int id = -1;
  int type = -1;
  int value = -1;
  int lastNode = 0;
  
  ArrayList<formula> children = new ArrayList<formula>();

  formula() {
  }

  int getLength() {
    int l = 0;
    return l;
  }

  int getDepth() {
    int d = 0;
    return d;
  }

}
