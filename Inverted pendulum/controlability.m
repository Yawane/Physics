
s = 1; % pendulum up (s=1)

A = [0 1 0 0;
    0 -d/M -m*g/M 0;
    0 0 0 1;
    0 -s*d/(M*L) -s*(m+M)*g/(M*L) 0];

B = [0; 1/M; 0; s*1/(M*L)];

C = ctrb(A, B)

eigs = [-1.1, -1.2, -1.3, -1.4];

K = place(A, B, eigs)