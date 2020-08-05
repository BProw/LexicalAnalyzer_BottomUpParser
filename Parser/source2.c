int main() {
  int a[10], sum, i;
  sum = 0;
  i = 0;
  while (i < 10) {
    a[i] = i;
    sum = sum + a[i];
    i = i + 1;
  }
}
