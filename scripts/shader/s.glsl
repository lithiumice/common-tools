for(float i, z, d; i ++ < 1e2; o += vec4(z / 7., 2, 3, 1) / d) {
    vec3 p = z * normalize(FC.rgb * 2. - r.xyy);
    p.z -= 5. * t;
    p.xy *= mat2(cos(z * .1 + t * .1 + vec4(0, 33, 11, 0)));
    for(d = 1.;
    d < 9.;
    d /= .7) p += cos(p.yzx * d + t) / d;
    z += d = .02 + abs(2. - dot(cos(p), sin(p.yzx * .6))) / 8.;
}
o = tanh(o * o / 1e7);