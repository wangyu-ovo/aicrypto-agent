\paragraph{Problem 1 (18 points)}
Recall the RSA assumption: Let $p,q$ be two random primes and $N=pq$, let $e$ be a random value in $\mathbb{Z}_{\phi(N)}^*$. The RSA assumption says $f_{e, N}: \mathbb{Z}_N^* \to \mathbb{Z}_N^*$, $f_{e, N}(x) = x^e\bmod N $ is a one-way function.

Now consider a new function 
$g_{e, N}: \mathbb{Z}_N^* \to \mathbb{Z}_N^* \times \mathbb{Z}_N^*$,  $g_{e, N}(x) = x^e\bmod N, x^{2e} \bmod N$ (meaning that $g_{e, N}$, on input $x$, outputs two numbers: $x^e\bmod N$ and $x^{2e} \bmod N$). Show that $g_{e, N}$ is a one-way function based on the RSA assumption. 