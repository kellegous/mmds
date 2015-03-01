A = [1 0 1 0 1 2; 1 1 0 0 1 6; 0 1 0 1 0 2];

for a = [0 0.5 1 2]
  Ap = [A(1:3, 1:5)*a A(:, 6)];
  D = zeros(3, 3);
  for i = 1:3
    for j = 1:3
      D(i, j) = (Ap(i, :) * Ap(j, :)') / (norm(Ap(i, :)) * norm(Ap(j, :)));
    endfor
  endfor
  D
endfor
