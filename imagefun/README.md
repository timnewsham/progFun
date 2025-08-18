# imageFun

This is fun with image generation in JS. It has a simple engine that calls
the `color` function to compute each pixel color. It also has a `text` function
for generating status text on the image.  The idea is to build fun images with
math functions.  Time units are in seconds. X and Y coordinates are over the range
from zero to one.

## Example

See [example.html](example.html) for a simple example.

```javascript
// text returns text to display at time t for engine e.
function text(e, t) {
    var txt = `time: ${t.toFixed(2)} sec`;
    txt += `\nframe: ${e.frame}`;
    if(t > 0) {
        const rate = e.frame / t;
        txt += `\nrate: ${rate.toFixed(2)} frames/sec`;
    }
    return txt;
}

// color returns a color for each pixel position x,y in range 0..1, and time t in seconds.
function color(x, y, t) {
	if(x == 0 || y == 0 || x == 1 || y == 1) {
		return black;
	}

    const xx = x - 0.5;
    const yy = y - 0.5;
    const d = Math.sqrt(xx*xx + yy*yy);

    const rad = 0.1 + 0.1 * (sin1(t / 3.0) + 1.0);
    if (d < rad) {
        return lerpV(y, red, blue);
    }
    return avgV(lerpV(x, blue, red), lerpV(y, black, white));
}
```

## Load

You can use `load('tim.js')` from the JS console to load in replacement functions dynamically.
