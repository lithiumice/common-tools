for(float i, z, d, iter; i ++ < 1e2; o += vec4(z / 7., 1, 2, 3) / d) {
    vec2 p = FC.xy / r.xy * 2. - 1.;
    p.x *= r.x / r.y;
    p = p * 2. - vec2(0.5, 0);
    
    vec2 c = p;
    z = 0.;
    vec2 zp = vec2(0.);
    
    for(iter = 0.; iter < 50.; iter++) {
        zp = vec2(zp.x * zp.x - zp.y * zp.y, 2. * zp.x * zp.y) + c;
        if(dot(zp, zp) > 4.) break;
    }
    
    z += d = .02 + (iter / 50.) * 8.;
    d = mix(0.05, 0.5, iter / 50.);
}
o = tanh(o * o / 1e7);