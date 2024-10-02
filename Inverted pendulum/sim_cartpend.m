M = 5;
m = 1;
L = 2;
g = -9.81;
d = 1;

tspan = 0:.1:20;
y0 = [0, 0, pi, 0];

[t, y] = ode45(@(t,y)cartpend(y,M,m,L,g,d, -K*(y-[3; 0; pi; 0])), tspan, y0);


for k=1:length(t)
    draw_cartpend(y(k,:), M, m, L);
end

%% Energie

Ec_cart = .5 * M * y(:,2).^2;
Ec_pend = .5 * m * (y(:,2) + L*y(:,4).*cos(y(:,3)).^2 + (L*y(:,4).*sin(y(:,3))).^2);
Ep = m * g * (L * cos(y(:,3)));

plot(t, Ec_cart, 'LineWidth', 1); hold on;
plot(t, Ec_pend, 'LineWidth', 1);
plot(t, Ec_cart + Ec_pend, 'LineWidth', 2);
plot(t, Ep, 'LineWidth', 2);
plot(t, Ep+Ec_pend+Ec_cart, 'LineWidth', 3);

legend("Ec_cart", "Ec_pend", "Ec", "Ep", "Em");
hold off;
% for k=1:len(t)