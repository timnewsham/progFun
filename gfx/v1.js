abs = Math.abs;
sqrt = Math.sqrt;
min = Math.min;
max = Math.max;
round = Math.round;
sin = Math.sin;
cos = Math.cos;
PI = Math.PI;

/// make a vector
function vec() {
  return [].slice.call(arguments);
}

/// scale vector xs by scalar f.
function scale(f, xs) {
  return xs.map(x => f * x);
}

/// normalize xs by scaling it to have unit length.
function norm(xs) {
  return scale(1.0 / len(xs), xs);
}

/// sum of all elements in a vector or array
function sum(xs) {
  return xs.reduce((acc,s) => acc+s);
}

/// apply f to pairise elements of two equal length vectors
function zipWith(f, xs, ys) {
  return xs.map((x, idx) => f(x, ys[idx]));
}

/// add two vectors
function add(xs, ys) {
  return zipWith((x,y) => x + y, xs, ys);
}

/// subtract two vectors
function sub(xs, ys) {
  return zipWith((x,y) => x - y, xs, ys);
}

/// dot product of two equal length vectors
function dot(xs, ys) {
  return sum(zipWith((x,y) => x * y, xs, ys));
}

/// length squared of a vector
function len2(xs) {
  return sum(xs.map(x => x*x));
}

function len(xs) {
  return sqrt(len2(xs));
}
