
abs = Math.abs;
sqrt = Math.sqrt;
min = Math.min;
max = Math.max;
round = Math.round;
sin = Math.sin;
cos = Math.cos;
PI = Math.PI;

/// make a vector
function vec(x,y,z) {
  return new Float32Array([x,y,z]);
}

/// scale vector xs by scalar f.
function scale(f, xs) {
  return new Float32Array([f*xs[0],
                           f*xs[1],
                           f*xs[2] ]);
}

/// normalize xs by scaling it to have unit length.
function norm(xs) {
  return scale(1.0 / len(xs), xs);
}

/// sum of all elements in a vector or array
function sum(xs) {
  return xs[0] + xs[1] + xs[2];
}

/// apply f to pairise elements of two equal length vectors
function zipWith(f, xs, ys) {
  return new Float32Array([ f(xs[0], ys[0]),
                          f(xs[1], ys[1]),
                          f(xs[2], ys[2]) ]);
}

/// add two vectors
function add(xs, ys) {
  return new Float32Array([ xs[0] + ys[0],
                            xs[1] + ys[1],
                            xs[2] + ys[2] ]);
}

/// subtract two vectors
function sub(xs, ys) {
  return new Float32Array([ xs[0] - ys[0],
                            xs[1] - ys[1],
                            xs[2] - ys[2] ]);
}

/// dot product of two equal length vectors
function dot(xs, ys) {
  return (xs[0]*ys[0]) +
         (xs[1]*ys[1]) +
         (xs[2]*ys[2]);
}

/// length squared of a vector
function len2(xs) {
  return dot(xs, xs);
}

function len(xs) {
  return sqrt(len2(xs));
}

