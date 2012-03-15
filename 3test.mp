\Avec == \vec{A}
\Bvec == \vec{B}
\def == \equiv
\=> == \Rightarrow
\<= == \Leftarrow
\int == \int
\arctan == tan^{-1}

        parse.py test
      Anton Bovin
    1.1
Avec def xhat + 2 yhat, Bvec def xhat + s yhat
 Need  Bvec  orthogonal to  Avec =>  need  Avec dot Bvec = 0.
Avec dot Bvec = 1 + 2s = 0 => s = -1/2

    1.2
  a.
xddot(t) = At/m
  b.
xdot(t) = int At/m dt = At^2/2m + xdot_0 = At^2/2m
  c.
x(t) = int At^2/2m dt = At^3/6m + x_0 = At^3/6m
  d.
x(t_0) = At_0^3/6m = 1
x(2t_0) = 8At_0^3/6m = 8
 The mass will move 8 in. in time  2t_0.
  e.
x(t_0, m) = At_0^3/6m = 1
x(t_0, 2m) = 1/2 At_0^3/6m = 1/2
 The mass will move half the distance in time  t_0  if the mass is doubled.

    1.3
  a.
F_phi = mR phiddot = mg sin phi - mu N = mg sin phi - mu (mg cos phi - F_r)
mR phiddot = mg sin phi - mu (mg cos phi - m phidot^2 R)
  b.
   phi_c  is an angle such that  phiddot = 0  , i.e.  mg (sin phi_c - mu cos phi_c) = 0.
=> phi_c = arctan mu