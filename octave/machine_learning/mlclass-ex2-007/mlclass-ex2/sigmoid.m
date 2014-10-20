function g = sigmoid(z)
%SIGMOID Compute sigmoid function
%   J = SIGMOID(z) computes the sigmoid of z.

% You need to return the following variables correctly 
g = zeros(size(z))

% ====================== YOUR CODE HERE ======================
% Instructions: Compute the sigmoid of each value of z (z can be a matrix,
%               vector or scalar).

if size(z, 1) > 1
%	fprintf('\nz has several rows\n');

	for i = 1:size(z, 1),
		if size(z, 2) > 1
			for j = 1:size(z, 2),
				g(i, j) = 1 / (1 + e ^ -z(i, j));
			end
		else
			g(i) = 1 / (1 + e ^ -z(i));
		end
	end
	
elseif size(z, 2) > 1
%	fprintf('\nz has 1 row but multiple columns\n');
	for j = 1:size(z, 2),
		g(j) = 1 / (1 + e ^ -z(j));
	end

else
%	fprintf('\nz is a scalar\n');
	g = 1 / (1 + e^-z)
end

% =============================================================

end
