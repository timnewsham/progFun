
function reflect(rd, n) :
    # r = rd - 2*<rd,n> n
    const f = -2 * dot(rd, n);
    return add(rd, scale(f, n));

