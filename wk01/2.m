M = [0 .5 .5; 0 0 1; 1 0 0 ];
M = M';
A = ones(3,3)/3;
B = 0.85;
R = ones(3,1) / 3;
for i = 1:100
  R = B*M*R + (1-B)*A*R;
endfor

a = R(1);
b = R(2);
c = R(3);

# c = .9b + .475a
printf('%0.2f = %0.2f\n', c, 0.9*b + 0.475*a);
# b = .475a + .05c
printf('%0.2f = %0.2f\n', b, 0.475*a + 0.05*c);
# .85a = c + .15b
printf('%0.2f = %0.2f\n', 0.85*a, c + 0.15*b);
# .95c = .9b + .475a
printf('%0.2f = %0.2f\n', 0.95*c, 0.9*b + 0.475*a);



R = ones(3, 1);
for i = 1:5
  R = M*R;
endfor

R

for i = 1:1000
  R = M*R;
endfor

R

