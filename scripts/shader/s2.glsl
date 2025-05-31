for(float i, z, d, iter; i ++ < 1e2; o += vec4(z / 7., 1, 2, 3) / d) {
    vec2 p = FC.xy / r.xy * 2. - 1.;
    p.x *= r.x / r.y;
    
    // Add time-based zoom and rotation effects
    float zoom = 1.5 + sin(t * 0.1) * 0.5;
    p = p * zoom;
    
    // Apply rotation using time
    float angle = t * 0.05;
    mat2 rotation = mat2(cos(angle), -sin(angle), sin(angle), cos(angle));
    p = rotation * p;
    
    // Slowly moving center point
    p -= vec2(sin(t * 0.07) * 0.2, cos(t * 0.05) * 0.1);
    
    vec2 c = p;
    z = 0.;
    vec2 zp = vec2(0.);
    
    for(iter = 0.; iter < 50.; iter++) {
        zp = vec2(zp.x * zp.x - zp.y * zp.y, 2. * zp.x * zp.y) + c;
        if(dot(zp, zp) > 4.) break;
    }
    
    // Animate color using time variable
    z += d = .02 + (iter / 50.) * (8. + sin(t * 0.3) * 2.);
    d = mix(0.05, 0.5, iter / 50.) + sin(t * 0.2) * 0.1;
}
o = tanh(o * o / 1e7);