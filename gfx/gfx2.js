
abs = Math.abs;
sqrt = Math.sqrt;
min = Math.min;
max = Math.max;
round = Math.round;
sin = Math.sin;
cos = Math.cos;
PI = Math.PI;

/// make a vector
function vec(x,y,z,w) {
  return new Float32Array([x,y,z,w]);
}

/// scale vector xs by scalar f.
function scale(f, xs) {
  return new Float32Array([f*xs[0],
                           f*xs[1],
                           f*xs[2],
                           f*xs[3]]);
}

/// normalize xs by scaling it to have unit length.
function norm(xs) {
  return scale(1.0 / len(xs), xs);
}

/// sum of all elements in a vector or array
function sum(xs) {
  return xs[0] + xs[1] + xs[2] + xs[3];
}

/// apply f to pairise elements of two equal length vectors
function zipWith(f, xs, ys) {
  return new Float32Array([ f(xs[0], ys[0]),
                          f(xs[1], ys[1]),
                          f(xs[2], ys[2]),
                          f(xs[3], ys[3]) ]);
}

/// add two vectors
function add(xs, ys) {
  return new Float32Array([ xs[0] + ys[0],
                            xs[1] + ys[1],
                            xs[2] + ys[2],
                            xs[3] + ys[3] ]);
}

/// subtract two vectors
function sub(xs, ys) {
  return new Float32Array([ xs[0] - ys[0],
                            xs[1] - ys[1],
                            xs[2] - ys[2],
                            xs[3] - ys[3] ]);
}

/// dot product of two equal length vectors
function dot(xs, ys) {
  return (xs[0]*ys[0]) +
         (xs[1]*ys[1]) +
         (xs[2]*ys[2]) +
         (xs[3]*ys[3]);
}

/// length squared of a vector
function len2(xs) {
  return dot(xs, xs);
}

function len(xs) {
  return sqrt(len2(xs));
}

// sdf for sphere
function sdfSphere(p, c, r) {
  const pc = sub(p, c);
  const l = len(pc);
  const t = l - r;
  //const n = scale(1/l, pc);
  return t;
}

// sdf for box
function sdfBox(p, c, r, t) {
  // translate box to origin, and map point to first quadrant
  const p2 = sub(p, c);

  // rotate box with time
  const ang = 2*PI * t / 31;
  const p3 = vec(p2[0],
             p2[1] * cos(ang) - p2[2] * sin(ang),
             p2[1] * sin(ang) + p2[2] * cos(ang),
             0);

  const p4 = p3.map(x => abs(x));

  const d = sub(p4, r);
  const clipped = d.map(x => max(x, 0));
  const dist = len(clipped);
  return dist;
}

// return the smallest sdf result
function sdfMin(a0, ...args) {
  var best = a0;
  for(const arg of args) {
    if(arg[0] < best[0]) {
      best = arg;
    }
  }
  return best;
}

// evaluate sdf of scene at p.
function map(p, t) {
  return sdfMin(
    [sdfBox(p, vec(0.8, 0.8, -0.5, 0), vec(0.5, 0.3, 0.7, 0), t) - 0.1, vec(1,1,0,1)],
    [sdfSphere(p, vec(1, -1.5, 0, 0), 1), vec(1,0,0,1)],
    [sdfSphere(p, vec(-2.0, 0, 1, 0), 0.5), vec(0,0,1,1)],
    [sdfSphere(p, vec(2.0, 0.2, 1.3, 0), 0.3), vec(1,0,1,1)]
  );
}

const Zscreen = 4; // screen distance from origin
const Zcam = 6; // camera distance from origin
const FAR = 10.0
const TOL = 0.10;
const MAXITER = 30;

function bg(pos) {
  const [x,y,z] = pos;
  var col = add(scale(0.1 * abs(x), vec(1,1,0.5,1)),
                scale(0.2 * abs(y), vec(1,0.5,0.5,1)));
  col[3] = 1;
  return col;
}

/// Numeric calculation of normal using forward differences
function calcNorm(p, t) {
  const e = 0.001;
  const t0 = map(p, t)[0];
  const v = vec(
    map(add(p, vec(e,0,0,0)), t)[0] - t0,
    map(add(p, vec(0,e,0,0)), t)[0] - t0,
    map(add(p, vec(0,0,e,0)), t)[0] - t0,
    0);
  return norm(v);
}

/// Perform lighting given a surface normal
function lighting(n, matcol) {
  const above = (n[1] + 1.0) * 0.5; 
  const left = (n[0] + 1.0) * 0.5;
  const below = 1-above;
  var col = vec(0,0,0,1);
  col = add(col, scale(0.8*above,  matcol));
  col = add(col, scale(0.25*left,  vec(0,0,1,1)));
  col = add(col, scale(0.25*below, vec(1,1,0,1)));
  col = add(col, vec(0.1, 0.1, 0.1, 1));
  col[3] = 1;
  return col;
}

/// Calculate a pixel at untranslated position pos, translated position r0
/// with translated camera cam, at time t.
function pixelFunc(cam, pos, r0, t) {
  // direction from our camera through the pixel on the screen
  const rd = norm(sub(r0, cam));

  // march r0 forward through the scene until we hit something, we
  // get too far away, or we wasted too much time trying...
  for(var i = 0; ; i++) {
    const [dist, col] = map(r0, t);
    if(dist < 0.5*TOL) { // hit!
      const n = calcNorm(r0, t);
      return lighting(n, col);
    }
    if(dist > FAR) { // miss!
      return bg(pos);
    }
    if(i > MAXITER) { // we give up...
      return bg(pos);
      // perhaps blend bg with hit if we're somewhat close 
      return vec(1, 0, 0, 1);
    }

    r0 = add(r0, scale(max(dist, TOL), rd));
  }
}

/// transform camera and screen with time
function rotView(p, t) {
  const ang = 2*PI * t / 20;
  return vec(p[0] * cos(ang) - p[2] * sin(ang),
             p[1],
             p[0] * sin(ang) + p[2] * cos(ang),
             0);
}

/// generate an image on the canvas
function genImage(canvas, t) {
  const ctx = canvas.getContext('2d');
  const bm = ctx.getImageData(0, 0, canvas.width, canvas.height);

  const W = bm.width;
  const H = bm.height;

  // constants to convert from pixel coordinates to image space.
  // The screen is located at z=-1.0, centered, with the minor axis
  // ranging from -1.0 to 1.0 and the major axis extending slightly
  // further.
  const sf = 2.0 / min(W, H);
  const C = vec((W-1)/2.0, (H-1)/2.0, Zscreen / sf, 0);

  const cam = rotView(vec(0, 0, -Zcam, 0), t);

  // iterate over every pixel and compute its color
  var idx = 0;
  for(var y = 0; y < H; y++) {
    for(var x = 0; x < W; x++) {
      var pixelpos = vec(x, y, 0.0, 0);
      var pos = scale(sf, sub(pixelpos, C));
      pos[1] *= -1; // make Y point upwards
      var col = pixelFunc(cam, pos, rotView(pos, t), t);

      // assert: idx == 4 * (x + y * W)
      bm.data[idx++] = round(255.0 * col[0]);
      bm.data[idx++] = round(255.0 * col[1]);
      bm.data[idx++] = round(255.0 * col[2]);
      bm.data[idx++] = round(255.0 * col[3]);
    }
  }

  // push the pixel data onto the canvas
  ctx.putImageData(bm, 0, 0);
}

const DT = 0.5;

function animate(canvas, t) {
  genImage(canvas, t);
  setTimeout(() => animate(canvas, t + DT), 10);
}

function runGfx(name) {
  const canvas = document.getElementById(name);
  animate(canvas, 0);
}
