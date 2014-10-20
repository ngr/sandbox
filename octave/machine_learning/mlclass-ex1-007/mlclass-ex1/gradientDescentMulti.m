function [theta, J_history] = gradientDescentMulti(X, y, theta, alpha, num_iters)
%GRADIENTDESCENTMULTI Performs gradient descent to learn theta
%   theta = GRADIENTDESCENTMULTI(x, y, theta, alpha, num_iters) updates theta by
%   taking num_iters gradient steps with learning rate alpha

% Initialize some useful values
m = length(y); % number of training examples
J_history = zeros(num_iters, 1);

X

for iter = 1:num_iters

    % ====================== YOUR CODE HERE ======================
    % Instructions: Perform a single gradient step on the parameter vector
    %               theta. 
    %
    % Hint: While debugging, it can be useful to print out the values
    %       of the cost function (computeCostMulti) and gradient here.
    %

%	h_of_X = theta(1) + theta(2) * X(:,2);
	%theta(1) = theta(1) - alpha * (1 / m) * sum((h_of_X - y)(:));
	%theta(2) = theta(2) - alpha * (1 / m) * sum(((h_of_X - y) .* X(:,2))(:));	

%	h_of_X = zeros(m,1);

	%h_of_X = theta(1) + theta(2) * X(:,2) + theta(3) * X(:,3);
	h_of_X = X * theta - y;
	theta = theta - alpha / m * ( h_of_X' * X)';
%	h_of_X = theta' .* X;
%	for j = 1:3
%		h_of_X = h_of_X + theta(j) * X(:,j);
%	end
%	h_of_X;
%	h_of_X = theta' .* X;
%	theta = theta - alpha .* (1 / m) * sum(((h_of_X - y) .* X)(:));
%	theta(1) = theta(1) - alpha * (1 / m) * sum((h_of_X - y)(:));
%	theta(2) = theta(2) - alpha * (1 / m) * sum(((h_of_X - y) .* X(:,2))(:));	
%	theta(3) = theta(3) - alpha * (1 / m) * sum(((h_of_X - y) .* X(:,3))(:));	

	computeCost(X, y, theta);


    % ============================================================

    % Save the cost J in every iteration    
    J_history(iter) = computeCostMulti(X, y, theta);

end

end
