// Subtle CRT look for Ghostty: phosphor bloom + faint scanlines.
// Static effect, so it needs no custom-shader-animation and costs nothing at idle.
// Ghostty passes the rendered terminal as iChannel0 (Shadertoy conventions).

const float BLOOM_SPREAD    = 2.5;  // px between bloom samples; larger = wider glow
const float BLOOM_STRENGTH  = 0.55; // 0 = no glow
const float BLOOM_THRESHOLD = 0.20; // pixels darker than this don't glow (keeps the background flat)
const float SCAN_PERIOD     = 3.0;  // px per scanline (framebuffer px, so 1.5pt on Retina)
const float SCAN_DEPTH      = 0.07; // 0 = no scanlines

float luma(vec3 c) {
    return dot(c, vec3(0.2126, 0.7152, 0.0722));
}

void mainImage(out vec4 fragColor, in vec2 fragCoord) {
    vec2 uv = fragCoord / iResolution.xy;
    vec2 px = 1.0 / iResolution.xy;
    vec4 base = texture(iChannel0, uv);

    // Bloom: Gaussian-weighted 5x5 sample of only the bright pixels around us.
    vec3 glow = vec3(0.0);
    float weights = 0.0;
    for (int x = -2; x <= 2; x++) {
        for (int y = -2; y <= 2; y++) {
            vec2 o = vec2(float(x), float(y));
            float w = exp(-dot(o, o) / 4.0);
            vec3 s = texture(iChannel0, uv + o * BLOOM_SPREAD * px).rgb;
            glow += s * smoothstep(BLOOM_THRESHOLD, 1.0, luma(s)) * w;
            weights += w;
        }
    }
    vec3 color = base.rgb + BLOOM_STRENGTH * glow / weights;

    // Scanlines: gentle sine darkening, never below 1 - SCAN_DEPTH.
    float scan = 0.5 + 0.5 * sin(fragCoord.y * 6.2831853 / SCAN_PERIOD);
    color *= 1.0 - SCAN_DEPTH * scan;

    fragColor = vec4(min(color, vec3(1.0)), base.a);
}
