A = [
  1 2 3 4 5;
  2 3 2 5 3;
  5 5 5 3 2;
];

[r, c] = size(A);

A = A - repmat(sum(A, 2) / c, 1, c)
A = A - repmat(sum(A) / r, r, 1)
