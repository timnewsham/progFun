class Vertex {
	constructor(v, vt, vn) {
		console.assert(v !== undefined && vt !== undefined && vn !== undefined);
		this.v = v;
		this.vt = vt;
		this.vn = vn;
	}
}

class Face {
	constructor() {
		this.vs = [];
	}

	add(v) {
		this.vs.push(v);
	}

	// forEachTriangle decomposes polygons into triangle fans,
	// calling f(a,b,c) for each triangle a,b,c.
	forEachTriangle(f) {
		f(this.vs[0], this.vs[1], this.vs[2]);
		for(var n = 3; n < this.vs.length; n++) {
			f(this.vs[0], this.vs[n-1], this.vs[n]);
		}
	}
}

class Model {
	constructor() {
		this.vs = [];
		this.vns = [];
		this.vts = [];
		this.fs = [];
		this.sval = 0;
	}

	// Add a vertex.
	v(x,y,z) {
		this.vs.push(new Vec3(x,y,z));
	}

	// Add a normal.
	vn(x,y,z) {
		this.vns.push(new Vec3(x,y,z));
	}

	// Add a texture coordinate.
	vt(u,v) {
		this.vts.push(new Vec2(u,v));
	}

	// ?
	s(x) {
		this.sval = x;
	}

	// Add a face with a list of 3 or more vertices.
	f() {
		// assert arguments.length >= 3
		var face = new Face();		
		for(const [vidx, vtidx, vnidx] of arguments) {
			const v = this.vs[vidx-1];
			const vt = this.vts[vtidx-1];
			const vn = this.vns[vnidx-1];
			const vert = new Vertex(v, vt, vn);
			vert.index = vidx; // debug
			face.add(vert);
		}
		this.fs.push(face);
	}
}

// cube model from
// https://www.youtube.com/watch?v=yyJ-hdISgnw&t=536s
function cube() {
	var m = new Model();

	// vertices.
	m.v(1, 1, -1);
	m.v(1, -1, -1);
	m.v(1, 1, 1);
	m.v(1, -1, 1);
	m.v(-1, 1, -1);
	m.v(-1, -1, -1);
	m.v(-1, 1, 1);
	m.v(-1, -1, 1);

	// normals
	m.vn(0, 1, 0);
	m.vn(0, 0, 1);
	m.vn(-1, 0, 0);
	m.vn(0, -1, 0);
	m.vn(1, 0, 0);
	m.vn(0, 0, -1);

	// textures.
	m.vt(0.625, 0.5);
	m.vt(0.875, 0.5);
	m.vt(0.875, 0.75);
	m.vt(0.625, 0.75);
	m.vt(0.375, 0.75);
	m.vt(0.625, 1);
	m.vt(0.375, 1);
	m.vt(0.375, 0);
	m.vt(0.625, 0);
	m.vt(0.625, 0.25);
	m.vt(0.375, 0.25);
	m.vt(0.125, 0.5);
	m.vt(0.375, 0.5);
	m.vt(0.125, 0.75);

	m.s(0); //?

	// faces of [virtex position, texture position, normal].
	m.f([1,1,1], [5,2,1], [7,3,1], [3,4,1]);
	m.f([4,5,2], [3,4,2], [7,6,2], [8,7,2]);
	m.f([8,8,3], [7,9,3], [5,10,3], [6,11,3]);
	m.f([6,12,4], [2,13,4], [4,5,4], [8,14,4]);
	m.f([2,13,5], [1,1,5], [3,4,5], [4,5,5]);
	m.f([6,11,6], [5,10,6], [1,1,6], [2,13,6]);

	return m;
}
