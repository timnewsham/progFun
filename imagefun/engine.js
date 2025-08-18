class Engine {
	constructor(statusSelector, canvasSelector) {
		this.frame = 0;
		this.status = document.querySelector(statusSelector);
    	this.canvas = document.querySelector(canvasSelector);
		//addEventListener("resize", (ev) => this.resizeFull);
		this.resize(this.canvas.width, this.canvas.height);
		this.animate(0);
	}

	resizeFull() {
		this.resize(window.innerWidth, window.innerHeight);
	}

	resize(W, H) {
		this.canvas.width = W;
		this.canvas.height = H;
		this.W = W;
		this.H = H;
		this.ctx = this.canvas.getContext('2d');
		this.imageData = this.ctx.getImageData(0, 0, this.W, this.H);
	}

	draw(ts) {
		this.status.innerText = text(this, ts);

		const WS = 1.0 / (this.W - 1);
		const HS = 1.0 / (this.H - 1);
		const pixelData = this.imageData.data;
		var off = 0;
    	for(var y = 0; y < this.H; y++) {
        	for(var x = 0; x < this.W; x++) {
            	const col = color(x * WS, y * HS, ts);
				pixelData[off++] = colorscale(col.i);
				pixelData[off++] = colorscale(col.j);
				pixelData[off++] = colorscale(col.k);
				pixelData[off++] = 255;
			}
		}
		this.ctx.putImageData(this.imageData, 0, 0);
	}

	animate(ts) {
		this.frame ++;
		this.draw(ts);
		requestAnimationFrame((ts) => this.animate(ts / 1000.0));
	}
}

function avg() {
	var sum = 0;
	for (const arg of arguments) {
		sum += arg;
	}
	return sum / arguments.length;
}

function avgV() {
	var sum = new Vec3(0, 0, 0);
	for (const arg of arguments) {
		sum = sum.add(arg);
	}
	return sum.scale(1.0 / arguments.length);
}

// clamp clamps the value x to the range [lo..hi].
function clamp(x, lo, hi) {
	return Math.max(lo, Math.min(hi, x));
}

// clampUnit clamps the value x to the range [0..1].
function clampUnit(x) {
	return clamp(x, 0.0, 1.0);
}

function colorscale(x) {
	return Math.floor(255 * clampUnit(x));
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

function sin1(x) {
	return Math.sin(2 * Math.PI * x);
}

function cos1(x) {
	return Math.sin(2 * Math.PI * x);
}

class Vec3 {
	constructor(i,j,k) {
		this.i = i;
		this.j = j;
		this.k = k;
	}

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

	// mul computes the pointwise product of this vector and x.
	mul(x) {
		return new Vec3(this.i * x.i, this.j*x.j, this.k*x.k);
	}

	// cross computes the cross product of this vector and x.
	cross(x) {
		return new Vec3(
			this.j * x.k - this.k * x.j,
			this.k * x.i - this.i * x.k,
			this.i * x.j - this.j * x.i,
		);
	}
}

const black = new Vec3(0, 0, 0);
const white = new Vec3(1, 1, 1);
const red = new Vec3(1, 0, 0);
const green = new Vec3(0, 1, 0);
const blue = new Vec3(0, 0, 1);
