function avg() {
	var sum = 0;
	for (const arg of arguments) {
		sum += arg;
	}
	return sum / arguments.length;
}

// clamp clamps the value x to the range [lo..hi].
function clamp(x, lo, hi) {
	return Math.max(lo, Math.min(hi, x));
}

// clampUnit clamps the value x to the range [0..1].
function clampUnit(x) {
	return clamp(x, 0.0, 1.0);
}

// rgba returns a color string from RGBA components.
function rgba(r, g, b, a) {
	const R = Math.floor(255 * clampUnit(r));
	const G = Math.floor(255 * clampUnit(g));
	const B = Math.floor(255 * clampUnit(b));
	const A = Math.floor(100 * clampUnit(a));
	return `rgb(${R} ${G} ${B} / ${A}%)`;
}

// rgb returns a color string from RGB components.
function rgb(r, g, b) {
	return rgba(r, g, b, 1.0);
}

// hsla returns a color string from HSLA components.
function hsla(h, s, l, a) {
	const H = Math.floor(360 * clampUnit(h));
	const S = Math.floor(100 * clampUnit(s));
	const L = Math.floor(100 * clampUnit(l));
	const A = Math.floor(100 * clampUnit(a));
	return `hsl(${H} ${S}% ${L}% / ${A}%)`;
}

// hsl returns a color string from HSL components.
function hsl(h, s, l) {
	return hsla(h, s, l, 1.0);
}

// lerp returns linear interpolation of t between numbers a and b.
function lerp(t, a, b) {
	return (b-a) * t + a;
}

// lerpV returns linear interpolation of t between vecs a and b.
// This is generic over any type that supports add() and scale().
function lerpV(t, a, b) {
	const dBA = b.add(a.scale(-1));
	return dBA.scale(t).add(a);
}

// randrange returns a random value in the range [min..max].
function randrange(min, max) {
	return lerp(Math.random(), min, max);
}

// randrangei returns a random integer value in the range [min..max].
function randrangei(min, max) {
	return Math.floor(randrange(min, max));
}

// Vec holds generic vector methods.
class Vec {
	// implement:
	// add(x)
	// scale(s)
	// mag2()
	// dot(x)

	// clone makes a copy of a vector.
	clone() {
		return this.scale(1);
	}

	// sub subtracts x from this vector to form a new vector.
	sub(x) {
		return this.add(x.scale(-1));
	}

	// mag returns the magnitude of this vector.
	mag() {
		return Math.sqrt(this.mag2());
	}

	// norm returns this vector scaled to unit length.
	norm() {
		return this.scale(1.0 / this.mag());
	}
}

// Vec2 is a 2-dimensional vector.
class Vec2 extends Vec {
	constructor(i,j) {
		super();
		this.i = i;
		this.j = j;
	}

	// add adds this vector with x to form a new vector.
	add(x) {
		return new Vec2(this.i + x.i, this.j + x.j);
	}

	// scale scales the vector by s to form a new vector.
	scale(s) {
		return new Vec2(s*this.i, s*this.j);
	}

	// mag2 returns the square magnitude of this vector.
	mag2() {
		return this.i*this.i + this.j*this.j;
	}

	// dot computes the dot product of this vector and x.
	dot(x) {
		return this.i*x.i + this.j*x.j;
	}

	// cross computes the cross product of this vector and x.
	cross(x) {
		return this.i * x.j - x.i * this.j;
	}

	// perp returns a vector perpendicular to this one.
	perp() {
		return new Vec2(-this.j, this.i);
	}
}

// Vec3 is a 3-dimensional vector.
// Convention: i points right, j points up, k points in to the screen.
class Vec3 extends Vec {
	constructor(i,j,k) {
		super();
		this.i = i;
		this.j = j;
		this.k = k;
	}

	// add adds this vector with x to form a new vector.
	add(x) {
		return new Vec3(this.i + x.i, this.j + x.j, this.k + x.k);
	}

	// scale scales the vector by s to form a new vector.
	scale(s) {
		return new Vec3(s*this.i, s*this.j, s*this.k);
	}

	// mag2 returns the square magnitude of this vector.
	mag2() {
		return this.i*this.i + this.j*this.j + this.k*this.k;
	}

	// dot computes the dot product of this vector and x.
	dot(x) {
		return this.i*x.i + this.j*x.j + this.k*x.k;
	}

	// cross computes the cross product of this vector and x.
	cross(x) {
		return new Vec3(
			this.j * x.k - this.k * x.j,
			this.k * x.i - this.i * x.k,
			this.i * x.j - this.j * x.i,
		);
	}

	rgb() {
		return rgb(this.i, this.j, this.k);
	}

	hsl() {
		return hsl(this.i, this.j, this.k);
	}

	// vec4 turns a Vec3 into a Vec4 in homogenous coordinates.
	vec4() {
		return new Vec4(this.i, this.j, this.k, 1.0);
	}

	vec2() {
		return new Vec2(this.i, this.j);
	}
}

// Vec4 is a 4-dimensional vector.
class Vec4 extends Vec {
	constructor(i,j,k,w) {
		super();
		this.i = i;
		this.j = j;
		this.k = k;
		this.w = w
	}

	// add adds this vector with x to form a new vector.
	add(x) {
		return new Vec4(this.i + x.i, this.j + x.j, this.k + x.k, this.w + x.w);
	}

	// scale scales the vector by s to form a new vector.
	scale(s) {
		return new Vec4(s*this.i, s*this.j, s*this.k, s*this.w);
	}

	// mag2 returns the square magnitude of this vector.
	mag2() {
		return this.i*this.i + this.j*this.j + this.k*this.k + this.w*this.w;
	}

	// dot computes the dot product of this vector and x.
	dot(x) {
		return this.i*x.i + this.j*x.j + this.k*x.k + this.w*x.w;
	}

	rgba() {
		return rgba(this.i, this.j, this.k, this.w);
	}

	hsla() {
		return hsla(this.i, this.j, this.k, this.w);
	}

	vec2() {
		return new Vec2(this.i, this.j);
	}

	vec3() {
		return new Vec3(this.i, this.j, this.k);
	}

	// hvec3 returns a vec3 when w is normalized to 1.0.
	hvec3() {
		const f = 1.0 / this.w;
		return new Vec3(f * this.i, f * this.j, f * this.k);
	}

	// hvec4 returns a vec4 when w is normalized to 1.0.
	hvec4() {
		const f = 1.0 / this.w;

		// hack: don't normalize the depth value, we want to use it later.
		//return this.scale(f);
		return new Vec4(f * this.i, f * this.j, this.k, 1.0);
	}
}

class Mat2 {
	constructor(a00,a01, a10,a11) {
		this.row0 = new Vec2(a00, a01);
		this.row1 = new Vec2(a10, a11);
	}

	// id returns the identity matrix.
	static id() {
		return Mat2.scale(1.0);
	}

	// scale returns a matrix that scales in all dimensions by s.
	static scale(s) {
		return Mat2.scales(new Vec2(s, s));
	}

	// scales returns a matrix that scales each dimension separately.
	static scales(v) {
		return new Mat2(
			v.i, 0.0,
			0.0, v.j,
		);
	}

	// rot returns a matrix that rotates by theta.
	// identity matrix when theta == 0.
	static roll(theta) {
		const cos = Math.cos(theta);
		const sin = Math.sin(theta);
		return new Mat2(
			cos,  sin,
			-sin, cos,
		);
	}

	// tranpose turns rows into columns.
	transpose(m) {
		return new Mat2(
			this.row0.i, this.row1.i,
			this.row0.j, this.row1.j,
		);
	}

	// mulvec multiplies this matrix with a vector
	// by taking the dot product of each row with the vector.
	mulvec(v) {
		// calculate M x v.
		return new Vec2(
			this.row0.dot(v),
			this.row1.dot(v),
		);
	}

	// mul multiplies two vectors together by multiplying
	// this matrix with each column of x to form the new
	// columns of the resulting vector.
	mul(x) {
		const tx = x.transpose(); // tx.row0 = x.col0.
		const col0 = this.mulvec(tx.row0); // this . x.row0
		const col1 = this.mulvec(tx.row1); // this . x.row1
		return new Mat2(
			col0.i, col1.i,
			col0.j, col1.j,
		);
	}
}

class Mat3 {
	constructor(a00,a01,a02, a10,a11,a12, a20,a21,a22) {
		this.row0 = new Vec3(a00, a01, a02);
		this.row1 = new Vec3(a10, a11, a12);
		this.row2 = new Vec3(a20, a21, a22);
	}

	// id returns the identity matrix.
	static id() {
		return Math3.scale(1.0);
	}

	// scale returns a matrix that scales in all dimensions by s.
	static scale(s) {
		return Mat3.scales(new Vec3(s, s, s));
	}

	// scales returns a matrix that scales each dimension separately.
	static scales(v) {
		return new Mat3(
			v.i, 0.0, 0.0,
			0.0, v.j, 0.0,
			0.0, 0.0, v.k,
		);
	}

	// roll returns a matrix that rotates around the k-axis by theta.
	// identity matrix when theta == 0.
	static roll(theta) {
		const cos = Math.cos(theta);
		const sin = Math.sin(theta);
		return new Mat3(
			cos, -sin, 0.0,
			sin, cos,  0.0,
			0.0, 0.0,  1.0,
		);
	}

	// pitch returns a matrix that rotates around the i-axis by theta.
	// identity matrix when theta == 0.
	static pitch(theta) {
		const cos = Math.cos(theta);
		const sin = Math.sin(theta);
		return new Mat3(
			1.0, 0.0, 0.0,
			0.0, cos, -sin,
			0.0, sin, cos,
		);
	}

	// yaw returns a matrix that rotates around the j-axis by theta.
	// identity matrix when theta == 0.
	static yaw(theta) {
		const cos = Math.cos(theta);
		const sin = Math.sin(theta);
		return new Mat3(
			cos,  0.0, sin,
			0.0,  1.0, 0.0,
			-sin, 0.0, cos,
		);
	}

	// tranpose turns rows into columns.
	transpose(m) {
		return new Mat3(
			this.row0.i, this.row1.i, this.row2.i,
			this.row0.j, this.row1.j, this.row2.j,
			this.row0.k, this.row1.k, this.row2.k
		);
	}

	// mulvec multiplies this matrix with a vector
	// by taking the dot product of each row with the vector.
	mulvec(v) {
		// calculate M x v.
		return new Vec3(
			this.row0.dot(v),
			this.row1.dot(v),
			this.row2.dot(v)
		);
	}

	// mul multiplies two vectors together by multiplying
	// this matrix with each column of x to form the new
	// columns of the resulting vector.
	mul(x) {
		const tx = x.transpose(); // tx.row0 = x.col0.
		const col0 = this.mulvec(tx.row0); // this . x.row0
		const col1 = this.mulvec(tx.row1); // this . x.row1
		const col2 = this.mulvec(tx.row2); // this . x.row2
		return new Mat3(
			col0.i, col1.i, col2.i,
			col0.j, col1.j, col2.j,
			col0.k, col1.k, col2.k
		);
	}
}

class Mat4 {
	constructor(a00,a01,a02,a03, a10,a11,a12,a13, a20,a21,a22,a23, a30,a31,a32,a33) {
		this.row0 = new Vec4(a00, a01, a02, a03);
		this.row1 = new Vec4(a10, a11, a12, a13);
		this.row2 = new Vec4(a20, a21, a22, a23);
		this.row3 = new Vec4(a30, a31, a32, a33);
	}

	// id returns the identity matrix.
	static id() {
		return Mat4.scale(1.0);
	}

	// scale returns a matrix that scales in all dimensions by s.
	static scale(s) {
		return Mat4.scales(new Vec4(s, s, s, s));
	}

	// scales returns a matrix that scales each dimension separately.
	static scales(v) {
		return new Mat4(
			v.i, 0.0, 0.0, 0.0,
			0.0, v.j, 0.0, 0.0,
			0.0, 0.0, v.k, 0.0,
			0.0, 0.0, 0.0, 1.0,
		);
	}

	// persp returns a matrix which scales w by the k component,
	// so that when converted with hvec3(), coordinates are scaled for perspective.
	static persp(v) {
		return new Mat4(
			1.0, 0.0, 0.0, 0.0,
			0.0, 1.0, 0.0, 0.0,
			0.0, 0.0, 1.0, 0.0,
			0.0, 0.0, 1.0, 0.0,
		);
	}

	// roll returns a matrix that rotates around the k-axis by theta.
	// identity matrix when theta == 0.
	static roll(theta) {
		const cos = Math.cos(theta);
		const sin = Math.sin(theta);
		return new Mat4(
			cos, -sin, 0.0, 0.0,
			sin, cos,  0.0, 0.0,
			0.0, 0.0,  1.0, 0.0,
			0.0, 0.0,  0.0, 1.0,
		);
	}

	// pitch returns a matrix that rotates around the i-axis by theta.
	// identity matrix when theta == 0.
	static pitch(theta) {
		const cos = Math.cos(theta);
		const sin = Math.sin(theta);
		return new Mat4(
			1.0, 0.0, 0.0,  0.0,
			0.0, cos, -sin, 0.0,
			0.0, sin, cos,  0.0,
			0.0, 0.0,  0.0, 1.0,
		);
	}

	// yaw returns a matrix that rotates around the j-axis by theta.
	// identity matrix when theta == 0.
	static yaw(theta) {
		const cos = Math.cos(theta);
		const sin = Math.sin(theta);
		return new Mat4(
			cos,  0.0, sin, 0.0,
			0.0,  1.0, 0.0, 0.0,
			-sin, 0.0, cos, 0.0,
			0.0 , 0.0, 0.0, 1.0,
		);
	}

	// translate returns a matrix that translates by v: Vec3.
	static translate(v) {
		return new Mat4(
			1.0, 0.0, 0.0, v.i,
			0.0, 1.0, 0.0, v.j,
			0.0, 0.0, 1.0, v.k,
			0.0, 0.0, 0.0, 1.0,
		);
	}

	// tranpose turns rows into columns.
	transpose(m) {
		return new Mat4(
			this.row0.i, this.row1.i, this.row2.i, this.row3.i,
			this.row0.j, this.row1.j, this.row2.j, this.row3.j,
			this.row0.k, this.row1.k, this.row2.k, this.row3.k,
			this.row0.w, this.row1.w, this.row2.w, this.row3.w,
		);
	}

	// mulvec multiplies this matrix with a vector
	// by taking the dot product of each row with the vector.
	mulvec(v) {
		// calculate M x v.
		return new Vec4(
			this.row0.dot(v),
			this.row1.dot(v),
			this.row2.dot(v),
			this.row3.dot(v),
		);
	}

	// mul multiplies two vectors together by multiplying
	// this matrix with each column of x to form the new
	// columns of the resulting vector.
	mul(x) {
		const tx = x.transpose(); // tx.row0 = x.col0.
		const col0 = this.mulvec(tx.row0); // this . x.row0
		const col1 = this.mulvec(tx.row1); // this . x.row1
		const col2 = this.mulvec(tx.row2); // this . x.row2
		const col3 = this.mulvec(tx.row3); // this . x.row3
		return new Mat4(
			col0.i, col1.i, col2.i, col3.i,
			col0.j, col1.j, col2.j, col3.j,
			col0.k, col1.k, col2.k, col3.k,
			col0.w, col1.w, col2.w, col3.w,
		);
	}
}

// transforms composes the argument matrices,
// pre-multiplying each transform to the previous ones.
function transforms() {
	const args = Array.from(arguments);
	var t = args.shift();
	for (const arg of args) {
		t = arg.mul(t);
	}
	return t;
}

// deg converts an angle in degrees to radians.
function deg(theta) {
	return theta * Math.PI / 180.0;
}
