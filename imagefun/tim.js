// text returns text to display at time t for engine e.
function text(e, t) {
	return "Chess Board";
}

function int(x) {
	return Math.floor(x);
}

// step(x, 10) will round down x to 10 steps between 0 and 1.
// examples:
//   `step(0.20, 10)` returns `0.20`.
//   `step(0.28, 10)` returns `0.20`.
//   `step(0.38, 10)` returns `0.30`.
function step(x, n) {
	return int(x * n) / n;
}

// even(x) returns true if x (as an integer) is even.
function even(x) {
	// remainder of dividing by two is zero.
	return int(x) % 2 == 0;
}

// color returns a color for each pixel position x,y in range 0..1, and time t in seconds.
function color(x, y, t) {
	const n = int(x * 8) + int(y * 8);
	if(even(n)) {
		const tt = 0.5 * (sin1(t/3.0) + 1.0); // from 0 to 1, repeating every 3 seconds.
		col1 = lerpV(tt, green, red);
		col2 = lerpV(tt, red, green);
		return lerpV((x+y)/2, col1, col2);
	}
	return black;
}
