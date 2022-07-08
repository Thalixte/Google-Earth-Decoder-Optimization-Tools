
    'use strict';
    var nb = this || self;
    function tb(n, r) {
        n = n.split(".");
        var p = nb;
        n[0]in p || "undefined" == typeof p.execScript || p.execScript("var " + n[0]);
        for (var G; n.length && (G = n.shift()); )
            n.length || void 0 === r ? p[G] && p[G] !== Object.prototype[G] ? p = p[G] : p = p[G] = {} : p[G] = r
    }
    var ub = Date.now;
    function Fb(n) {
        this.length = n.length || n;
        for (var r = 0; r < this.length; r++)
            this[r] = n[r] || 0
    }
    Fb.prototype.a = 4;
    Fb.prototype.set = function(n, r) {
        r = r || 0;
        for (var p = 0; p < n.length && r + p < this.length; p++)
            this[r + p] = n[p]
    }
    ;
    Fb.prototype.toString = Array.prototype.join;
    "undefined" == typeof Float32Array && (Fb.BYTES_PER_ELEMENT = 4,
    Fb.prototype.BYTES_PER_ELEMENT = Fb.prototype.a,
    Fb.prototype.set = Fb.prototype.set,
    Fb.prototype.toString = Fb.prototype.toString,
    tb("Float32Array", Fb));
    function Kb(n) {
        this.length = n.length || n;
        for (var r = 0; r < this.length; r++)
            this[r] = n[r] || 0
    }
    Kb.prototype.a = 8;
    Kb.prototype.set = function(n, r) {
        r = r || 0;
        for (var p = 0; p < n.length && r + p < this.length; p++)
            this[r + p] = n[p]
    }
    ;
    Kb.prototype.toString = Array.prototype.join;
    if ("undefined" == typeof Float64Array) {
        try {
            Kb.BYTES_PER_ELEMENT = 8
        } catch (n) {}
        Kb.prototype.BYTES_PER_ELEMENT = Kb.prototype.a;
        Kb.prototype.set = Kb.prototype.set;
        Kb.prototype.toString = Kb.prototype.toString;
        tb("Float64Array", Kb)
    };
    function Lb() {
        this.matrixMeshFromGlobe = this.matrixGlobeFromMesh = null;
        this.meshes = [];
        this.overlaySurfaceMeshes = [];
        this.copyrightIds = this.waterMesh = null;
        this.nonEmptyOctants = 0;
        this.bvhTriPermutation = this.bvhNodes = null
    }
    function bc() {
        this.vertexAlphas = this.indices = this.uvOffsetAndScale = this.layerBounds = this.texture = this.vertices = null;
        this.numNonDegenerateTriangles = 0;
        this.meshId = -1;
        this.octantCounts = this.normals = null
    }
    function pc() {
        this.bytes = null;
        this.textureFormat = 1;
        this.viewDirection = this.height = this.width = 0;
        this.meshId = -1
    }
    function qc() {
        this.headNodePath = "";
        this.obbRotations = this.obbExtents = this.obbCenters = this.metersPerTexel = this.flags = this.bulkMetadataEpoch = this.epoch = this.childIndices = null;
        this.defaultImageryEpoch = 0;
        this.imageryEpochArray = null;
        this.defaultTextureFormat = 0;
        this.textureFormatArray = null;
        this.defaultAvailableViewDirections = 0;
        this.childBulkMetadata = this.nodes = this.viewDependentTextureFormatArray = this.availableViewDirectionsArray = null
    }
    function Lc() {
        this.textures = [];
        this.transformInfo = [];
        this.projectionOrigin = null
    }
    function Zc() {
        this.vertexTransformMap = this.transformTable = null;
        this.meshId = -1;
        this.uvOffsetAndScale = null
    }
    ;function $c(n) {
        this.D = new DataView(n.buffer);
        this.c = n;
        this.a = 0;
        this.g = n.length;
        this.l = [];
        this.s = this.v = 0
    }
    function ad(n) {
        if (n.a < n.g) {
            var r = n.m();
            n.v = r & 7;
            n.s = r >> 3;
            return n.s
        }
        return 0
    }
    function ld(n, r) {
        n.l.push(n.g);
        n.g = r
    }
    function md(n) {
        n.l.length && (n.g = n.l.pop())
    }
    $c.prototype.m = function() {
        var n = 0
          , r = 1;
        do {
            var p = this.c[this.a++];
            n += (127 & p) * r;
            r *= 128
        } while (p & 128);return n
    }
    ;
    function nd(n) {
        switch (n.v) {
        case 0:
            do
                var r = n.c[n.a++];
            while (r & 128);break;
        case 1:
            n.a += 8;
            break;
        case 2:
            n.a = n.m() + n.a;
            break;
        case 5:
            n.a += 4
        }
    }
    function od(n) {
        var r = n.D.getFloat32(n.a, !0);
        n.a += 4;
        return r
    }
    function pd(n) {
        var r = n.D.getFloat64(n.a, !0);
        n.a += 8;
        return r
    }
    function Id(n) {
        var r = n.c[n.a++];
        n = n.c[n.a++] << 8 | r;
        return n & 32768 ? n | 4294901760 : n
    }
    function Jd(n) {
        var r = n.c[n.a++];
        return n.c[n.a++] << 8 | r
    }
    $c.prototype.data = function() {
        return this.c
    }
    ;
    function Kd(n, r) {
        n.a += r
    }
    $c.prototype.b = $c.prototype.m;
    function Ld(n, r) {
        this.g = new $c(n);
        this.da = r;
        this.c = null;
        this.b = new Float64Array(3);
        this.a = new Float32Array(4);
        this.m = {};
        this.l = this.s = 0;
        this.W = this.v = this.U = this.D = !1
    }
    function Md(n) {
        var r = n.g, p, G = [], x = n.c = new qc;
        n.a[0] = Infinity;
        n.a[1] = Infinity;
        n.a[2] = Infinity;
        n.a[3] = Infinity;
        x.defaultTextureFormat = 6;
        for (var E; p = ad(r); )
            switch (p) {
            case 1:
                E = r.b();
                ld(r, r.a + E);
                G.push(Nd(n));
                md(r);
                break;
            case 2:
                E = r.b();
                ld(r, r.a + E);
                var w;
                E = n;
                p = E.g;
                for (var I = E.c; w = ad(p); )
                    switch (w) {
                    case 1:
                        w = p;
                        var L = w.c[w.a++];
                        L = w.a + L;
                        for (var K = ""; w.a < L; ) {
                            var H = w.c[w.a++];
                            if (128 > H)
                                K += String.fromCharCode(H);
                            else if (!(192 > H))
                                if (224 > H) {
                                    var J = w.c[w.a++];
                                    K += String.fromCharCode((H & 31) << 6 | J & 63)
                                } else if (240 > H) {
                                    J = w.c[w.a++];
                                    var O = w.c[w.a++];
                                    K += String.fromCharCode((H & 15) << 12 | (J & 63) << 6 | O & 63)
                                }
                        }
                        I.headNodePath = K;
                        break;
                    case 2:
                        E.l = p.b();
                        break;
                    default:
                        nd(p)
                    }
                md(r);
                break;
            case 3:
                r.b();
                n.b[0] = pd(r);
                n.b[1] = pd(r);
                n.b[2] = pd(r);
                break;
            case 4:
                r.b();
                n.a[0] = od(r);
                n.a[1] = od(r);
                n.a[2] = od(r);
                n.a[3] = od(r);
                break;
            case 5:
                x.defaultImageryEpoch = r.b();
                break;
            case 6:
                x.defaultTextureFormat = Od(r.b());
                break;
            case 7:
                x.defaultAvailableViewDirections = r.b();
                break;
            case 8:
                x.defaultViewDependentTextureFormat = Od(r.b());
                break;
            default:
                nd(r)
            }
        r.v = 0;
        r.s = 0;
        r.a = 0;
        r.g = r.c.length;
        r.l = [];
        E = G.slice();
        E.sort(Pd);
        for (p = 0; p < G.length; p++)
            n.m[E[p]] = p;
        E = G.length;
        x.epoch = new Uint32Array(E);
        x.bulkMetadataEpoch = new Uint32Array(E);
        x.flags = new Uint8Array(E);
        x.metersPerTexel = new Float32Array(E);
        x.obbCenters = new Float64Array(3 * E);
        x.obbExtents = new Float32Array(3 * E);
        x.obbRotations = new Float32Array(9 * E);
        x.imageryEpochArray = new Uint32Array(E);
        x.textureFormatArray = new Uint8Array(E);
        x.viewDependentTextureFormatArray = new Uint8Array(E);
        x.availableViewDirectionsArray = new Uint8Array(E);
        for (E = 0; p = ad(r); )
            switch (p) {
            case 1:
                p = r.b();
                ld(r, r.a + p);
                K = n;
                var T = G[E++]
                  , M = K.g;
                p = K.c;
                var Z;
                J = 0;
                I = [];
                w = [];
                H = [];
                O = 0;
                var U = K.l
                  , ca = K.l;
                L = K.m[T];
                p.imageryEpochArray[L] = p.defaultImageryEpoch;
                p.textureFormatArray[L] = p.defaultTextureFormat;
                for (p.availableViewDirectionsArray[L] = p.defaultAvailableViewDirections; Z = ad(M); )
                    switch (Z) {
                    case 1:
                        J = M.b();
                        break;
                    case 3:
                        M.b();
                        I[0] = Id(M);
                        I[1] = Id(M);
                        I[2] = Id(M);
                        w[0] = M.c[M.a++];
                        w[1] = M.c[M.a++];
                        w[2] = M.c[M.a++];
                        H[0] = Jd(M);
                        H[1] = Jd(M);
                        H[2] = Jd(M);
                        break;
                    case 4:
                        O = od(M);
                        break;
                    case 2:
                        U = M.b();
                        break;
                    case 5:
                        ca = M.b();
                        break;
                    case 7:
                        K.D = !0;
                        p.imageryEpochArray[L] = M.b();
                        break;
                    case 8:
                        K.U = !0;
                        p.textureFormatArray[L] = Od(M.b());
                        break;
                    case 9:
                        K.v = !0;
                        p.availableViewDirectionsArray[L] = M.b();
                        break;
                    case 10:
                        K.W = !0;
                        p.viewDependentTextureFormatArray[L] = Od(M.b());
                        break;
                    default:
                        nd(M)
                    }
                T = T.length;
                4 > T && K.s++;
                p.epoch[L] = U;
                p.bulkMetadataEpoch[L] = ca;
                p.flags[L] = J >> 2 + 3 * T;
                0 == O && (O = K.a[T - 1]);
                p.metersPerTexel[L] = O;
                I[0] = I[0] * O + K.b[0];
                I[1] = I[1] * O + K.b[1];
                I[2] = I[2] * O + K.b[2];
                w[0] *= O;
                w[1] *= O;
                w[2] *= O;
                H[0] = H[0] * Math.PI / 32768;
                H[1] = H[1] * Math.PI / 65536;
                H[2] = H[2] * Math.PI / 32768;
                J = K = new Float32Array(9);
                U = H[0];
                T = H[1];
                O = H[2];
                H = Math.cos(U);
                U = Math.sin(U);
                ca = Math.cos(T);
                T = Math.sin(T);
                M = Math.cos(O);
                O = Math.sin(O);
                J[0] = H * M - ca * U * O;
                J[1] = ca * H * O + M * U;
                J[2] = O * T;
                J[3] = -H * O - M * ca * U;
                J[4] = H * ca * M - U * O;
                J[5] = M * T;
                J[6] = T * U;
                J[7] = -H * T;
                J[8] = ca;
                J = H = K;
                J == H ? (O = H[1],
                U = H[2],
                ca = H[5],
                J[1] = H[3],
                J[2] = H[6],
                J[3] = O,
                J[5] = H[7],
                J[6] = U,
                J[7] = ca) : (J[0] = H[0],
                J[1] = H[3],
                J[2] = H[6],
                J[3] = H[1],
                J[4] = H[4],
                J[5] = H[7],
                J[6] = H[2],
                J[7] = H[5],
                J[8] = H[8]);
                p.obbCenters.set(I, 3 * L);
                p.obbRotations.set(K, 9 * L);
                p.obbExtents.set(w, 3 * L);
                md(r);
                break;
            default:
                nd(r)
            }
        n.c.childIndices = new Int16Array(8 * (n.s + 1));
        Qd(n, "", -1);
        r = [x.childIndices.buffer, x.epoch.buffer, x.bulkMetadataEpoch.buffer, x.flags.buffer, x.metersPerTexel.buffer, x.obbCenters.buffer, x.obbExtents.buffer, x.obbRotations.buffer];
        n.D ? r.push(x.imageryEpochArray.buffer) : x.imageryEpochArray = null;
        n.U ? r.push(x.textureFormatArray.buffer) : x.textureFormatArray = null;
        n.v ? r.push(x.availableViewDirectionsArray.buffer) : x.availableViewDirectionsArray = null;
        n.W ? r.push(x.viewDependentTextureFormatArray.buffer) : x.viewDependentTextureFormatArray = null;
        
        return n;
    }
    function Pd(n, r) {
        var p = n.length - r.length;
        return 0 != p ? p : n < r ? -1 : 1
    }
    function Nd(n) {
        n = n.g;
        for (var r, p = ""; r = ad(n); )
            switch (r) {
            case 1:
                p = n.b();
                r = (p & 3) + 1;
                p = p >> 2 & (1 << 3 * r) - 1;
                for (var G = "", x = 0; x < r; x++)
                    G += p >> 3 * x & 7;
                p = G;
                break;
            default:
                nd(n)
            }
        return p
    }
    function Qd(n, r, p) {
        if (4 != r.length)
            for (var G = 0; 8 > G; G++) {
                var x = r + G
                  , E = n.m[x];
                void 0 !== E ? Qd(n, x, E) : E = -1;
                n.c.childIndices[8 * (p + 1) + G] = E
            }
    }
    function Od(n) {
        for (var r = 0; r < Rd.length; r++) {
            var p = Rd[r];
            if (n & 1 << p - 1)
                return 0 == p && n.toString(16),
                p
        }
        n.toString(16);
        return Rd[0]
    }
    var Rd = [6, 1];
    function Sd(n, r) {
        return 0 == r ? n + 1 & -2 : 1 == r ? n | 1 : n + 2
    }
    ;function Oe(n) {
        this.da = n;
        this.l = null;
        this.m = 0;
        this.b = this.g = this.v = this.D = this.c = this.s = null;
        this.a = 0
    }
    Oe.prototype.start = function() {
        for (var n = this.da, r = 0, p = 0; p < n.length; ++p)
            r += n[p].numNonDegenerateTriangles;
        if (0 >= r)
            return null;
        this.D = new Uint32Array(r);
        this.c = new Uint32Array(r);
        this.v = new Uint8Array(6 * r);
        this.g = Array(3);
        this.g[0] = new Uint8Array(r);
        this.g[1] = new Uint8Array(r);
        this.g[2] = new Uint8Array(r);
        for (var G = this.v, x = this.g, E, w, I, L, K, H, J = 0, O = p = 0, T = 0, M = 0, Z = 0, U = 0, ca = 0, Da = 0; Da < n.length; ++Da) {
            var Aa = n[Da]
              , Ua = Aa.indices;
            Aa = Aa.vertices;
            for (var ta = Ua.length - 2, Va = 0; Va < ta; ++Va) {
                w = Ua[Sd(Va, 0)];
                var ja = Ua[Sd(Va, 1)]
                  , Oa = Ua[Sd(Va, 2)];
                if (w != ja && ja != Oa && Oa != w) {
                    this.D[ca] = Da << 24 | Va;
                    this.c[ca] = ca;
                    I = 8 * w;
                    E = L = Aa[I++];
                    w = K = Aa[I++];
                    I = H = Aa[I];
                    var Qa = 8 * ja;
                    ja = Aa[Qa++];
                    ja < E ? E = ja : ja > L && (L = ja);
                    ja = Aa[Qa++];
                    ja < w ? w = ja : ja > K && (K = ja);
                    ja = Aa[Qa];
                    ja < I ? I = ja : ja > H && (H = ja);
                    Oa *= 8;
                    ja = Aa[Oa++];
                    ja < E ? E = ja : ja > L && (L = ja);
                    ja = Aa[Oa++];
                    ja < w ? w = ja : ja > K && (K = ja);
                    ja = Aa[Oa];
                    ja < I ? I = ja : ja > H && (H = ja);
                    G[J++] = E;
                    G[J++] = w;
                    G[J++] = I;
                    G[J++] = L;
                    G[J++] = K;
                    G[J++] = H;
                    E = E + L >> 1;
                    w = w + K >> 1;
                    I = I + H >> 1;
                    x[0][ca] = E;
                    x[1][ca] = w;
                    x[2][ca] = I;
                    0 < ca ? (E < p ? p = E : E > M && (M = E),
                    w < O ? O = w : w > Z && (Z = w),
                    I < T ? T = I : I > U && (U = I)) : (p = M = E,
                    O = Z = w,
                    T = U = I);
                    ++ca
                }
            }
        }
        this.l = n = new Uint8Array(24 * r);
        this.s = new Uint32Array(n.buffer);
        n[0] = p;
        n[1] = O;
        n[2] = T;
        n[3] = M;
        n[4] = Z;
        n[5] = U;
        this.b = new Uint32Array(3 * r);
        this.a = 0;
        this.b[this.a++] = 0;
        this.b[this.a++] = 0;
        this.b[this.a++] = r;
        this.m = 1;
        return this.U
    }
    ;
    Oe.prototype.U = function() {
        for (var n = this.b, r = 0; 0 < this.a; ) {
            var p = n[--this.a]
              , G = n[--this.a]
              , x = n[--this.a]
              , E = p - G;
            if (0 == r || 1E4 > r + E) {
                a: {
                    var w = p - G;
                    if (4 >= w)
                        Pe(this, x, G, p);
                    else {
                        var I = this.l
                          , L = 12 * x;
                        var K = I[L + 3] - I[L + 0];
                        var H = I[L + 4] - I[L + 1]
                          , J = I[L + 5] - I[L + 2];
                        if (K > H && K > J)
                            var O = 0;
                        else
                            H > J ? (O = 1,
                            K = H) : (O = 2,
                            K = J);
                        I = I[L + O] + (K >> 1);
                        L = G;
                        K = p;
                        H = this.g[O];
                        for (J = this.c; ; ) {
                            for (; L < K && !(H[J[L]] >= I); )
                                L++;
                            for (; L < K && !(H[J[K - 1]] < I); )
                                K--;
                            if (L == K) {
                                I = K;
                                break
                            }
                            var T = J[L];
                            J[L] = J[K - 1];
                            J[K - 1] = T
                        }
                        if (I == G || I == p) {
                            if (255 > w) {
                                Pe(this, x, G, p);
                                break a
                            }
                            I = (G + p) / 2
                        }
                        w = this.m++;
                        L = this.m++;
                        K = w;
                        J = O;
                        O = I;
                        H = this.l;
                        x *= 12;
                        H[x + 6] = 0;
                        H[x + 7] = J;
                        this.s[x + 8 >> 2] = K;
                        x = this.g[0];
                        J = this.g[1];
                        T = this.g[2];
                        for (var M = 0; 2 > M; M++) {
                            var Z = 0 == M ? G : O
                              , U = 0 == M ? O : p;
                            if (!(4 >= U - Z)) {
                                var ca = this.c[Z]
                                  , Da = x[ca]
                                  , Aa = J[ca];
                                ca = T[ca];
                                var Ua = Da
                                  , ta = Da
                                  , Va = Aa
                                  , ja = Aa
                                  , Oa = ca
                                  , Qa = ca;
                                for (Z += 1; Z < U; Z++)
                                    ca = this.c[Z],
                                    Da = x[ca],
                                    Aa = J[ca],
                                    ca = T[ca],
                                    Da < Ua ? Ua = Da : Da > ta && (ta = Da),
                                    Aa < Va ? Va = Aa : Aa > ja && (ja = Aa),
                                    ca < Oa ? Oa = ca : ca > Qa && (Qa = ca);
                                U = 12 * (0 == M ? K : K + 1);
                                H[U++] = Ua;
                                H[U++] = Va;
                                H[U++] = Oa;
                                H[U++] = ta;
                                H[U++] = ja;
                                H[U] = Qa
                            }
                        }
                        this.b[this.a++] = L;
                        this.b[this.a++] = I;
                        this.b[this.a++] = p;
                        this.b[this.a++] = w;
                        this.b[this.a++] = G;
                        this.b[this.a++] = I
                    }
                }
                r += E
            } else {
                this.a += 3;
                break
            }
        }
        return 0 == this.a ? this.W : this.U
    }
    ;
    function Pe(n, r, p, G) {
        var x = n.v, E = n.c, w, I, L, K;
        var H = w = I = 255;
        var J = L = K = 0;
        for (var O = p; O < G; ++O) {
            var T = 6 * E[O]
              , M = x[T++];
            H = H < M ? H : M;
            M = x[T++];
            w = w < M ? w : M;
            M = x[T++];
            I = I < M ? I : M;
            M = x[T++];
            J = J > M ? J : M;
            M = x[T++];
            L = L > M ? L : M;
            M = x[T++];
            K = K > M ? K : M
        }
        x = n.l;
        r *= 12;
        E = r + 0;
        x[E++] = H;
        x[E++] = w;
        x[E++] = I;
        x[E++] = J;
        x[E++] = L;
        x[E] = K;
        x[r + 6] = 1;
        x[r + 7] = G - p;
        n.s[r + 8 >> 2] = p
    }
    Oe.prototype.W = function() {
        for (var n = this.l, r = this.s, p = this.m - 1; 0 <= p; p--) {
            var G = 12 * p;
            if (0 == n[G + 6]) {
                var x = G + 0;
                G = 12 * r[G + 8 >> 2];
                for (var E = G + 12, w = 0; 3 > w; w++,
                x++,
                G++,
                E++) {
                    var I = n[G]
                      , L = n[E];
                    n[x] = I <= L ? I : L;
                    I = n[3 + G];
                    L = n[3 + E];
                    n[3 + x] = I >= L ? I : L
                }
            }
        }
        for (r = 0; r < this.c.length; ++r)
            this.c[r] = this.D[this.c[r]];
        this.l = n.subarray(0, 12 * this.m);
        return null
    }
    ;
    var Qe = null;
    function Re() {
        this.b()
    }
    Re.prototype.b = function() {
        function n() {
            return Ra.a
        }
        function r(a) {
            eval.call(null, a)
        }
        function p(a) {
            N.print(a + ":\n" + Error().stack);
            throw "Assertion: " + a;
        }
        function G(a, c) {
            a || p("Assertion failed: " + c)
        }
        function x(a, c, d, e) {
            var g = 0;
            try {
                var h = eval("_" + a)
            } catch (t) {
                try {
                    h = cf.Module["_" + a]
                } catch (q) {}
            }
            G(h, "Cannot call unknown function " + a + " (perhaps LLVM optimizations or closure removed it?)");
            var l = 0;
            a = e ? e.map(function(t) {
                var q = d[l++];
                "string" == q ? (g || (g = Ea.jb()),
                q = Ea.Aa(t.length + 1),
                T(t, q),
                t = q) : "array" == q && (g || (g = Ea.jb()),
                q = Ea.Aa(t.length),
                M(t, q),
                t = q);
                return t
            }) : [];
            c = function(t, q) {
                if ("string" == q)
                    return I(t);
                G("array" != q);
                return t
            }(h.apply(null, a), c);
            g && Ea.sc(g);
            return c
        }
        function E(a, c, d) {
            d = d || "i8";
            "*" === d[d.length - 1] && (d = "i32");
            switch (d) {
            case "i1":
                ba[a] = c;
                break;
            case "i8":
                ba[a] = c;
                break;
            case "i16":
                vb[a >> 1] = c;
                break;
            case "i32":
                b[a >> 2] = c;
                break;
            case "i64":
                b[a >> 2] = c;
                break;
            case "float":
                bd[a >> 2] = c;
                break;
            case "double":
                qd[0] = c;
                b[a >> 2] = yc[0];
                b[a + 4 >> 2] = yc[1];
                break;
            default:
                p("invalid type for setValue: " + d)
            }
        }
        function w(a, c, d) {
            if ("number" === typeof a) {
                var e = !0;
                var g = a
            } else
                e = !1,
                g = a.length;
            var h = "string" === typeof c ? c : null;
            d = [zc, Ea.Aa, Ea.kb][void 0 === d ? 2 : d](Math.max(g, h ? 1 : c.length));
            if (e)
                return Mb(d, 0, g),
                d;
            e = 0;
            for (var l; e < g; ) {
                var t = a[e];
                "function" === typeof t && (t = Ea.me(t));
                l = h || c[e];
                0 === l ? e++ : ("i64" == l && (l = "i32"),
                E(d + e, t, l),
                e += Ea.wa(l))
            }
            return d
        }
        function I(a, c) {
            for (var d = "undefined" == typeof c, e = "", g = 0, h, l = String.fromCharCode(0); ; ) {
                h = String.fromCharCode(Q[a + g]);
                if (d && h == l)
                    break;
                e += h;
                g += 1;
                if (!d && g == c)
                    break
            }
            return e
        }
        function L(a) {
            for (; 0 < a.length; ) {
                var c = a.shift()
                  , d = c.va;
                "number" === typeof d && (d = Nb[d]);
                d(void 0 === c.Qb ? null : c.Qb)
            }
        }
        function K(a, c) {
            return Array.prototype.slice.call(ba.subarray(a, a + c))
        }
        function H(a) {
            for (var c = 0; ba[a + c]; )
                c++;
            return c
        }
        function J(a, c) {
            var d = H(a);
            c && d++;
            a = K(a, d);
            c && (a[d - 1] = 0);
            return a
        }
        function O(a, c, d) {
            var e = []
              , g = 0;
            void 0 === d && (d = a.length);
            for (; g < d; ) {
                var h = a.charCodeAt(g);
                255 < h && (h &= 255);
                e.push(h);
                g += 1
            }
            c || e.push(0);
            return e
        }
        function T(a, c, d) {
            for (var e = 0; e < a.length; ) {
                var g = a.charCodeAt(e);
                255 < g && (g &= 255);
                ba[c + e] = g;
                e += 1
            }
            d || (ba[c + e] = 0)
        }
        function M(a, c) {
            for (var d = 0; d < a.length; d++)
                ba[c + d] = a[d]
        }
        function Z(a, c) {
            return 0 <= a ? a : 32 >= c ? 2 * Math.abs(1 << c - 1) + a : Math.pow(2, c) + a
        }
        function U(a, c) {
            if (0 >= a)
                return a;
            var d = 32 >= c ? Math.abs(1 << c - 1) : Math.pow(2, c - 1);
            a >= d && (32 >= c || a > d) && (a = -2 * d + a);
            return a
        }
        function ca(a) {
            return 0 == (a | 0) ? 0 : 0 == (a - 1 & a | 0)
        }
        function Da(a) {
            a = a - 1 | 0;
            a |= a >>> 16;
            a |= a >>> 8;
            a |= a >>> 4;
            a |= a >>> 2;
            return (a >>> 1 | a) + 1 | 0
        }
        function Aa(a, c) {
            return a >>> 0 < c >>> 0 ? a : c
        }
        function Ua(a, c) {
            return a >>> 0 > c >>> 0 ? a : c
        }
        function ta(a, c, d) {
            var e = V;
            V += 512;
            var g = e | 0;
            df(g, F.uc | 0, (Mc = V,
            V += 12,
            b[Mc >> 2] = c,
            b[Mc + 4 >> 2] = d,
            b[Mc + 8 >> 2] = a,
            Mc));
            ef(g);
            V = e
        }
        function Va(a, c, d, e, g) {
            var h = V;
            V += 4;
            var l = a + 4 | 0;
            var t = (a + 8 | 0) >> 2;
            y[l >> 2] >>> 0 > y[t] >>> 0 && ta(F.mb | 0, F.a | 0, 2181);
            Math.floor(2147418112 / (e >>> 0)) >>> 0 <= c >>> 0 && ta(F.Eb | 0, F.a | 0, 2182);
            var q = y[t]
              , D = q >>> 0 < c >>> 0;
            do {
                if (D) {
                    var A = d ? ca(c) ? c : Da(c) : c;
                    0 != (A | 0) & A >>> 0 > q >>> 0 || ta(F.Jb | 0, F.a | 0, 2191);
                    var f = A * e | 0;
                    if (0 == (g | 0)) {
                        var k = a | 0;
                        var m = ja(b[k >> 2], f, h, 1);
                        if (0 == (m | 0)) {
                            A = 0;
                            break
                        }
                        b[k >> 2] = m
                    } else {
                        m = Oa(f, h);
                        if (0 == (m | 0)) {
                            A = 0;
                            break
                        }
                        k = (a | 0) >> 2;
                        Nb[g](m, b[k], b[l >> 2]);
                        var u = b[k];
                        0 != (u | 0) && Qa(u);
                        b[k] = m
                    }
                    k = y[h >> 2];
                    b[t] = k >>> 0 > f >>> 0 ? Math.floor((k >>> 0) / (e >>> 0)) : A
                }
                A = 1
            } while (0);V = h;
            return A
        }
        function ja(a, c, d, e) {
            var g = V;
            V += 4;
            0 == (a & 7 | 0) ? 2147418112 < c >>> 0 ? (Nc(F.m | 0),
            d = 0) : (b[g >> 2] = c,
            a = Nb[b[rd >> 2]](a, c, g, e, b[sd >> 2]),
            0 != (d | 0) && (b[d >> 2] = b[g >> 2]),
            0 != (a & 7 | 0) && ta(F.s | 0, F.a | 0, 2654),
            d = a) : (Nc(F.ob | 0),
            d = 0);
            V = g;
            return d
        }
        function Oa(a, c) {
            var d = V;
            V += 4;
            a = a + 3 & -4;
            a = 0 == (a | 0) ? 4 : a;
            if (2147418112 < a >>> 0)
                Nc(F.m | 0),
                c = 0;
            else {
                b[d >> 2] = a;
                var e = Nb[b[rd >> 2]](0, a, d, 1, b[sd >> 2])
                  , g = y[d >> 2];
                0 != (c | 0) && (b[c >> 2] = g);
                0 == (e | 0) | g >>> 0 < a >>> 0 ? (Nc(F.nb | 0),
                c = 0) : (0 != (e & 7 | 0) && ta(F.s | 0, F.a | 0, 2629),
                c = e)
            }
            V = d;
            return c
        }
        function Qa(a) {
            if (0 != (a | 0))
                if (0 == (a & 7 | 0))
                    Nb[b[rd >> 2]](a, 0, 0, 1, b[sd >> 2]);
                else
                    Nc(F.pb | 0)
        }
        function cc(a, c, d, e) {
            var g = a >> 2
              , h = V;
            V += 200;
            var l = h >> 2;
            var t = h + 64;
            var q = t >> 2;
            var D = h + 132
              , A = 0 == (c | 0) | 11 < e >>> 0;
            a: do
                if (A)
                    var f = 0;
                else {
                    b[g] = c;
                    rc(t);
                    for (var k = 0; ; ) {
                        var m = Q[d + k | 0];
                        if (0 != m << 24 >> 24) {
                            var u = ((m & 255) << 2) + t | 0;
                            b[u >> 2] = b[u >> 2] + 1 | 0
                        }
                        var z = k + 1 | 0;
                        if ((z | 0) == (c | 0)) {
                            var B = 1
                              , C = -1
                              , S = 0
                              , W = 0
                              , ea = 0;
                            break
                        }
                        k = z
                    }
                    for (; ; ) {
                        var X = y[(B << 2 >> 2) + q];
                        if (0 == (X | 0)) {
                            b[((B - 1 << 2) + 28 >> 2) + g] = 0;
                            var P = ea
                              , Y = W
                              , R = S
                              , ma = C
                        } else {
                            var Fa = Aa(C, B)
                              , za = Ua(S, B)
                              , ra = B - 1 | 0;
                            b[(ra << 2 >> 2) + l] = ea;
                            var Sa = X + ea | 0
                              , Ka = 16 - B | 0;
                            b[((ra << 2) + 28 >> 2) + g] = (Sa - 1 << Ka | (1 << Ka) - 1) + 1 | 0;
                            b[((ra << 2) + 96 >> 2) + g] = W;
                            b[D + (B << 2) >> 2] = W;
                            P = Sa;
                            Y = X + W | 0;
                            R = za;
                            ma = Fa
                        }
                        var Ga = B + 1 | 0;
                        if (17 == (Ga | 0))
                            break;
                        B = Ga;
                        C = ma;
                        S = R;
                        W = Y;
                        ea = P << 1
                    }
                    b[g + 1] = Y;
                    var Ba = (a + 172 | 0) >> 2;
                    if (Y >>> 0 > y[Ba] >>> 0) {
                        if (ca(Y))
                            var La = Y;
                        else {
                            var ua = Da(Y);
                            La = Aa(c, ua)
                        }
                        b[Ba] = La;
                        var va = a + 176 | 0
                          , Na = b[va >> 2];
                        if (0 == (Na | 0))
                            var wa = La;
                        else
                            Ob(Na),
                            wa = b[Ba];
                        var oa = dc(wa);
                        b[va >> 2] = oa;
                        if (0 == (oa | 0)) {
                            f = 0;
                            break
                        }
                        var ka = va
                    } else
                        ka = a + 176 | 0;
                    var pa = a + 24 | 0;
                    ba[pa] = ma & 255;
                    ba[a + 25 | 0] = R & 255;
                    for (var ia = 0; ; ) {
                        var qa = Q[d + ia | 0]
                          , xa = qa & 255;
                        if (0 != qa << 24 >> 24) {
                            0 == (b[(xa << 2 >> 2) + q] | 0) && ta(F.Kb | 0, F.a | 0, 2334);
                            var aa = (xa << 2) + D | 0
                              , fa = y[aa >> 2];
                            b[aa >> 2] = fa + 1 | 0;
                            fa >>> 0 >= Y >>> 0 && ta(F.Lb | 0, F.a | 0, 2338);
                            vb[b[ka >> 2] + (fa << 1) >> 1] = ia & 65535
                        }
                        var sa = ia + 1 | 0;
                        if ((sa | 0) == (c | 0))
                            break;
                        ia = sa
                    }
                    var la = Q[pa]
                      , Ca = (la & 255) >>> 0 < e >>> 0 ? e : 0
                      , Ha = a + 8 | 0;
                    b[Ha >> 2] = Ca;
                    var Ia = 0 != (Ca | 0);
                    if (Ia) {
                        var Ya = 1 << Ca
                          , bb = a + 164 | 0;
                        if (Ya >>> 0 > y[bb >> 2] >>> 0) {
                            b[bb >> 2] = Ya;
                            var Ja = a + 168 | 0
                              , wb = b[Ja >> 2];
                            0 != (wb | 0) && Pb(wb);
                            var hb = Ta(Ya);
                            b[Ja >> 2] = hb;
                            if (0 == (hb | 0)) {
                                f = 0;
                                break a
                            }
                            Mb(hb, -1, Ya << 2, 1);
                            if (0 == (Ca | 0))
                                var ob = 26;
                            else
                                Qb = Ja,
                                ob = 34
                        } else {
                            var Ac = a + 168 | 0;
                            Mb(b[Ac >> 2], -1, Ya << 2, 1);
                            var Qb = Ac;
                            ob = 34
                        }
                        b: do
                            if (34 == ob)
                                for (var Wa = 1; ; ) {
                                    var Pa = 0 == (b[(Wa << 2 >> 2) + q] | 0);
                                    c: do
                                        if (!Pa) {
                                            var Rb = Ca - Wa | 0
                                              , Sb = 1 << Rb
                                              , xb = Wa - 1 | 0
                                              , ib = y[(xb << 2 >> 2) + l]
                                              , Tb = ff(a, Wa);
                                            if (!(ib >>> 0 > Tb >>> 0))
                                                for (var Bc = b[((xb << 2) + 96 >> 2) + g] - ib | 0, sc = Wa << 16, Gb = ib; ; ) {
                                                    var ec = ya[b[ka >> 2] + (Bc + Gb << 1) >> 1] & 65535;
                                                    (Q[d + ec | 0] & 255 | 0) != (Wa | 0) && ta(F.Nb | 0, F.a | 0, 2380);
                                                    for (var cb = Gb << Rb, Za = ec | sc, jb = 0; ; ) {
                                                        var eb = jb + cb | 0;
                                                        eb >>> 0 >= Ya >>> 0 && ta(F.Ob | 0, F.a | 0, 2386);
                                                        var pb = y[Qb >> 2];
                                                        if (-1 == (b[pb + (eb << 2) >> 2] | 0))
                                                            var fc = pb;
                                                        else
                                                            ta(F.Pb | 0, F.a | 0, 2388),
                                                            fc = b[Qb >> 2];
                                                        b[fc + (eb << 2) >> 2] = Za;
                                                        var gc = jb + 1 | 0;
                                                        if (gc >>> 0 >= Sb >>> 0)
                                                            break;
                                                        jb = gc
                                                    }
                                                    var hc = Gb + 1 | 0;
                                                    if (hc >>> 0 > Tb >>> 0)
                                                        break c;
                                                    Gb = hc
                                                }
                                        }
                                    while (0);var Ub = Wa + 1 | 0;
                                    if (Ub >>> 0 > Ca >>> 0)
                                        break b;
                                    Wa = Ub
                                }
                        while (0);var Vb = ba[pa]
                    } else
                        Vb = la;
                    var tc = a + 96 | 0;
                    b[tc >> 2] = b[tc >> 2] - b[l] | 0;
                    var uc = a + 100 | 0;
                    b[uc >> 2] = b[uc >> 2] - b[l + 1] | 0;
                    var ic = a + 104 | 0;
                    b[ic >> 2] = b[ic >> 2] - b[l + 2] | 0;
                    var Wb = a + 108 | 0;
                    b[Wb >> 2] = b[Wb >> 2] - b[l + 3] | 0;
                    var Hb = a + 112 | 0;
                    b[Hb >> 2] = b[Hb >> 2] - b[l + 4] | 0;
                    var db = a + 116 | 0;
                    b[db >> 2] = b[db >> 2] - b[l + 5] | 0;
                    var yb = a + 120 | 0;
                    b[yb >> 2] = b[yb >> 2] - b[l + 6] | 0;
                    var vc = a + 124 | 0;
                    b[vc >> 2] = b[vc >> 2] - b[l + 7] | 0;
                    var jc = a + 128 | 0;
                    b[jc >> 2] = b[jc >> 2] - b[l + 8] | 0;
                    var kc = a + 132 | 0;
                    b[kc >> 2] = b[kc >> 2] - b[l + 9] | 0;
                    var Ib = a + 136 | 0;
                    b[Ib >> 2] = b[Ib >> 2] - b[l + 10] | 0;
                    var lc = a + 140 | 0;
                    b[lc >> 2] = b[lc >> 2] - b[l + 11] | 0;
                    var mc = a + 144 | 0;
                    b[mc >> 2] = b[mc >> 2] - b[l + 12] | 0;
                    var nc = a + 148 | 0;
                    b[nc >> 2] = b[nc >> 2] - b[l + 13] | 0;
                    var zb = a + 152 | 0;
                    b[zb >> 2] = b[zb >> 2] - b[l + 14] | 0;
                    var Xb = a + 156 | 0;
                    b[Xb >> 2] = b[Xb >> 2] - b[l + 15] | 0;
                    var lb = a + 16 | 0;
                    b[lb >> 2] = 0;
                    var Yb = (a + 20 | 0) >> 2;
                    b[Yb] = Vb & 255;
                    b: do
                        if (Ia) {
                            for (var fb = Ca; ; ) {
                                if (0 == (fb | 0))
                                    break b;
                                var Zb = fb - 1 | 0;
                                if (0 != (b[(fb << 2 >> 2) + q] | 0))
                                    break;
                                fb = Zb
                            }
                            b[lb >> 2] = b[((Zb << 2) + 28 >> 2) + g];
                            for (var qb = Ca + 1 | 0, Ab = b[Yb] = qb; ; ) {
                                if (Ab >>> 0 > R >>> 0)
                                    break b;
                                if (0 != (b[(Ab << 2 >> 2) + q] | 0))
                                    break;
                                Ab = Ab + 1 | 0
                            }
                            b[Yb] = Ab
                        }
                    while (0);b[g + 23] = -1;
                    b[g + 40] = 1048575;
                    b[g + 3] = 32 - b[Ha >> 2] | 0;
                    f = 1
                }
            while (0);V = h;
            return f
        }
        function rc(a) {
            Mb(a, 0, 68, 1)
        }
        function Ob(a) {
            if (0 != (a | 0)) {
                var c = b[a - 4 >> 2];
                a = a - 8 | 0;
                var d = 0 == (c | 0) ? 4 : (c | 0) == (b[a >> 2] ^ -1 | 0) ? 5 : 4;
                4 == d && ta(F.D | 0, F.a | 0, 696);
                Qa(a)
            }
        }
        function dc(a) {
            a = 0 == (a | 0) ? 1 : a;
            var c = Oa((a << 1) + 8 | 0, 0);
            0 == (c | 0) ? a = 0 : (b[c + 4 >> 2] = a,
            b[c >> 2] = a ^ -1,
            a = c + 8 | 0);
            return a
        }
        function Pb(a) {
            if (0 != (a | 0)) {
                var c = b[a - 4 >> 2];
                a = a - 8 | 0;
                var d = 0 == (c | 0) ? 4 : (c | 0) == (b[a >> 2] ^ -1 | 0) ? 5 : 4;
                4 == d && ta(F.D | 0, F.a | 0, 696);
                Qa(a)
            }
        }
        function Ta(a) {
            a = 0 == (a | 0) ? 1 : a;
            var c = Oa((a << 2) + 8 | 0, 0);
            0 == (c | 0) ? a = 0 : (b[c + 4 >> 2] = a,
            b[c >> 2] = a ^ -1,
            a = c + 8 | 0);
            return a
        }
        function ff(a, c) {
            0 != (c | 0) & 17 > c >>> 0 || ta(F.Ib | 0, F.a | 0, 2018);
            a = b[a + (c - 1 << 2) + 28 >> 2];
            return 0 == (a | 0) ? -1 : (a - 1 | 0) >>> ((16 - c | 0) >>> 0)
        }
        function $a(a) {
            return (Q[a | 0] & 255) << 8 | Q[a + 1 | 0] & 255
        }
        function Oc(a) {
            return (Q[a + 1 | 0] & 255) << 16 | (Q[a | 0] & 255) << 24 | Q[a + 3 | 0] & 255 | (Q[a + 2 | 0] & 255) << 8
        }
        function Bb(a) {
            return Q[a | 0] & 255
        }
        function $b(a) {
            return Q[a + 2 | 0] & 255 | (Q[a | 0] & 255) << 16 | (Q[a + 1 | 0] & 255) << 8
        }
        function gf(a) {
            return 0 != (ba[a + 12 | 0] & 1) << 24 >> 24
        }
        function Nc(a) {
            ta(a, F.a | 0, 2602)
        }
        function hf(a, c) {
            0 == a && 0 == c || 9 == a && 0 == c ? a = 4 : 1 == a && 0 == c || 2 == a && 0 == c || 7 == a && 0 == c || 8 == a && 0 == c || 3 == a && 0 == c || 4 == a && 0 == c || 5 == a && 0 == c || 6 == a && 0 == c ? a = 8 : (ta(F.xb | 0, F.a | 0, 2766),
            a = 0);
            return a
        }
        function Td(a, c) {
            return hf(a, c) << 1 & 536870910
        }
        function Ud(a, c, d) {
            if (0 == (c | 0) | 74 > d >>> 0)
                var e = 0;
            else
                18552 != ($a(c) | 0) ? e = 0 : 74 > $a(c + 2 | 0) >>> 0 ? e = 0 : Oc(c + 6 | 0) >>> 0 > d >>> 0 ? e = 0 : e = c;
            return e
        }
        function wc(a, c, d) {
            var e = d >> 2;
            if (0 == (a | 0) | 74 > c >>> 0 | 0 == (d | 0))
                e = 0;
            else if (40 != (b[e] | 0))
                e = 0;
            else if (a = Ud(0, a, c),
            0 == (a | 0))
                e = 0;
            else {
                c = $a(a + 12 | 0);
                b[e + 1] = c;
                c = $a(a + 14 | 0);
                b[e + 2] = c;
                c = Bb(a + 16 | 0);
                b[e + 3] = c;
                c = Bb(a + 17 | 0);
                b[e + 4] = c;
                c = a + 18 | 0;
                var g = Bb(c);
                d = d + 32 | 0;
                b[d >> 2] = g;
                b[d + 4 >> 2] = 0;
                d = Bb(c);
                b[e + 5] = 0 == (d | 0) ? 8 : 9 == (d | 0) ? 8 : 16;
                d = Oc(a + 25 | 0);
                b[e + 6] = d;
                a = Oc(a + 29 | 0);
                b[e + 7] = a;
                e = 1
            }
            return e
        }
        function rb(a) {
            b[a >> 2] = 0;
            Vd(a + 4 | 0);
            b[a + 20 >> 2] = 0
        }
        function Vd(a) {
            jf(a)
        }
        function kf(a, c) {
            if ((a | 0) != (c | 0)) {
                b[a >> 2] = b[c >> 2];
                var d = a + 4 | 0;
                lf(d, c + 4 | 0);
                if (gf(d))
                    Wd(a);
                else {
                    d = b[c + 20 >> 2];
                    c = (a + 20 | 0) >> 2;
                    var e = b[c];
                    0 == (d | 0) ? (td(e),
                    b[c] = 0) : 0 == (e | 0) ? (d = mf(d),
                    b[c] = d) : Xd(e, d)
                }
            }
            return a
        }
        function nf(a) {
            of(a)
        }
        function td(a) {
            0 != (a | 0) && (pf(a),
            Qa(a))
        }
        function lf(a, c) {
            qf(a, c);
            return a
        }
        function Wd(a) {
            b[a >> 2] = 0;
            ud(a + 4 | 0);
            a = a + 20 | 0;
            var c = b[a >> 2];
            0 != (c | 0) && (td(c),
            b[a >> 2] = 0)
        }
        function sb(a) {
            var c = b[a + 20 >> 2];
            0 != (c | 0) && td(c);
            nf(a + 4 | 0)
        }
        function rf(a) {
            var c = 0 == (a | 0);
            a: do
                if (c)
                    var d = 0;
                else
                    for (c = 0; ; )
                        if (a >>>= 1,
                        c = c + 1 | 0,
                        0 == (a | 0)) {
                            d = c;
                            break a
                        }
            while (0);return d
        }
        function sf(a) {
            return b[a + 4 >> 2]
        }
        function Yd(a) {
            a >>= 2;
            b[a] = 0;
            b[a + 1] = 0;
            b[a + 2] = 0;
            b[a + 3] = 0;
            b[a + 4] = 0;
            b[a + 5] = 0
        }
        function tf(a) {
            b[a + 16 >> 2] = 0;
            b[a + 20 >> 2] = 0
        }
        function Xd(a, c) {
            if ((a | 0) != (c | 0)) {
                uf(a);
                Pc(a, c, 180, 1);
                var d = c + 168 | 0;
                if (0 != (b[d >> 2] | 0)) {
                    var e = a + 164 | 0
                      , g = Ta(b[e >> 2]);
                    b[a + 168 >> 2] = g;
                    0 != (g | 0) && Pc(g, b[d >> 2], b[e >> 2] << 2, 1)
                }
                c = c + 176 | 0;
                0 != (b[c >> 2] | 0) && (d = a + 172 | 0,
                e = dc(b[d >> 2]),
                b[a + 176 >> 2] = e,
                0 != (e | 0) && Pc(e, b[c >> 2], b[d >> 2] << 1, 1))
            }
            return a
        }
        function mf(a) {
            var c = Oa(180, 0);
            return 0 == (c | 0) ? 0 : vf(c, a)
        }
        function ud(a) {
            var c = a | 0
              , d = b[c >> 2];
            if (0 != (d | 0)) {
                var e = a + 4 | 0;
                Qa(d);
                b[c >> 2] = 0;
                b[e >> 2] = 0;
                b[a + 8 >> 2] = 0
            }
            ba[a + 12 | 0] = 0
        }
        function vd(a, c) {
            var d = (a + 4 | 0) >> 2;
            var e = y[d]
              , g = (e | 0) == (c | 0);
            do
                if (g)
                    var h = 1;
                else {
                    if (e >>> 0 <= c >>> 0) {
                        if (y[a + 8 >> 2] >>> 0 < c >>> 0) {
                            if (!Zd(a, c, (e + 1 | 0) == (c | 0))) {
                                h = 0;
                                break
                            }
                            h = b[d]
                        } else
                            h = e;
                        wf(b[a >> 2] + h | 0, c - h | 0)
                    }
                    b[d] = c;
                    h = 1
                }
            while (0);return h
        }
        function Cc(a, c) {
            y[a + 4 >> 2] >>> 0 <= c >>> 0 && ta(F.l | 0, F.a | 0, 968);
            return b[a >> 2] + c | 0
        }
        function xf() {
            var a = Oa(180, 0);
            return 0 == (a | 0) ? 0 : yf(a)
        }
        function zf(a) {
            a = y[a >> 2];
            16 < a >>> 0 ? (a = Af(a) + 1 | 0,
            a = Aa(a, 11) & 255) : a = 0;
            return a
        }
        function $d(a) {
            var c = a + 4 | 0
              , d = sf(c);
            0 != (d | 0) & 8193 > d >>> 0 || ta(F.yb | 0, F.a | 0, 3106);
            var e = a | 0;
            b[e >> 2] = d;
            var g = a + 20 | 0
              , h = y[g >> 2];
            0 == (h | 0) ? (d = xf(),
            g = b[g >> 2] = d,
            e = b[e >> 2]) : (g = h,
            e = d);
            c = Cc(c, 0);
            a = zf(a);
            return cc(g, e, c, a)
        }
        function Af(a) {
            var c = Bf(a);
            return 32 == (c | 0) ? 32 : (1 << c >>> 0 < a >>> 0 & 1) + c | 0
        }
        function xc(a, c) {
            0 == (c | 0) ? a = 0 : 16 < c >>> 0 ? (c = cd(a, c - 16 | 0),
            a = cd(a, 16),
            a |= c << 16) : a = cd(a, c);
            return a
        }
        function na(a, c) {
            var d = y[c + 20 >> 2] >> 2;
            var e = (a + 20 | 0) >> 2;
            var g = y[e];
            if (24 > (g | 0)) {
                var h = (a + 4 | 0) >> 2;
                var l = y[h]
                  , t = y[a + 8 >> 2]
                  , q = l >>> 0 < t >>> 0;
                16 > (g | 0) ? (q ? (q = l + 1 | 0,
                l = (Q[l] & 255) << 8) : (q = l,
                l = 0),
                q >>> 0 < t >>> 0 ? (t = q + 1 | 0,
                q = Q[q] & 255) : (t = q,
                q = 0),
                b[h] = t,
                b[e] = g + 16 | 0,
                h = a + 16 | 0,
                g = (q | l) << 16 - g | b[h >> 2],
                b[h >> 2] = g) : (q ? (b[h] = l + 1 | 0,
                l = Q[l] & 255) : l = 0,
                b[e] = g + 8 | 0,
                h = a + 16 | 0,
                g = l << 24 - g | b[h >> 2],
                b[h >> 2] = g)
            } else
                g = b[a + 16 >> 2];
            a = a + 16 | 0;
            h = (g >>> 16) + 1 | 0;
            if (h >>> 0 > y[d + 4] >>> 0) {
                t = y[d + 5];
                q = t - 1 | 0;
                var D = h >>> 0 > y[((q << 2) + 28 >> 2) + d] >>> 0;
                a: do
                    if (D)
                        for (; ; ) {
                            l = t + 1 | 0;
                            if (h >>> 0 <= y[((t << 2) + 28 >> 2) + d] >>> 0) {
                                var A = t;
                                break a
                            }
                            t = l
                        }
                    else
                        l = t,
                        A = q;
                while (0);g = (g >>> ((32 - l | 0) >>> 0)) + b[((A << 2) + 96 >> 2) + d] | 0;
                if (g >>> 0 < y[c >> 2] >>> 0) {
                    m = l;
                    u = ya[b[d + 44] + (g << 1) >> 1] & 65535;
                    var f = 22
                } else {
                    ta(F.v | 0, F.a | 0, 3375);
                    var k = 0;
                    f = 23
                }
            } else {
                m = y[b[d + 42] + (g >>> ((32 - b[d + 2] | 0) >>> 0) << 2) >> 2];
                -1 == (m | 0) && ta(F.Cb | 0, F.a | 0, 3353);
                d = m & 65535;
                m >>>= 16;
                c = Cf(c + 4 | 0, d);
                if ((Q[c] & 255 | 0) == (m | 0))
                    var m = m
                      , u = d;
                else
                    ta(F.Db | 0, F.a | 0, 3357),
                    u = d;
                f = 22
            }
            22 == f && (b[a >> 2] <<= m,
            b[e] = b[e] - m | 0,
            k = u);
            return k
        }
        function Dc(a, c, d) {
            0 == (d | 0) ? a = 0 : (b[a >> 2] = c,
            b[a + 4 >> 2] = c,
            b[a + 12 >> 2] = d,
            b[a + 8 >> 2] = c + d | 0,
            tf(a),
            a = 1);
            return a
        }
        function cd(a, c) {
            33 <= c >>> 0 && ta(F.zb | 0, F.a | 0, 3299);
            var d = (a + 20 | 0) >> 2;
            var e = y[d]
              , g = (e | 0) < (c | 0);
            a: do
                if (g) {
                    var h = a + 4 | 0;
                    g = a + 8 | 0;
                    for (var l = a + 16 | 0, t = e; ; )
                        if (e = b[h >> 2],
                        (e | 0) == (b[g >> 2] | 0) ? e = 0 : (b[h >> 2] = e + 1 | 0,
                        e = Q[e] & 255),
                        t = t + 8 | 0,
                        b[d] = t,
                        33 > (t | 0) || (ta(F.Bb | 0, F.a | 0, 3308),
                        t = b[d]),
                        e = e << 32 - t | b[l >> 2],
                        b[l >> 2] = e,
                        (t | 0) >= (c | 0)) {
                            h = t;
                            l = e;
                            break a
                        }
                } else
                    h = e,
                    l = b[a + 16 >> 2];
            while (0);b[a + 16 >> 2] = l << c;
            b[d] = h - c | 0;
            return l >>> ((32 - c | 0) >>> 0)
        }
        function Cf(a, c) {
            y[a + 4 >> 2] >>> 0 <= c >>> 0 && ta(F.l | 0, F.a | 0, 967);
            return b[a >> 2] + c | 0
        }
        function Jb(a, c) {
            var d = V;
            V += 24;
            var e = rf(8192);
            e = xc(a, e);
            if (0 == (e | 0))
                Wd(c),
                a = 1;
            else {
                var g = c + 4 | 0;
                if (vd(g, e)) {
                    var h = Cc(g, 0);
                    Mb(h, 0, e, 1);
                    h = xc(a, 5);
                    if (0 == (h | 0) | 21 < h >>> 0)
                        a = 0;
                    else {
                        rb(d);
                        var l = d + 4 | 0
                          , t = vd(l, 21);
                        a: do
                            if (t) {
                                for (var q = 0; ; ) {
                                    var D = xc(a, 3)
                                      , A = Cc(l, Q[F.U + q | 0] & 255);
                                    ba[A] = D & 255;
                                    q = q + 1 | 0;
                                    if ((q | 0) == (h | 0))
                                        break
                                }
                                if ($d(d))
                                    b: for (h = 0; ; ) {
                                        q = h >>> 0 < e >>> 0;
                                        l = e - h | 0;
                                        D = 0 == (h | 0);
                                        for (A = h - 1 | 0; ; ) {
                                            if (!q) {
                                                if ((h | 0) != (e | 0)) {
                                                    q = 0;
                                                    break a
                                                }
                                                q = $d(c);
                                                break a
                                            }
                                            t = na(a, d);
                                            if (17 > t >>> 0) {
                                                l = Cc(g, h);
                                                ba[l] = t & 255;
                                                h = h + 1 | 0;
                                                continue b
                                            }
                                            if (17 == (t | 0)) {
                                                t = xc(a, 3) + 3 | 0;
                                                if (t >>> 0 > l >>> 0) {
                                                    q = 0;
                                                    break a
                                                }
                                                h = t + h | 0;
                                                continue b
                                            } else if (18 == (t | 0)) {
                                                t = xc(a, 7) + 11 | 0;
                                                if (t >>> 0 > l >>> 0) {
                                                    q = 0;
                                                    break a
                                                }
                                                h = t + h | 0;
                                                continue b
                                            } else {
                                                if (2 <= (t - 19 | 0) >>> 0) {
                                                    ta(F.v | 0, F.a | 0, 3249);
                                                    q = 0;
                                                    break a
                                                }
                                                var f = 19 == (t | 0) ? xc(a, 2) + 3 | 0 : xc(a, 6) + 7 | 0;
                                                if (D | f >>> 0 > l >>> 0) {
                                                    q = 0;
                                                    break a
                                                }
                                                t = Cc(g, A);
                                                t = Q[t];
                                                if (0 == t << 24 >> 24) {
                                                    q = 0;
                                                    break a
                                                }
                                                f = f + h | 0;
                                                if (h >>> 0 < f >>> 0) {
                                                    l = h;
                                                    break
                                                }
                                            }
                                        }
                                        for (; ; )
                                            if (h = Cc(g, l),
                                            l = l + 1 | 0,
                                            ba[h] = t,
                                            (l | 0) == (f | 0)) {
                                                h = f;
                                                continue b
                                            }
                                    }
                                else
                                    q = 0
                            } else
                                q = 0;
                        while (0);sb(d);
                        a = q
                    }
                } else
                    a = 0
            }
            V = d;
            return a
        }
        function ae(a) {
            return 519686845 == (b[a >> 2] | 0)
        }
        function Df(a, c) {
            if (0 == (a | 0) | 62 > c >>> 0)
                a = 0;
            else {
                var d = Ef();
                0 == (d | 0) ? a = 0 : Ff(d, a, c) ? a = d : (be(d),
                a = 0)
            }
            return a
        }
        function Ef() {
            var a = Oa(300, 0);
            return 0 == (a | 0) ? 0 : Gf(a)
        }
        function Ff(a, c, d) {
            var e = Ud(0, c, d);
            b[a + 88 >> 2] = e;
            if (0 == (e | 0))
                var g = 0;
            else
                b[a + 4 >> 2] = c,
                b[a + 8 >> 2] = d,
                Hf(a) ? g = If(a) : g = 0;
            return g
        }
        function be(a) {
            0 != (a | 0) && (Jf(a),
            Qa(a))
        }
        function Kf(a, c, d, e, g) {
            if (0 == (a | 0) | 0 == (c | 0) | 8 > d >>> 0 | 15 < g >>> 0)
                var h = 0;
            else
                ae(a) ? h = Lf(a, c, d, e, g) : h = 0;
            return h
        }
        function Lf(a, c, d, e, g) {
            var h = y[a + 88 >> 2]
              , l = Oc((g << 2) + h + 70 | 0)
              , t = b[a + 8 >> 2]
              , q = g + 1 | 0
              , D = Bb(h + 16 | 0);
            h = q >>> 0 < D >>> 0 ? Oc((q << 2) + h + 70 | 0) : t;
            h >>> 0 <= l >>> 0 && ta(F.Gb | 0, F.a | 0, 3794);
            return ce(a, b[a + 4 >> 2] + l | 0, h - l | 0, c, d, e, g)
        }
        function ce(a, c, d, e, g, h, l) {
            var t = a + 88 | 0
              , q = y[t >> 2]
              , D = $a(q + 12 | 0) >>> (l >>> 0);
            D = Ua(D, 1);
            l = $a(q + 14 | 0) >>> (l >>> 0);
            l = Ua(l, 1);
            D = (D + 3 | 0) >>> 2;
            l = (l + 3 | 0) >>> 2;
            q = Bb(q + 18 | 0);
            q = (0 == (q | 0) ? 8 : 9 == (q | 0) ? 8 : 16) * D | 0;
            if (0 == (h | 0)) {
                var A = q;
                var f = 5
            } else if (q >>> 0 <= h >>> 0 & 0 == (h & 3 | 0))
                A = h,
                f = 5;
            else {
                var k = 0;
                f = 12
            }
            5 == f && ((A * l | 0) >>> 0 > g >>> 0 ? k = 0 : (g = (D + 1 | 0) >>> 1,
            h = (l + 1 | 0) >>> 1,
            Dc(a + 92 | 0, c, d) ? (c = Bb(b[t >> 2] + 18 | 0),
            0 == (c | 0) ? (de(a, e, 0, A, D, l, g, h),
            k = 1) : 2 == (c | 0) || 3 == (c | 0) || 5 == (c | 0) || 6 == (c | 0) || 4 == (c | 0) ? (ee(a, e, 0, A, D, l, g, h),
            k = 1) : 9 == (c | 0) ? (fe(a, e, 0, A, D, l, g, h),
            k = 1) : 7 == (c | 0) || 8 == (c | 0) ? (ge(a, e, 0, A, D, l, g, h),
            k = 1) : k = 0) : k = 0));
            return k
        }
        function Mf(a) {
            0 == (a | 0) ? a = 0 : ae(a) ? (be(a),
            a = 1) : a = 0;
            return a
        }
        function Ec(a) {
            Nf(a)
        }
        function Jf(a) {
            Of(a)
        }
        function Of(a) {
            he(a)
        }
        function Pf(a) {
            b[a >> 2] = 0;
            b[a + 4 >> 2] = 0;
            b[a + 8 >> 2] = 0;
            ba[a + 12 | 0] = 0
        }
        function Qf(a) {
            b[a >> 2] = 0;
            b[a + 4 >> 2] = 0;
            b[a + 8 >> 2] = 0;
            ba[a + 12 | 0] = 0
        }
        function Rf(a) {
            b[a + 164 >> 2] = 0;
            b[a + 168 >> 2] = 0;
            b[a + 172 >> 2] = 0;
            b[a + 176 >> 2] = 0
        }
        function jf(a) {
            b[a >> 2] = 0;
            b[a + 4 >> 2] = 0;
            b[a + 8 >> 2] = 0;
            ba[a + 12 | 0] = 0
        }
        function Nf(a) {
            b[a >> 2] = 40
        }
        function ie(a) {
            Sf(a)
        }
        function je(a) {
            Tf(a)
        }
        function Tf(a) {
            Uf(a)
        }
        function Uf(a) {
            var c = a | 0
              , d = b[c >> 2];
            if (0 != (d | 0)) {
                var e = a + 4 | 0;
                Qa(d);
                b[c >> 2] = 0;
                b[e >> 2] = 0;
                b[a + 8 >> 2] = 0
            }
            ba[a + 12 | 0] = 0
        }
        function Sf(a) {
            Vf(a)
        }
        function Vf(a) {
            var c = a | 0
              , d = b[c >> 2];
            if (0 != (d | 0)) {
                var e = a + 4 | 0;
                Qa(d);
                b[c >> 2] = 0;
                b[e >> 2] = 0;
                b[a + 8 >> 2] = 0
            }
            ba[a + 12 | 0] = 0
        }
        function Gf(a) {
            0 == (a | 0) ? a = 0 : Wf(a);
            return a
        }
        function Wf(a) {
            Xf(a)
        }
        function Xf(a) {
            b[a >> 2] = 519686845;
            b[a + 4 >> 2] = 0;
            b[a + 8 >> 2] = 0;
            b[a + 88 >> 2] = 0;
            Yd(a + 92 | 0);
            rb(a + 116 | 0);
            rb(a + 140 | 0);
            rb(a + 164 | 0);
            rb(a + 188 | 0);
            rb(a + 212 | 0);
            ke(a + 236 | 0);
            ke(a + 252 | 0);
            le(a + 268 | 0);
            le(a + 284 | 0)
        }
        function ke(a) {
            Qf(a)
        }
        function le(a) {
            Pf(a)
        }
        function yf(a) {
            0 == (a | 0) ? a = 0 : Yf(a);
            return a
        }
        function Yf(a) {
            Rf(a)
        }
        function Zd(a, c, d) {
            Va(a, c, d, 1, 0) ? a = 1 : (ba[a + 12 | 0] = 1,
            a = 0);
            return a
        }
        function wf(a, c) {
            Mb(a, 0, c, 1)
        }
        function vf(a, c) {
            0 == (a | 0) ? a = 0 : Zf(a, c);
            return a
        }
        function Zf(a, c) {
            $f(a, c)
        }
        function $f(a, c) {
            b[a + 164 >> 2] = 0;
            b[a + 168 >> 2] = 0;
            b[a + 172 >> 2] = 0;
            b[a + 176 >> 2] = 0;
            Xd(a, c)
        }
        function qf(a, c) {
            var d = (a | 0) == (c | 0);
            do
                if (d)
                    var e = 1;
                else {
                    e = (c + 4 | 0) >> 2;
                    if ((b[a + 8 >> 2] | 0) == (b[e] | 0))
                        vd(a, 0);
                    else if (ud(a),
                    !Zd(a, b[e], 0)) {
                        e = 0;
                        break
                    }
                    Pc(b[a >> 2], b[c >> 2], b[e], 1);
                    b[a + 4 >> 2] = b[e];
                    e = 1
                }
            while (0);return e
        }
        function pf(a) {
            ag(a)
        }
        function ag(a) {
            bg(a)
        }
        function bg(a) {
            var c = b[a + 168 >> 2];
            0 != (c | 0) && Pb(c);
            a = b[a + 176 >> 2];
            0 != (a | 0) && Ob(a)
        }
        function of(a) {
            ud(a)
        }
        function de(a, c, d, e, g, h, l, t) {
            var q, D = V;
            V += 24;
            var A = D >> 2;
            var f = D + 4;
            var k = f >> 2;
            d = D + 8 >> 2;
            var m = a + 236 | 0
              , u = dd(m)
              , z = a + 252 | 0
              , B = dd(z);
            b[A] = 0;
            b[k] = 0;
            var C = Bb(b[a + 88 >> 2] + 17 | 0)
              , S = e >>> 2
              , W = 0 == (C | 0);
            a: do
                if (!W) {
                    W = 0 == (t | 0);
                    var ea = t - 1 | 0;
                    h = 0 != (h & 1 | 0);
                    var X = e << 1
                      , P = a + 92 | 0
                      , Y = a + 116 | 0
                      , R = a + 188 | 0
                      , ma = S + 1 | 0
                      , Fa = S + 2 | 0
                      , za = S + 3 | 0
                      , ra = l - 1 | 0;
                    a = a + 140 | 0;
                    var Sa = ra << 4;
                    g = 0 != (g & 1 | 0);
                    for (var Ka = 0, Ga = 1; ; ) {
                        b: do
                            if (W)
                                var Ba = Ga;
                            else {
                                Ba = b[c + (Ka << 2) >> 2];
                                for (var La = 0, ua = Ga; ; ) {
                                    if (0 == (La & 1 | 0)) {
                                        var va = Ba;
                                        Ga = 16;
                                        var Na = 1
                                          , wa = l
                                          , oa = 0
                                    } else
                                        va = Ba + Sa | 0,
                                        Ga = -16,
                                        wa = Na = -1,
                                        oa = ra;
                                    var ka = (La | 0) == (ea | 0)
                                      , pa = ka & h
                                      , ia = (oa | 0) == (wa | 0);
                                    c: do
                                        if (ia)
                                            var qa = ua;
                                        else
                                            for (qa = ka & h ^ 1,
                                            ka = ua,
                                            ua = va,
                                            va = ua >> 2; ; ) {
                                                ia = 1 == (ka | 0) ? na(P, Y) | 512 : ka;
                                                ka = ia & 7;
                                                ia >>>= 3;
                                                var xa = Q[F.g + ka | 0] & 255;
                                                var aa = 0;
                                                for (q = b[A]; ; ) {
                                                    var fa = na(P, a);
                                                    b[A] = q + fa | 0;
                                                    Ma(D, u);
                                                    q = y[A];
                                                    fa = mb(m, q);
                                                    b[(aa << 2 >> 2) + d] = b[fa >> 2];
                                                    aa = aa + 1 | 0;
                                                    if (aa >>> 0 >= xa >>> 0)
                                                        break
                                                }
                                                xa = (oa | 0) == (ra | 0) & g;
                                                aa = ua >> 2;
                                                q = pa | xa;
                                                d: do
                                                    if (q)
                                                        for (aa = 0; ; ) {
                                                            var sa = aa * e | 0;
                                                            q = sa >> 2;
                                                            var la = ua + sa | 0
                                                              , Ca = 0 == (aa | 0) | qa;
                                                            fa = aa << 1;
                                                            var Ha = na(P, R);
                                                            b[k] = b[k] + Ha | 0;
                                                            Ma(f, B);
                                                            xa ? (Ca ? (b[la >> 2] = b[((Q[(ka << 2) + kb + fa | 0] & 255) << 2 >> 2) + d],
                                                            fa = mb(z, b[k]),
                                                            b[q + (va + 1)] = b[fa >> 2],
                                                            q = na(P, R),
                                                            b[k] = b[k] + q | 0) : (q = na(P, R),
                                                            b[k] = b[k] + q | 0),
                                                            Ma(f, B)) : Ca ? (b[la >> 2] = b[((Q[(ka << 2) + kb + fa | 0] & 255) << 2 >> 2) + d],
                                                            la = mb(z, b[k]),
                                                            b[q + (va + 1)] = b[la >> 2],
                                                            sa = sa + (ua + 8) | 0,
                                                            la = na(P, R),
                                                            b[k] = b[k] + la | 0,
                                                            Ma(f, B),
                                                            b[sa >> 2] = b[((Q[(ka << 2) + kb + (fa | 1) | 0] & 255) << 2 >> 2) + d],
                                                            fa = mb(z, b[k]),
                                                            b[q + (va + 3)] = b[fa >> 2]) : (q = na(P, R),
                                                            b[k] = b[k] + q | 0,
                                                            Ma(f, B));
                                                            aa = aa + 1 | 0;
                                                            if (2 == (aa | 0))
                                                                break d
                                                        }
                                                    else
                                                        b[aa] = b[((Q[(ka << 2) + kb | 0] & 255) << 2 >> 2) + d],
                                                        fa = na(P, R),
                                                        b[k] = b[k] + fa | 0,
                                                        Ma(f, B),
                                                        fa = mb(z, b[k]),
                                                        b[va + 1] = b[fa >> 2],
                                                        b[va + 2] = b[((Q[(ka << 2) + kb + 1 | 0] & 255) << 2 >> 2) + d],
                                                        fa = na(P, R),
                                                        b[k] = b[k] + fa | 0,
                                                        Ma(f, B),
                                                        fa = mb(z, b[k]),
                                                        b[va + 3] = b[fa >> 2],
                                                        b[(S << 2 >> 2) + aa] = b[((Q[(ka << 2) + kb + 2 | 0] & 255) << 2 >> 2) + d],
                                                        fa = na(P, R),
                                                        b[k] = b[k] + fa | 0,
                                                        Ma(f, B),
                                                        fa = mb(z, b[k]),
                                                        b[(ma << 2 >> 2) + aa] = b[fa >> 2],
                                                        b[(Fa << 2 >> 2) + aa] = b[((Q[(ka << 2) + kb + 3 | 0] & 255) << 2 >> 2) + d],
                                                        fa = na(P, R),
                                                        b[k] = b[k] + fa | 0,
                                                        Ma(f, B),
                                                        fa = mb(z, b[k]),
                                                        b[(za << 2 >> 2) + aa] = b[fa >> 2];
                                                while (0);oa = oa + Na | 0;
                                                if ((oa | 0) == (wa | 0)) {
                                                    qa = ia;
                                                    break c
                                                }
                                                ka = ia;
                                                ua = ua + Ga | 0;
                                                va = ua >> 2
                                            }
                                    while (0);La = La + 1 | 0;
                                    if ((La | 0) == (t | 0)) {
                                        Ba = qa;
                                        break b
                                    }
                                    Ba = Ba + X | 0;
                                    ua = qa
                                }
                            }
                        while (0);Ka = Ka + 1 | 0;
                        if ((Ka | 0) == (C | 0))
                            break a;
                        Ga = Ba
                    }
                }
            while (0);V = D;
            return 1
        }
        function he(a) {
            b[a >> 2] = 0;
            ie(a + 284 | 0);
            ie(a + 268 | 0);
            je(a + 252 | 0);
            je(a + 236 | 0);
            var c = a + 188 | 0;
            sb(a + 212 | 0);
            sb(c);
            c = a + 140 | 0;
            sb(a + 164 | 0);
            sb(c);
            sb(a + 116 | 0)
        }
        function Ma(a, c) {
            var d = b[a >> 2];
            c = d - c | 0;
            var e = c >> 31;
            b[a >> 2] = e & d | c & (e ^ -1)
        }
        function wd(a) {
            return b[a + 4 >> 2]
        }
        function dd(a) {
            return b[a + 4 >> 2]
        }
        function ee(a, c, d, e, g, h, l, t) {
            var q = V;
            V += 48;
            var D = q >> 2;
            var A = q + 4;
            var f = A >> 2;
            var k = q + 8;
            var m = k >> 2;
            var u = q + 12;
            var z = u >> 2;
            var B = q + 16 >> 2;
            d = q + 32 >> 2;
            var C = a + 236 | 0
              , S = dd(C)
              , W = a + 252 | 0
              , ea = dd(W)
              , X = a + 268 | 0
              , P = wd(X)
              , Y = b[a + 88 >> 2]
              , R = $a(Y + 63 | 0);
            b[D] = 0;
            b[f] = 0;
            b[m] = 0;
            b[z] = 0;
            Y = Bb(Y + 17 | 0);
            var ma = 0 == (Y | 0);
            a: do
                if (!ma) {
                    ma = 0 == (t | 0);
                    var Fa = t - 1 | 0;
                    h = 0 == (h & 1 | 0);
                    var za = e << 1
                      , ra = a + 92 | 0
                      , Sa = a + 116 | 0
                      , Ka = a + 212 | 0
                      , Ga = a + 188 | 0
                      , Ba = a + 284 | 0
                      , La = a + 140 | 0;
                    a = a + 164 | 0;
                    var ua = l - 1 | 0
                      , va = ua << 5;
                    g = 0 != (g & 1 | 0);
                    for (var Na = 0, wa = 1; ; ) {
                        b: do
                            if (ma)
                                var oa = wa;
                            else {
                                oa = b[c + (Na << 2) >> 2];
                                for (var ka = 0, pa = wa; ; ) {
                                    if (0 == (ka & 1 | 0)) {
                                        var ia = oa;
                                        wa = 32;
                                        var qa = 1
                                          , xa = l
                                          , aa = 0
                                    } else
                                        ia = oa + va | 0,
                                        wa = -32,
                                        xa = qa = -1,
                                        aa = ua;
                                    var fa = h | (ka | 0) != (Fa | 0);
                                    var sa = (aa | 0) == (xa | 0);
                                    c: do
                                        if (sa)
                                            var la = pa;
                                        else
                                            for (la = pa; ; ) {
                                                pa = 1 == (la | 0) ? na(ra, Sa) | 512 : la;
                                                la = pa & 7;
                                                pa >>>= 3;
                                                sa = Q[F.g + la | 0] & 255;
                                                for (var Ca = 0, Ha = b[m]; ; ) {
                                                    var Ia = na(ra, a);
                                                    b[m] = Ha + Ia | 0;
                                                    Ma(k, P);
                                                    Ha = y[m];
                                                    Ia = gb(X, Ha);
                                                    b[(Ca << 2 >> 2) + d] = ya[Ia >> 1] & 65535;
                                                    Ca = Ca + 1 | 0;
                                                    if (Ca >>> 0 >= sa >>> 0)
                                                        break
                                                }
                                                Ca = 0;
                                                for (Ha = b[D]; !(Ia = na(ra, La),
                                                b[D] = Ha + Ia | 0,
                                                Ma(q, S),
                                                Ha = y[D],
                                                Ia = mb(C, Ha),
                                                b[(Ca << 2 >> 2) + B] = b[Ia >> 2],
                                                Ca = Ca + 1 | 0,
                                                Ca >>> 0 >= sa >>> 0); )
                                                    ;
                                                Ca = (aa | 0) == (ua | 0) & g;
                                                Ha = ia;
                                                sa = Ha >> 2;
                                                for (Ia = 0; ; ) {
                                                    var Ya = 0 == (Ia | 0) | fa;
                                                    var bb = Ia << 1;
                                                    var Ja = na(ra, Ka);
                                                    b[z] = b[z] + Ja | 0;
                                                    Ma(u, R);
                                                    Ja = na(ra, Ga);
                                                    b[f] = b[f] + Ja | 0;
                                                    Ma(A, ea);
                                                    if (Ya) {
                                                        var wb = Ha
                                                          , hb = Q[(la << 2) + kb + bb | 0] & 255;
                                                        Ja = gb(Ba, 3 * b[z] | 0) >> 1;
                                                        b[wb >> 2] = (ya[Ja] & 65535) << 16 | b[(hb << 2 >> 2) + d];
                                                        b[sa + 1] = (ya[Ja + 2] & 65535) << 16 | ya[Ja + 1] & 65535;
                                                        b[sa + 2] = b[(hb << 2 >> 2) + B];
                                                        Ja = mb(W, b[f]);
                                                        b[sa + 3] = b[Ja >> 2]
                                                    }
                                                    Ja = na(ra, Ka);
                                                    b[z] = b[z] + Ja | 0;
                                                    Ma(u, R);
                                                    Ja = na(ra, Ga);
                                                    b[f] = b[f] + Ja | 0;
                                                    Ma(A, ea);
                                                    Ca | Ya ^ 1 || (Ya = Ha + 16 | 0,
                                                    Ja = Q[(la << 2) + kb + (bb | 1) | 0] & 255,
                                                    bb = gb(Ba, 3 * b[z] | 0) >> 1,
                                                    b[Ya >> 2] = (ya[bb] & 65535) << 16 | b[(Ja << 2 >> 2) + d],
                                                    b[sa + 5] = (ya[bb + 2] & 65535) << 16 | ya[bb + 1] & 65535,
                                                    b[sa + 6] = b[(Ja << 2 >> 2) + B],
                                                    bb = mb(W, b[f]),
                                                    b[sa + 7] = b[bb >> 2]);
                                                    Ia = Ia + 1 | 0;
                                                    if (2 == (Ia | 0))
                                                        break;
                                                    Ha = Ha + e | 0;
                                                    sa = Ha >> 2
                                                }
                                                aa = aa + qa | 0;
                                                if ((aa | 0) == (xa | 0)) {
                                                    la = pa;
                                                    break c
                                                }
                                                la = pa;
                                                ia = ia + wa | 0
                                            }
                                    while (0);ka = ka + 1 | 0;
                                    if ((ka | 0) == (t | 0)) {
                                        oa = la;
                                        break b
                                    }
                                    oa = oa + za | 0;
                                    pa = la
                                }
                            }
                        while (0);Na = Na + 1 | 0;
                        if ((Na | 0) == (Y | 0))
                            break a;
                        wa = oa
                    }
                }
            while (0);V = q;
            return 1
        }
        function fe(a, c, d, e, g, h, l, t) {
            var q, D = V;
            V += 24;
            var A = D >> 2;
            var f = D + 4;
            var k = f >> 2;
            d = D + 8 >> 2;
            var m = a + 268 | 0
              , u = wd(m)
              , z = b[a + 88 >> 2]
              , B = $a(z + 63 | 0);
            b[A] = 0;
            b[k] = 0;
            z = Bb(z + 17 | 0);
            var C = 0 == (z | 0);
            a: do
                if (!C) {
                    C = 0 == (t | 0);
                    var S = t - 1 | 0;
                    h = 0 == (h & 1 | 0);
                    var W = e << 1
                      , ea = a + 92 | 0
                      , X = a + 116 | 0;
                    g = 0 == (g & 1 | 0);
                    var P = a + 164 | 0
                      , Y = a + 212 | 0;
                    a = a + 284 | 0;
                    for (var R = l - 1 | 0, ma = R << 4, Fa = 0, za = 1; ; ) {
                        b: do
                            if (C)
                                var ra = za;
                            else {
                                ra = b[c + (Fa << 2) >> 2];
                                for (var Sa = 0, Ka = za; ; ) {
                                    if (0 == (Sa & 1 | 0)) {
                                        var Ga = ra;
                                        za = 16;
                                        var Ba = 1
                                          , La = l
                                          , ua = 0
                                    } else
                                        Ga = ra + ma | 0,
                                        za = -16,
                                        La = Ba = -1,
                                        ua = R;
                                    var va = h | (Sa | 0) != (S | 0)
                                      , Na = (ua | 0) == (La | 0);
                                    c: do
                                        if (Na)
                                            var wa = Ka;
                                        else
                                            for (wa = Ka; ; ) {
                                                Ka = 1 == (wa | 0) ? na(ea, X) | 512 : wa;
                                                wa = Ka & 7;
                                                Ka >>>= 3;
                                                var oa = Q[F.g + wa | 0] & 255;
                                                Na = g | (ua | 0) != (R | 0);
                                                var ka = 0;
                                                for (q = b[A]; ; ) {
                                                    var pa = na(ea, P);
                                                    b[A] = q + pa | 0;
                                                    Ma(D, u);
                                                    q = y[A];
                                                    pa = gb(m, q);
                                                    b[(ka << 2 >> 2) + d] = ya[pa >> 1] & 65535;
                                                    ka = ka + 1 | 0;
                                                    if (ka >>> 0 >= oa >>> 0) {
                                                        oa = Ga;
                                                        q = oa >> 2;
                                                        ka = 0;
                                                        break
                                                    }
                                                }
                                                for (; ; ) {
                                                    pa = oa;
                                                    var ia = 0 == (ka | 0) | va;
                                                    var qa = ka << 1;
                                                    var xa = na(ea, Y);
                                                    b[k] = b[k] + xa | 0;
                                                    Ma(f, B);
                                                    Na ? ia ? (xa = Q[(wa << 2) + kb + qa | 0] & 255,
                                                    ia = gb(a, 3 * b[k] | 0) >> 1,
                                                    b[pa >> 2] = (ya[ia] & 65535) << 16 | b[(xa << 2 >> 2) + d],
                                                    b[q + 1] = (ya[ia + 2] & 65535) << 16 | ya[ia + 1] & 65535,
                                                    pa = oa + 8 | 0,
                                                    ia = na(ea, Y),
                                                    b[k] = b[k] + ia | 0,
                                                    Ma(f, B),
                                                    ia = Q[(wa << 2) + kb + (qa | 1) | 0] & 255,
                                                    qa = gb(a, 3 * b[k] | 0) >> 1,
                                                    b[pa >> 2] = (ya[qa] & 65535) << 16 | b[(ia << 2 >> 2) + d],
                                                    b[q + 3] = (ya[qa + 2] & 65535) << 16 | ya[qa + 1] & 65535) : (q = na(ea, Y),
                                                    b[k] = b[k] + q | 0,
                                                    Ma(f, B)) : (ia ? (ia = Q[(wa << 2) + kb + qa | 0] & 255,
                                                    qa = gb(a, 3 * b[k] | 0) >> 1,
                                                    b[pa >> 2] = (ya[qa] & 65535) << 16 | b[(ia << 2 >> 2) + d],
                                                    b[q + 1] = (ya[qa + 2] & 65535) << 16 | ya[qa + 1] & 65535,
                                                    q = na(ea, Y),
                                                    b[k] = b[k] + q | 0) : (q = na(ea, Y),
                                                    b[k] = b[k] + q | 0),
                                                    Ma(f, B));
                                                    ka = ka + 1 | 0;
                                                    if (2 == (ka | 0))
                                                        break;
                                                    oa = oa + e | 0;
                                                    q = oa >> 2
                                                }
                                                ua = ua + Ba | 0;
                                                if ((ua | 0) == (La | 0)) {
                                                    wa = Ka;
                                                    break c
                                                }
                                                wa = Ka;
                                                Ga = Ga + za | 0
                                            }
                                    while (0);Sa = Sa + 1 | 0;
                                    if ((Sa | 0) == (t | 0)) {
                                        ra = wa;
                                        break b
                                    }
                                    ra = ra + W | 0;
                                    Ka = wa
                                }
                            }
                        while (0);Fa = Fa + 1 | 0;
                        if ((Fa | 0) == (z | 0))
                            break a;
                        za = ra
                    }
                }
            while (0);V = D;
            return 1
        }
        function ge(a, c, d, e, g, h, l, t) {
            var q = V;
            V += 48;
            var D = q >> 2;
            var A = q + 4;
            var f = A >> 2;
            var k = q + 8;
            var m = k >> 2;
            var u = q + 12;
            var z = u >> 2;
            var B = q + 16 >> 2;
            d = q + 32 >> 2;
            var C = a + 268 | 0
              , S = wd(C)
              , W = b[a + 88 >> 2]
              , ea = $a(W + 63 | 0);
            b[D] = 0;
            b[f] = 0;
            b[m] = 0;
            b[z] = 0;
            W = Bb(W + 17 | 0);
            var X = 0 == (W | 0);
            a: do
                if (!X) {
                    X = 0 == (t | 0);
                    var P = t - 1 | 0;
                    h = 0 == (h & 1 | 0);
                    var Y = e << 1
                      , R = a + 92 | 0
                      , ma = a + 116 | 0
                      , Fa = a + 212 | 0
                      , za = a + 284 | 0;
                    a = a + 164 | 0;
                    var ra = l - 1 | 0
                      , Sa = ra << 5;
                    g = 0 != (g & 1 | 0);
                    for (var Ka = 0, Ga = 1; ; ) {
                        b: do
                            if (X)
                                var Ba = Ga;
                            else {
                                Ba = b[c + (Ka << 2) >> 2];
                                for (var La = 0, ua = Ga; ; ) {
                                    if (0 == (La & 1 | 0)) {
                                        var va = Ba;
                                        Ga = 32;
                                        var Na = 1
                                          , wa = l
                                          , oa = 0
                                    } else
                                        va = Ba + Sa | 0,
                                        Ga = -32,
                                        wa = Na = -1,
                                        oa = ra;
                                    var ka = h | (La | 0) != (P | 0);
                                    var pa = (oa | 0) == (wa | 0);
                                    c: do
                                        if (pa)
                                            var ia = ua;
                                        else
                                            for (ia = ua; ; ) {
                                                ua = 1 == (ia | 0) ? na(R, ma) | 512 : ia;
                                                ia = ua & 7;
                                                ua >>>= 3;
                                                pa = Q[F.g + ia | 0] & 255;
                                                for (var qa = 0, xa = b[D]; ; ) {
                                                    var aa = na(R, a);
                                                    b[D] = xa + aa | 0;
                                                    Ma(q, S);
                                                    xa = y[D];
                                                    aa = gb(C, xa);
                                                    b[(qa << 2 >> 2) + B] = ya[aa >> 1] & 65535;
                                                    qa = qa + 1 | 0;
                                                    if (qa >>> 0 >= pa >>> 0)
                                                        break
                                                }
                                                qa = 0;
                                                for (xa = b[m]; !(aa = na(R, a),
                                                b[m] = xa + aa | 0,
                                                Ma(k, S),
                                                xa = y[m],
                                                aa = gb(C, xa),
                                                b[(qa << 2 >> 2) + d] = ya[aa >> 1] & 65535,
                                                qa = qa + 1 | 0,
                                                qa >>> 0 >= pa >>> 0); )
                                                    ;
                                                qa = (oa | 0) == (ra | 0) & g;
                                                xa = va;
                                                pa = xa >> 2;
                                                for (aa = 0; ; ) {
                                                    var fa = 0 == (aa | 0) | ka;
                                                    var sa = aa << 1;
                                                    var la = na(R, Fa);
                                                    b[f] = b[f] + la | 0;
                                                    Ma(A, ea);
                                                    la = na(R, Fa);
                                                    b[z] = b[z] + la | 0;
                                                    Ma(u, ea);
                                                    if (fa) {
                                                        var Ca = xa
                                                          , Ha = Q[(ia << 2) + kb + sa | 0] & 255;
                                                        var Ia = gb(za, 3 * b[f] | 0) >> 1;
                                                        la = gb(za, 3 * b[z] | 0) >> 1;
                                                        b[Ca >> 2] = (ya[Ia] & 65535) << 16 | b[(Ha << 2 >> 2) + B];
                                                        b[pa + 1] = (ya[Ia + 2] & 65535) << 16 | ya[Ia + 1] & 65535;
                                                        b[pa + 2] = (ya[la] & 65535) << 16 | b[(Ha << 2 >> 2) + d];
                                                        b[pa + 3] = (ya[la + 2] & 65535) << 16 | ya[la + 1] & 65535
                                                    }
                                                    la = na(R, Fa);
                                                    b[f] = b[f] + la | 0;
                                                    Ma(A, ea);
                                                    la = na(R, Fa);
                                                    b[z] = b[z] + la | 0;
                                                    Ma(u, ea);
                                                    qa | fa ^ 1 || (fa = xa + 16 | 0,
                                                    Ia = Q[(ia << 2) + kb + (sa | 1) | 0] & 255,
                                                    la = gb(za, 3 * b[f] | 0) >> 1,
                                                    sa = gb(za, 3 * b[z] | 0) >> 1,
                                                    b[fa >> 2] = (ya[la] & 65535) << 16 | b[(Ia << 2 >> 2) + B],
                                                    b[pa + 5] = (ya[la + 2] & 65535) << 16 | ya[la + 1] & 65535,
                                                    b[pa + 6] = (ya[sa] & 65535) << 16 | b[(Ia << 2 >> 2) + d],
                                                    b[pa + 7] = (ya[sa + 2] & 65535) << 16 | ya[sa + 1] & 65535);
                                                    aa = aa + 1 | 0;
                                                    if (2 == (aa | 0))
                                                        break;
                                                    xa = xa + e | 0;
                                                    pa = xa >> 2
                                                }
                                                oa = oa + Na | 0;
                                                if ((oa | 0) == (wa | 0)) {
                                                    ia = ua;
                                                    break c
                                                }
                                                ia = ua;
                                                va = va + Ga | 0
                                            }
                                    while (0);La = La + 1 | 0;
                                    if ((La | 0) == (t | 0)) {
                                        Ba = ia;
                                        break b
                                    }
                                    Ba = Ba + Y | 0;
                                    ua = ia
                                }
                            }
                        while (0);Ka = Ka + 1 | 0;
                        if ((Ka | 0) == (W | 0))
                            break a;
                        Ga = Ba
                    }
                }
            while (0);V = q;
            return 1
        }
        function gb(a, c) {
            y[a + 4 >> 2] >>> 0 <= c >>> 0 && ta(F.l | 0, F.a | 0, 968);
            return (c << 1) + b[a >> 2] | 0
        }
        function mb(a, c) {
            y[a + 4 >> 2] >>> 0 <= c >>> 0 && ta(F.l | 0, F.a | 0, 968);
            return (c << 2) + b[a >> 2] | 0
        }
        function Hf(a) {
            var c = a + 92 | 0
              , d = b[a + 4 >> 2];
            var e = (a + 88 | 0) >> 2;
            var g = b[e]
              , h = $b(g + 67 | 0);
            d = d + h | 0;
            g = $a(g + 65 | 0);
            g = Dc(c, d, g);
            do
                if (g)
                    if (Jb(c, a + 116 | 0)) {
                        d = b[e];
                        if (0 == ($a(d + 39 | 0) | 0)) {
                            if (0 == ($a(d + 55 | 0) | 0)) {
                                d = 0;
                                break
                            }
                        } else {
                            if (!Jb(c, a + 140 | 0)) {
                                d = 0;
                                break
                            }
                            if (!Jb(c, a + 188 | 0)) {
                                d = 0;
                                break
                            }
                            d = b[e]
                        }
                        if (0 != ($a(d + 55 | 0) | 0)) {
                            if (!Jb(c, a + 164 | 0)) {
                                d = 0;
                                break
                            }
                            if (!Jb(c, a + 212 | 0)) {
                                d = 0;
                                break
                            }
                        }
                        d = 1
                    } else
                        d = 0;
                else
                    d = 0;
            while (0);return d
        }
        function Bf(a) {
            var c = 1 < a >>> 0;
            a: do
                if (c)
                    for (c = 0; ; ) {
                        c = c + 1 | 0;
                        if (3 >= a >>> 0) {
                            var d = c;
                            break a
                        }
                        a >>>= 1
                    }
                else
                    d = 0;
            while (0);return d
        }
        function If(a) {
            var c = a + 88 | 0
              , d = b[c >> 2];
            if (0 == ($a(d + 39 | 0) | 0)) {
                g = d;
                var e = 5
            } else if (me(a))
                if (ne(a)) {
                    var g = b[c >> 2];
                    e = 5
                } else
                    h = 0,
                    e = 9;
            else {
                var h = 0;
                e = 9
            }
            do
                if (5 == e) {
                    if (0 != ($a(g + 55 | 0) | 0)) {
                        if (!oe(a)) {
                            h = 0;
                            break
                        }
                        if (!pe(a)) {
                            h = 0;
                            break
                        }
                    }
                    h = 1
                }
            while (0);return h
        }
        function qe(a) {
            Mb(a, 0, 64, 1)
        }
        function re(a, c) {
            var d = (a + 4 | 0) >> 2;
            var e = y[d]
              , g = (e | 0) == (c | 0);
            do
                if (g)
                    var h = 1;
                else {
                    if (e >>> 0 <= c >>> 0) {
                        if (y[a + 8 >> 2] >>> 0 < c >>> 0) {
                            if (!cg(a, c, (e + 1 | 0) == (c | 0))) {
                                h = 0;
                                break
                            }
                            h = b[d]
                        } else
                            h = e;
                        dg((h << 1) + b[a >> 2] | 0, c - h | 0)
                    }
                    b[d] = c;
                    h = 1
                }
            while (0);return h
        }
        function cg(a, c, d) {
            Va(a, c, d, 2, 0) ? a = 1 : (ba[a + 12 | 0] = 1,
            a = 0);
            return a
        }
        function dg(a, c) {
            Mb(a, 0, c << 1, 1)
        }
        function se(a, c) {
            var d = (a + 4 | 0) >> 2;
            var e = y[d]
              , g = (e | 0) == (c | 0);
            do
                if (g)
                    var h = 1;
                else {
                    if (e >>> 0 <= c >>> 0) {
                        if (y[a + 8 >> 2] >>> 0 < c >>> 0) {
                            if (!eg(a, c, (e + 1 | 0) == (c | 0))) {
                                h = 0;
                                break
                            }
                            h = b[d]
                        } else
                            h = e;
                        fg((h << 2) + b[a >> 2] | 0, c - h | 0)
                    }
                    b[d] = c;
                    h = 1
                }
            while (0);return h
        }
        function eg(a, c, d) {
            Va(a, c, d, 4, 0) ? a = 1 : (ba[a + 12 | 0] = 1,
            a = 0);
            return a
        }
        function fg(a, c) {
            Mb(a, 0, c << 2, 1)
        }
        function uf(a) {
            var c = a + 168 | 0
              , d = b[c >> 2];
            0 != (d | 0) && (Pb(d),
            b[c >> 2] = 0,
            b[a + 164 >> 2] = 0);
            c = a + 176 | 0;
            d = b[c >> 2];
            0 != (d | 0) && (Ob(d),
            b[c >> 2] = 0,
            b[a + 172 >> 2] = 0)
        }
        function me(a) {
            var c = V;
            V += 48;
            var d = a + 88 | 0
              , e = $a(b[d >> 2] + 39 | 0)
              , g = a + 236 | 0;
            if (se(g, e)) {
                var h = a + 92 | 0;
                a = b[a + 4 >> 2];
                d = b[d >> 2];
                var l = $b(d + 33 | 0);
                a = a + l | 0;
                d = $b(d + 36 | 0);
                if (Dc(h, a, d)) {
                    a = c | 0;
                    rb(a);
                    d = c + 24 | 0;
                    rb(d);
                    for (l = 0; ; ) {
                        if (2 <= l >>> 0) {
                            var t = 9;
                            break
                        }
                        if (!Jb(h, c + 24 * l | 0)) {
                            var q = 0;
                            t = 11;
                            break
                        }
                        l = l + 1 | 0
                    }
                    a: do
                        if (9 == t)
                            if (q = mb(g, 0),
                            0 == (e | 0))
                                q = 1;
                            else
                                for (var D = l = g = 0, A = 0, f = 0, k = 0, m = 0; ; ) {
                                    k = na(h, a) + k & 31;
                                    f = na(h, d) + f & 63;
                                    A = na(h, a) + A & 31;
                                    var u = na(h, a) + D | 0;
                                    D = u & 31;
                                    l = na(h, d) + l & 63;
                                    g = na(h, a) + g & 31;
                                    b[q >> 2] = f << 5 | k << 11 | A | u << 27 | l << 21 | g << 16;
                                    m = m + 1 | 0;
                                    if ((m | 0) == (e | 0)) {
                                        q = 1;
                                        break a
                                    }
                                    q = q + 4 | 0
                                }
                    while (0);sb(d);
                    sb(a);
                    e = q
                } else
                    e = 0
            } else
                e = 0;
            V = c;
            return e
        }
        function ne(a) {
            var c = V;
            V += 480;
            var d = c + 24
              , e = c + 220
              , g = c + 416
              , h = b[a + 88 >> 2]
              , l = $a(h + 47 | 0)
              , t = a + 92 | 0
              , q = b[a + 4 >> 2]
              , D = $b(h + 41 | 0);
            q = q + D | 0;
            h = $b(h + 44 | 0);
            if (Dc(t, q, h)) {
                rb(c);
                h = Jb(t, c);
                a: do
                    if (h) {
                        var A = -3;
                        q = -3;
                        for (D = 0; ; ) {
                            b[d + (D << 2) >> 2] = A;
                            b[e + (D << 2) >> 2] = q;
                            A = A + 1 | 0;
                            var f = 3 < (A | 0);
                            q = (f & 1) + q | 0;
                            D = D + 1 | 0;
                            if (49 == (D | 0))
                                break;
                            A = f ? -3 : A
                        }
                        qe(g);
                        q = a + 252 | 0;
                        if (se(q, l)) {
                            var k = mb(q, 0);
                            if (0 == (l | 0))
                                q = 1;
                            else {
                                a = g | 0;
                                h = g + 4 | 0;
                                q = g + 8 | 0;
                                D = g + 12 | 0;
                                A = g + 16 | 0;
                                f = g + 20 | 0;
                                for (var m = g + 24 | 0, u = g + 28 | 0, z = g + 32 | 0, B = g + 36 | 0, C = g + 40 | 0, S = g + 44 | 0, W = g + 48 | 0, ea = g + 52 | 0, X = g + 56 | 0, P = g + 60 | 0, Y = 0; ; ) {
                                    for (var R = 0; ; ) {
                                        var ma = na(t, c)
                                          , Fa = R << 1
                                          , za = (Fa << 2) + g | 0;
                                        b[za >> 2] = b[za >> 2] + b[d + (ma << 2) >> 2] & 3;
                                        Fa = ((Fa | 1) << 2) + g | 0;
                                        b[Fa >> 2] = b[Fa >> 2] + b[e + (ma << 2) >> 2] & 3;
                                        R = R + 1 | 0;
                                        if (8 == (R | 0))
                                            break
                                    }
                                    b[k >> 2] = (Q[F.c + b[h >> 2] | 0] & 255) << 2 | Q[F.c + b[a >> 2] | 0] & 255 | (Q[F.c + b[q >> 2] | 0] & 255) << 4 | (Q[F.c + b[D >> 2] | 0] & 255) << 6 | (Q[F.c + b[A >> 2] | 0] & 255) << 8 | (Q[F.c + b[f >> 2] | 0] & 255) << 10 | (Q[F.c + b[m >> 2] | 0] & 255) << 12 | (Q[F.c + b[u >> 2] | 0] & 255) << 14 | (Q[F.c + b[z >> 2] | 0] & 255) << 16 | (Q[F.c + b[B >> 2] | 0] & 255) << 18 | (Q[F.c + b[C >> 2] | 0] & 255) << 20 | (Q[F.c + b[S >> 2] | 0] & 255) << 22 | (Q[F.c + b[W >> 2] | 0] & 255) << 24 | (Q[F.c + b[ea >> 2] | 0] & 255) << 26 | (Q[F.c + b[X >> 2] | 0] & 255) << 28 | (Q[F.c + b[P >> 2] | 0] & 255) << 30;
                                    Y = Y + 1 | 0;
                                    if ((Y | 0) == (l | 0)) {
                                        q = 1;
                                        break a
                                    }
                                    k = k + 4 | 0
                                }
                            }
                        } else
                            q = 0
                    } else
                        q = 0;
                while (0);sb(c);
                d = q
            } else
                d = 0;
            V = c;
            return d
        }
        function oe(a) {
            var c = V;
            V += 24;
            var d = b[a + 88 >> 2]
              , e = $a(d + 55 | 0)
              , g = a + 92 | 0
              , h = b[a + 4 >> 2]
              , l = $b(d + 49 | 0);
            h = h + l | 0;
            d = $b(d + 52 | 0);
            if (Dc(g, h, d)) {
                rb(c);
                d = Jb(g, c);
                a: do
                    if (d)
                        if (h = a + 268 | 0,
                        re(h, e))
                            if (h = gb(h, 0),
                            0 == (e | 0))
                                h = 1;
                            else
                                for (a = h,
                                l = h = d = 0; ; ) {
                                    var t = na(g, c)
                                      , q = na(g, c);
                                    d = t + d & 255;
                                    h = q + h & 255;
                                    vb[a >> 1] = (h << 8 | d) & 65535;
                                    l = l + 1 | 0;
                                    if ((l | 0) == (e | 0)) {
                                        h = 1;
                                        break a
                                    }
                                    a = a + 2 | 0
                                }
                        else
                            h = 0;
                    else
                        h = 0;
                while (0);sb(c);
                e = h
            } else
                e = 0;
            V = c;
            return e
        }
        function pe(a) {
            var c = V;
            V += 1888;
            var d = c + 24
              , e = c + 924
              , g = c + 1824
              , h = b[a + 88 >> 2]
              , l = $a(h + 63 | 0)
              , t = a + 92 | 0
              , q = b[a + 4 >> 2]
              , D = $b(h + 57 | 0);
            q = q + D | 0;
            h = $b(h + 60 | 0);
            if (Dc(t, q, h)) {
                rb(c);
                h = Jb(t, c);
                a: do
                    if (h) {
                        var A = -7;
                        q = -7;
                        for (D = 0; ; ) {
                            b[d + (D << 2) >> 2] = A;
                            b[e + (D << 2) >> 2] = q;
                            A = A + 1 | 0;
                            var f = 7 < (A | 0);
                            q = (f & 1) + q | 0;
                            D = D + 1 | 0;
                            if (225 == (D | 0))
                                break;
                            A = f ? -7 : A
                        }
                        qe(g);
                        q = a + 284 | 0;
                        if (re(q, 3 * l | 0)) {
                            var k = gb(q, 0);
                            if (0 == (l | 0))
                                q = 1;
                            else {
                                a = g | 0;
                                h = g + 4 | 0;
                                q = g + 8 | 0;
                                D = g + 12 | 0;
                                A = g + 16 | 0;
                                f = g + 20 | 0;
                                var m = g + 24 | 0
                                  , u = g + 28 | 0
                                  , z = g + 32 | 0
                                  , B = g + 36 | 0
                                  , C = g + 40 | 0
                                  , S = g + 44 | 0
                                  , W = g + 48 | 0
                                  , ea = g + 52 | 0
                                  , X = g + 56 | 0
                                  , P = g + 60 | 0
                                  , Y = k;
                                k = Y >> 1;
                                for (var R = 0; ; ) {
                                    for (var ma = 0; ; ) {
                                        var Fa = na(t, c)
                                          , za = ma << 1
                                          , ra = (za << 2) + g | 0;
                                        b[ra >> 2] = b[ra >> 2] + b[d + (Fa << 2) >> 2] & 7;
                                        za = ((za | 1) << 2) + g | 0;
                                        b[za >> 2] = b[za >> 2] + b[e + (Fa << 2) >> 2] & 7;
                                        ma = ma + 1 | 0;
                                        if (8 == (ma | 0))
                                            break
                                    }
                                    vb[k] = (Q[F.b + b[h >> 2] | 0] & 255) << 3 | Q[F.b + b[a >> 2] | 0] & 255 | (Q[F.b + b[q >> 2] | 0] & 255) << 6 | (Q[F.b + b[D >> 2] | 0] & 255) << 9 | (Q[F.b + b[A >> 2] | 0] & 255) << 12 | (Q[F.b + b[f >> 2] | 0] & 255) << 15;
                                    vb[k + 1] = (Q[F.b + b[m >> 2] | 0] & 255) << 2 | (Q[F.b + b[f >> 2] | 0] & 255) >>> 1 | (Q[F.b + b[u >> 2] | 0] & 255) << 5 | (Q[F.b + b[z >> 2] | 0] & 255) << 8 | (Q[F.b + b[B >> 2] | 0] & 255) << 11 | (Q[F.b + b[C >> 2] | 0] & 255) << 14;
                                    vb[k + 2] = (Q[F.b + b[S >> 2] | 0] & 255) << 1 | (Q[F.b + b[C >> 2] | 0] & 255) >>> 2 | (Q[F.b + b[W >> 2] | 0] & 255) << 4 | (Q[F.b + b[ea >> 2] | 0] & 255) << 7 | (Q[F.b + b[X >> 2] | 0] & 255) << 10 | (Q[F.b + b[P >> 2] | 0] & 255) << 13;
                                    R = R + 1 | 0;
                                    if ((R | 0) == (l | 0)) {
                                        q = 1;
                                        break a
                                    }
                                    Y = Y + 6 | 0;
                                    k = Y >> 1
                                }
                            }
                        } else
                            q = 0
                    } else
                        q = 0;
                while (0);sb(c);
                d = q
            } else
                d = 0;
            V = c;
            return d
        }
        function zc(a) {
            var c = 245 > a >>> 0;
            do {
                if (c) {
                    var d = 11 > a >>> 0 ? 16 : a + 11 & -8
                      , e = d >>> 3
                      , g = y[v >> 2]
                      , h = g >>> (e >>> 0);
                    if (0 != (h & 3 | 0)) {
                        a = (h & 1 ^ 1) + e | 0;
                        d = a << 1;
                        c = (d << 2) + v + 40 | 0;
                        e = (d + 2 << 2) + v + 40 | 0;
                        var l = y[e >> 2];
                        d = l + 8 | 0;
                        h = y[d >> 2];
                        if ((c | 0) == (h | 0))
                            b[v >> 2] = g & (1 << a ^ -1);
                        else {
                            if (h >>> 0 < y[v + 16 >> 2] >>> 0)
                                throw ha(),
                                "Reached an unreachable!";
                            b[e >> 2] = h;
                            b[h + 12 >> 2] = c
                        }
                        g = a << 3;
                        b[l + 4 >> 2] = g | 3;
                        g = l + (g | 4) | 0;
                        b[g >> 2] |= 1;
                        l = d;
                        var t = 38;
                        break
                    }
                    if (d >>> 0 <= y[v + 8 >> 2] >>> 0) {
                        var q = d;
                        t = 30;
                        break
                    }
                    if (0 != (h | 0)) {
                        a = 2 << e;
                        a = h << e & (a | -a);
                        c = (a & -a) - 1 | 0;
                        a = c >>> 12 & 16;
                        l = c >>> (a >>> 0);
                        c = l >>> 5 & 8;
                        e = l >>> (c >>> 0);
                        l = e >>> 2 & 4;
                        h = e >>> (l >>> 0);
                        e = h >>> 1 & 2;
                        h >>>= e >>> 0;
                        var D = h >>> 1 & 1;
                        l = (c | a | l | e | D) + (h >>> (D >>> 0)) | 0;
                        a = l << 1;
                        e = (a << 2) + v + 40 | 0;
                        h = (a + 2 << 2) + v + 40 | 0;
                        c = y[h >> 2];
                        a = c + 8 | 0;
                        D = y[a >> 2];
                        if ((e | 0) == (D | 0))
                            b[v >> 2] = g & (1 << l ^ -1);
                        else {
                            if (D >>> 0 < y[v + 16 >> 2] >>> 0)
                                throw ha(),
                                "Reached an unreachable!";
                            b[h >> 2] = D;
                            b[D + 12 >> 2] = e
                        }
                        l <<= 3;
                        g = l - d | 0;
                        b[c + 4 >> 2] = d | 3;
                        e = c;
                        c = e + d | 0;
                        b[e + (d | 4) >> 2] = g | 1;
                        b[e + l >> 2] = g;
                        D = y[v + 8 >> 2];
                        if (0 != (D | 0)) {
                            d = b[v + 20 >> 2];
                            e = D >>> 2 & 1073741822;
                            l = (e << 2) + v + 40 | 0;
                            h = y[v >> 2];
                            D = 1 << (D >>> 3);
                            if (0 == (h & D | 0))
                                b[v >> 2] = h | D,
                                h = l,
                                e = (e + 2 << 2) + v + 40 | 0;
                            else if (e = (e + 2 << 2) + v + 40 | 0,
                            h = y[e >> 2],
                            !(h >>> 0 >= y[v + 16 >> 2] >>> 0))
                                throw ha(),
                                "Reached an unreachable!";
                            b[e >> 2] = d;
                            b[h + 12 >> 2] = d;
                            b[(d + 8 | 0) >> 2] = h;
                            b[(d + 12 | 0) >> 2] = l
                        }
                        b[v + 8 >> 2] = g;
                        b[v + 20 >> 2] = c;
                        l = a;
                        t = 38;
                        break
                    }
                    if (0 == (b[v + 4 >> 2] | 0)) {
                        q = d;
                        t = 30;
                        break
                    }
                    g = te(d);
                    if (0 == (g | 0)) {
                        q = d;
                        t = 30;
                        break
                    }
                    l = g
                } else {
                    if (4294967231 < a >>> 0) {
                        q = -1;
                        t = 30;
                        break
                    }
                    g = a + 11 & -8;
                    if (0 == (b[v + 4 >> 2] | 0)) {
                        q = g;
                        t = 30;
                        break
                    }
                    d = ue(g);
                    if (0 == (d | 0)) {
                        q = g;
                        t = 30;
                        break
                    }
                    l = d
                }
                t = 38
            } while (0);30 == t && (d = y[v + 8 >> 2],
            q >>> 0 > d >>> 0 ? (g = y[v + 12 >> 2],
            q >>> 0 < g >>> 0 ? (g = g - q | 0,
            b[v + 12 >> 2] = g,
            d = y[v + 24 >> 2],
            b[v + 24 >> 2] = d + q | 0,
            b[q + (d + 4) >> 2] = g | 1,
            b[d + 4 >> 2] = q | 3,
            l = d + 8 | 0) : l = ve(q)) : (a = d - q | 0,
            g = y[v + 20 >> 2],
            15 < a >>> 0 ? (b[v + 20 >> 2] = g + q | 0,
            b[v + 8 >> 2] = a,
            b[q + (g + 4) >> 2] = a | 1,
            b[g + d >> 2] = a,
            b[g + 4 >> 2] = q | 3) : (b[v + 8 >> 2] = 0,
            b[v + 20 >> 2] = 0,
            b[g + 4 >> 2] = d | 3,
            q = d + (g + 4) | 0,
            b[q >> 2] |= 1),
            l = g + 8 | 0));
            return l
        }
        function te(a) {
            var c = b[v + 4 >> 2]
              , d = (c & -c) - 1 | 0;
            c = d >>> 12 & 16;
            var e = d >>> (c >>> 0);
            d = e >>> 5 & 8;
            var g = e >>> (d >>> 0);
            e = g >>> 2 & 4;
            var h = g >>> (e >>> 0);
            g = h >>> 1 & 2;
            h >>>= g >>> 0;
            var l = h >>> 1 & 1;
            c = d = y[v + ((d | c | e | g | l) + (h >>> (l >>> 0)) << 2) + 304 >> 2];
            g = c >> 2;
            d = (b[d + 4 >> 2] & -8) - a | 0;
            a: for (; ; )
                for (e = c; ; ) {
                    h = b[e + 16 >> 2];
                    if (0 == (h | 0)) {
                        if (e = b[e + 20 >> 2],
                        0 == (e | 0))
                            break a
                    } else
                        e = h;
                    h = (b[e + 4 >> 2] & -8) - a | 0;
                    if (h >>> 0 < d >>> 0) {
                        c = e;
                        g = c >> 2;
                        d = h;
                        continue a
                    }
                }
            h = c;
            var t = y[v + 16 >> 2];
            if (!(h >>> 0 < t >>> 0 || (e = h + a | 0,
            h >>> 0 >= e >>> 0))) {
                l = y[g + 6];
                var q = y[g + 3]
                  , D = (q | 0) == (c | 0);
                do {
                    if (D) {
                        var A = c + 20 | 0;
                        var f = b[A >> 2];
                        if (0 == (f | 0) && (A = c + 16 | 0,
                        f = b[A >> 2],
                        0 == (f | 0))) {
                            f = 0;
                            A = f >> 2;
                            break
                        }
                        for (; ; ) {
                            var k = f + 20 | 0
                              , m = b[k >> 2];
                            if (0 != (m | 0))
                                A = k,
                                f = m;
                            else {
                                k = f + 16 | 0;
                                m = y[k >> 2];
                                if (0 == (m | 0))
                                    break;
                                A = k;
                                f = m
                            }
                        }
                        if (A >>> 0 < t >>> 0)
                            throw ha(),
                            "Reached an unreachable!";
                        b[A >> 2] = 0
                    } else {
                        A = y[g + 2];
                        if (A >>> 0 < t >>> 0)
                            throw ha(),
                            "Reached an unreachable!";
                        b[A + 12 >> 2] = q;
                        b[q + 8 >> 2] = A;
                        f = q
                    }
                    A = f >> 2
                } while (0);t = 0 == (l | 0);
                a: do
                    if (!t) {
                        q = c + 28 | 0;
                        D = (b[q >> 2] << 2) + v + 304 | 0;
                        k = (c | 0) == (b[D >> 2] | 0);
                        do {
                            if (k) {
                                b[D >> 2] = f;
                                if (0 != (f | 0))
                                    break;
                                b[v + 4 >> 2] &= 1 << b[q >> 2] ^ -1;
                                break a
                            }
                            if (l >>> 0 < y[v + 16 >> 2] >>> 0)
                                throw ha(),
                                "Reached an unreachable!";
                            m = l + 16 | 0;
                            (b[m >> 2] | 0) == (c | 0) ? b[m >> 2] = f : b[l + 20 >> 2] = f;
                            if (0 == (f | 0))
                                break a
                        } while (0);if (f >>> 0 < y[v + 16 >> 2] >>> 0)
                            throw ha(),
                            "Reached an unreachable!";
                        b[A + 6] = l;
                        q = y[g + 4];
                        if (0 != (q | 0)) {
                            if (q >>> 0 < y[v + 16 >> 2] >>> 0)
                                throw ha(),
                                "Reached an unreachable!";
                            b[A + 4] = q;
                            b[q + 24 >> 2] = f
                        }
                        q = y[g + 5];
                        if (0 != (q | 0)) {
                            if (q >>> 0 < y[v + 16 >> 2] >>> 0)
                                throw ha(),
                                "Reached an unreachable!";
                            b[A + 5] = q;
                            b[q + 24 >> 2] = f
                        }
                    }
                while (0);if (16 > d >>> 0)
                    a = d + a | 0,
                    b[g + 1] = a | 3,
                    a = a + (h + 4) | 0,
                    b[a >> 2] |= 1;
                else {
                    b[g + 1] = a | 3;
                    b[a + (h + 4) >> 2] = d | 1;
                    b[h + d + a >> 2] = d;
                    t = y[v + 8 >> 2];
                    if (0 != (t | 0)) {
                        a = y[v + 20 >> 2];
                        h = t >>> 2 & 1073741822;
                        g = (h << 2) + v + 40 | 0;
                        l = y[v >> 2];
                        t = 1 << (t >>> 3);
                        if (0 == (l & t | 0))
                            b[v >> 2] = l | t,
                            l = g,
                            h = (h + 2 << 2) + v + 40 | 0;
                        else if (h = (h + 2 << 2) + v + 40 | 0,
                        l = y[h >> 2],
                        !(l >>> 0 >= y[v + 16 >> 2] >>> 0))
                            throw ha(),
                            "Reached an unreachable!";
                        b[h >> 2] = a;
                        b[l + 12 >> 2] = a;
                        b[a + 8 >> 2] = l;
                        b[a + 12 >> 2] = g
                    }
                    b[v + 8 >> 2] = d;
                    b[v + 20 >> 2] = e
                }
                return c + 8 | 0
            }
            ha();
            throw "Reached an unreachable!";
        }
        function ve(a) {
            0 == (b[ab >> 2] | 0) && we();
            var c = 0 == (b[v + 440 >> 2] & 4 | 0);
            do
                if (c) {
                    var d = b[v + 24 >> 2];
                    if (0 == (d | 0))
                        var e = 6;
                    else if (d = xd(d),
                    0 == (d | 0))
                        e = 6;
                    else {
                        var g = b[ab + 8 >> 2];
                        g = a + 47 - b[v + 12 >> 2] + g & -g;
                        if (2147483647 <= g >>> 0)
                            e = 14;
                        else {
                            var h = Cb(g);
                            if ((h | 0) == (b[d >> 2] + b[d + 4 >> 2] | 0)) {
                                var l = h
                                  , t = g;
                                var q = h;
                                e = 13
                            } else {
                                var D = h
                                  , A = g;
                                e = 15
                            }
                        }
                    }
                    if (6 == e)
                        if (d = Cb(0),
                        -1 == (d | 0))
                            e = 14;
                        else {
                            g = b[ab + 8 >> 2];
                            g = g + (a + 47) & -g;
                            h = d;
                            var f = b[ab + 4 >> 2]
                              , k = f - 1 | 0;
                            g = 0 == (k & h | 0) ? g : g - h + (k + h & -f) | 0;
                            2147483647 <= g >>> 0 ? e = 14 : (h = Cb(g),
                            (h | 0) == (d | 0) ? (l = d,
                            t = g,
                            q = h,
                            e = 13) : (D = h,
                            A = g,
                            e = 15))
                        }
                    if (13 == e) {
                        if (-1 != (l | 0)) {
                            var m = t
                              , u = l;
                            e = 26;
                            break
                        }
                        D = q;
                        A = t
                    } else if (14 == e) {
                        b[v + 440 >> 2] |= 4;
                        e = 23;
                        break
                    }
                    d = -A | 0;
                    if (-1 != (D | 0) & 2147483647 > A >>> 0)
                        if (A >>> 0 >= (a + 48 | 0) >>> 0) {
                            var z = A;
                            e = 21
                        } else
                            g = b[ab + 8 >> 2],
                            g = a + 47 - A + g & -g,
                            2147483647 <= g >>> 0 ? (z = A,
                            e = 21) : -1 == (Cb(g) | 0) ? (Cb(d),
                            e = 22) : (z = g + A | 0,
                            e = 21);
                    else
                        z = A,
                        e = 21;
                    21 == e && -1 != (D | 0) ? (m = z,
                    u = D,
                    e = 26) : (b[v + 440 >> 2] |= 4,
                    e = 23)
                } else
                    e = 23;
            while (0);23 == e && (c = b[ab + 8 >> 2],
            c = c + (a + 47) & -c,
            2147483647 <= c >>> 0 ? e = 49 : (c = Cb(c),
            l = Cb(0),
            -1 != (l | 0) & -1 != (c | 0) & c >>> 0 < l >>> 0 ? (l = l - c | 0,
            l >>> 0 <= (a + 40 | 0) >>> 0 | -1 == (c | 0) ? e = 49 : (m = l,
            u = c,
            e = 26)) : e = 49));
            a: do
                if (26 == e) {
                    c = b[v + 432 >> 2] + m | 0;
                    b[v + 432 >> 2] = c;
                    c >>> 0 > y[v + 436 >> 2] >>> 0 && (b[v + 436 >> 2] = c);
                    c = y[v + 24 >> 2];
                    l = 0 == (c | 0);
                    b: do
                        if (l)
                            t = y[v + 16 >> 2],
                            0 == (t | 0) | u >>> 0 < t >>> 0 && (b[v + 16 >> 2] = u),
                            b[v + 444 >> 2] = u,
                            b[v + 448 >> 2] = m,
                            b[v + 456 >> 2] = 0,
                            b[v + 36 >> 2] = b[ab >> 2],
                            b[v + 32 >> 2] = -1,
                            gg(),
                            ed(u, m - 40 | 0);
                        else {
                            D = v + 444 | 0;
                            for (q = D >> 2; 0 != (D | 0); ) {
                                t = y[q];
                                D = D + 4 | 0;
                                A = y[D >> 2];
                                z = t + A | 0;
                                if ((u | 0) == (z | 0)) {
                                    if (0 != (b[q + 3] & 8 | 0))
                                        break;
                                    q = c;
                                    if (!(q >>> 0 >= t >>> 0 & q >>> 0 < z >>> 0))
                                        break;
                                    b[D >> 2] = A + m | 0;
                                    ed(b[v + 24 >> 2], b[v + 12 >> 2] + m | 0);
                                    break b
                                }
                                D = b[q + 2];
                                q = D >> 2
                            }
                            u >>> 0 < y[v + 16 >> 2] >>> 0 && (b[v + 16 >> 2] = u);
                            q = u + m | 0;
                            for (D = v + 444 | 0; 0 != (D | 0); ) {
                                A = D | 0;
                                t = y[A >> 2];
                                if ((t | 0) == (q | 0)) {
                                    if (0 != (b[D + 12 >> 2] & 8 | 0))
                                        break;
                                    b[A >> 2] = u;
                                    var B = D + 4 | 0;
                                    b[B >> 2] = b[B >> 2] + m | 0;
                                    B = xe(u, t, a);
                                    e = 50;
                                    break a
                                }
                                D = b[D + 8 >> 2]
                            }
                            ye(u, m)
                        }
                    while (0);c = y[v + 12 >> 2];
                    c >>> 0 <= a >>> 0 ? e = 49 : (B = c - a | 0,
                    b[v + 12 >> 2] = B,
                    l = c = y[v + 24 >> 2],
                    b[v + 24 >> 2] = l + a | 0,
                    b[a + (l + 4) >> 2] = B | 1,
                    b[c + 4 >> 2] = a | 3,
                    B = c + 8 | 0,
                    e = 50)
                }
            while (0);49 == e && (a = n(),
            b[a >> 2] = 12,
            B = 0);
            return B
        }
        function ue(a) {
            var c = a >> 2
              , d = -a | 0
              , e = a >>> 8;
            if (0 == (e | 0))
                var g = 0;
            else if (16777215 < a >>> 0)
                g = 31;
            else {
                var h = (e + 1048320 | 0) >>> 16 & 8
                  , l = e << h
                  , t = (l + 520192 | 0) >>> 16 & 4
                  , q = l << t
                  , D = (q + 245760 | 0) >>> 16 & 2
                  , A = 14 - (t | h | D) + (q << D >>> 15) | 0;
                g = a >>> ((A + 7 | 0) >>> 0) & 1 | A << 1
            }
            var f = y[v + (g << 2) + 304 >> 2]
              , k = 0 == (f | 0);
            a: do
                if (k)
                    var m = 0
                      , u = d
                      , z = 0;
                else {
                    var B = 31 == (g | 0) ? 0 : 25 - (g >>> 1) | 0
                      , C = 0
                      , S = d
                      , W = f;
                    var ea = W >> 2;
                    for (var X = a << B, P = 0; ; ) {
                        var Y = b[ea + 1] & -8
                          , R = Y - a | 0;
                        if (R >>> 0 < S >>> 0) {
                            if ((Y | 0) == (a | 0)) {
                                m = W;
                                u = R;
                                z = W;
                                break a
                            }
                            var ma = W
                              , Fa = R
                        } else
                            ma = C,
                            Fa = S;
                        var za = y[ea + 5]
                          , ra = y[((X >>> 31 << 2) + 16 >> 2) + ea]
                          , Sa = 0 == (za | 0) | (za | 0) == (ra | 0) ? P : za;
                        if (0 == (ra | 0)) {
                            m = ma;
                            u = Fa;
                            z = Sa;
                            break a
                        }
                        C = ma;
                        S = Fa;
                        W = ra;
                        ea = W >> 2;
                        X <<= 1;
                        P = Sa
                    }
                }
            while (0);if (0 == (z | 0) & 0 == (m | 0)) {
                var Ka = 2 << g
                  , Ga = b[v + 4 >> 2] & (Ka | -Ka);
                if (0 == (Ga | 0))
                    var Ba = z;
                else {
                    var La = (Ga & -Ga) - 1 | 0
                      , ua = La >>> 12 & 16
                      , va = La >>> (ua >>> 0)
                      , Na = va >>> 5 & 8
                      , wa = va >>> (Na >>> 0)
                      , oa = wa >>> 2 & 4
                      , ka = wa >>> (oa >>> 0)
                      , pa = ka >>> 1 & 2
                      , ia = ka >>> (pa >>> 0)
                      , qa = ia >>> 1 & 1;
                    Ba = b[v + ((Na | ua | oa | pa | qa) + (ia >>> (qa >>> 0)) << 2) + 304 >> 2]
                }
            } else
                Ba = z;
            var xa = 0 == (Ba | 0);
            a: do
                if (xa) {
                    var aa = u
                      , fa = m;
                    var sa = fa >> 2
                } else {
                    var la = Ba;
                    var Ca = la >> 2;
                    for (var Ha = u, Ia = m; ; ) {
                        var Ya = (b[Ca + 1] & -8) - a | 0
                          , bb = Ya >>> 0 < Ha >>> 0
                          , Ja = bb ? Ya : Ha
                          , wb = bb ? la : Ia
                          , hb = y[Ca + 4];
                        if (0 != (hb | 0))
                            la = hb;
                        else {
                            var ob = y[Ca + 5];
                            if (0 == (ob | 0)) {
                                aa = Ja;
                                fa = wb;
                                sa = fa >> 2;
                                break a
                            }
                            la = ob
                        }
                        Ca = la >> 2;
                        Ha = Ja;
                        Ia = wb
                    }
                }
            while (0);var Ac = 0 == (fa | 0);
            a: do
                if (Ac)
                    var Qb = 0;
                else if (aa >>> 0 >= (b[v + 8 >> 2] - a | 0) >>> 0)
                    Qb = 0;
                else {
                    var Wa = fa;
                    var Pa = Wa >> 2;
                    var Rb = y[v + 16 >> 2];
                    if (!(Wa >>> 0 < Rb >>> 0)) {
                        var Sb = Wa + a | 0
                          , xb = Sb;
                        if (!(Wa >>> 0 >= Sb >>> 0)) {
                            var ib = y[sa + 6]
                              , Tb = y[sa + 3]
                              , Bc = (Tb | 0) == (fa | 0);
                            do {
                                if (Bc) {
                                    var sc = fa + 20 | 0
                                      , Gb = b[sc >> 2];
                                    if (0 == (Gb | 0)) {
                                        var ec = fa + 16 | 0
                                          , cb = b[ec >> 2];
                                        if (0 == (cb | 0)) {
                                            var Za = 0;
                                            var jb = Za >> 2;
                                            break
                                        }
                                        var eb = ec
                                          , pb = cb
                                    } else
                                        eb = sc,
                                        pb = Gb;
                                    for (; ; ) {
                                        var fc = pb + 20 | 0
                                          , gc = b[fc >> 2];
                                        if (0 != (gc | 0))
                                            eb = fc,
                                            pb = gc;
                                        else {
                                            var hc = pb + 16 | 0
                                              , Ub = y[hc >> 2];
                                            if (0 == (Ub | 0))
                                                break;
                                            eb = hc;
                                            pb = Ub
                                        }
                                    }
                                    if (eb >>> 0 < Rb >>> 0)
                                        throw ha(),
                                        "Reached an unreachable!";
                                    b[eb >> 2] = 0;
                                    Za = pb
                                } else {
                                    var Vb = y[sa + 2];
                                    if (Vb >>> 0 < Rb >>> 0)
                                        throw ha(),
                                        "Reached an unreachable!";
                                    b[Vb + 12 >> 2] = Tb;
                                    b[Tb + 8 >> 2] = Vb;
                                    Za = Tb
                                }
                                jb = Za >> 2
                            } while (0);var tc = 0 == (ib | 0);
                            b: do
                                if (!tc) {
                                    var uc = fa + 28 | 0
                                      , ic = (b[uc >> 2] << 2) + v + 304 | 0
                                      , Wb = (fa | 0) == (b[ic >> 2] | 0);
                                    do {
                                        if (Wb) {
                                            b[ic >> 2] = Za;
                                            if (0 != (Za | 0))
                                                break;
                                            b[v + 4 >> 2] &= 1 << b[uc >> 2] ^ -1;
                                            break b
                                        }
                                        if (ib >>> 0 < y[v + 16 >> 2] >>> 0)
                                            throw ha(),
                                            "Reached an unreachable!";
                                        var Hb = ib + 16 | 0;
                                        (b[Hb >> 2] | 0) == (fa | 0) ? b[Hb >> 2] = Za : b[ib + 20 >> 2] = Za;
                                        if (0 == (Za | 0))
                                            break b
                                    } while (0);if (Za >>> 0 < y[v + 16 >> 2] >>> 0)
                                        throw ha(),
                                        "Reached an unreachable!";
                                    b[jb + 6] = ib;
                                    var db = y[sa + 4];
                                    if (0 != (db | 0)) {
                                        if (db >>> 0 < y[v + 16 >> 2] >>> 0)
                                            throw ha(),
                                            "Reached an unreachable!";
                                        b[jb + 4] = db;
                                        b[db + 24 >> 2] = Za
                                    }
                                    var yb = y[sa + 5];
                                    if (0 != (yb | 0)) {
                                        if (yb >>> 0 < y[v + 16 >> 2] >>> 0)
                                            throw ha(),
                                            "Reached an unreachable!";
                                        b[jb + 5] = yb;
                                        b[yb + 24 >> 2] = Za
                                    }
                                }
                            while (0);var vc = 16 > aa >>> 0;
                            b: do
                                if (vc) {
                                    var jc = aa + a | 0;
                                    b[sa + 1] = jc | 3;
                                    var kc = jc + (Wa + 4) | 0;
                                    b[kc >> 2] |= 1
                                } else if (b[sa + 1] = a | 3,
                                b[c + (Pa + 1)] = aa | 1,
                                b[(aa >> 2) + Pa + c] = aa,
                                256 > aa >>> 0) {
                                    var Ib = aa >>> 2 & 1073741822
                                      , lc = (Ib << 2) + v + 40 | 0
                                      , mc = y[v >> 2]
                                      , nc = 1 << (aa >>> 3);
                                    if (0 == (mc & nc | 0)) {
                                        b[v >> 2] = mc | nc;
                                        var zb = lc
                                          , Xb = (Ib + 2 << 2) + v + 40 | 0
                                    } else {
                                        var lb = (Ib + 2 << 2) + v + 40 | 0
                                          , Yb = y[lb >> 2];
                                        if (Yb >>> 0 >= y[v + 16 >> 2] >>> 0)
                                            zb = Yb,
                                            Xb = lb;
                                        else
                                            throw ha(),
                                            "Reached an unreachable!";
                                    }
                                    b[Xb >> 2] = xb;
                                    b[zb + 12 >> 2] = xb;
                                    b[c + (Pa + 2)] = zb;
                                    b[c + (Pa + 3)] = lc
                                } else {
                                    var fb = Sb
                                      , Zb = aa >>> 8;
                                    if (0 == (Zb | 0))
                                        var qb = 0;
                                    else if (16777215 < aa >>> 0)
                                        qb = 31;
                                    else {
                                        var Ab = (Zb + 1048320 | 0) >>> 16 & 8
                                          , Qc = Zb << Ab
                                          , Fc = (Qc + 520192 | 0) >>> 16 & 4
                                          , Rc = Qc << Fc
                                          , Sc = (Rc + 245760 | 0) >>> 16 & 2
                                          , fd = 14 - (Fc | Ab | Sc) + (Rc << Sc >>> 15) | 0;
                                        qb = aa >>> ((fd + 7 | 0) >>> 0) & 1 | fd << 1
                                    }
                                    var Gc = (qb << 2) + v + 304 | 0;
                                    b[c + (Pa + 7)] = qb;
                                    var ac = a + (Wa + 16) | 0;
                                    b[c + (Pa + 5)] = 0;
                                    b[ac >> 2] = 0;
                                    var Tc = b[v + 4 >> 2]
                                      , Hc = 1 << qb;
                                    if (0 == (Tc & Hc | 0))
                                        b[v + 4 >> 2] = Tc | Hc,
                                        b[Gc >> 2] = fb,
                                        b[c + (Pa + 6)] = Gc,
                                        b[c + (Pa + 3)] = fb,
                                        b[c + (Pa + 2)] = fb;
                                    else
                                        for (var Uc = aa << (31 == (qb | 0) ? 0 : 25 - (qb >>> 1) | 0), Db = b[Gc >> 2]; ; ) {
                                            if ((b[Db + 4 >> 2] & -8 | 0) == (aa | 0)) {
                                                var Vc = Db + 8 | 0
                                                  , Ic = y[Vc >> 2]
                                                  , ze = y[v + 16 >> 2];
                                                if (!(Db >>> 0 < ze >>> 0 || Ic >>> 0 < ze >>> 0)) {
                                                    b[Ic + 12 >> 2] = fb;
                                                    b[Vc >> 2] = fb;
                                                    b[c + (Pa + 2)] = Ic;
                                                    b[c + (Pa + 3)] = Db;
                                                    b[c + (Pa + 6)] = 0;
                                                    break b
                                                }
                                                ha();
                                                throw "Reached an unreachable!";
                                            }
                                            var yd = (Uc >>> 31 << 2) + Db + 16 | 0
                                              , Ae = y[yd >> 2];
                                            if (0 == (Ae | 0)) {
                                                if (yd >>> 0 >= y[v + 16 >> 2] >>> 0) {
                                                    b[yd >> 2] = fb;
                                                    b[c + (Pa + 6)] = Db;
                                                    b[c + (Pa + 3)] = fb;
                                                    b[c + (Pa + 2)] = fb;
                                                    break b
                                                }
                                                ha();
                                                throw "Reached an unreachable!";
                                            }
                                            Uc <<= 1;
                                            Db = Ae
                                        }
                                }
                            while (0);Qb = fa + 8 | 0;
                            break a
                        }
                    }
                    ha();
                    throw "Reached an unreachable!";
                }
            while (0);return Qb
        }
        function Be(a) {
            0 == (b[ab >> 2] | 0) && we();
            var c = 4294967232 > a >>> 0;
            a: do {
                if (c) {
                    var d = y[v + 24 >> 2];
                    if (0 == (d | 0)) {
                        d = 0;
                        break
                    }
                    var e = y[v + 12 >> 2];
                    if (e >>> 0 > (a + 40 | 0) >>> 0) {
                        var g = y[ab + 8 >> 2]
                          , h = (Math.floor(((-40 - a - 1 + e + g | 0) >>> 0) / (g >>> 0)) - 1) * g | 0
                          , l = xd(d);
                        if (0 == (b[l + 12 >> 2] & 8 | 0) && (e = Cb(0),
                        d = (l + 4 | 0) >> 2,
                        (e | 0) == (b[l >> 2] + b[d] | 0) && (h = Cb(-(2147483646 < h >>> 0 ? -2147483648 - g | 0 : h) | 0),
                        g = Cb(0),
                        -1 != (h | 0) & g >>> 0 < e >>> 0 && (h = e - g | 0,
                        (e | 0) != (g | 0))))) {
                            b[d] = b[d] - h | 0;
                            b[v + 432 >> 2] = b[v + 432 >> 2] - h | 0;
                            ed(b[v + 24 >> 2], b[v + 12 >> 2] - h | 0);
                            d = (e | 0) != (g | 0);
                            break a
                        }
                    }
                    if (y[v + 12 >> 2] >>> 0 <= y[v + 28 >> 2] >>> 0) {
                        d = 0;
                        break
                    }
                    b[v + 28 >> 2] = -1
                }
                d = 0
            } while (0);return d & 1
        }
        function Jc(a) {
            var c = a >> 2
              , d = 0 == (a | 0);
            a: do
                if (!d) {
                    var e = a - 8 | 0
                      , g = e
                      , h = y[v + 16 >> 2]
                      , l = e >>> 0 < h >>> 0;
                    b: do
                        if (!l) {
                            var t = y[a - 4 >> 2]
                              , q = t & 3;
                            if (1 != (q | 0)) {
                                var D = t & -8;
                                var A = D >> 2;
                                var f = a + (D - 8) | 0
                                  , k = f
                                  , m = 0 == (t & 1 | 0);
                                c: do
                                    if (m) {
                                        var u = y[e >> 2];
                                        if (0 == (q | 0))
                                            break a;
                                        var z = -8 - u | 0;
                                        var B = z >> 2;
                                        var C = a + z | 0
                                          , S = C
                                          , W = u + D | 0;
                                        if (C >>> 0 < h >>> 0)
                                            break b;
                                        if ((S | 0) == (b[v + 20 >> 2] | 0)) {
                                            var ea = (a + (D - 4) | 0) >> 2;
                                            if (3 != (b[ea] & 3 | 0)) {
                                                var X = S;
                                                var P = X >> 2;
                                                var Y = W;
                                                break
                                            }
                                            b[v + 8 >> 2] = W;
                                            b[ea] &= -2;
                                            b[B + (c + 1)] = W | 1;
                                            b[f >> 2] = W;
                                            break a
                                        }
                                        if (256 > u >>> 0) {
                                            var R = y[B + (c + 2)]
                                              , ma = y[B + (c + 3)];
                                            if ((R | 0) == (ma | 0))
                                                b[v >> 2] &= 1 << (u >>> 3) ^ -1,
                                                X = S,
                                                P = X >> 2,
                                                Y = W;
                                            else {
                                                var Fa = ((u >>> 2 & 1073741822) << 2) + v + 40 | 0;
                                                if (!((R | 0) != (Fa | 0) & R >>> 0 < h >>> 0) && (ma | 0) == (Fa | 0) | ma >>> 0 >= h >>> 0) {
                                                    b[R + 12 >> 2] = ma;
                                                    b[ma + 8 >> 2] = R;
                                                    X = S;
                                                    P = X >> 2;
                                                    Y = W;
                                                    break c
                                                }
                                                ha();
                                                throw "Reached an unreachable!";
                                            }
                                        } else {
                                            var za = C
                                              , ra = y[B + (c + 6)]
                                              , Sa = y[B + (c + 3)]
                                              , Ka = (Sa | 0) == (za | 0);
                                            do {
                                                if (Ka) {
                                                    var Ga = z + (a + 20) | 0
                                                      , Ba = b[Ga >> 2];
                                                    if (0 == (Ba | 0)) {
                                                        var La = z + (a + 16) | 0
                                                          , ua = b[La >> 2];
                                                        if (0 == (ua | 0)) {
                                                            var va = 0;
                                                            var Na = va >> 2;
                                                            break
                                                        }
                                                        var wa = La
                                                          , oa = ua
                                                    } else {
                                                        wa = Ga;
                                                        oa = Ba;
                                                        var ka = 21
                                                    }
                                                    for (; ; ) {
                                                        var pa = oa + 20 | 0
                                                          , ia = b[pa >> 2];
                                                        if (0 != (ia | 0))
                                                            wa = pa,
                                                            oa = ia;
                                                        else {
                                                            var qa = oa + 16 | 0
                                                              , xa = y[qa >> 2];
                                                            if (0 == (xa | 0))
                                                                break;
                                                            wa = qa;
                                                            oa = xa
                                                        }
                                                    }
                                                    if (wa >>> 0 < h >>> 0)
                                                        throw ha(),
                                                        "Reached an unreachable!";
                                                    b[wa >> 2] = 0;
                                                    va = oa
                                                } else {
                                                    var aa = y[B + (c + 2)];
                                                    if (aa >>> 0 < h >>> 0)
                                                        throw ha(),
                                                        "Reached an unreachable!";
                                                    b[aa + 12 >> 2] = Sa;
                                                    b[Sa + 8 >> 2] = aa;
                                                    va = Sa
                                                }
                                                Na = va >> 2
                                            } while (0);if (0 != (ra | 0)) {
                                                var fa = z + (a + 28) | 0
                                                  , sa = (b[fa >> 2] << 2) + v + 304 | 0
                                                  , la = (za | 0) == (b[sa >> 2] | 0);
                                                do {
                                                    if (la) {
                                                        b[sa >> 2] = va;
                                                        if (0 != (va | 0))
                                                            break;
                                                        b[v + 4 >> 2] &= 1 << b[fa >> 2] ^ -1;
                                                        X = S;
                                                        P = X >> 2;
                                                        Y = W;
                                                        break c
                                                    }
                                                    if (ra >>> 0 < y[v + 16 >> 2] >>> 0)
                                                        throw ha(),
                                                        "Reached an unreachable!";
                                                    var Ca = ra + 16 | 0;
                                                    (b[Ca >> 2] | 0) == (za | 0) ? b[Ca >> 2] = va : b[ra + 20 >> 2] = va;
                                                    if (0 == (va | 0)) {
                                                        X = S;
                                                        P = X >> 2;
                                                        Y = W;
                                                        break c
                                                    }
                                                } while (0);if (va >>> 0 < y[v + 16 >> 2] >>> 0)
                                                    throw ha(),
                                                    "Reached an unreachable!";
                                                b[Na + 6] = ra;
                                                var Ha = y[B + (c + 4)];
                                                if (0 != (Ha | 0)) {
                                                    if (Ha >>> 0 < y[v + 16 >> 2] >>> 0)
                                                        throw ha(),
                                                        "Reached an unreachable!";
                                                    b[Na + 4] = Ha;
                                                    b[Ha + 24 >> 2] = va
                                                }
                                                var Ia = y[B + (c + 5)];
                                                if (0 != (Ia | 0)) {
                                                    if (Ia >>> 0 < y[v + 16 >> 2] >>> 0)
                                                        throw ha(),
                                                        "Reached an unreachable!";
                                                    b[Na + 5] = Ia;
                                                    b[Ia + 24 >> 2] = va
                                                }
                                            }
                                            X = S;
                                            P = X >> 2;
                                            Y = W
                                        }
                                    } else
                                        X = g,
                                        P = X >> 2,
                                        Y = D;
                                while (0);var Ya = X;
                                if (!(Ya >>> 0 >= f >>> 0)) {
                                    var bb = a + (D - 4) | 0
                                      , Ja = y[bb >> 2];
                                    if (0 != (Ja & 1 | 0)) {
                                        if (0 == (Ja & 2 | 0)) {
                                            if ((k | 0) == (b[v + 24 >> 2] | 0)) {
                                                var wb = b[v + 12 >> 2] + Y | 0;
                                                b[v + 12 >> 2] = wb;
                                                b[v + 24 >> 2] = X;
                                                b[P + 1] = wb | 1;
                                                (X | 0) == (b[v + 20 >> 2] | 0) && (b[v + 20 >> 2] = 0,
                                                b[v + 8 >> 2] = 0);
                                                if (wb >>> 0 <= y[v + 28 >> 2] >>> 0)
                                                    break a;
                                                Be(0);
                                                break a
                                            }
                                            if ((k | 0) == (b[v + 20 >> 2] | 0)) {
                                                var hb = b[v + 8 >> 2] + Y | 0;
                                                b[v + 8 >> 2] = hb;
                                                b[v + 20 >> 2] = X;
                                                b[P + 1] = hb | 1;
                                                b[(Ya + hb | 0) >> 2] = hb;
                                                break a
                                            }
                                            var ob = (Ja & -8) + Y | 0
                                              , Ac = Ja >>> 3
                                              , Qb = 256 > Ja >>> 0;
                                            c: do
                                                if (Qb) {
                                                    var Wa = y[c + A]
                                                      , Pa = y[((D | 4) >> 2) + c];
                                                    if ((Wa | 0) == (Pa | 0))
                                                        b[v >> 2] &= 1 << Ac ^ -1;
                                                    else {
                                                        var Rb = ((Ja >>> 2 & 1073741822) << 2) + v + 40 | 0;
                                                        ka = (Wa | 0) == (Rb | 0) ? 63 : Wa >>> 0 < y[v + 16 >> 2] >>> 0 ? 66 : 63;
                                                        if (63 == ka && !((Pa | 0) != (Rb | 0) && Pa >>> 0 < y[v + 16 >> 2] >>> 0)) {
                                                            b[Wa + 12 >> 2] = Pa;
                                                            b[Pa + 8 >> 2] = Wa;
                                                            break c
                                                        }
                                                        ha();
                                                        throw "Reached an unreachable!";
                                                    }
                                                } else {
                                                    var Sb = f
                                                      , xb = y[A + (c + 4)]
                                                      , ib = y[((D | 4) >> 2) + c]
                                                      , Tb = (ib | 0) == (Sb | 0);
                                                    do {
                                                        if (Tb) {
                                                            var Bc = D + (a + 12) | 0
                                                              , sc = b[Bc >> 2];
                                                            if (0 == (sc | 0)) {
                                                                var Gb = D + (a + 8) | 0
                                                                  , ec = b[Gb >> 2];
                                                                if (0 == (ec | 0)) {
                                                                    var cb = 0;
                                                                    var Za = cb >> 2;
                                                                    break
                                                                }
                                                                var jb = Gb
                                                                  , eb = ec
                                                            } else
                                                                jb = Bc,
                                                                eb = sc,
                                                                ka = 73;
                                                            for (; ; ) {
                                                                var pb = eb + 20 | 0
                                                                  , fc = b[pb >> 2];
                                                                if (0 != (fc | 0))
                                                                    jb = pb,
                                                                    eb = fc;
                                                                else {
                                                                    var gc = eb + 16 | 0
                                                                      , hc = y[gc >> 2];
                                                                    if (0 == (hc | 0))
                                                                        break;
                                                                    jb = gc;
                                                                    eb = hc
                                                                }
                                                            }
                                                            if (jb >>> 0 < y[v + 16 >> 2] >>> 0)
                                                                throw ha(),
                                                                "Reached an unreachable!";
                                                            b[jb >> 2] = 0;
                                                            cb = eb
                                                        } else {
                                                            var Ub = y[c + A];
                                                            if (Ub >>> 0 < y[v + 16 >> 2] >>> 0)
                                                                throw ha(),
                                                                "Reached an unreachable!";
                                                            b[Ub + 12 >> 2] = ib;
                                                            b[ib + 8 >> 2] = Ub;
                                                            cb = ib
                                                        }
                                                        Za = cb >> 2
                                                    } while (0);if (0 != (xb | 0)) {
                                                        var Vb = D + (a + 20) | 0
                                                          , tc = (b[Vb >> 2] << 2) + v + 304 | 0
                                                          , uc = (Sb | 0) == (b[tc >> 2] | 0);
                                                        do {
                                                            if (uc) {
                                                                b[tc >> 2] = cb;
                                                                if (0 != (cb | 0))
                                                                    break;
                                                                b[v + 4 >> 2] &= 1 << b[Vb >> 2] ^ -1;
                                                                break c
                                                            }
                                                            if (xb >>> 0 < y[v + 16 >> 2] >>> 0)
                                                                throw ha(),
                                                                "Reached an unreachable!";
                                                            var ic = xb + 16 | 0;
                                                            (b[ic >> 2] | 0) == (Sb | 0) ? b[ic >> 2] = cb : b[xb + 20 >> 2] = cb;
                                                            if (0 == (cb | 0))
                                                                break c
                                                        } while (0);if (cb >>> 0 < y[v + 16 >> 2] >>> 0)
                                                            throw ha(),
                                                            "Reached an unreachable!";
                                                        b[Za + 6] = xb;
                                                        var Wb = y[A + (c + 2)];
                                                        if (0 != (Wb | 0)) {
                                                            if (Wb >>> 0 < y[v + 16 >> 2] >>> 0)
                                                                throw ha(),
                                                                "Reached an unreachable!";
                                                            b[Za + 4] = Wb;
                                                            b[Wb + 24 >> 2] = cb
                                                        }
                                                        var Hb = y[A + (c + 3)];
                                                        if (0 != (Hb | 0)) {
                                                            if (Hb >>> 0 < y[v + 16 >> 2] >>> 0)
                                                                throw ha(),
                                                                "Reached an unreachable!";
                                                            b[Za + 5] = Hb;
                                                            b[Hb + 24 >> 2] = cb
                                                        }
                                                    }
                                                }
                                            while (0);b[P + 1] = ob | 1;
                                            b[Ya + ob >> 2] = ob;
                                            if ((X | 0) != (b[v + 20 >> 2] | 0))
                                                var db = ob;
                                            else {
                                                b[v + 8 >> 2] = ob;
                                                break a
                                            }
                                        } else
                                            b[bb >> 2] = Ja & -2,
                                            b[P + 1] = Y | 1,
                                            db = b[Ya + Y >> 2] = Y;
                                        if (256 > db >>> 0) {
                                            var yb = db >>> 2 & 1073741822
                                              , vc = (yb << 2) + v + 40 | 0
                                              , jc = y[v >> 2]
                                              , kc = 1 << (db >>> 3);
                                            if (0 == (jc & kc | 0)) {
                                                b[v >> 2] = jc | kc;
                                                var Ib = vc
                                                  , lc = (yb + 2 << 2) + v + 40 | 0
                                            } else {
                                                var mc = (yb + 2 << 2) + v + 40 | 0
                                                  , nc = y[mc >> 2];
                                                if (nc >>> 0 >= y[v + 16 >> 2] >>> 0)
                                                    Ib = nc,
                                                    lc = mc;
                                                else
                                                    throw ha(),
                                                    "Reached an unreachable!";
                                            }
                                            b[lc >> 2] = X;
                                            b[Ib + 12 >> 2] = X;
                                            b[P + 2] = Ib;
                                            b[P + 3] = vc;
                                            break a
                                        }
                                        var zb = X
                                          , Xb = db >>> 8;
                                        if (0 == (Xb | 0))
                                            var lb = 0;
                                        else if (16777215 < db >>> 0)
                                            lb = 31;
                                        else {
                                            var Yb = (Xb + 1048320 | 0) >>> 16 & 8
                                              , fb = Xb << Yb
                                              , Zb = (fb + 520192 | 0) >>> 16 & 4
                                              , qb = fb << Zb
                                              , Ab = (qb + 245760 | 0) >>> 16 & 2
                                              , Qc = 14 - (Zb | Yb | Ab) + (qb << Ab >>> 15) | 0;
                                            lb = db >>> ((Qc + 7 | 0) >>> 0) & 1 | Qc << 1
                                        }
                                        var Fc = (lb << 2) + v + 304 | 0;
                                        b[P + 7] = lb;
                                        b[P + 5] = 0;
                                        b[P + 4] = 0;
                                        var Rc = b[v + 4 >> 2]
                                          , Sc = 1 << lb
                                          , fd = 0 == (Rc & Sc | 0);
                                        c: do
                                            if (fd)
                                                b[v + 4 >> 2] = Rc | Sc,
                                                b[Fc >> 2] = zb,
                                                b[P + 6] = Fc,
                                                b[P + 3] = X,
                                                b[P + 2] = X;
                                            else
                                                for (var Gc = db << (31 == (lb | 0) ? 0 : 25 - (lb >>> 1) | 0), ac = b[Fc >> 2]; ; ) {
                                                    if ((b[ac + 4 >> 2] & -8 | 0) == (db | 0)) {
                                                        var Tc = ac + 8 | 0
                                                          , Hc = y[Tc >> 2]
                                                          , Uc = y[v + 16 >> 2];
                                                        if (!(ac >>> 0 < Uc >>> 0 || Hc >>> 0 < Uc >>> 0)) {
                                                            b[Hc + 12 >> 2] = zb;
                                                            b[Tc >> 2] = zb;
                                                            b[P + 2] = Hc;
                                                            b[P + 3] = ac;
                                                            b[P + 6] = 0;
                                                            break c
                                                        }
                                                        ha();
                                                        throw "Reached an unreachable!";
                                                    }
                                                    var Db = (Gc >>> 31 << 2) + ac + 16 | 0
                                                      , Vc = y[Db >> 2];
                                                    if (0 == (Vc | 0)) {
                                                        if (Db >>> 0 >= y[v + 16 >> 2] >>> 0) {
                                                            b[Db >> 2] = zb;
                                                            b[P + 6] = ac;
                                                            b[P + 3] = X;
                                                            b[P + 2] = X;
                                                            break c
                                                        }
                                                        ha();
                                                        throw "Reached an unreachable!";
                                                    }
                                                    Gc <<= 1;
                                                    ac = Vc
                                                }
                                        while (0);var Ic = b[v + 32 >> 2] - 1 | 0;
                                        b[v + 32 >> 2] = Ic;
                                        if (0 != (Ic | 0))
                                            break a;
                                        hg();
                                        break a
                                    }
                                }
                            }
                        }
                    while (0);ha();
                    throw "Reached an unreachable!";
                }
            while (0)
        }
        function hg() {
            var a = b[v + 452 >> 2]
              , c = 0 == (a | 0);
            a: do
                if (!c)
                    for (; ; )
                        if (a = b[a + 8 >> 2],
                        0 == (a | 0))
                            break a;
            while (0);b[v + 32 >> 2] = -1
        }
        function ig(a, c) {
            return 0 == (a | 0) ? zc(c) : Ce(a, c)
        }
        function Ce(a, c) {
            var d;
            var e = 4294967231 < c >>> 0;
            a: do
                if (e) {
                    var g = n();
                    b[g >> 2] = 12;
                    g = 0
                } else {
                    var h = d = a - 8 | 0;
                    e = (a - 4 | 0) >> 2;
                    var l = y[e];
                    g = l & -8;
                    var t = g - 8 | 0
                      , q = a + t | 0;
                    if (!(d >>> 0 < y[v + 16 >> 2] >>> 0)) {
                        var D = l & 3;
                        if (1 != (D | 0) & -8 < (t | 0) && (d = (a + (g - 4) | 0) >> 2,
                        0 != (b[d] & 1 | 0))) {
                            t = 11 > c >>> 0 ? 16 : c + 11 & -8;
                            if (0 == (D | 0)) {
                                var A = 0
                                  , f = jg(h, t);
                                var k = 17
                            } else
                                g >>> 0 < t >>> 0 ? (q | 0) != (b[v + 24 >> 2] | 0) ? k = 21 : (q = b[v + 12 >> 2] + g | 0,
                                q >>> 0 <= t >>> 0 ? k = 21 : (A = q - t | 0,
                                f = a + (t - 8) | 0,
                                b[e] = t | l & 1 | 2,
                                b[a + (t - 4) >> 2] = A | 1,
                                b[v + 24 >> 2] = f,
                                b[v + 12 >> 2] = A,
                                A = 0,
                                f = h,
                                k = 17)) : (A = g - t | 0,
                                15 >= A >>> 0 ? A = 0 : (b[e] = t | l & 1 | 2,
                                b[a + (t - 4) >> 2] = A | 3,
                                b[d] |= 1,
                                A = a + t | 0),
                                f = h,
                                k = 17);
                            if (17 == k && 0 != (f | 0)) {
                                0 != (A | 0) && Jc(A);
                                g = f + 8 | 0;
                                break a
                            }
                            h = zc(c);
                            if (0 == (h | 0)) {
                                g = 0;
                                break a
                            }
                            e = g - (0 == (b[e] & 3 | 0) ? 8 : 4) | 0;
                            Pc(h, a, e >>> 0 < c >>> 0 ? e : c, 1);
                            Jc(a);
                            g = h;
                            break a
                        }
                    }
                    ha();
                    throw "Reached an unreachable!";
                }
            while (0);return g
        }
        function we() {
            if (0 == (b[ab >> 2] | 0)) {
                var a = kg(8);
                if (0 == (a - 1 & a | 0))
                    b[ab + 8 >> 2] = a,
                    b[ab + 4 >> 2] = a,
                    b[ab + 12 >> 2] = -1,
                    b[ab + 16 >> 2] = 2097152,
                    b[ab + 20 >> 2] = 0,
                    b[v + 440 >> 2] = 0,
                    a = lg(0),
                    b[ab >> 2] = a & -16 ^ 1431655768;
                else
                    throw ha(),
                    "Reached an unreachable!";
            }
        }
        function zd(a) {
            if (0 == (a | 0))
                a = 0;
            else {
                a = b[a - 4 >> 2];
                var c = a & 3;
                a = 1 == (c | 0) ? 0 : (a & -8) - (0 == (c | 0) ? 8 : 4) | 0
            }
            return a
        }
        function jg(a, c) {
            var d = b[a + 4 >> 2] & -8;
            if (256 > c >>> 0)
                var e = 0;
            else
                d >>> 0 >= (c + 4 | 0) >>> 0 && (d - c | 0) >>> 0 <= b[ab + 8 >> 2] << 1 >>> 0 ? e = a : e = 0;
            return e
        }
        function xd(a) {
            var c, d = v + 444 | 0;
            for (c = d >> 2; ; ) {
                var e = y[c];
                if (e >>> 0 <= a >>> 0 && (e + b[c + 1] | 0) >>> 0 > a >>> 0) {
                    a = d;
                    break
                }
                c = y[c + 2];
                if (0 == (c | 0)) {
                    a = 0;
                    break
                }
                d = c;
                c = d >> 2
            }
            return a
        }
        function ed(a, c) {
            var d = a + 8 | 0;
            d = 0 == (d & 7 | 0) ? 0 : -d & 7;
            var e = c - d | 0;
            b[v + 24 >> 2] = a + d | 0;
            b[v + 12 >> 2] = e;
            b[d + (a + 4) >> 2] = e | 1;
            b[c + (a + 4) >> 2] = 40;
            b[v + 28 >> 2] = b[ab + 16 >> 2]
        }
        function gg() {
            for (var a = 0; ; ) {
                var c = a << 1
                  , d = (c << 2) + v + 40 | 0;
                b[v + (c + 3 << 2) + 40 >> 2] = d;
                b[v + (c + 2 << 2) + 40 >> 2] = d;
                a = a + 1 | 0;
                if (32 == (a | 0))
                    break
            }
        }
        function xe(a, c, d) {
            var e = c >> 2
              , g = a >> 2
              , h = a + 8 | 0;
            h = 0 == (h & 7 | 0) ? 0 : -h & 7;
            var l = c + 8 | 0;
            var t = 0 == (l & 7 | 0) ? 0 : -l & 7;
            var q = t >> 2;
            var D = c + t | 0
              , A = h + d | 0;
            l = A >> 2;
            var f = a + A | 0
              , k = D - (a + h) - d | 0;
            b[(h + 4 >> 2) + g] = d | 3;
            d = (D | 0) == (b[v + 24 >> 2] | 0);
            a: do
                if (d) {
                    var m = b[v + 12 >> 2] + k | 0;
                    b[v + 12 >> 2] = m;
                    b[v + 24 >> 2] = f;
                    b[l + (g + 1)] = m | 1
                } else if ((D | 0) == (b[v + 20 >> 2] | 0))
                    m = b[v + 8 >> 2] + k | 0,
                    b[v + 8 >> 2] = m,
                    b[v + 20 >> 2] = f,
                    b[l + (g + 1)] = m | 1,
                    b[(a + m + A | 0) >> 2] = m;
                else {
                    var u = y[q + (e + 1)];
                    if (1 == (u & 3 | 0)) {
                        m = u & -8;
                        var z = u >>> 3
                          , B = 256 > u >>> 0;
                        b: do
                            if (B) {
                                var C = y[((t | 8) >> 2) + e]
                                  , S = y[q + (e + 3)];
                                if ((C | 0) == (S | 0))
                                    b[v >> 2] &= 1 << z ^ -1;
                                else {
                                    u = ((u >>> 2 & 1073741822) << 2) + v + 40 | 0;
                                    var W = (C | 0) == (u | 0) ? 15 : C >>> 0 < y[v + 16 >> 2] >>> 0 ? 18 : 15;
                                    if (15 == W && !((S | 0) != (u | 0) && S >>> 0 < y[v + 16 >> 2] >>> 0)) {
                                        b[C + 12 >> 2] = S;
                                        b[S + 8 >> 2] = C;
                                        break b
                                    }
                                    ha();
                                    throw "Reached an unreachable!";
                                }
                            } else {
                                C = D;
                                S = y[((t | 24) >> 2) + e];
                                var ea = y[q + (e + 3)]
                                  , X = (ea | 0) == (C | 0);
                                do {
                                    if (X) {
                                        var P = t | 16;
                                        var Y = P + (c + 4) | 0
                                          , R = b[Y >> 2];
                                        if (0 == (R | 0)) {
                                            if (P = c + P | 0,
                                            R = b[P >> 2],
                                            0 == (R | 0)) {
                                                R = 0;
                                                P = R >> 2;
                                                break
                                            }
                                        } else
                                            P = Y,
                                            W = 25;
                                        for (; ; ) {
                                            Y = R + 20 | 0;
                                            var ma = b[Y >> 2];
                                            if (0 != (ma | 0))
                                                P = Y,
                                                R = ma;
                                            else {
                                                Y = R + 16 | 0;
                                                ma = y[Y >> 2];
                                                if (0 == (ma | 0))
                                                    break;
                                                P = Y;
                                                R = ma
                                            }
                                        }
                                        if (P >>> 0 < y[v + 16 >> 2] >>> 0)
                                            throw ha(),
                                            "Reached an unreachable!";
                                        b[P >> 2] = 0
                                    } else {
                                        P = y[((t | 8) >> 2) + e];
                                        if (P >>> 0 < y[v + 16 >> 2] >>> 0)
                                            throw ha(),
                                            "Reached an unreachable!";
                                        b[P + 12 >> 2] = ea;
                                        b[ea + 8 >> 2] = P;
                                        R = ea
                                    }
                                    P = R >> 2
                                } while (0);if (0 != (S | 0)) {
                                    ea = t + (c + 28) | 0;
                                    X = (b[ea >> 2] << 2) + v + 304 | 0;
                                    Y = (C | 0) == (b[X >> 2] | 0);
                                    do {
                                        if (Y) {
                                            b[X >> 2] = R;
                                            if (0 != (R | 0))
                                                break;
                                            b[v + 4 >> 2] &= 1 << b[ea >> 2] ^ -1;
                                            break b
                                        }
                                        if (S >>> 0 < y[v + 16 >> 2] >>> 0)
                                            throw ha(),
                                            "Reached an unreachable!";
                                        ma = S + 16 | 0;
                                        (b[ma >> 2] | 0) == (C | 0) ? b[ma >> 2] = R : b[S + 20 >> 2] = R;
                                        if (0 == (R | 0))
                                            break b
                                    } while (0);if (R >>> 0 < y[v + 16 >> 2] >>> 0)
                                        throw ha(),
                                        "Reached an unreachable!";
                                    b[P + 6] = S;
                                    C = t | 16;
                                    S = y[(C >> 2) + e];
                                    if (0 != (S | 0)) {
                                        if (S >>> 0 < y[v + 16 >> 2] >>> 0)
                                            throw ha(),
                                            "Reached an unreachable!";
                                        b[P + 4] = S;
                                        b[S + 24 >> 2] = R
                                    }
                                    C = y[(C + 4 >> 2) + e];
                                    if (0 != (C | 0)) {
                                        if (C >>> 0 < y[v + 16 >> 2] >>> 0)
                                            throw ha(),
                                            "Reached an unreachable!";
                                        b[P + 5] = C;
                                        b[C + 24 >> 2] = R
                                    }
                                }
                            }
                        while (0);u = c + (m | t) | 0;
                        m = m + k | 0
                    } else
                        u = D,
                        m = k;
                    u = u + 4 | 0;
                    b[u >> 2] &= -2;
                    b[l + (g + 1)] = m | 1;
                    b[(m >> 2) + g + l] = m;
                    if (256 > m >>> 0) {
                        z = m >>> 2 & 1073741822;
                        u = (z << 2) + v + 40 | 0;
                        B = y[v >> 2];
                        m = 1 << (m >>> 3);
                        if (0 == (B & m | 0))
                            b[v >> 2] = B | m,
                            m = u,
                            z = (z + 2 << 2) + v + 40 | 0;
                        else if (z = (z + 2 << 2) + v + 40 | 0,
                        m = y[z >> 2],
                        !(m >>> 0 >= y[v + 16 >> 2] >>> 0))
                            throw ha(),
                            "Reached an unreachable!";
                        b[z >> 2] = f;
                        b[m + 12 >> 2] = f;
                        b[l + (g + 2)] = m;
                        b[l + (g + 3)] = u
                    } else if (u = f,
                    B = m >>> 8,
                    0 == (B | 0) ? B = 0 : 16777215 < m >>> 0 ? B = 31 : (z = (B + 1048320 | 0) >>> 16 & 8,
                    C = B << z,
                    B = (C + 520192 | 0) >>> 16 & 4,
                    C <<= B,
                    S = (C + 245760 | 0) >>> 16 & 2,
                    z = 14 - (B | z | S) + (C << S >>> 15) | 0,
                    B = m >>> ((z + 7 | 0) >>> 0) & 1 | z << 1),
                    z = (B << 2) + v + 304 | 0,
                    b[l + (g + 7)] = B,
                    C = A + (a + 16) | 0,
                    b[l + (g + 5)] = 0,
                    b[C >> 2] = 0,
                    C = b[v + 4 >> 2],
                    S = 1 << B,
                    0 == (C & S | 0))
                        b[v + 4 >> 2] = C | S,
                        b[z >> 2] = u,
                        b[l + (g + 6)] = z,
                        b[l + (g + 3)] = u,
                        b[l + (g + 2)] = u;
                    else
                        for (e = m << (31 == (B | 0) ? 0 : 25 - (B >>> 1) | 0),
                        c = b[z >> 2]; ; ) {
                            if ((b[c + 4 >> 2] & -8 | 0) == (m | 0)) {
                                e = c + 8 | 0;
                                q = y[e >> 2];
                                t = y[v + 16 >> 2];
                                if (!(c >>> 0 < t >>> 0 || q >>> 0 < t >>> 0)) {
                                    b[q + 12 >> 2] = u;
                                    b[e >> 2] = u;
                                    b[l + (g + 2)] = q;
                                    b[l + (g + 3)] = c;
                                    b[l + (g + 6)] = 0;
                                    break a
                                }
                                ha();
                                throw "Reached an unreachable!";
                            }
                            q = (e >>> 31 << 2) + c + 16 | 0;
                            t = y[q >> 2];
                            if (0 == (t | 0)) {
                                if (q >>> 0 >= y[v + 16 >> 2] >>> 0) {
                                    b[q >> 2] = u;
                                    b[l + (g + 6)] = c;
                                    b[l + (g + 3)] = u;
                                    b[l + (g + 2)] = u;
                                    break a
                                }
                                ha();
                                throw "Reached an unreachable!";
                            }
                            e <<= 1;
                            c = t
                        }
                }
            while (0);return a + (h | 8) | 0
        }
        function De(a) {
            b[a >> 2] = Ee + 8 | 0
        }
        function Fe(a) {
            0 != (a | 0) && Jc(a)
        }
        function Ad(a) {
            mg(a | 0)
        }
        function ye(a, c) {
            var d = y[v + 24 >> 2];
            var e = d >> 2;
            var g = xd(d)
              , h = b[g >> 2];
            var l = b[g + 4 >> 2];
            g = h + l | 0;
            var t = h + (l - 39) | 0;
            h = h + (l - 47) + (0 == (t & 7 | 0) ? 0 : -t & 7) | 0;
            h = h >>> 0 < (d + 16 | 0) >>> 0 ? d : h;
            t = h + 8 | 0;
            l = t >> 2;
            ed(a, c - 40 | 0);
            b[(h + 4 | 0) >> 2] = 27;
            b[l] = b[v + 444 >> 2];
            b[l + 1] = b[v + 448 >> 2];
            b[l + 2] = b[v + 452 >> 2];
            b[l + 3] = b[v + 456 >> 2];
            b[v + 444 >> 2] = a;
            b[v + 448 >> 2] = c;
            b[v + 456 >> 2] = 0;
            b[v + 452 >> 2] = t;
            a = h + 28 | 0;
            b[a >> 2] = 7;
            c = (h + 32 | 0) >>> 0 < g >>> 0;
            a: do
                if (c)
                    for (; ; ) {
                        c = a + 4 | 0;
                        b[c >> 2] = 7;
                        if ((a + 8 | 0) >>> 0 >= g >>> 0)
                            break a;
                        a = c
                    }
            while (0);g = (h | 0) == (d | 0);
            a: do
                if (!g)
                    if (a = h - d | 0,
                    c = d + a | 0,
                    l = a + (d + 4) | 0,
                    b[l >> 2] &= -2,
                    b[e + 1] = a | 1,
                    b[c >> 2] = a,
                    256 > a >>> 0) {
                        l = a >>> 2 & 1073741822;
                        c = (l << 2) + v + 40 | 0;
                        t = y[v >> 2];
                        a = 1 << (a >>> 3);
                        if (0 == (t & a | 0))
                            b[v >> 2] = t | a,
                            a = c,
                            l = (l + 2 << 2) + v + 40 | 0;
                        else if (l = (l + 2 << 2) + v + 40 | 0,
                        a = y[l >> 2],
                        !(a >>> 0 >= y[v + 16 >> 2] >>> 0))
                            throw ha(),
                            "Reached an unreachable!";
                        b[l >> 2] = d;
                        b[a + 12 >> 2] = d;
                        b[e + 2] = a;
                        b[e + 3] = c
                    } else {
                        c = d;
                        t = a >>> 8;
                        if (0 == (t | 0))
                            t = 0;
                        else if (16777215 < a >>> 0)
                            t = 31;
                        else {
                            l = (t + 1048320 | 0) >>> 16 & 8;
                            var q = t << l;
                            t = (q + 520192 | 0) >>> 16 & 4;
                            q <<= t;
                            var D = (q + 245760 | 0) >>> 16 & 2;
                            l = 14 - (t | l | D) + (q << D >>> 15) | 0;
                            t = a >>> ((l + 7 | 0) >>> 0) & 1 | l << 1
                        }
                        l = (t << 2) + v + 304 | 0;
                        b[e + 7] = t;
                        b[e + 5] = 0;
                        b[e + 4] = 0;
                        q = b[v + 4 >> 2];
                        D = 1 << t;
                        if (0 == (q & D | 0))
                            b[v + 4 >> 2] = q | D,
                            b[l >> 2] = c,
                            b[e + 6] = l,
                            b[e + 3] = d,
                            b[e + 2] = d;
                        else
                            for (g = a << (31 == (t | 0) ? 0 : 25 - (t >>> 1) | 0),
                            h = b[l >> 2]; ; ) {
                                if ((b[h + 4 >> 2] & -8 | 0) == (a | 0)) {
                                    d = h + 8 | 0;
                                    g = y[d >> 2];
                                    a = y[v + 16 >> 2];
                                    if (!(h >>> 0 < a >>> 0 || g >>> 0 < a >>> 0)) {
                                        b[g + 12 >> 2] = c;
                                        b[d >> 2] = c;
                                        b[e + 2] = g;
                                        b[e + 3] = h;
                                        b[e + 6] = 0;
                                        break a
                                    }
                                    ha();
                                    throw "Reached an unreachable!";
                                }
                                l = (g >>> 31 << 2) + h + 16 | 0;
                                t = y[l >> 2];
                                if (0 == (t | 0)) {
                                    if (l >>> 0 >= y[v + 16 >> 2] >>> 0) {
                                        b[l >> 2] = c;
                                        b[e + 6] = h;
                                        b[e + 3] = d;
                                        b[e + 2] = d;
                                        break a
                                    }
                                    ha();
                                    throw "Reached an unreachable!";
                                }
                                g <<= 1;
                                h = t
                            }
                    }
            while (0)
        }
        function ng(a, c) {
            function d(W) {
                if ("double" === W)
                    var ea = (yc[0] = b[c + e >> 2],
                    yc[1] = b[c + e + 4 >> 2],
                    qd[0]);
                else
                    "i64" == W ? ea = [b[c + e >> 2], b[c + e + 4 >> 2]] : (W = "i32",
                    ea = b[c + e >> 2]);
                e += Ea.bc(W);
                return ea
            }
            for (var e = 0, g = [], h, l; ; ) {
                var t = a;
                h = ba[a];
                if (0 === h)
                    break;
                l = ba[a + 1];
                if (37 == h) {
                    var q = !1
                      , D = !1
                      , A = !1
                      , f = !1;
                    a: for (; ; ) {
                        switch (l) {
                        case 43:
                            q = !0;
                            break;
                        case 45:
                            D = !0;
                            break;
                        case 35:
                            A = !0;
                            break;
                        case 48:
                            if (f)
                                break a;
                            else {
                                f = !0;
                                break
                            }
                        default:
                            break a
                        }
                        a++;
                        l = ba[a + 1]
                    }
                    var k = 0;
                    if (42 == l)
                        k = d("i32"),
                        a++,
                        l = ba[a + 1];
                    else
                        for (; 48 <= l && 57 >= l; )
                            k = 10 * k + (l - 48),
                            a++,
                            l = ba[a + 1];
                    var m = !1;
                    if (46 == l) {
                        var u = 0;
                        m = !0;
                        a++;
                        l = ba[a + 1];
                        if (42 == l)
                            u = d("i32"),
                            a++;
                        else
                            for (; ; ) {
                                l = ba[a + 1];
                                if (48 > l || 57 < l)
                                    break;
                                u = 10 * u + (l - 48);
                                a++
                            }
                        l = ba[a + 1]
                    } else
                        u = 6;
                    switch (String.fromCharCode(l)) {
                    case "h":
                        l = ba[a + 2];
                        if (104 == l) {
                            a++;
                            var z = 1
                        } else
                            z = 2;
                        break;
                    case "l":
                        l = ba[a + 2];
                        108 == l ? (a++,
                        z = 8) : z = 4;
                        break;
                    case "L":
                    case "q":
                    case "j":
                        z = 8;
                        break;
                    case "z":
                    case "t":
                    case "I":
                        z = 4;
                        break;
                    default:
                        z = null
                    }
                    z && a++;
                    l = ba[a + 1];
                    if (-1 != "diuoxXp".split("").indexOf(String.fromCharCode(l))) {
                        t = 100 == l || 105 == l;
                        z = z || 4;
                        var B = h = d("i" + 8 * z), C;
                        8 == z && (h = Ea.kc(h[0], h[1], 117 == l));
                        4 >= z && (h = (t ? U : Z)(h & Math.pow(256, z) - 1, 8 * z));
                        var S = Math.abs(h);
                        t = "";
                        if (100 == l || 105 == l)
                            8 == z && gd ? C = gd.stringify(B[0], B[1]) : C = U(h, 8 * z, 1).toString(10);
                        else if (117 == l)
                            8 == z && gd ? C = gd.stringify(B[0], B[1], !0) : C = Z(h, 8 * z, 1).toString(10),
                            h = Math.abs(h);
                        else if (111 == l)
                            C = (A ? "0" : "") + S.toString(8);
                        else if (120 == l || 88 == l) {
                            t = A ? "0x" : "";
                            if (0 > h) {
                                h = -h;
                                C = (S - 1).toString(16);
                                A = [];
                                for (B = 0; B < C.length; B++)
                                    A.push((15 - parseInt(C[B], 16)).toString(16));
                                for (C = A.join(""); C.length < 2 * z; )
                                    C = "f" + C
                            } else
                                C = S.toString(16);
                            88 == l && (t = t.toUpperCase(),
                            C = C.toUpperCase())
                        } else
                            112 == l && (0 === S ? C = "(nil)" : (t = "0x",
                            C = S.toString(16)));
                        if (m)
                            for (; C.length < u; )
                                C = "0" + C;
                        for (q && (t = 0 > h ? "-" + t : "+" + t); t.length + C.length < k; )
                            D ? C += " " : f ? C = "0" + C : t = " " + t;
                        C = t + C;
                        C.split("").forEach(function(W) {
                            g.push(W.charCodeAt(0))
                        })
                    } else if (-1 != "fFeEgG".split("").indexOf(String.fromCharCode(l))) {
                        h = d("double");
                        if (isNaN(h))
                            C = "nan",
                            f = !1;
                        else if (isFinite(h)) {
                            m = !1;
                            z = Math.min(u, 20);
                            if (103 == l || 71 == l)
                                m = !0,
                                u = u || 1,
                                z = parseInt(h.toExponential(z).split("e")[1], 10),
                                u > z && -4 <= z ? (l = (103 == l ? "f" : "F").charCodeAt(0),
                                u -= z + 1) : (l = (103 == l ? "e" : "E").charCodeAt(0),
                                u--),
                                z = Math.min(u, 20);
                            if (101 == l || 69 == l)
                                C = h.toExponential(z),
                                /[eE][-+]\d$/.test(C) && (C = C.slice(0, -1) + "0" + C.slice(-1));
                            else if (102 == l || 70 == l)
                                C = h.toFixed(z);
                            t = C.split("e");
                            if (m && !A)
                                for (; 1 < t[0].length && -1 != t[0].indexOf(".") && ("0" == t[0].slice(-1) || "." == t[0].slice(-1)); )
                                    t[0] = t[0].slice(0, -1);
                            else
                                for (A && -1 == C.indexOf(".") && (t[0] += "."); u > z++; )
                                    t[0] += "0";
                            C = t[0] + (1 < t.length ? "e" + t[1] : "");
                            69 == l && (C = C.toUpperCase());
                            q && 0 <= h && (C = "+" + C)
                        } else
                            C = (0 > h ? "-" : "") + "inf",
                            f = !1;
                        for (; C.length < k; )
                            C = D ? C + " " : !f || "-" != C[0] && "+" != C[0] ? (f ? "0" : " ") + C : C[0] + "0" + C.slice(1);
                        97 > l && (C = C.toUpperCase());
                        C.split("").forEach(function(W) {
                            g.push(W.charCodeAt(0))
                        })
                    } else if (115 == l) {
                        (q = d("i8*")) ? (q = J(q),
                        m && q.length > u && (q = q.slice(0, u))) : q = O("(null)", !0);
                        if (!D)
                            for (; q.length < k--; )
                                g.push(32);
                        g = g.concat(q);
                        if (D)
                            for (; q.length < k--; )
                                g.push(32)
                    } else if (99 == l) {
                        for (D && g.push(d("i8")); 0 < --k; )
                            g.push(32);
                        D || g.push(d("i8"))
                    } else if (110 == l)
                        D = d("i32*"),
                        b[D >> 2] = g.length;
                    else if (37 == l)
                        g.push(h);
                    else
                        for (B = t; B < a + 2; B++)
                            g.push(ba[B]);
                    a += 2
                } else
                    g.push(h),
                    a += 1
            }
            return g
        }
        function og(a, c, d, e) {
            d = ng(d, e);
            c = void 0 === c ? d.length : Math.min(d.length, c - 1);
            for (e = 0; e < c; e++)
                ba[a + e] = d[e];
            ba[a + e] = 0;
            return d.length
        }
        function df(a, c, d) {
            return og(a, void 0, c, d)
        }
        function Ra(a) {
            Ra.a || (Ra.a = w([0], "i32", 2));
            return b[Ra.a >> 2] = a
        }
        function pg(a, c, d, e) {
            a = da.streams[a];
            if (!a || a.object.O)
                return Ra(Xa.Ca),
                -1;
            if (a.ka) {
                if (a.object.S)
                    return Ra(Xa.rb),
                    -1;
                if (0 > d || 0 > e)
                    return Ra(Xa.oa),
                    -1;
                for (var g = a.object.u; g.length < e; )
                    g.push(0);
                for (var h = 0; h < d; h++)
                    g[e + h] = Q[c + h];
                a.object.timestamp = Date.now();
                return h
            }
            Ra(Xa.aa);
            return -1
        }
        function Ge(a, c, d) {
            var e = da.streams[a];
            if (e) {
                if (e.ka) {
                    if (0 > d)
                        return Ra(Xa.oa),
                        -1;
                    if (e.object.O) {
                        if (e.object.Y) {
                            for (a = 0; a < d; a++)
                                try {
                                    e.object.Y(ba[c + a])
                                } catch (g) {
                                    return Ra(Xa.Da),
                                    -1
                                }
                            e.object.timestamp = Date.now();
                            return a
                        }
                        Ra(Xa.tb);
                        return -1
                    }
                    c = pg(a, c, d, e.position);
                    -1 != c && (e.position += c);
                    return c
                }
                Ra(Xa.aa);
                return -1
            }
            Ra(Xa.Ca);
            return -1
        }
        function qg(a) {
            return H(a)
        }
        function rg(a, c) {
            return Ge(c, a, qg(a))
        }
        function hd(a, c) {
            a = Z(a & 255);
            ba[hd.a] = a;
            return -1 == Ge(c, hd.a, 1) ? (c in da.streams && (da.streams[c].error = !0),
            -1) : a
        }
        function ef(a) {
            var c = b[id >> 2];
            a = rg(a, c);
            return 0 > a ? a : 0 > hd(10, c) ? -1 : a + 1
        }
        function Mb(a, c, d) {
            if (20 <= d) {
                for (d = a + d; a % 4; )
                    ba[a++] = c;
                0 > c && (c += 256);
                a >>= 2;
                for (var e = d >> 2, g = c | c << 8 | c << 16 | c << 24; a < e; )
                    b[a++] = g;
                for (a <<= 2; a < d; )
                    ba[a++] = c
            } else
                for (; d--; )
                    ba[a++] = c
        }
        function Pc(a, c, d) {
            if (20 <= d && c % 2 == a % 2)
                if (c % 4 == a % 4) {
                    for (d = c + d; c % 4; )
                        ba[a++] = ba[c++];
                    c >>= 2;
                    a >>= 2;
                    for (var e = d >> 2; c < e; )
                        b[a++] = b[c++];
                    c <<= 2;
                    for (a <<= 2; c < d; )
                        ba[a++] = ba[c++]
                } else {
                    d = c + d;
                    c % 2 && (ba[a++] = ba[c++]);
                    c >>= 1;
                    a >>= 1;
                    for (e = d >> 1; c < e; )
                        vb[a++] = vb[c++];
                    c <<= 1;
                    a <<= 1;
                    c < d && (ba[a++] = ba[c++])
                }
            else
                for (; d--; )
                    ba[a++] = ba[c++]
        }
        function ha() {
            throw "abort() at " + Error().stack;
        }
        function kg(a) {
            switch (a) {
            case 8:
                return 4096;
            case 54:
            case 56:
            case 21:
            case 61:
            case 63:
            case 22:
            case 67:
            case 23:
            case 24:
            case 25:
            case 26:
            case 27:
            case 69:
            case 28:
            case 101:
            case 70:
            case 71:
            case 29:
            case 30:
            case 199:
            case 75:
            case 76:
            case 32:
            case 43:
            case 44:
            case 80:
            case 46:
            case 47:
            case 45:
            case 48:
            case 49:
            case 42:
            case 82:
            case 33:
            case 7:
            case 108:
            case 109:
            case 107:
            case 112:
            case 119:
            case 121:
                return 200809;
            case 13:
            case 104:
            case 94:
            case 95:
            case 34:
            case 35:
            case 77:
            case 81:
            case 83:
            case 84:
            case 85:
            case 86:
            case 87:
            case 88:
            case 89:
            case 90:
            case 91:
            case 94:
            case 95:
            case 110:
            case 111:
            case 113:
            case 114:
            case 115:
            case 116:
            case 117:
            case 118:
            case 120:
            case 40:
            case 16:
            case 79:
            case 19:
                return -1;
            case 92:
            case 93:
            case 5:
            case 72:
            case 6:
            case 74:
            case 92:
            case 93:
            case 96:
            case 97:
            case 98:
            case 99:
            case 102:
            case 103:
            case 105:
                return 1;
            case 38:
            case 66:
            case 50:
            case 51:
            case 4:
                return 1024;
            case 15:
            case 64:
            case 41:
                return 32;
            case 55:
            case 37:
            case 17:
                return 2147483647;
            case 18:
            case 1:
                return 47839;
            case 59:
            case 57:
                return 99;
            case 68:
            case 58:
                return 2048;
            case 0:
                return 2097152;
            case 3:
                return 65536;
            case 14:
                return 32768;
            case 73:
                return 32767;
            case 39:
                return 16384;
            case 60:
                return 1E3;
            case 106:
                return 700;
            case 52:
                return 256;
            case 62:
                return 255;
            case 2:
                return 100;
            case 65:
                return 64;
            case 36:
                return 20;
            case 100:
                return 16;
            case 20:
                return 6;
            case 53:
                return 4
            }
            Ra(Xa.oa);
            return -1
        }
        function lg(a) {
            var c = Math.floor(Date.now() / 1E3);
            a && (b[a >> 2] = c);
            return c
        }
        function Cb(a) {
            var c = Cb;
            c.b || (Eb = Eb + 4095 >> 12 << 12,
            c.b = !0);
            c = Eb;
            0 != a && Ea.kb(a);
            return c
        }
        function He(a) {
            a = a || N.arguments;
            N.setStatus && N.setStatus("");
            N.preRun && N.preRun();
            var c = null;
            N._main && (L(Ie),
            c = N.Sb(a),
            N.noExitRuntime || (L(Je),
            sg.print()));
            N.postRun && N.postRun();
            return c
        }
        var Wc = {};
        if ("undefined" == typeof Xc)
            var Xc = {};
        var N = {};
        try {
            this.Module = N
        } catch (a) {
            this.Module = N = {}
        }
        var Ke = "object" === typeof Xc;
        if (Ke)
            if (Ke)
                N.print || (N.print = function(a) {
                    console.log(a)
                }
                ),
                N.printErr || (N.printErr = function(a) {
                    console.log(a)
                }
                ),
                N.read = function(a) {
                    var c = new XMLHttpRequest;
                    c.open("GET", a, !1);
                    c.send(null);
                    return c.responseText
                }
                ,
                N.arguments || "undefined" != typeof arguments && (N.arguments = arguments);
            else
                throw "Unknown runtime environment. Where are we?";
        else
            N.print = print,
            N.printErr = printErr,
            N.read = "undefined" != typeof read ? read : function(a) {
                snarf(a)
            }
            ,
            N.arguments || ("undefined" != typeof scriptArgs ? N.arguments = scriptArgs : "undefined" != typeof arguments && (N.arguments = arguments));
        "undefined" == !N.load && N.read && (N.load = function(a) {
            r(N.read(a))
        }
        );
        N.printErr || (N.printErr = function() {}
        );
        N.print || (N.print = N.printErr);
        N.arguments || (N.arguments = []);
        N.print = N.print;
        N.ye = N.printErr;
        var Ea = {
            jb: function() {
                return V
            },
            sc: function(a) {
                V = a
            },
            je: function(a, c) {
                c = c || 4;
                return 1 == c ? a : "Math.ceil((" + a + ")/" + c + ")*" + c
            },
            fc: function(a) {
                return a in Ea.Ab || a in Ea.vb
            },
            hc: function(a) {
                return "*" == a[a.length - 1]
            },
            jc: function(a) {
                return isPointerType(a) ? !1 : /^\[\d+ x (.*)\]/.test(a) || /<?{ ?[^}]* ?}>?/.test(a) ? !0 : "%" == a[0]
            },
            Ab: {
                i1: 0,
                i8: 0,
                i16: 0,
                i32: 0,
                i64: 0
            },
            vb: {
                "float": 0,
                "double": 0
            },
            Zd: function(a, c, d, e) {
                var g = Math.pow(2, e) - 1;
                if (32 > e)
                    switch (d) {
                    case "shl":
                        return [a << e, c << e | (a & g << 32 - e) >>> 32 - e];
                    case "ashr":
                        return [(a >>> e | (c & g) << 32 - e) >> 0 >>> 0, c >> e >>> 0];
                    case "lshr":
                        return [(a >>> e | (c & g) << 32 - e) >>> 0, c >>> e]
                    }
                else if (32 == e)
                    switch (d) {
                    case "shl":
                        return [0, a];
                    case "ashr":
                        return [c, 0 > (c | 0) ? g : 0];
                    case "lshr":
                        return [c, 0]
                    }
                else
                    switch (d) {
                    case "shl":
                        return [0, a << e - 32];
                    case "ashr":
                        return [c >> e - 32 >>> 0, 0 > (c | 0) ? g : 0];
                    case "lshr":
                        return [c >>> e - 32, 0]
                    }
                p("unknown bitshift64 op: " + [value, d, e])
            },
            we: function(a, c) {
                return (a | 0 | c | 0) + 4294967296 * (Math.round(a / 4294967296) | Math.round(c / 4294967296))
            },
            Xd: function(a, c) {
                return ((a | 0) & (c | 0)) + 4294967296 * (Math.round(a / 4294967296) & Math.round(c / 4294967296))
            },
            Ee: function(a, c) {
                return ((a | 0) ^ (c | 0)) + 4294967296 * (Math.round(a / 4294967296) ^ Math.round(c / 4294967296))
            },
            wa: function(a) {
                if (1 == Ea.ea)
                    return 1;
                var c = {
                    "%i1": 1,
                    "%i8": 1,
                    "%i16": 2,
                    "%i32": 4,
                    "%i64": 8,
                    "%float": 4,
                    "%double": 8
                }["%" + a];
                c || ("*" == a[a.length - 1] ? c = Ea.ea : "i" == a[0] && (a = parseInt(a.substr(1)),
                G(0 == a % 8),
                c = a / 8));
                return c
            },
            bc: function(a) {
                return Math.max(Ea.wa(a), Ea.ea)
            },
            Wb: function(a, c) {
                var d = {};
                return c ? a.filter(function(e) {
                    return d[e[c]] ? !1 : d[e[c]] = !0
                }) : a.filter(function(e) {
                    return d[e] ? !1 : d[e] = !0
                })
            },
            set: function() {
                for (var a = "object" === typeof arguments[0] ? arguments[0] : arguments, c = {}, d = 0; d < a.length; d++)
                    c[a[d]] = 0;
                return c
            },
            Rb: function(a) {
                a.R = 0;
                a.ga = 0;
                var c = []
                  , d = -1;
                a.Xa = a.ua.map(function(e) {
                    var g;
                    if (Ea.fc(e) || Ea.hc(e))
                        e = g = Ea.wa(e);
                    else if (Ea.jc(e))
                        g = Wc.types[e].R,
                        e = Wc.types[e].ga;
                    else
                        throw "Unclear type in struct: " + e + ", in " + a.mc + " :: " + dump(Wc.types[a.mc]);
                    e = a.xe ? 1 : Math.min(e, Ea.ea);
                    a.ga = Math.max(a.ga, e);
                    e = Ea.fa(a.R, e);
                    a.R = e + g;
                    0 <= d && c.push(e - d);
                    return d = e
                });
                a.R = Ea.fa(a.R, a.ga);
                0 == c.length ? a.Wa = a.R : 1 == Ea.Wb(c).length && (a.Wa = c[0]);
                a.ue = 1 != a.Wa;
                return a.Xa
            },
            $b: function(a, c, d) {
                if (c) {
                    d = d || 0;
                    var e = ("undefined" === typeof Wc ? Ea.De : Wc.types)[c];
                    if (!e)
                        return null;
                    G(e.ua.length === a.length, "Number of named fields must match the type for " + c);
                    var g = e.Xa
                } else
                    e = {
                        ua: a.map(function(l) {
                            return l[0]
                        })
                    },
                    g = Ea.Rb(e);
                var h = {
                    Ud: e.R
                };
                c ? a.forEach(function(l, t) {
                    if ("string" === typeof l)
                        h[l] = g[t] + d;
                    else {
                        var q;
                        for (q in l)
                            var D = q;
                        h[D] = Ea.$b(l[D], e.ua[t], g[t])
                    }
                }) : a.forEach(function(l, t) {
                    h[l[1]] = g[t]
                });
                return h
            },
            Wd: function(a) {
                var c = Nb.length;
                Nb.push(a);
                Nb.push(0);
                return c
            },
            Aa: function(a) {
                var c = V;
                V += a;
                V = V + 3 >> 2 << 2;
                return c
            },
            kb: function(a) {
                var c = Eb;
                Eb += a;
                Eb = Eb + 3 >> 2 << 2;
                if (Eb >= Kc) {
                    for (; Kc <= Eb; )
                        Kc = 2 * Kc + 4095 >> 12 << 12;
                    a = ba;
                    var d = new ArrayBuffer(Kc);
                    ba = new Int8Array(d);
                    vb = new Int16Array(d);
                    b = new Int32Array(d);
                    Q = new Uint8Array(d);
                    ya = new Uint16Array(d);
                    y = new Uint32Array(d);
                    bd = new Float32Array(d);
                    Bd = new Float64Array(d);
                    ba.set(a)
                }
                return c
            },
            fa: function(a, c) {
                return Math.ceil(a / (c ? c : 4)) * (c ? c : 4)
            },
            kc: function(a, c, d) {
                return d ? (a >>> 0) + 4294967296 * (c >>> 0) : (a >>> 0) + 4294967296 * (c | 0)
            },
            ea: 4,
            Td: 0
        }, sg = {
            Fb: 0,
            Pa: 0,
            Ae: {},
            ve: function(a, c) {
                c || (this.Pa++,
                this.Pa >= this.Fb && p("\n\nToo many corrections!"))
            },
            print: function() {}
        }, Mc, cf = this;
        N.ccall = x;
        N.cwrap = function(a, c, d) {
            return function() {
                return x(a, c, d, Array.prototype.slice.call(arguments))
            }
        }
        ;
        N.setValue = E;
        N.getValue = function(a, c) {
            c = c || "i8";
            "*" === c[c.length - 1] && (c = "i32");
            switch (c) {
            case "i1":
                return ba[a];
            case "i8":
                return ba[a];
            case "i16":
                return vb[a >> 1];
            case "i32":
                return b[a >> 2];
            case "i64":
                return b[a >> 2];
            case "float":
                return bd[a >> 2];
            case "double":
                return yc[0] = b[a >> 2],
                yc[1] = b[a + 4 >> 2],
                qd[0];
            default:
                p("invalid type for setValue: " + c)
            }
            return null
        }
        ;
        N.ALLOC_NORMAL = 0;
        N.ALLOC_STACK = 1;
        N.ALLOC_STATIC = 2;
        N.allocate = w;
        N.Pointer_stringify = I;
        N.Array_stringify = function(a) {
            for (var c = "", d = 0; d < a.length; d++)
                c += String.fromCharCode(a[d]);
            return c
        }
        ;
        var V, tg = N.TOTAL_STACK || 5242880, Kc = N.TOTAL_MEMORY || 10485760;
        G(!!Int32Array && !!Float64Array && !!(new Int32Array(1)).subarray && !!(new Int32Array(1)).set, "Cannot fallback to non-typed array case: Code is too specialized");
        var oc = new ArrayBuffer(Kc);
        var ba = new Int8Array(oc);
        var vb = new Int16Array(oc);
        var b = new Int32Array(oc);
        var Q = new Uint8Array(oc);
        var ya = new Uint16Array(oc);
        var y = new Uint32Array(oc);
        var bd = new Float32Array(oc);
        var Bd = new Float64Array(oc);
        b[0] = 255;
        G(255 === Q[0] && 0 === Q[3], "Typed arrays 2 must be run on a little-endian system");
        var Cd = O("(null)");
        var Eb = Cd.length;
        for (var jd = 0; jd < Cd.length; jd++)
            ba[jd] = Cd[jd];
        N.HEAP = void 0;
        N.HEAP8 = ba;
        N.HEAP16 = vb;
        N.HEAP32 = b;
        N.HEAPU8 = Q;
        N.HEAPU16 = ya;
        N.HEAPU32 = y;
        N.HEAPF32 = bd;
        N.HEAPF64 = Bd;
        var Dd = (V = Ea.fa(Eb)) + tg;
        var Ed = Ea.fa(Dd, 8)
          , yc = b.subarray(Ed >> 2)
          , qd = Bd.subarray(Ed >> 3);
        Dd = Ed + 8;
        Eb = Dd + 4095 >> 12 << 12;
        var Le = []
          , Ie = []
          , Je = [];
        N.Array_copy = K;
        N.TypedArray_copy = function(a, c, d) {
            void 0 === d && (d = 0);
            for (var e = new Uint8Array(c - d), g = d; g < c; ++g)
                e[g - d] = ba[a + g];
            return e.buffer
        }
        ;
        N.String_len = H;
        N.String_copy = J;
        N.intArrayFromString = O;
        N.intArrayToString = function(a) {
            for (var c = [], d = 0; d < a.length; d++) {
                var e = a[d];
                255 < e && (e &= 255);
                c.push(String.fromCharCode(e))
            }
            return c.join("")
        }
        ;
        N.writeStringToMemory = T;
        N.writeArrayToMemory = M;
        var F = []
          , Fd = 0;
        Va.X = 1;
        cc.X = 1;
        wc.X = 1;
        na.X = 1;
        cd.X = 1;
        Jb.X = 1;
        ce.X = 1;
        N._crn_get_width = function(a, c) {
            var d = V;
            V += 40;
            Ec(d);
            wc(a, c, d);
            a = b[d + 4 >> 2];
            V = d;
            return a
        }
        ;
        N._crn_get_height = function(a, c) {
            var d = V;
            V += 40;
            Ec(d);
            wc(a, c, d);
            a = b[d + 8 >> 2];
            V = d;
            return a
        }
        ;
        N._crn_get_levels = function(a, c) {
            var d = V;
            V += 40;
            Ec(d);
            wc(a, c, d);
            a = b[d + 12 >> 2];
            V = d;
            return a
        }
        ;
        N._crn_get_dxt_format = function(a, c) {
            var d = V;
            V += 40;
            Ec(d);
            wc(a, c, d);
            a = b[(d + 32 | 0) >> 2];
            V = d;
            return a
        }
        ;
        N._crn_get_decompressed_size = function(a, c) {
            var d = V;
            V += 40;
            Ec(d);
            wc(a, c, d);
            a = (b[d + 4 >> 2] + 3 | 0) >>> 2;
            c = (b[d + 8 >> 2] + 3 | 0) >>> 2;
            var e = d + 32 | 0;
            e = Td(b[e >> 2], b[e + 4 >> 2]);
            V = d;
            return c * a * e | 0
        }
        ;
        N._crn_decompress = function(a, c, d, e) {
            var g = V;
            V += 44;
            var h = g + 40;
            Ec(g);
            wc(a, c, g);
            var l = (b[g + 4 >> 2] + 3 | 0) >>> 2
              , t = g + 32 | 0;
            t = Td(b[t >> 2], b[t + 4 >> 2]);
            l = l * t | 0;
            a = Df(a, c);
            h |= 0;
            b[h >> 2] = d;
            Kf(a, h, e, l, 0);
            Mf(a);
            V = g
        }
        ;
        de.X = 1;
        he.X = 1;
        ee.X = 1;
        fe.X = 1;
        ge.X = 1;
        me.X = 1;
        ne.X = 1;
        oe.X = 1;
        pe.X = 1;
        N._malloc = zc;
        zc.X = 1;
        te.X = 1;
        ve.X = 1;
        ue.X = 1;
        Be.X = 1;
        N._free = Jc;
        Jc.X = 1;
        Ce.X = 1;
        xe.X = 1;
        ye.X = 1;
        var gd = function() {
            function a(f, k) {
                this.h = f | 0;
                this.j = k | 0
            }
            function c(f, k) {
                null != f && ("number" == typeof f ? this.F(f) : null == k && "string" != typeof f ? this.J(f, 256) : this.J(f, k))
            }
            function d() {
                return new c(null)
            }
            function e(f) {
                return "0123456789abcdefghijklmnopqrstuvwxyz".charAt(f)
            }
            function g(f, k) {
                f = t[f.charCodeAt(k)];
                return null == f ? -1 : f
            }
            function h(f) {
                var k = d();
                k.N(f);
                return k
            }
            function l(f) {
                var k = 1, m;
                0 != (m = f >>> 16) && (f = m,
                k += 16);
                0 != (m = f >> 8) && (f = m,
                k += 8);
                0 != (m = f >> 4) && (f = m,
                k += 4);
                0 != (m = f >> 2) && (f = m,
                k += 2);
                0 != f >> 1 && (k += 1);
                return k
            }
            a.Ia = {};
            a.N = function(f) {
                if (-128 <= f && 128 > f) {
                    var k = a.Ia[f];
                    if (k)
                        return k
                }
                k = new a(f | 0,0 > f ? -1 : 0);
                -128 <= f && 128 > f && (a.Ia[f] = k);
                return k
            }
            ;
            a.F = function(f) {
                return isNaN(f) || !isFinite(f) ? a.K : f <= -a.La ? a.B : f + 1 >= a.La ? a.Zb : 0 > f ? a.F(-f).o() : new a(f % a.L | 0,f / a.L | 0)
            }
            ;
            a.A = function(f, k) {
                return new a(f,k)
            }
            ;
            a.J = function(f, k) {
                if (0 == f.length)
                    throw Error("number format error: empty string");
                k = k || 10;
                if (2 > k || 36 < k)
                    throw Error("radix out of range: " + k);
                if ("-" == f.charAt(0))
                    return a.J(f.substring(1), k).o();
                if (0 <= f.indexOf("-"))
                    throw Error('number format error: interior "-" character: ' + f);
                for (var m = a.F(Math.pow(k, 8)), u = a.K, z = 0; z < f.length; z += 8) {
                    var B = Math.min(8, f.length - z)
                      , C = parseInt(f.substring(z, z + B), k);
                    8 > B ? (B = a.F(Math.pow(k, B)),
                    u = u.multiply(B).add(a.F(C))) : (u = u.multiply(m),
                    u = u.add(a.F(C)))
                }
                return u
            }
            ;
            a.pa = 65536;
            a.Od = 16777216;
            a.L = a.pa * a.pa;
            a.Pd = a.L / 2;
            a.Qd = a.L * a.pa;
            a.Mb = a.L * a.L;
            a.La = a.Mb / 2;
            a.K = a.N(0);
            a.ba = a.N(1);
            a.Ja = a.N(-1);
            a.Zb = a.A(-1, 2147483647);
            a.B = a.A(0, -2147483648);
            a.Ka = a.N(16777216);
            a.prototype.na = function() {
                return this.j * a.L + this.ac()
            }
            ;
            a.prototype.toString = function(f) {
                f = f || 10;
                if (2 > f || 36 < f)
                    throw Error("radix out of range: " + f);
                if (this.T())
                    return "0";
                if (this.C()) {
                    if (this.equals(a.B)) {
                        var k = a.F(f)
                          , m = this.I(k);
                        k = m.multiply(k).P(this);
                        return m.toString(f) + k.h.toString(f)
                    }
                    return "-" + this.o().toString(f)
                }
                m = a.F(Math.pow(f, 6));
                k = this;
                for (var u = ""; ; ) {
                    var z = k.I(m)
                      , B = k.P(z.multiply(m)).h.toString(f);
                    k = z;
                    if (k.T())
                        return B + u;
                    for (; 6 > B.length; )
                        B = "0" + B;
                    u = "" + B + u
                }
            }
            ;
            a.prototype.ac = function() {
                return 0 <= this.h ? this.h : a.L + this.h
            }
            ;
            a.prototype.T = function() {
                return 0 == this.j && 0 == this.h
            }
            ;
            a.prototype.C = function() {
                return 0 > this.j
            }
            ;
            a.prototype.ab = function() {
                return 1 == (this.h & 1)
            }
            ;
            a.prototype.equals = function(f) {
                return this.j == f.j && this.h == f.h
            }
            ;
            a.prototype.fb = function(f) {
                return 0 > this.compare(f)
            }
            ;
            a.prototype.cc = function(f) {
                return 0 < this.compare(f)
            }
            ;
            a.prototype.dc = function(f) {
                return 0 <= this.compare(f)
            }
            ;
            a.prototype.compare = function(f) {
                if (this.equals(f))
                    return 0;
                var k = this.C()
                  , m = f.C();
                return k && !m ? -1 : !k && m ? 1 : this.P(f).C() ? -1 : 1
            }
            ;
            a.prototype.o = function() {
                return this.equals(a.B) ? a.B : this.oc().add(a.ba)
            }
            ;
            a.prototype.add = function(f) {
                var k = this.j >>> 16
                  , m = this.j & 65535
                  , u = this.h >>> 16
                  , z = f.j >>> 16
                  , B = f.j & 65535
                  , C = f.h >>> 16;
                f = (this.h & 65535) + (f.h & 65535);
                C = (f >>> 16) + (u + C);
                u = C >>> 16;
                u += m + B;
                k = (u >>> 16) + (k + z) & 65535;
                return a.A((C & 65535) << 16 | f & 65535, k << 16 | u & 65535)
            }
            ;
            a.prototype.P = function(f) {
                return this.add(f.o())
            }
            ;
            a.prototype.multiply = function(f) {
                if (this.T() || f.T())
                    return a.K;
                if (this.equals(a.B))
                    return f.ab() ? a.B : a.K;
                if (f.equals(a.B))
                    return this.ab() ? a.B : a.K;
                if (this.C())
                    return f.C() ? this.o().multiply(f.o()) : this.o().multiply(f).o();
                if (f.C())
                    return this.multiply(f.o()).o();
                if (this.fb(a.Ka) && f.fb(a.Ka))
                    return a.F(this.na() * f.na());
                var k = this.j >>> 16
                  , m = this.j & 65535
                  , u = this.h >>> 16
                  , z = this.h & 65535
                  , B = f.j >>> 16
                  , C = f.j & 65535
                  , S = f.h >>> 16;
                f = f.h & 65535;
                var W = z * f;
                var ea = (W >>> 16) + u * f;
                var X = ea >>> 16;
                ea = (ea & 65535) + z * S;
                X += ea >>> 16;
                X += m * f;
                var P = X >>> 16;
                X = (X & 65535) + u * S;
                P += X >>> 16;
                X = (X & 65535) + z * C;
                P = P + (X >>> 16) + (k * f + m * S + u * C + z * B) & 65535;
                return a.A((ea & 65535) << 16 | W & 65535, P << 16 | X & 65535)
            }
            ;
            a.prototype.I = function(f) {
                if (f.T())
                    throw Error("division by zero");
                if (this.T())
                    return a.K;
                if (this.equals(a.B)) {
                    if (f.equals(a.ba) || f.equals(a.Ja))
                        return a.B;
                    if (f.equals(a.B))
                        return a.ba;
                    var k = this.rc().I(f).shiftLeft(1);
                    if (k.equals(a.K))
                        return f.C() ? a.ba : a.Ja;
                    var m = this.P(f.multiply(k));
                    return k.add(m.I(f))
                }
                if (f.equals(a.B))
                    return a.K;
                if (this.C())
                    return f.C() ? this.o().I(f.o()) : this.o().I(f).o();
                if (f.C())
                    return this.I(f.o()).o();
                var u = a.K;
                for (m = this; m.dc(f); ) {
                    k = Math.max(1, Math.floor(m.na() / f.na()));
                    var z = Math.ceil(Math.log(k) / Math.LN2);
                    z = 48 >= z ? 1 : Math.pow(2, z - 48);
                    for (var B = a.F(k), C = B.multiply(f); C.C() || C.cc(m); )
                        k -= z,
                        B = a.F(k),
                        C = B.multiply(f);
                    B.T() && (B = a.ba);
                    u = u.add(B);
                    m = m.P(C)
                }
                return u
            }
            ;
            a.prototype.hb = function(f) {
                return this.P(this.I(f).multiply(f))
            }
            ;
            a.prototype.oc = function() {
                return a.A(~this.h, ~this.j)
            }
            ;
            a.prototype.and = function(f) {
                return a.A(this.h & f.h, this.j & f.j)
            }
            ;
            a.prototype.or = function(f) {
                return a.A(this.h | f.h, this.j | f.j)
            }
            ;
            a.prototype.xor = function(f) {
                return a.A(this.h ^ f.h, this.j ^ f.j)
            }
            ;
            a.prototype.shiftLeft = function(f) {
                f &= 63;
                if (0 == f)
                    return this;
                var k = this.h;
                return 32 > f ? a.A(k << f, this.j << f | k >>> 32 - f) : a.A(0, k << f - 32)
            }
            ;
            a.prototype.rc = function() {
                var f = 1;
                if (0 == f)
                    return this;
                var k = this.j;
                return 32 > f ? a.A(this.h >>> f | k << 32 - f, k >> f) : a.A(k >> f - 32, 0 <= k ? 0 : -1)
            }
            ;
            c.prototype.qa = function(f, k, m, u) {
                for (var z = 0, B = 0; 0 <= --u; ) {
                    var C = f * this[z++] + k[m] + B;
                    B = Math.floor(C / 67108864);
                    k[m++] = C & 67108863
                }
                return B
            }
            ;
            c.prototype.i = 26;
            c.prototype.H = 67108863;
            c.prototype.$ = 67108864;
            c.prototype.wb = Math.pow(2, 52);
            c.prototype.Ga = 26;
            c.prototype.Ha = 0;
            var t = [], q;
            var D = 48;
            for (q = 0; 9 >= q; ++q)
                t[D++] = q;
            D = 97;
            for (q = 10; 36 > q; ++q)
                t[D++] = q;
            D = 65;
            for (q = 10; 36 > q; ++q)
                t[D++] = q;
            c.prototype.copyTo = function(f) {
                for (var k = this.t - 1; 0 <= k; --k)
                    f[k] = this[k];
                f.t = this.t;
                f.f = this.f
            }
            ;
            c.prototype.N = function(f) {
                this.t = 1;
                this.f = 0 > f ? -1 : 0;
                0 < f ? this[0] = f : -1 > f ? this[0] = f + DV : this.t = 0
            }
            ;
            c.prototype.J = function(f, k) {
                if (16 == k)
                    k = 4;
                else if (8 == k)
                    k = 3;
                else if (256 == k)
                    k = 8;
                else if (2 == k)
                    k = 1;
                else if (32 == k)
                    k = 5;
                else if (4 == k)
                    k = 2;
                else {
                    this.Yb(f, k);
                    return
                }
                this.f = this.t = 0;
                for (var m = f.length, u = !1, z = 0; 0 <= --m; ) {
                    var B = 8 == k ? f[m] & 255 : g(f, m);
                    0 > B ? "-" == f.charAt(m) && (u = !0) : (u = !1,
                    0 == z ? this[this.t++] = B : z + k > this.i ? (this[this.t - 1] |= (B & (1 << this.i - z) - 1) << z,
                    this[this.t++] = B >> this.i - z) : this[this.t - 1] |= B << z,
                    z += k,
                    z >= this.i && (z -= this.i))
                }
                8 == k && 0 != (f[0] & 128) && (this.f = -1,
                0 < z && (this[this.t - 1] |= (1 << this.i - z) - 1 << z));
                this.M();
                u && c.a.G(this, this)
            }
            ;
            c.prototype.M = function() {
                for (var f = this.f & this.H; 0 < this.t && this[this.t - 1] == f; )
                    --this.t
            }
            ;
            c.prototype.ta = function(f, k) {
                var m;
                for (m = this.t - 1; 0 <= m; --m)
                    k[m + f] = this[m];
                for (m = f - 1; 0 <= m; --m)
                    k[m] = 0;
                k.t = this.t + f;
                k.f = this.f
            }
            ;
            c.prototype.Xb = function(f, k) {
                for (var m = f; m < this.t; ++m)
                    k[m - f] = this[m];
                k.t = Math.max(this.t - f, 0);
                k.f = this.f
            }
            ;
            c.prototype.eb = function(f, k) {
                var m = f % this.i
                  , u = this.i - m
                  , z = (1 << u) - 1;
                f = Math.floor(f / this.i);
                var B = this.f << m & this.H, C;
                for (C = this.t - 1; 0 <= C; --C)
                    k[C + f + 1] = this[C] >> u | B,
                    B = (this[C] & z) << m;
                for (C = f - 1; 0 <= C; --C)
                    k[C] = 0;
                k[f] = B;
                k.t = this.t + f + 1;
                k.f = this.f;
                k.M()
            }
            ;
            c.prototype.qc = function(f, k) {
                k.f = this.f;
                var m = Math.floor(f / this.i);
                if (m >= this.t)
                    k.t = 0;
                else {
                    f %= this.i;
                    var u = this.i - f
                      , z = (1 << f) - 1;
                    k[0] = this[m] >> f;
                    for (var B = m + 1; B < this.t; ++B)
                        k[B - m - 1] |= (this[B] & z) << u,
                        k[B - m] = this[B] >> f;
                    0 < f && (k[this.t - m - 1] |= (this.f & z) << u);
                    k.t = this.t - m;
                    k.M()
                }
            }
            ;
            c.prototype.G = function(f, k) {
                for (var m = 0, u = 0, z = Math.min(f.t, this.t); m < z; )
                    u += this[m] - f[m],
                    k[m++] = u & this.H,
                    u >>= this.i;
                if (f.t < this.t) {
                    for (u -= f.f; m < this.t; )
                        u += this[m],
                        k[m++] = u & this.H,
                        u >>= this.i;
                    u += this.f
                } else {
                    for (u += this.f; m < f.t; )
                        u -= f[m],
                        k[m++] = u & this.H,
                        u >>= this.i;
                    u -= f.f
                }
                k.f = 0 > u ? -1 : 0;
                -1 > u ? k[m++] = this.$ + u : 0 < u && (k[m++] = u);
                k.t = m;
                k.M()
            }
            ;
            c.prototype.lc = function(f, k) {
                var m = this.abs()
                  , u = f.abs()
                  , z = m.t;
                for (k.t = z + u.t; 0 <= --z; )
                    k[z] = 0;
                for (z = 0; z < u.t; ++z)
                    k[z + m.t] = m.qa(u[z], k, z, m.t);
                k.f = 0;
                k.M();
                this.f != f.f && c.a.G(k, k)
            }
            ;
            c.prototype.V = function(f, k, m) {
                var u = f.abs();
                if (!(0 >= u.t)) {
                    var z = this.abs();
                    if (z.t < u.t)
                        null != k && k.N(0),
                        null != m && this.copyTo(m);
                    else {
                        null == m && (m = d());
                        var B = d()
                          , C = this.f;
                        f = f.f;
                        var S = this.i - l(u[u.t - 1]);
                        0 < S ? (u.eb(S, B),
                        z.eb(S, m)) : (u.copyTo(B),
                        z.copyTo(m));
                        u = B.t;
                        z = B[u - 1];
                        if (0 != z) {
                            var W = z * (1 << this.Ga) + (1 < u ? B[u - 2] >> this.Ha : 0)
                              , ea = this.wb / W;
                            W = (1 << this.Ga) / W;
                            var X = 1 << this.Ha
                              , P = m.t
                              , Y = P - u
                              , R = null == k ? d() : k;
                            B.ta(Y, R);
                            0 <= m.Tb(R) && (m[m.t++] = 1,
                            m.G(R, m));
                            c.c.ta(u, R);
                            for (R.G(B, B); B.t < u; )
                                B[B.t++] = 0;
                            for (; 0 <= --Y; ) {
                                var ma = m[--P] == z ? this.H : Math.floor(m[P] * ea + (m[P - 1] + X) * W);
                                if ((m[P] += B.qa(ma, m, Y, u)) < ma)
                                    for (B.ta(Y, R),
                                    m.G(R, m); m[P] < --ma; )
                                        m.G(R, m)
                            }
                            null != k && (m.Xb(u, k),
                            C != f && c.a.G(k, k));
                            m.t = u;
                            m.M();
                            0 < S && m.qc(S, m);
                            0 > C && c.a.G(m, m)
                        }
                    }
                }
            }
            ;
            c.prototype.exp = function(f, k) {
                if (4294967295 < f || 1 > f)
                    return c.c;
                var m = d()
                  , u = d()
                  , z = k.ae(this)
                  , B = l(f) - 1;
                for (z.copyTo(m); 0 <= --B; )
                    if (k.Be(m, u),
                    0 < (f & 1 << B))
                        k.te(u, z, m);
                    else {
                        var C = m;
                        m = u;
                        u = C
                    }
                return k.ze(m)
            }
            ;
            c.prototype.toString = function(f) {
                if (0 > this.f)
                    return "-" + this.o().toString(f);
                if (16 == f)
                    f = 4;
                else if (8 == f)
                    f = 3;
                else if (2 == f)
                    f = 1;
                else if (32 == f)
                    f = 5;
                else if (4 == f)
                    f = 2;
                else
                    return this.tc(f);
                var k = (1 << f) - 1, m, u = !1, z = "", B = this.t, C = this.i - B * this.i % f;
                if (0 < B--)
                    for (C < this.i && 0 < (m = this[B] >> C) && (u = !0,
                    z = e(m)); 0 <= B; )
                        C < f ? (m = (this[B] & (1 << C) - 1) << f - C,
                        m |= this[--B] >> (C += this.i - f)) : (m = this[B] >> (C -= f) & k,
                        0 >= C && (C += this.i,
                        --B)),
                        0 < m && (u = !0),
                        u && (z += e(m));
                return u ? z : "0"
            }
            ;
            c.prototype.o = function() {
                var f = d();
                c.a.G(this, f);
                return f
            }
            ;
            c.prototype.abs = function() {
                return 0 > this.f ? this.o() : this
            }
            ;
            c.prototype.Tb = function(f) {
                var k = this.f - f.f;
                if (0 != k)
                    return k;
                var m = this.t;
                k = m - f.t;
                if (0 != k)
                    return k;
                for (; 0 <= --m; )
                    if (0 != (k = this[m] - f[m]))
                        return k;
                return 0
            }
            ;
            c.a = h(0);
            c.c = h(1);
            c.prototype.Yb = function(f, k) {
                this.N(0);
                null == k && (k = 10);
                for (var m = this.Oa(k), u = Math.pow(k, m), z = !1, B = 0, C = 0, S = 0; S < f.length; ++S) {
                    var W = g(f, S);
                    0 > W ? "-" == f.charAt(S) && 0 == this.za() && (z = !0) : (C = k * C + W,
                    ++B >= m && (this.Sa(u),
                    this.Ra(C),
                    C = B = 0))
                }
                0 < B && (this.Sa(Math.pow(k, B)),
                this.Ra(C));
                z && c.a.G(this, this)
            }
            ;
            c.prototype.Oa = function(f) {
                return Math.floor(Math.LN2 * this.i / Math.log(f))
            }
            ;
            c.prototype.za = function() {
                return 0 > this.f ? -1 : 0 >= this.t || 1 == this.t && 0 >= this[0] ? 0 : 1
            }
            ;
            c.prototype.Sa = function(f) {
                this[this.t] = this.qa(f - 1, this, 0, this.t);
                ++this.t;
                this.M()
            }
            ;
            c.prototype.Ra = function(f) {
                var k = 0;
                if (0 != f) {
                    for (; this.t <= k; )
                        this[this.t++] = 0;
                    for (this[k] += f; this[k] >= this.$; )
                        this[k] -= this.$,
                        ++k >= this.t && (this[this.t++] = 0),
                        ++this[k]
                }
            }
            ;
            c.prototype.tc = function(f) {
                null == f && (f = 10);
                if (0 == this.za() || 2 > f || 36 < f)
                    return "0";
                var k = Math.pow(f, this.Oa(f))
                  , m = h(k)
                  , u = d()
                  , z = d()
                  , B = "";
                for (this.V(m, u, z); 0 < u.za(); )
                    B = (k + z.Za()).toString(f).substr(1) + B,
                    u.V(m, u, z);
                return z.Za().toString(f) + B
            }
            ;
            c.prototype.Za = function() {
                if (0 > this.f) {
                    if (1 == this.t)
                        return this[0] - this.$;
                    if (0 == this.t)
                        return -1
                } else {
                    if (1 == this.t)
                        return this[0];
                    if (0 == this.t)
                        return 0
                }
                return (this[1] & (1 << 32 - this.i) - 1) << this.i | this[0]
            }
            ;
            c.prototype.Na = function(f, k) {
                for (var m = 0, u = 0, z = Math.min(f.t, this.t); m < z; )
                    u += this[m] + f[m],
                    k[m++] = u & this.H,
                    u >>= this.i;
                if (f.t < this.t) {
                    for (u += f.f; m < this.t; )
                        u += this[m],
                        k[m++] = u & this.H,
                        u >>= this.i;
                    u += this.f
                } else {
                    for (u += this.f; m < f.t; )
                        u += f[m],
                        k[m++] = u & this.H,
                        u >>= this.i;
                    u += f.f
                }
                k.f = 0 > u ? -1 : 0;
                0 < u ? k[m++] = u : -1 > u && (k[m++] = this.$ + u);
                k.t = m;
                k.M()
            }
            ;
            var A = {
                result: [0, 0],
                add: function(f, k, m, u) {
                    f = (new a(f,k)).add(new a(m,u));
                    A.result[0] = f.h;
                    A.result[1] = f.j
                },
                P: function(f, k, m, u) {
                    f = (new a(f,k)).P(new a(m,u));
                    A.result[0] = f.h;
                    A.result[1] = f.j
                },
                multiply: function(f, k, m, u) {
                    f = (new a(f,k)).multiply(new a(m,u));
                    A.result[0] = f.h;
                    A.result[1] = f.j
                },
                gb: function() {
                    A.Z = new c;
                    A.Z.J("4294967296", 10)
                },
                la: function(f, k) {
                    var m = new c;
                    m.J(k.toString(), 10);
                    k = new c;
                    m.lc(A.Z, k);
                    m = new c;
                    m.J(f.toString(), 10);
                    f = new c;
                    m.Na(k, f);
                    return f
                },
                ge: function(f, k, m, u, z) {
                    A.Z || A.gb();
                    z ? (f = A.la(f >>> 0, k >>> 0),
                    u = A.la(m >>> 0, u >>> 0),
                    m = new c,
                    f.V(u, m, null),
                    u = new c,
                    f = new c,
                    m.V(A.Z, f, u),
                    A.result[0] = parseInt(u.toString()) | 0,
                    A.result[1] = parseInt(f.toString()) | 0) : (f = new a(f,k),
                    u = new a(m,u),
                    m = f.I(u),
                    A.result[0] = m.h,
                    A.result[1] = m.j)
                },
                hb: function(f, k, m, u, z) {
                    A.Z || A.gb();
                    z ? (f = A.la(f >>> 0, k >>> 0),
                    u = A.la(m >>> 0, u >>> 0),
                    m = new c,
                    f.V(u, null, m),
                    u = new c,
                    f = new c,
                    m.V(A.Z, f, u),
                    A.result[0] = parseInt(u.toString()) | 0,
                    A.result[1] = parseInt(f.toString()) | 0) : (f = new a(f,k),
                    u = new a(m,u),
                    m = f.hb(u),
                    A.result[0] = m.h,
                    A.result[1] = m.j)
                },
                stringify: function(f, k, m) {
                    f = (new a(f,k)).toString();
                    m && "-" == f[0] && (A.Ba || (A.Ba = new c,
                    A.Ba.J("18446744073709551616", 10)),
                    m = new c,
                    m.J(f, 10),
                    f = new c,
                    A.Ba.Na(m, f),
                    f = f.toString(10));
                    return f
                }
            };
            return A
        }(), Xa = {
            wc: 7,
            aa: 13,
            xc: 98,
            yc: 99,
            zc: 97,
            Ac: 11,
            Bc: 114,
            Ca: 9,
            Cc: 74,
            Dc: 16,
            Ec: 125,
            Fc: 10,
            Gc: 103,
            Hc: 111,
            Ic: 104,
            Jc: 35,
            Kc: 89,
            Lc: 33,
            Mc: 122,
            qb: 17,
            Nc: 14,
            Oc: 27,
            Pc: 113,
            Qc: 43,
            Rc: 84,
            Sc: 115,
            Tc: 4,
            oa: 22,
            Da: 5,
            Uc: 106,
            rb: 21,
            sb: 40,
            Vc: 24,
            Wc: 31,
            Xc: 90,
            Yc: 72,
            Zc: 36,
            $c: 100,
            ad: 102,
            bd: 101,
            cd: 23,
            dd: 105,
            ed: 61,
            fd: 19,
            Ea: 2,
            gd: 8,
            hd: 37,
            jd: 67,
            kd: 12,
            ld: 42,
            md: 92,
            nd: 28,
            od: 63,
            pd: 60,
            qd: 38,
            rd: 107,
            Fa: 20,
            sd: 39,
            td: 131,
            ud: 88,
            vd: 95,
            wd: 25,
            tb: 6,
            xd: 75,
            yd: 130,
            zd: 1,
            Ad: 32,
            Bd: 71,
            Cd: 93,
            Dd: 91,
            Ed: 34,
            Fd: 30,
            Gd: 29,
            Hd: 3,
            Id: 116,
            Jd: 62,
            Kd: 110,
            Ld: 26,
            Md: 11,
            Nd: 18
        }, Gd = 0, id = 0, Hd = 0, da = {
            Vb: "/",
            nc: 2,
            streams: [null],
            Ya: !0,
            Ma: function(a, c) {
                if ("string" !== typeof a)
                    return null;
                void 0 === c && (c = da.Vb);
                a && "/" == a[0] && (c = "");
                a = (c + "/" + a).split("/").reverse();
                for (c = [""]; a.length; ) {
                    var d = a.pop();
                    "" != d && "." != d && (".." == d ? 1 < c.length && c.pop() : c.push(d))
                }
                return 1 == c.length ? "/" : c.join("/")
            },
            ra: function(a, c, d) {
                var e = {
                    ic: !1,
                    ja: !1,
                    error: 0,
                    name: null,
                    path: null,
                    object: null,
                    xa: !1,
                    ib: null,
                    ya: null
                };
                a = da.Ma(a);
                if ("/" == a)
                    e.ic = !0,
                    e.ja = e.xa = !0,
                    e.name = "/",
                    e.path = e.ib = "/",
                    e.object = e.ya = da.root;
                else if (null !== a) {
                    d = d || 0;
                    a = a.slice(1).split("/");
                    for (var g = da.root, h = [""]; a.length; ) {
                        1 == a.length && g.S && (e.xa = !0,
                        e.ib = 1 == h.length ? "/" : h.join("/"),
                        e.ya = g,
                        e.name = a[0]);
                        var l = a.shift();
                        if (!g.S) {
                            e.error = Xa.Fa;
                            break
                        } else if (!g.read) {
                            e.error = Xa.aa;
                            break
                        } else if (!g.u.hasOwnProperty(l)) {
                            e.error = Xa.Ea;
                            break
                        }
                        g = g.u[l];
                        if (g.link && (!c || 0 != a.length)) {
                            if (40 < d) {
                                e.error = Xa.sb;
                                break
                            }
                            e = da.Ma(g.link, h.join("/"));
                            e = da.ra([e].concat(a).join("/"), c, d + 1);
                            break
                        }
                        h.push(l);
                        0 == a.length && (e.ja = !0,
                        e.path = h.join("/"),
                        e.object = g)
                    }
                }
                return e
            },
            Va: function(a, c) {
                da.Ta();
                a = da.ra(a, c);
                if (a.ja)
                    return a.object;
                Ra(a.error);
                return null
            },
            Qa: function(a, c, d, e, g) {
                a || (a = "/");
                "string" === typeof a && (a = da.Va(a));
                if (!a)
                    throw Ra(Xa.aa),
                    Error("Parent path must exist.");
                if (!a.S)
                    throw Ra(Xa.Fa),
                    Error("Parent must be a folder.");
                if (!a.write && !da.Ya)
                    throw Ra(Xa.aa),
                    Error("Parent folder must be writeable.");
                if (!c || "." == c || ".." == c)
                    throw Ra(Xa.Ea),
                    Error("Name must not be empty.");
                if (a.u.hasOwnProperty(c))
                    throw Ra(Xa.qb),
                    Error("Can't overwrite object.");
                a.u[c] = {
                    read: void 0 === e ? !0 : e,
                    write: void 0 === g ? !1 : g,
                    timestamp: Date.now(),
                    ec: da.nc++
                };
                for (var h in d)
                    d.hasOwnProperty(h) && (a.u[c][h] = d[h]);
                return a.u[c]
            },
            sa: function(a, c, d, e) {
                return da.Qa(a, c, {
                    S: !0,
                    O: !1,
                    u: {}
                }, d, e)
            },
            Ub: function(a, c, d, e) {
                a = da.Va(a);
                if (null === a)
                    throw Error("Invalid parent.");
                for (c = c.split("/").reverse(); c.length; ) {
                    var g = c.pop();
                    g && (a.u.hasOwnProperty(g) || da.sa(a, g, d, e),
                    a = a.u[g])
                }
                return a
            },
            ia: function(a, c, d, e, g) {
                d.S = !1;
                return da.Qa(a, c, d, e, g)
            },
            be: function(a, c, d, e, g) {
                if ("string" === typeof d) {
                    for (var h = Array(d.length), l = 0, t = d.length; l < t; ++l)
                        h[l] = d.charCodeAt(l);
                    d = h
                }
                return da.ia(a, c, {
                    O: !1,
                    u: d
                }, e, g)
            },
            ce: function(a, c, d, e, g) {
                return da.ia(a, c, {
                    O: !1,
                    url: d
                }, e, g)
            },
            de: function(a, c, d, e, g) {
                return da.ia(a, c, {
                    O: !1,
                    link: d
                }, e, g)
            },
            ha: function(a, c, d, e) {
                if (!d && !e)
                    throw Error("A device must have at least one callback defined.");
                return da.ia(a, c, {
                    O: !0,
                    input: d,
                    Y: e
                }, !!d, !!e)
            },
            ke: function(a) {
                if (a.O || a.S || a.link || a.u)
                    return !0;
                var c = !0;
                if ("undefined" !== typeof XMLHttpRequest)
                    G("Cannot do synchronous binary XHRs in modern browsers. Use --embed-file or --preload-file in emcc");
                else if (N.read)
                    try {
                        a.u = O(N.read(a.url), !0)
                    } catch (d) {
                        c = !1
                    }
                else
                    throw Error("Cannot load without read() or XMLHttpRequest.");
                c || Ra(Xa.Da);
                return c
            },
            Ta: function() {
                da.root || (da.root = {
                    read: !0,
                    write: !0,
                    S: !0,
                    O: !1,
                    timestamp: Date.now(),
                    ec: 1,
                    u: {}
                })
            },
            ca: function(a, c, d) {
                function e(A) {
                    null === A || 10 === A ? (c.ma(c.buffer.join("")),
                    c.buffer = []) : c.buffer.push(String.fromCharCode(A))
                }
                G(!da.ca.b, "FS.init was previously called. If you want to initialize later with custom parameters, remove any earlier calls (note that one is automatically added to the generated code)");
                da.ca.b = !0;
                da.Ta();
                a = a || N.stdin;
                c = c || N.stdout;
                d = d || N.stderr;
                var g = !0
                  , h = !0
                  , l = !0;
                a || (g = !1,
                a = function() {
                    if (!a.cache || !a.cache.length) {
                        var A;
                        "undefined" != typeof Xc && "function" == typeof Xc.prompt ? A = Xc.prompt("Input: ") : "function" == typeof readline && (A = readline());
                        A || (A = "");
                        a.cache = O(A + "\n", !0)
                    }
                    return a.cache.shift()
                }
                );
                c || (h = !1,
                c = e);
                c.ma || (c.ma = N.print);
                c.buffer || (c.buffer = []);
                d || (l = !1,
                d = e);
                d.ma || (d.ma = N.print);
                d.buffer || (d.buffer = []);
                da.sa("/", "tmp", !0, !0);
                var t = da.sa("/", "dev", !0, !0)
                  , q = da.ha(t, "stdin", a)
                  , D = da.ha(t, "stdout", null, c);
                d = da.ha(t, "stderr", null, d);
                da.ha(t, "tty", a, c);
                da.streams[1] = {
                    path: "/dev/stdin",
                    object: q,
                    position: 0,
                    bb: !0,
                    ka: !1,
                    $a: !1,
                    cb: !g,
                    error: !1,
                    Ua: !1,
                    lb: []
                };
                da.streams[2] = {
                    path: "/dev/stdout",
                    object: D,
                    position: 0,
                    bb: !1,
                    ka: !0,
                    $a: !1,
                    cb: !h,
                    error: !1,
                    Ua: !1,
                    lb: []
                };
                da.streams[3] = {
                    path: "/dev/stderr",
                    object: d,
                    position: 0,
                    bb: !1,
                    ka: !0,
                    $a: !1,
                    cb: !l,
                    error: !1,
                    Ua: !1,
                    lb: []
                };
                Gd = w([1], "void*", 2);
                id = w([2], "void*", 2);
                Hd = w([3], "void*", 2);
                da.Ub("/", "dev/shm/tmp", !0, !0);
                da.streams[Gd] = da.streams[1];
                da.streams[id] = da.streams[2];
                da.streams[Hd] = da.streams[3];
                w([w([0, 0, 0, 0, Gd, 0, 0, 0, id, 0, 0, 0, Hd, 0, 0, 0], "void*", 2)], "void*", 2)
            },
            pc: function() {
                da.ca.b && (da.streams[2] && 0 < da.streams[2].object.Y.buffer.length && da.streams[2].object.Y(10),
                da.streams[3] && 0 < da.streams[3].object.Y.buffer.length && da.streams[3].object.Y(10))
            },
            Ce: function(a) {
                "./" == a.substr(0, 2) && (a = a.substr(2));
                return a
            },
            fe: function(a) {
                a = da.ra(a);
                if (!a.xa || !a.ja)
                    throw "Invalid path " + a;
                delete a.ya.u[a.name]
            }
        }, mg;
        Le.unshift({
            va: function() {
                N.noFSInit || da.ca.b || da.ca()
            }
        });
        Ie.push({
            va: function() {
                da.Ya = !1
            }
        });
        Je.push({
            va: function() {
                da.pc()
            }
        });
        Ra(0);
        hd.a = w([0], "i8", 2);
        w(12, "void*", 2);
        N.Sb = function(a) {
            function c() {
                for (var h = 0; 3 > h; h++)
                    e.push(0)
            }
            var d = a.length + 1
              , e = [w(O("/bin/this.program"), "i8", 2)];
            c();
            for (var g = 0; g < d - 1; g += 1)
                e.push(w(O(a[g]), "i8", 2)),
                c();
            e.push(0);
            e = w(e, "i32", 2);
            return _main(d, e, 0)
        }
        ;
        F.uc = w([37, 115, 40, 37, 117, 41, 58, 32, 65, 115, 115, 101, 114, 116, 105, 111, 110, 32, 102, 97, 105, 108, 117, 114, 101, 58, 32, 34, 37, 115, 34, 10, 0], "i8", 2);
        F.mb = w([109, 95, 115, 105, 122, 101, 32, 60, 61, 32, 109, 95, 99, 97, 112, 97, 99, 105, 116, 121, 0], "i8", 2);
        F.a = w([116, 104, 105, 114, 100, 95, 112, 97, 114, 116, 121, 47, 99, 114, 117, 110, 99, 104, 47, 101, 109, 115, 99, 114, 105, 112, 116, 101, 110, 47, 46, 46, 47, 105, 110, 99, 47, 99, 114, 110, 95, 100, 101, 99, 111, 109, 112, 46, 104, 0], "i8", 2);
        F.Eb = w([109, 105, 110, 95, 110, 101, 119, 95, 99, 97, 112, 97, 99, 105, 116, 121, 32, 60, 32, 40, 48, 120, 55, 70, 70, 70, 48, 48, 48, 48, 85, 32, 47, 32, 101, 108, 101, 109, 101, 110, 116, 95, 115, 105, 122, 101, 41, 0], "i8", 2);
        F.Jb = w([110, 101, 119, 95, 99, 97, 112, 97, 99, 105, 116, 121, 32, 38, 38, 32, 40, 110, 101, 119, 95, 99, 97, 112, 97, 99, 105, 116, 121, 32, 62, 32, 109, 95, 99, 97, 112, 97, 99, 105, 116, 121, 41, 0], "i8", 2);
        F.Kb = w([110, 117, 109, 95, 99, 111, 100, 101, 115, 91, 99, 93, 0], "i8", 2);
        F.Lb = w([115, 111, 114, 116, 101, 100, 95, 112, 111, 115, 32, 60, 32, 116, 111, 116, 97, 108, 95, 117, 115, 101, 100, 95, 115, 121, 109, 115, 0], "i8", 2);
        F.Nb = w([112, 67, 111, 100, 101, 115, 105, 122, 101, 115, 91, 115, 121, 109, 95, 105, 110, 100, 101, 120, 93, 32, 61, 61, 32, 99, 111, 100, 101, 115, 105, 122, 101, 0], "i8", 2);
        F.Ob = w([116, 32, 60, 32, 40, 49, 85, 32, 60, 60, 32, 116, 97, 98, 108, 101, 95, 98, 105, 116, 115, 41, 0], "i8", 2);
        F.Pb = w([109, 95, 108, 111, 111, 107, 117, 112, 91, 116, 93, 32, 61, 61, 32, 99, 85, 73, 78, 84, 51, 50, 95, 77, 65, 88, 0], "i8", 2);
        var rd = w([2], ["i8* (i8*, i32, i32*, i1, i8*)*", 0, 0, 0, 0], 2);
        w([4], ["i32 (i8*, i8*)*", 0, 0, 0, 0], 2);
        var sd = w(1, "i8*", 2);
        F.m = w([99, 114, 110, 100, 95, 109, 97, 108, 108, 111, 99, 58, 32, 115, 105, 122, 101, 32, 116, 111, 111, 32, 98, 105, 103, 0], "i8", 2);
        F.nb = w([99, 114, 110, 100, 95, 109, 97, 108, 108, 111, 99, 58, 32, 111, 117, 116, 32, 111, 102, 32, 109, 101, 109, 111, 114, 121, 0], "i8", 2);
        F.s = w([40, 40, 117, 105, 110, 116, 51, 50, 41, 112, 95, 110, 101, 119, 32, 38, 32, 40, 67, 82, 78, 68, 95, 77, 73, 78, 95, 65, 76, 76, 79, 67, 95, 65, 76, 73, 71, 78, 77, 69, 78, 84, 32, 45, 32, 49, 41, 41, 32, 61, 61, 32, 48, 0], "i8", 2);
        F.ob = w([99, 114, 110, 100, 95, 114, 101, 97, 108, 108, 111, 99, 58, 32, 98, 97, 100, 32, 112, 116, 114, 0], "i8", 2);
        F.pb = w([99, 114, 110, 100, 95, 102, 114, 101, 101, 58, 32, 98, 97, 100, 32, 112, 116, 114, 0], "i8", 2);
        F.$d = w([99, 114, 110, 100, 95, 109, 115, 105, 122, 101, 58, 32, 98, 97, 100, 32, 112, 116, 114, 0], "i8", 2);
        w([1, 0, 0, 0, 2, 0, 0, 0, 4, 0, 0, 0, 8, 0, 0, 0, 16, 0, 0, 0, 32, 0, 0, 0, 64, 0, 0, 0, 128, 0, 0, 0, 256, 0, 0, 0, 512, 0, 0, 0, 1024, 0, 0, 0, 2048, 0, 0, 0, 4096, 0, 0, 0, 8192, 0, 0, 0, 16384, 0, 0, 0, 32768, 0, 0, 0, 65536, 0, 0, 0, 131072, 0, 0, 0, 262144, 0, 0, 0, 524288, 0, 0, 0, 1048576, 0, 0, 0, 2097152, 0, 0, 0, 4194304, 0, 0, 0, 8388608, 0, 0, 0, 16777216, 0, 0, 0, 33554432, 0, 0, 0, 67108864, 0, 0, 0, 134217728, 0, 0, 0, 268435456, 0, 0, 0, 536870912, 0, 0, 0, 1073741824, 0, 0, 0, -2147483648, 0, 0, 0], ["i32", 0, 0, 0, "i32", 0, 0, 0, "i32", 0, 0, 0, "i32", 0, 0, 0, "i32", 0, 0, 0, "i32", 0, 0, 0, "i32", 0, 0, 0, "i32", 0, 0, 0, "i32", 0, 0, 0, "i32", 0, 0, 0, "i32", 0, 0, 0, "i32", 0, 0, 0, "i32", 0, 0, 0, "i32", 0, 0, 0, "i32", 0, 0, 0, "i32", 0, 0, 0, "i32", 0, 0, 0, "i32", 0, 0, 0, "i32", 0, 0, 0, "i32", 0, 0, 0, "i32", 0, 0, 0, "i32", 0, 0, 0, "i32", 0, 0, 0, "i32", 0, 0, 0, "i32", 0, 0, 0, "i32", 0, 0, 0, "i32", 0, 0, 0, "i32", 0, 0, 0, "i32", 0, 0, 0, "i32", 0, 0, 0, "i32", 0, 0, 0, "i32", 0, 0, 0], 2);
        F.xb = w([102, 97, 108, 115, 101, 0], "i8", 2);
        F.ee = w([99, 114, 110, 100, 95, 118, 97, 108, 105, 100, 97, 116, 101, 95, 102, 105, 108, 101, 40, 38, 110, 101, 119, 95, 104, 101, 97, 100, 101, 114, 44, 32, 97, 99, 116, 117, 97, 108, 95, 98, 97, 115, 101, 95, 100, 97, 116, 97, 95, 115, 105, 122, 101, 44, 32, 78, 85, 76, 76, 41, 0], "i8", 2);
        F.he = w([40, 116, 111, 116, 97, 108, 95, 115, 121, 109, 115, 32, 62, 61, 32, 49, 41, 32, 38, 38, 32, 40, 116, 111, 116, 97, 108, 95, 115, 121, 109, 115, 32, 60, 61, 32, 112, 114, 101, 102, 105, 120, 95, 99, 111, 100, 105, 110, 103, 58, 58, 99, 77, 97, 120, 83, 117, 112, 112, 111, 114, 116, 101, 100, 83, 121, 109, 115, 41, 32, 38, 38, 32, 40, 99, 111, 100, 101, 95, 115, 105, 122, 101, 95, 108, 105, 109, 105, 116, 32, 62, 61, 32, 49, 41, 0], "i8", 2);
        F.yb = w([40, 116, 111, 116, 97, 108, 95, 115, 121, 109, 115, 32, 62, 61, 32, 49, 41, 32, 38, 38, 32, 40, 116, 111, 116, 97, 108, 95, 115, 121, 109, 115, 32, 60, 61, 32, 112, 114, 101, 102, 105, 120, 95, 99, 111, 100, 105, 110, 103, 58, 58, 99, 77, 97, 120, 83, 117, 112, 112, 111, 114, 116, 101, 100, 83, 121, 109, 115, 41, 0], "i8", 2);
        F.U = w([17, 18, 19, 20, 0, 8, 7, 9, 6, 10, 5, 11, 4, 12, 3, 13, 2, 14, 1, 15, 16], "i8", 2);
        F.v = w([48, 0], "i8", 2);
        F.zb = w([110, 117, 109, 95, 98, 105, 116, 115, 32, 60, 61, 32, 51, 50, 85, 0], "i8", 2);
        F.Bb = w([109, 95, 98, 105, 116, 95, 99, 111, 117, 110, 116, 32, 60, 61, 32, 99, 66, 105, 116, 66, 117, 102, 83, 105, 122, 101, 0], "i8", 2);
        F.Cb = w([116, 32, 33, 61, 32, 99, 85, 73, 78, 84, 51, 50, 95, 77, 65, 88, 0], "i8", 2);
        F.Db = w([109, 111, 100, 101, 108, 46, 109, 95, 99, 111, 100, 101, 95, 115, 105, 122, 101, 115, 91, 115, 121, 109, 93, 32, 61, 61, 32, 108, 101, 110, 0], "i8", 2);
        w([1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 0, 0, 0, 8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 0, 0, 0, 4, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 8, 0, 0, 0, 4, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 8, 0, 0, 0, 3, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 8, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 0, 0, 0, 4, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 4, 0, 0, 0, 4, 0, 0, 0, 7, 0, 0, 0, 4, 0, 0, 0, 4, 0, 0, 0, 4, 0, 0, 0, 4, 0, 0, 0, 8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 8, 0, 0, 0, 4, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 4, 0, 0, 0, 5, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 4, 0, 0, 0, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 8, 0, 0, 0, 3, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 4, 0, 0, 0, 6, 0, 0, 0, 4, 0, 0, 0, 4, 0, 0, 0, 4, 0, 0, 0, 4, 0, 0, 0, 8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 8, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 4, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 4, 0, 0, 0, 4, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 4, 0, 0, 0, 5, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 4, 0, 0, 0, 6, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 4, 0, 0, 0, 4, 0, 0, 0, 7, 0, 0, 0, 4, 0, 0, 0, 4, 0, 0, 0, 4, 0, 0, 0, 4, 0, 0, 0, 8, 0, 0, 0], ["i32", 0, 0, 0, "i32", 0, 0, 0, "i32", 0, 0, 0, "i32", 0, 0, 0, "i32", 0, 0, 0, "i32", 0, 0, 0, "i32", 0, 0, 0, "i32", 0, 0, 0, "i32", 0, 0, 0, "i32", 0, 0, 0, "i32", 0, 0, 0, "i32", 0, 0, 0, "i32", 0, 0, 0, "i32", 0, 0, 0, "i32", 0, 0, 0, "i32", 0, 0, 0, "i32", 0, 0, 0, "i32", 0, 0, 0, "i32", 0, 0, 0, "i32", 0, 0, 0, "i32", 0, 0, 0, "i32", 0, 0, 0, "i32", 0, 0, 0, "i32", 0, 0, 0, "i32", 0, 0, 0, "i32", 0, 0, 0, "i32", 0, 0, 0, "i32", 0, 0, 0, "i32", 0, 0, 0, "i32", 0, 0, 0, "i32", 0, 0, 0, "i32", 0, 0, 0, "i32", 0, 0, 0, "i32", 0, 0, 0, "i32", 0, 0, 0, "i32", 0, 0, 0, "i32", 0, 0, 0, "i32", 0, 0, 0, "i32", 0, 0, 0, "i32", 0, 0, 0, "i32", 0, 0, 0, "i32", 0, 0, 0, "i32", 0, 0, 0, "i32", 0, 0, 0, "i32", 0, 0, 0, "i32", 0, 0, 0, "i32", 0, 0, 0, "i32", 0, 0, 0, "i32", 0, 0, 0, "i32", 0, 0, 0, "i32", 0, 0, 0, "i32", 0, 0, 0, "i32", 0, 0, 0, "i32", 0, 0, 0, "i32", 0, 0, 0, "i32", 0, 0, 0, "i32", 0, 0, 0, "i32", 0, 0, 0, "i32", 0, 0, 0, "i32", 0, 0, 0, "i32", 0, 0, 0, "i32", 0, 0, 0, "i32", 0, 0, 0, "i32", 0, 0, 0, "i32", 0, 0, 0, "i32", 0, 0, 0, "i32", 0, 0, 0, "i32", 0, 0, 0, "i32", 0, 0, 0, "i32", 0, 0, 0, "i32", 0, 0, 0, "i32", 0, 0, 0, "i32", 0, 0, 0, "i32", 0, 0, 0, "i32", 0, 0, 0, "i32", 0, 0, 0, "i32", 0, 0, 0, "i32", 0, 0, 0, "i32", 0, 0, 0, "i32", 0, 0, 0, "i32", 0, 0, 0, "i32", 0, 0, 0, "i32", 0, 0, 0, "i32", 0, 0, 0, "i32", 0, 0, 0, "i32", 0, 0, 0, "i32", 0, 0, 0, "i32", 0, 0, 0, "i32", 0, 0, 0, "i32", 0, 0, 0, "i32", 0, 0, 0, "i32", 0, 0, 0, "i32", 0, 0, 0, "i32", 0, 0, 0, "i32", 0, 0, 0, "i32", 0, 0, 0, "i32", 0, 0, 0, "i32", 0, 0, 0, "i32", 0, 0, 0, "i32", 0, 0, 0, "i32", 0, 0, 0, "i32", 0, 0, 0, "i32", 0, 0, 0, "i32", 0, 0, 0, "i32", 0, 0, 0, "i32", 0, 0, 0, "i32", 0, 0, 0, "i32", 0, 0, 0, "i32", 0, 0, 0, "i32", 0, 0, 0, "i32", 0, 0, 0, "i32", 0, 0, 0, "i32", 0, 0, 0, "i32", 0, 0, 0, "i32", 0, 0, 0, "i32", 0, 0, 0, "i32", 0, 0, 0, "i32", 0, 0, 0, "i32", 0, 0, 0, "i32", 0, 0, 0, "i32", 0, 0, 0, "i32", 0, 0, 0, "i32", 0, 0, 0, "i32", 0, 0, 0, "i32", 0, 0, 0, "i32", 0, 0, 0, "i32", 0, 0, 0, "i32", 0, 0, 0, "i32", 0, 0, 0, "i32", 0, 0, 0, "i32", 0, 0, 0, "i32", 0, 0, 0, "i32", 0, 0, 0, "i32", 0, 0, 0, "i32", 0, 0, 0, "i32", 0, 0, 0, "i32", 0, 0, 0, "i32", 0, 0, 0, "i32", 0, 0, 0, "i32", 0, 0, 0, "i32", 0, 0, 0, "i32", 0, 0, 0, "i32", 0, 0, 0, "i32", 0, 0, 0, "i32", 0, 0, 0, "i32", 0, 0, 0, "i32", 0, 0, 0, "i32", 0, 0, 0, "i32", 0, 0, 0, "i32", 0, 0, 0, "i32", 0, 0, 0, "i32", 0, 0, 0, "i32", 0, 0, 0, "i32", 0, 0, 0, "i32", 0, 0, 0, "i32", 0, 0, 0, "i32", 0, 0, 0, "i32", 0, 0, 0, "i32", 0, 0, 0, "i32", 0, 0, 0, "i32", 0, 0, 0, "i32", 0, 0, 0, "i32", 0, 0, 0, "i32", 0, 0, 0, "i32", 0, 0, 0, "i32", 0, 0, 0, "i32", 0, 0, 0, "i32", 0, 0, 0], 2);
        w([0, 0, 0, 0, 0, 0, 0, 0, 8, 0, 0, 0, 8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 0, 0, 0, 4, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 8, 0, 0, 0, 4, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 8, 0, 0, 0, 3, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 8, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 4, 0, 0, 0, 5, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 4, 0, 0, 0, 6, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 4, 0, 0, 0, 4, 0, 0, 0, 7, 0, 0, 0, 4, 0, 0, 0, 4, 0, 0, 0, 4, 0, 0, 0, 4, 0, 0, 0, 8, 0, 0, 0], ["i32", 0, 0, 0, "i32", 0, 0, 0, "i32", 0, 0, 0, "i32", 0, 0, 0, "i32", 0, 0, 0, "i32", 0, 0, 0, "i32", 0, 0, 0, "i32", 0, 0, 0, "i32", 0, 0, 0, "i32", 0, 0, 0, "i32", 0, 0, 0, "i32", 0, 0, 0, "i32", 0, 0, 0, "i32", 0, 0, 0, "i32", 0, 0, 0, "i32", 0, 0, 0, "i32", 0, 0, 0, "i32", 0, 0, 0, "i32", 0, 0, 0, "i32", 0, 0, 0, "i32", 0, 0, 0, "i32", 0, 0, 0, "i32", 0, 0, 0, "i32", 0, 0, 0, "i32", 0, 0, 0, "i32", 0, 0, 0, "i32", 0, 0, 0, "i32", 0, 0, 0, "i32", 0, 0, 0, "i32", 0, 0, 0, "i32", 0, 0, 0, "i32", 0, 0, 0, "i32", 0, 0, 0, "i32", 0, 0, 0, "i32", 0, 0, 0, "i32", 0, 0, 0, "i32", 0, 0, 0, "i32", 0, 0, 0, "i32", 0, 0, 0, "i32", 0, 0, 0, "i32", 0, 0, 0, "i32", 0, 0, 0, "i32", 0, 0, 0, "i32", 0, 0, 0, "i32", 0, 0, 0], 2);
        F.Rd = w([0, 3, 1, 2], "i8", 2);
        F.c = w([0, 2, 3, 1], "i8", 2);
        F.Sd = w([0, 7, 1, 2, 3, 4, 5, 6], "i8", 2);
        F.b = w([0, 2, 3, 4, 5, 6, 7, 1], "i8", 2);
        F.vc = w([1, 0, 5, 4, 3, 2, 6, 7], "i8", 2);
        F.Vd = w([1, 0, 7, 6, 5, 4, 3, 2], "i8", 2);
        F.le = w([105, 110, 100, 101, 120, 32, 60, 32, 50, 0], "i8", 2);
        F.ne = w([40, 108, 111, 32, 60, 61, 32, 48, 120, 70, 70, 70, 70, 85, 41, 32, 38, 38, 32, 40, 104, 105, 32, 60, 61, 32, 48, 120, 70, 70, 70, 70, 85, 41, 0], "i8", 2);
        F.oe = w([40, 120, 32, 60, 32, 99, 68, 88, 84, 66, 108, 111, 99, 107, 83, 105, 122, 101, 41, 32, 38, 38, 32, 40, 121, 32, 60, 32, 99, 68, 88, 84, 66, 108, 111, 99, 107, 83, 105, 122, 101, 41, 0], "i8", 2);
        F.pe = w([118, 97, 108, 117, 101, 32, 60, 61, 32, 48, 120, 70, 70, 0], "i8", 2);
        F.qe = w([118, 97, 108, 117, 101, 32, 60, 61, 32, 48, 120, 70, 0], "i8", 2);
        F.re = w([40, 108, 111, 32, 60, 61, 32, 48, 120, 70, 70, 41, 32, 38, 38, 32, 40, 104, 105, 32, 60, 61, 32, 48, 120, 70, 70, 41, 0], "i8", 2);
        F.l = w([105, 32, 60, 32, 109, 95, 115, 105, 122, 101, 0], "i8", 2);
        F.D = w([110, 117, 109, 32, 38, 38, 32, 40, 110, 117, 109, 32, 61, 61, 32, 126, 110, 117, 109, 95, 99, 104, 101, 99, 107, 41, 0], "i8", 2);
        F.g = w([1, 2, 2, 3, 3, 3, 3, 4], "i8", 2);
        var kb = w([0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 1, 0, 0, 1, 2, 1, 2, 0, 0, 0, 1, 0, 2, 1, 0, 2, 0, 0, 1, 2, 3], "i8", 2);
        F.Gb = w([110, 101, 120, 116, 95, 108, 101, 118, 101, 108, 95, 111, 102, 115, 32, 62, 32, 99, 117, 114, 95, 108, 101, 118, 101, 108, 95, 111, 102, 115, 0], "i8", 2);
        F.Ib = w([40, 108, 101, 110, 32, 62, 61, 32, 49, 41, 32, 38, 38, 32, 40, 108, 101, 110, 32, 60, 61, 32, 99, 77, 97, 120, 69, 120, 112, 101, 99, 116, 101, 100, 67, 111, 100, 101, 83, 105, 122, 101, 41, 0], "i8", 2);
        var v = w(468, ["i32", 0, 0, 0, "i32", 0, 0, 0, "i32", 0, 0, 0, "i32", 0, 0, 0, "*", 0, 0, 0, "*", 0, 0, 0, "*", 0, 0, 0, "i32", 0, 0, 0, "i32", 0, 0, 0, "i32", 0, 0, 0, "*", 0, 0, 0, "*", 0, 0, 0, "*", 0, 0, 0, "*", 0, 0, 0, "*", 0, 0, 0, "*", 0, 0, 0, "*", 0, 0, 0, "*", 0, 0, 0, "*", 0, 0, 0, "*", 0, 0, 0, "*", 0, 0, 0, "*", 0, 0, 0, "*", 0, 0, 0, "*", 0, 0, 0, "*", 0, 0, 0, "*", 0, 0, 0, "*", 0, 0, 0, "*", 0, 0, 0, "*", 0, 0, 0, "*", 0, 0, 0, "*", 0, 0, 0, "*", 0, 0, 0, "*", 0, 0, 0, "*", 0, 0, 0, "*", 0, 0, 0, "*", 0, 0, 0, "*", 0, 0, 0, "*", 0, 0, 0, "*", 0, 0, 0, "*", 0, 0, 0, "*", 0, 0, 0, "*", 0, 0, 0, "*", 0, 0, 0, "*", 0, 0, 0, "*", 0, 0, 0, "*", 0, 0, 0, "*", 0, 0, 0, "*", 0, 0, 0, "*", 0, 0, 0, "*", 0, 0, 0, "*", 0, 0, 0, "*", 0, 0, 0, "*", 0, 0, 0, "*", 0, 0, 0, "*", 0, 0, 0, "*", 0, 0, 0, "*", 0, 0, 0, "*", 0, 0, 0, "*", 0, 0, 0, "*", 0, 0, 0, "*", 0, 0, 0, "*", 0, 0, 0, "*", 0, 0, 0, "*", 0, 0, 0, "*", 0, 0, 0, "*", 0, 0, 0, "*", 0, 0, 0, "*", 0, 0, 0, "*", 0, 0, 0, "*", 0, 0, 0, "*", 0, 0, 0, "*", 0, 0, 0, "*", 0, 0, 0, "*", 0, 0, 0, "*", 0, 0, 0, "*", 0, 0, 0, "*", 0, 0, 0, "*", 0, 0, 0, "*", 0, 0, 0, "*", 0, 0, 0, "*", 0, 0, 0, "*", 0, 0, 0, "*", 0, 0, 0, "*", 0, 0, 0, "*", 0, 0, 0, "*", 0, 0, 0, "*", 0, 0, 0, "*", 0, 0, 0, "*", 0, 0, 0, "*", 0, 0, 0, "*", 0, 0, 0, "*", 0, 0, 0, "*", 0, 0, 0, "*", 0, 0, 0, "*", 0, 0, 0, "*", 0, 0, 0, "*", 0, 0, 0, "*", 0, 0, 0, "*", 0, 0, 0, "*", 0, 0, 0, "*", 0, 0, 0, "*", 0, 0, 0, "*", 0, 0, 0, "*", 0, 0, 0, "*", 0, 0, 0, "*", 0, 0, 0, "*", 0, 0, 0, "*", 0, 0, 0, "i32", 0, 0, 0, "i32", 0, 0, 0, "i32", 0, 0, 0, "*", 0, 0, 0, "i32", 0, 0, 0, "*", 0, 0, 0, "i32", 0, 0, 0, "*", 0, 0, 0, "i32", 0, 0, 0], 2);
        var ab = w(24, "i32", 2);
        F.se = w([109, 97, 120, 32, 115, 121, 115, 116, 101, 109, 32, 98, 121, 116, 101, 115, 32, 61, 32, 37, 49, 48, 108, 117, 10, 0], "i8", 2);
        F.Yd = w([115, 121, 115, 116, 101, 109, 32, 98, 121, 116, 101, 115, 32, 32, 32, 32, 32, 61, 32, 37, 49, 48, 108, 117, 10, 0], "i8", 2);
        F.ie = w([105, 110, 32, 117, 115, 101, 32, 98, 121, 116, 101, 115, 32, 32, 32, 32, 32, 61, 32, 37, 49, 48, 108, 117, 10, 0], "i8", 2);
        w([0], "i8", 2);
        w(1, "void ()*", 2);
        var Ee = w([0, 0, 0, 0, 0, 0, 0, 0, 6, 0, 0, 0, 8, 0, 0, 0, 10, 0, 0, 0], ["*", 0, 0, 0, "*", 0, 0, 0, "*", 0, 0, 0, "*", 0, 0, 0, "*", 0, 0, 0], 2);
        w(1, "void*", 2);
        F.Hb = w([115, 116, 100, 58, 58, 98, 97, 100, 95, 97, 108, 108, 111, 99, 0], "i8", 2);
        var Me = w([0, 0, 0, 0, 0, 0, 0, 0, 6, 0, 0, 0, 12, 0, 0, 0, 14, 0, 0, 0], ["*", 0, 0, 0, "*", 0, 0, 0, "*", 0, 0, 0, "*", 0, 0, 0, "*", 0, 0, 0], 2);
        w(1, "void*", 2);
        F.ub = w([98, 97, 100, 95, 97, 114, 114, 97, 121, 95, 110, 101, 119, 95, 108, 101, 110, 103, 116, 104, 0], "i8", 2);
        F.da = w([83, 116, 57, 98, 97, 100, 95, 97, 108, 108, 111, 99, 0], "i8", 2);
        var Yc = w(12, "*", 2);
        F.W = w([83, 116, 50, 48, 98, 97, 100, 95, 97, 114, 114, 97, 121, 95, 110, 101, 119, 95, 108, 101, 110, 103, 116, 104, 0], "i8", 2);
        var kd = w(12, "*", 2);
        b[Ee + 4 >> 2] = Yc;
        b[Me + 4 >> 2] = kd;
        var Ne = w([2, 0, 0, 0, 0], ["i8*", 0, 0, 0, 0], 2);
        b[Yc >> 2] = Ne + 8 | 0;
        b[Yc + 4 >> 2] = F.da | 0;
        b[Yc + 8 >> 2] = void 0;
        b[kd >> 2] = Ne + 8 | 0;
        b[kd + 4 >> 2] = F.W | 0;
        b[kd + 8 >> 2] = Yc;
        var Nb = [0, 0, function(a, c, d, e) {
            0 == (a | 0) ? (a = zc(c),
            0 == (d | 0) ? d = a : (c = 0 == (a | 0) ? 0 : zd(a),
            b[d >> 2] = c,
            d = a)) : 0 == (c | 0) ? (Jc(a),
            0 != (d | 0) && (b[d >> 2] = 0),
            d = 0) : (e ? (c = ig(a, c),
            0 == (c | 0) ? c = 0 : a = c) : c = 0,
            0 != (d | 0) && (a = zd(a),
            b[d >> 2] = a),
            d = c);
            return d
        }
        , 0, function(a) {
            return 0 == (a | 0) ? 0 : zd(a)
        }
        , 0, Ad, 0, function(a) {
            Ad(a);
            Fe(a)
        }
        , 0, function() {
            return F.Hb | 0
        }
        , 0, function(a) {
            Ad(a | 0);
            Fe(a)
        }
        , 0, function() {
            return F.ub | 0
        }
        , 0, rb, 0, function(a, c) {
            b[a >> 2] = 0;
            Vd(a + 4 | 0);
            b[a + 20 >> 2] = 0;
            kf(a, c)
        }
        , 0, sb, 0, Yd, 0, De, 0, function(a) {
            De(a | 0);
            b[a >> 2] = Me + 8 | 0
        }
        , 0];
        N.FUNCTION_TABLE = Nb;
        N.run = He;
        L(Le);
        N.noInitialRun && (Fd++,
        N.monitorRunDependencies && N.monitorRunDependencies(Fd));
        0 == Fd && He();
        this.a = N
    }
    ;
    function Se(n, r, p) {
        this.b = new $c(n);
        this.g = r;
        this.a = new Lc;
        this.c = p
    }
    function Te(n) {
        for (var r = n.b, p; p = ad(r); )
            switch (p) {
            case 2:
                p = r.b();
                ld(r, r.a + p);
                n.a.textures.push(Ue(r, n.g));
                md(r);
                break;
            case 3:
                p = r.b();
                ld(r, r.a + p);
                var G;
                p = n.b;
                for (var x = new Zc; G = ad(p); )
                    switch (G) {
                    case 1:
                        G = p.b();
                        var E = G / 6
                          , w = new Float64Array(5 * E);
                        var I = p.data();
                        var L = p.a;
                        for (var K = 0; K < E; ++K) {
                            var H = L + 6 * K
                              , J = I[H]
                              , O = I[H + 1]
                              , T = I[H + 2]
                              , M = I[H + 3]
                              , Z = I[H + 4];
                            H = I[H + 5];
                            127 < M && (M -= 256);
                            T += M << 8;
                            127 < H && (H -= 256);
                            Z += H << 8;
                            M = 2 * Math.PI * J / 256;
                            J = Math.cos(M);
                            M = Math.sin(M);
                            O /= 255;
                            w[5 * K] = 1 + (O - 1) * J * J;
                            w[5 * K + 1] = (O - 1) * J * M;
                            w[5 * K + 2] = 1 + (O - 1) * M * M;
                            w[5 * K + 3] = T;
                            w[5 * K + 4] = Z
                        }
                        x.transformTable = w;
                        Kd(p, G);
                        break;
                    case 2:
                        G = p.b();
                        E = G / 2;
                        w = new Uint16Array(E);
                        I = p.data();
                        L = p.a;
                        for (K = 0; K < E; ++K)
                            w[K] = I[L + 2 * K] + (I[L + 2 * K + 1] << 8);
                        x.vertexTransformMap = w;
                        Kd(p, G);
                        break;
                    case 3:
                        x.meshId = p.b();
                        break;
                    default:
                        nd(p)
                    }
                p = x;
                n.a.transformInfo[p.meshId] = p;
                md(r);
                break;
            case 4:
                p = r.b() / 4;
                n.a.projectionOrigin = new Float32Array(p);
                for (x = 0; x < p; ++x)
                    n.a.projectionOrigin[x] = od(r);
                break;
            default:
                nd(r)
            }
        r = [];
        p = n.a.textures;
        for (x = 0; x < p.length; x++)
            r.push(p[x].bytes.buffer);
        for (x = 0; x < n.a.transformInfo.length; ++x)
            n.a.transformInfo[x] && (r.push(n.a.transformInfo[x].transformTable.buffer),
            r.push(n.a.transformInfo[x].vertexTransformMap.buffer),
            G = p[n.a.transformInfo[x].meshId],
            G = new Float32Array([.5, .5 - G.height, 1 / G.width, -1 / G.height]),
            n.a.transformInfo[x].uvOffsetAndScale = G,
            r.push(G.buffer));
        n.a.projectionOrigin && r.push(n.a.projectionOrigin.buffer);
        n.c(n.a, r)
    }
    function Ue(n, r) {
        for (var p = n.data(), G, x = 1, E = 0, w = 0, I = 256, L = 256, K = 0, H = -1; G = ad(n); )
            switch (G) {
            case 1:
                w = n.m();
                w = w & 2147483648 ? (w & 2147483647) - 2147483648 : w;
                E || (E = n.a);
                Kd(n, w);
                break;
            case 3:
                I = n.b();
                break;
            case 4:
                L = n.b();
                break;
            case 2:
                x = n.b();
                break;
            case 5:
                K = n.b();
                break;
            case 6:
                H = n.b();
                break;
            default:
                nd(n)
            }
        n = new pc;
        switch (x) {
        case 1:
            n.bytes = new Uint8Array(w);
            n.bytes.set(p.subarray(E, E + w));
            break;
        case 6:
            Ve || (Ve = new Re);
            G = Ve;
            var J = G.a._malloc(w);
            G.a.HEAPU8.set(p.subarray(E, E + w), J);
            p = G.a._crn_get_decompressed_size(J, w);
            E = G.a._malloc(p);
            n.bytes = new Uint8Array(p);
            G.a._crn_decompress(J, w, E, p);
            n.bytes.set(G.a.HEAPU8.subarray(E, E + p), 0);
            G.a._free(J);
            G.a._free(E);
            if (!r) {
                r = new Uint16Array(n.bytes.buffer);
                w = I;
                J = L;
                p = new Uint16Array(w * J);
                Qe || (Qe = new Uint16Array(4));
                E = Qe;
                G = w / 4;
                for (var O = J / 4, T = 0; T < O; T++)
                    for (var M = 0; M < G; M++) {
                        J = 4 * (T * G + M);
                        E[0] = r[J];
                        E[1] = r[J + 1];
                        var Z = E[0] & 31;
                        var U = E[0] & 2016;
                        var ca = E[0] & 63488;
                        var Da = E[1] & 31;
                        var Aa = E[1] & 2016;
                        var Ua = E[1] & 63488;
                        E[2] = 5 * Z + 3 * Da >> 3 | 5 * U + 3 * Aa >> 3 & 2016 | 5 * ca + 3 * Ua >> 3 & 63488;
                        E[3] = 5 * Da + 3 * Z >> 3 | 5 * Aa + 3 * U >> 3 & 2016 | 5 * Ua + 3 * ca >> 3 & 63488;
                        U = 4 * T * w + 4 * M;
                        Z = r[J + 2];
                        p[U] = E[Z & 3];
                        p[U + 1] = E[Z >> 2 & 3];
                        p[U + 2] = E[Z >> 4 & 3];
                        p[U + 3] = E[Z >> 6 & 3];
                        U += w;
                        p[U] = E[Z >> 8 & 3];
                        p[U + 1] = E[Z >> 10 & 3];
                        p[U + 2] = E[Z >> 12 & 3];
                        p[U + 3] = E[Z >> 14];
                        Z = r[J + 3];
                        U += w;
                        p[U] = E[Z & 3];
                        p[U + 1] = E[Z >> 2 & 3];
                        p[U + 2] = E[Z >> 4 & 3];
                        p[U + 3] = E[Z >> 6 & 3];
                        U += w;
                        p[U] = E[Z >> 8 & 3];
                        p[U + 1] = E[Z >> 10 & 3];
                        p[U + 2] = E[Z >> 12 & 3];
                        p[U + 3] = E[Z >> 14]
                    }
                n.bytes = new Uint8Array(p.buffer)
            }
        }
        n.textureFormat = x;
        n.width = I;
        n.height = L;
        n.viewDirection = K;
        n.meshId = H;
        return n
    }
    var Ve = null;
    function We(n, r, p, G) {
        this.b = new $c(n);
        this.s = r;
        this.g = p;
        this.a = new Lb;
        this.l = [];
        this.m = G;
        this.c = null
    }
    function Xe(n) {
        for (var r = n.b, p; p = ad(r); )
            switch (p) {
            case 1:
                p = r.b() / 8;
                for (var G = n.a.matrixGlobeFromMesh = new Float64Array(16), x = 0; x < p; x++)
                    G[x] = pd(r);
                n.a.matrixMeshFromGlobe = new Float64Array(16);
                p = n.a.matrixMeshFromGlobe;
                x = G[0];
                var E = G[1]
                  , w = G[2]
                  , I = G[3]
                  , L = G[4]
                  , K = G[5]
                  , H = G[6]
                  , J = G[7]
                  , O = G[8]
                  , T = G[9]
                  , M = G[10]
                  , Z = G[11]
                  , U = G[12]
                  , ca = G[13]
                  , Da = G[14];
                G = G[15];
                var Aa = x * K - E * L
                  , Ua = x * H - w * L
                  , ta = x * J - I * L
                  , Va = E * H - w * K
                  , ja = E * J - I * K
                  , Oa = w * J - I * H
                  , Qa = O * ca - T * U
                  , cc = O * Da - M * U
                  , rc = O * G - Z * U
                  , Ob = T * Da - M * ca
                  , dc = T * G - Z * ca
                  , Pb = M * G - Z * Da
                  , Ta = Aa * Pb - Ua * dc + ta * Ob + Va * rc - ja * cc + Oa * Qa;
                0 != Ta && (Ta = 1 / Ta,
                p[0] = (K * Pb - H * dc + J * Ob) * Ta,
                p[1] = (-E * Pb + w * dc - I * Ob) * Ta,
                p[2] = (ca * Oa - Da * ja + G * Va) * Ta,
                p[3] = (-T * Oa + M * ja - Z * Va) * Ta,
                p[4] = (-L * Pb + H * rc - J * cc) * Ta,
                p[5] = (x * Pb - w * rc + I * cc) * Ta,
                p[6] = (-U * Oa + Da * ta - G * Ua) * Ta,
                p[7] = (O * Oa - M * ta + Z * Ua) * Ta,
                p[8] = (L * dc - K * rc + J * Qa) * Ta,
                p[9] = (-x * dc + E * rc - I * Qa) * Ta,
                p[10] = (U * ja - ca * ta + G * Aa) * Ta,
                p[11] = (-O * ja + T * ta - Z * Aa) * Ta,
                p[12] = (-L * Ob + K * cc - H * Qa) * Ta,
                p[13] = (x * Ob - E * cc + w * Qa) * Ta,
                p[14] = (-U * Va + ca * Ua - Da * Aa) * Ta,
                p[15] = (O * Va - T * Ua + M * Aa) * Ta);
                break;
            case 2:
                p = r.b();
                ld(r, r.a + p);
                n.a.meshes.push(Ye(n));
                md(r);
                break;
            case 3:
                p = r.b();
                n.a.copyrightIds ? n.a.copyrightIds.push(p) : n.a.copyrightIds = [p];
                break;
            case 6:
                p = r.b();
                ld(r, r.a + p);
                n.a.waterMesh = Ye(n);
                md(r);
                break;
            case 7:
                p = r.b();
                ld(r, r.a + p);
                n.a.overlaySurfaceMeshes.push(Ye(n));
                md(r);
                break;
            case 8:
                if (n.g) {
                    p = n;
                    x = p.b;
                    E = x.data();
                    w = x.b();
                    I = x.a;
                    L = E[I] + (E[I + 1] << 8);
                    K = E[I + 2];
                    I += 3;
                    p.c = new Uint8Array(3 * L);
                    for (H = 0; H < w; ++H)
                        O = E[I + H],
                        J = E[I + L + H],
                        O = Ze(O, K),
                        J = Ze(J, K),
                        M = O / 255,
                        U = J / 255,
                        J = p.c,
                        O = 3 * H,
                        Z = M,
                        T = U,
                        ca = Z + T,
                        Da = Z - T,
                        G = 1,
                        .5 <= ca && 1.5 >= ca && -.5 <= Da && .5 >= Da || (G = -1,
                        .5 >= ca ? (Z = .5 - U,
                        T = .5 - M) : 1.5 <= ca ? (Z = 1.5 - U,
                        T = 1.5 - M) : -.5 >= Da ? (Z = U - .5,
                        T = M + .5) : (Z = U + .5,
                        T = M - .5),
                        ca = Z + T,
                        Da = Z - T),
                        M = $e($e(2 * ca - 1, 3 - 2 * ca), $e(2 * Da + 1, 1 - 2 * Da)) * G,
                        Z = 2 * Z - 1,
                        T = 2 * T - 1,
                        U = 127 / Math.sqrt(M * M + Z * Z + T * T),
                        J[O + 0] = af(U * M + 127),
                        J[O + 1] = af(U * Z + 127),
                        J[O + 2] = af(U * T + 127);
                    Kd(x, w)
                } else
                    nd(r);
                break;
            default:
                nd(r)
            }
        r = n.a;
        p = r.meshes.slice();
        for (x = 0; x < r.overlaySurfaceMeshes.length; x++)
            p.push(r.overlaySurfaceMeshes[x]);
        r.waterMesh && p.push(r.waterMesh);
        if (0 != p.length) {
            r = new Oe(p);
            for (p = r.start(); null != p; )
                p = p.apply(r);
            n.a.bvhNodes = r.l;
            n.a.bvhTriPermutation = r.c
        }
        if (n.g)
            for (r = 0; r < n.a.meshes.length; ++r)
                if (x = n,
                p = n.a.meshes[r],
                (E = p.normals) && x.c)
                    for (w = E.length / 2,
                    p.normals = new Uint8Array(4 * w),
                    I = 0; I < w; ++I)
                        L = E[I] + (E[w + I] << 8),
                        p.normals[4 * I] = x.c[3 * L],
                        p.normals[4 * I + 1] = x.c[3 * L + 1],
                        p.normals[4 * I + 2] = x.c[3 * L + 2],
                        p.normals[4 * I + 3] = 0;
                else
                    for (x = p.vertices.length / 8,
                    p.normals = new Uint8Array(4 * x),
                    E = 0; E < x; ++E)
                        p.normals[4 * E] = 127,
                        p.normals[4 * E + 1] = 127,
                        p.normals[4 * E + 2] = 127,
                        p.normals[4 * E + 3] = 0;
                        
        return n.a;
    }
    function Ye(n) {
        var r = n.b
          , p = new bc
          , G = [];
        n.l.push(G);
        for (var x; x = ad(r); )
            switch (x) {
            case 1:
                x = n.b;
                for (var E = x.data(), w = x.b(), I = w / 3, L = p.vertices = new Uint8Array(8 * I), K = x.a, H = 0; 2 >= H; H++) {
                    var J = E[K++];
                    L[H] = J;
                    for (var O = 1; O < I; O++)
                        J = J + E[K++] & 255,
                        L[8 * O + H] = J
                }
                Kd(x, w);
                break;
            case 3:
                x = n.b;
                x.b();
                E = x.b();
                w = p.indices = new Uint16Array(E);
                for (O = J = H = L = I = 0; O < E; O++) {
                    var T = x.b();
                    K = H;
                    H = J;
                    J = I - T;
                    w[O] = J;
                    K != H && H != J && K != J && L++;
                    T || I++
                }
                p.numNonDegenerateTriangles = L;
                break;
            case 6:
                x = r.b();
                ld(r, r.a + x);
                p.texture = Ue(r, n.s);
                md(r);
                break;
            case 7:
                x = n.b;
                E = x.data();
                w = (x.b() - 4) / 4;
                I = Jd(x);
                L = Jd(x);
                H = K = 0;
                J = x.a;
                O = p.vertices;
                for (T = 0; T < w; T++) {
                    var M = E[J + 1 * w + T] + (E[J + 3 * w + T] << 8);
                    K = (K + (E[J + 0 * w + T] + (E[J + 2 * w + T] << 8))) % (I + 1);
                    H = (H + M) % (L + 1);
                    M = 8 * T + 4;
                    O[M + 0] = K & 255;
                    O[M + 1] = K >> 8;
                    O[M + 2] = H & 255;
                    O[M + 3] = H >> 8
                }
                p.uvOffsetAndScale || (p.uvOffsetAndScale = new Float32Array([.5, .5, 1 / (I + 1), 1 / (L + 1)]));
                Kd(x, 4 * w);
                break;
            case 8:
                x = n.b;
                x.b();
                E = x.b();
                w = 0;
                I = p.layerBounds = new Uint32Array(10);
                L = 0;
                K = p.octantCounts = new Uint32Array(72);
                for (H = 0; H < E; H++)
                    0 == H % 8 && (I[L++] = w),
                    J = x.b(),
                    G.push(J),
                    K[8 * (L - 1) + (H & 7)] = J,
                    w += J;
                for (; 10 > L; L++)
                    I[L] = w;
                break;
            case 9:
                x = n.b;
                E = x.data();
                w = x.b();
                I = p.vertexAlphas = new Uint8Array(w);
                L = x.a;
                K = E[L++];
                I[0] = K;
                for (H = 1; H < w; H++)
                    K = K + E[L++] & 255,
                    I[H] = K;
                Kd(x, w);
                break;
            case 10:
                x = r.b() / 4;
                E = p.uvOffsetAndScale = new Float32Array(4);
                for (w = 0; w < x; w++)
                    E[w] = od(r);
                break;
            case 11:
                n.g ? (x = n.b,
                E = x.data(),
                w = x.b(),
                I = x.a,
                p.normals = new Uint8Array(E.buffer.slice(I, I + w)),
                Kd(x, w)) : nd(r);
                break;
            case 12:
                p.meshId = r.b();
                break;
            default:
                nd(r)
            }
        p.uvOffsetAndScale && (p.uvOffsetAndScale[1] -= 1 / p.uvOffsetAndScale[3],
        p.uvOffsetAndScale[3] *= -1);
        r = p.vertices;
        x = p.indices;
        for (w = E = 0; w < G.length; w++)
            for (I = w & 7,
            0 < G[w] && (n.a.nonEmptyOctants |= 1 << I),
            L = 0; L < G[w]; L++)
                K = 8 * x[E++] + 3,
                r[K] = I;
        return p
    }
    function Ze(n, r) {
        if (4 >= r)
            return (n << r) + (n & (1 << r) - 1);
        if (6 >= r) {
            var p = 8 - r;
            return (n << r) + (n << r >> p) + (n << r >> p >> p) + (n << r >> p >> p >> p)
        }
        return -(n & 1)
    }
    function $e(n, r) {
        return n < r ? n : r
    }
    function af(n) {
        n = Math.round(n);
        return $e(0 > n ? 0 : n, 255)
    }
    ;var bf = [];
    function ug(n, r) {
        var p = ub()
          , G = r.data.id
          , x = r.data.command;
        r = r.data.payload;
        var E = n.a;
        void 0 !== G && void 0 !== x && r && (n = new Uint8Array(r),
        r = function(w, I) {
            var L = ub() - p
              , K = bf;
            bf = [];
            E.postMessage({
                id: G,
                time: L,
                payload: w,
                logs: K,
                complete: !0
            }, I)
        }
        ,
        0 == x ? Md(new Ld(n,r)) : 1 == x ? Xe(new We(n,!0,!1,r)) : 2 == x ? Xe(new We(n,!1,!0,r)) : 3 == x ? Xe(new We(n,!0,!0,r)) : 4 == x ? Te(new Se(n,!0,r)) : 5 == x ? Te(new Se(n,!1,r)) : bf.push("Bad DecodeTaskCommand: " + x))
    }

    var XMLHttpRequest = require('xhr2');
    const fs = require('fs');
    const Path = require('path');

    var metaPath = 'https://kh.google.com/rt/earth/BulkMetadata/pb=!1m2!1s';
    var dataPath = 'https://kh.google.com/rt/earth/NodeData/pb=!1m2!1s';
    var rootMeta = 'https://kh.google.com/rt/earth/BulkMetadata/pb=!1m2!1s!2u874';
    var earthRadius = 6370995;
    	
    function getMetaUrl(rootPath, childPath, epoch)
    {
        return metaPath + rootPath + childPath + '!2u' + epoch;
    }

    function getDataUrl(data, index, childPath)
    {
        var result = dataPath + data.headNodePath + childPath + '!2u' + data.epoch[index] + '!2e' + (data.textureFormatArray == null ? data.defaultTextureFormat : data.textureFormatArray[index]);
        if (data.flags[index] & 16)
        {
            result = result + '!3u' + (data.imageryEpochArray == null ? data.defaultImageryEpoch : data.imageryEpochArray[index]);
        }
        return result + '!4b' + (data.availableViewDirectionsArray == null ? data.defaultAvailableViewDirections : data.availableViewDirectionsArray[index]); 
    }

    function createAndSendXhr(i, url, resolve)
    {
        var xhr = new XMLHttpRequest();
            xhr.open('GET', url, true);
            xhr.responseType = 'arraybuffer';
            xhr.onload = function(e) 
            {
                if (this.status == 200)
                {
                    if (i > 0)
                    {
                        console.log(`Loaded: ${url} after ${i} trials`);
                    }
                    var data = new Uint8Array(this.response);
                    resolve(data);
                }
                else
                {
                    var data = null
                }
            };
            xhr.onerror = function(e) 
            {
                console.log(`Failed with status ${this.status}: ${url}. Trying again...`);
                createAndSendXhr(++i, url, resolve);
                var data = null
            };
            xhr.send();  
    }

    function load(url)
    {
        return new Promise(function (resolve, reject) {
            createAndSendXhr(0, url, resolve);  
        });
    }

    function loadMeta(url)
    {
        return load(url).then(data => Md(new Ld(data, null)));
    }

    function loadData(url)
    {
        return load(url).then(data => Xe(new We(data, true, true, null)));
    }

    function getSeparatingPlane(RPos, Plane, box1, box2)
    {
        return Math.abs(dot(RPos, Plane)) > 
            (Math.abs(dot(mul(box1.AxisX, box1.Extent.x), Plane)) +
            Math.abs(dot(mul(box1.AxisY, box1.Extent.y), Plane)) +
            Math.abs(dot(mul(box1.AxisZ, box1.Extent.z), Plane)) +
            Math.abs(dot(mul(box2.AxisX, box2.Extent.x), Plane)) + 
            Math.abs(dot(mul(box2.AxisY, box2.Extent.y), Plane)) +
            Math.abs(dot(mul(box2.AxisZ, box2.Extent.z), Plane)));
    }

    function getCollision(box1, box2)
    {
        var RPos = sub(box2.Pos, box1.Pos);

        return !(getSeparatingPlane(RPos, box1.AxisX, box1, box2) ||
            getSeparatingPlane(RPos, box1.AxisY, box1, box2) ||
            getSeparatingPlane(RPos, box1.AxisZ, box1, box2) ||
            getSeparatingPlane(RPos, box2.AxisX, box1, box2) ||
            getSeparatingPlane(RPos, box2.AxisY, box1, box2) ||
            getSeparatingPlane(RPos, box2.AxisZ, box1, box2) ||
            getSeparatingPlane(RPos, vmul(box1.AxisX, box2.AxisX), box1, box2) ||
            getSeparatingPlane(RPos, vmul(box1.AxisX, box2.AxisY), box1, box2) ||
            getSeparatingPlane(RPos, vmul(box1.AxisX, box2.AxisZ), box1, box2) ||
            getSeparatingPlane(RPos, vmul(box1.AxisY, box2.AxisX), box1, box2) ||
            getSeparatingPlane(RPos, vmul(box1.AxisY, box2.AxisY), box1, box2) ||
            getSeparatingPlane(RPos, vmul(box1.AxisY, box2.AxisZ), box1, box2) ||
            getSeparatingPlane(RPos, vmul(box1.AxisZ, box2.AxisX), box1, box2) ||
            getSeparatingPlane(RPos, vmul(box1.AxisZ, box2.AxisY), box1, box2) ||
            getSeparatingPlane(RPos, vmul(box1.AxisZ, box2.AxisZ), box1, box2));
    }

    function sub(a, b)
    {
        var result = makeVector();
        result.x = a.x - b.x;
        result.y = a.y - b.y;
        result.z = a.z - b.z;
        return result;
    }

    function mul(a, b)
    {
        var result = makeVector();
        result.x = a.x * b;
        result.y = a.y * b;
        result.z = a.z * b;
        return result;
    }

    function dot(a, b)
    {
        return a.x * b.x + a.y * b.y + a.z * b.z;
    }

    function vmul(a, b)
    {
        var result = makeVector();
        result.x = a.y * b.z - a.z * b.y;
        result.y = a.z * b.x - a.x * b.z;
        result.z = a.x * b.y - a.y * b.x;
        return result;
    }

    function makeBoxFromData(data, i)
    {
        var result = makeBox();

        result.Pos.x = data.obbCenters[3 * i];
        result.Pos.y = data.obbCenters[3 * i + 1];
        result.Pos.z = data.obbCenters[3 * i + 2];

        result.Extent.x = data.obbExtents[3 * i];
        result.Extent.y = data.obbExtents[3 * i + 1];
        result.Extent.z = data.obbExtents[3 * i + 2];

        result.AxisX.x = data.obbRotations[9 * i];
        result.AxisX.y = data.obbRotations[9 * i + 3];
        result.AxisX.z = data.obbRotations[9 * i + 6];

        result.AxisY.x = data.obbRotations[9 * i + 1];
        result.AxisY.y = data.obbRotations[9 * i + 4];
        result.AxisY.z = data.obbRotations[9 * i + 7];

        result.AxisZ.x = data.obbRotations[9 * i + 2];
        result.AxisZ.y = data.obbRotations[9 * i + 5];
        result.AxisZ.z = data.obbRotations[9 * i + 8];

        return result;
    }

    function degToRad(angle)
    {
        return angle * Math.PI / 180;
    }

    function radToDeg(angle)
    {
        return angle * 180 / Math.PI;
    }

    function makeVector()
    {
        return {x : 0, y : 0, z : 0};
    }

    function makeBox()
    {
        var result = 
        {
            Pos : makeVector(),
            Extent : makeVector(),
            AxisX : makeVector(),
            AxisY : makeVector(),
            AxisZ : makeVector(),
        };
        return result;
    }

    function makeSurfaceBox(latDeg, longDeg, x, y)
    {
        var lat = degToRad(latDeg);
        var long = degToRad(longDeg);
        var result = makeBox();
        result.Pos.x = earthRadius * Math.cos(lat) * Math.cos(long);
        result.Pos.y = earthRadius * Math.cos(lat) * Math.sin(long);
        result.Pos.z = earthRadius * Math.sin(lat);
        result.Extent.x = 1000.0;
        result.Extent.y = x;
        result.Extent.z = y;
        result.AxisX.x = Math.cos(lat) * Math.cos(long);
        result.AxisX.y = Math.cos(lat) * Math.sin(long);
        result.AxisX.z = Math.sin(lat);
        result.AxisY.x = Math.sin(lat) * Math.cos(long);
        result.AxisY.y = Math.sin(lat) * Math.sin(long);
        result.AxisY.z = -Math.cos(lat);
        result.AxisZ.x = -Math.sin(long);
        result.AxisZ.y = Math.cos(long);
        result.AxisZ.z = 0;
        return result;
    }

    function transformPosition(size, vector)
    {
        var result = makeVector();
        result.x = (vector.z) * size[2];
        result.y = -(vector.y) * size[1];
        result.z = (vector.x) * size[0];
        return result;
    }

    function applyMatrix(matrix, vector)
    {
        var result = makeVector();
        result.x = matrix[0] * vector.x + matrix[4] * vector.y + matrix[8] * vector.z + matrix[12];
        result.y = matrix[1] * vector.x + matrix[5] * vector.y + matrix[9] * vector.z + matrix[13];
        result.z = matrix[2] * vector.x + matrix[6] * vector.y + matrix[10] * vector.z + matrix[14];
        return result;
    }

    function transformToParent(matrix, parentTransform, vector)
    {
        return transformPosition(parentTransform.scale, applyMatrix(parentTransform.matrix, applyMatrix(matrix, vector)));
    }

    function getMeta(matrix)
    {
        var scaleX = Math.sqrt(matrix[0] * matrix[0] + matrix[4] * matrix[4] + matrix[8] * matrix[8]);
        var scaleY = Math.sqrt(matrix[1] * matrix[1] + matrix[5] * matrix[5] + matrix[9] * matrix[9]);
        var scaleZ = Math.sqrt(matrix[2] * matrix[2] + matrix[6] * matrix[6] + matrix[10] * matrix[10]);
        var meta = 
        {
            position : 
            [
                radToDeg(Math.atan2(matrix[14], Math.sqrt(matrix[12] * matrix[12] + matrix[13] * matrix[13]))), 
                radToDeg(Math.atan2(matrix[13], matrix[12])),
                Math.sqrt(matrix[12] * matrix[12] + matrix[13] * matrix[13] + matrix[14] * matrix[14])
            ],
            size : [scaleX, scaleY, scaleZ]
        };
        return meta;
    }

    function writeObj(folder, id, data)
    {
        if (data.overlaySurfaceMeshes.length > 0)
        {
            //console.log(`Overlay surface meshes at ${id}`);
        }
        if (data.waterMesh != null)
        {
            //console.log(`Water mesh at ${id}`);
        }
        if (data.meshes.length == 0)
        {
            return;
        }

        var meta = getMeta(data.matrixGlobeFromMesh);

        if (id.length == minLod)
        {
            lodMap.set(id, { matrix: data.matrixMeshFromGlobe, scale: meta.size});
        }
        else
        {
            var parentTransform = lodMap.get(id.substring(0, minLod));
        }

        fs.writeFileSync(`${folder}\\${id}.pos`, JSON.stringify(meta.position));

        var mtlFile = fs.openSync(`${folder}\\${id}.mtl`, 'w');
        for (var meshIndex = 0; meshIndex < data.meshes.length; meshIndex++)
        {
            fs.writeSync(mtlFile, `newmtl ${meshIndex}\nmap_Kd ${id}_${meshIndex}.dds\n`);
            writeDds(`${folder}\\${id}_${meshIndex}.dds`, data.meshes[meshIndex].texture);
        }
        fs.closeSync(mtlFile);

        var objFile = fs.openSync(`${folder}\\${id}.obj`, 'w');
        var totalVertices = 1;
        var totalTextureIndices = 1;
        for (var meshIndex = 0; meshIndex < data.meshes.length; meshIndex++)
        {
            fs.writeSync(objFile, `mtlib ${id}.mtl\n`);
            fs.writeSync(objFile, 'o ' + meshIndex + '\n');
            fs.writeSync(objFile, `usemtl ${meshIndex}\n`);
            var mesh = data.meshes[meshIndex];
            var vCount = mesh.vertices.length / 8;
            var newIndices = new Map();
            var vertices = Array(vCount);
            var newVertices = [];
            var count = 0;
            for (var i = 0; i < vCount; i++)
            {
                var vertex = (mesh.vertices[8 * i] << 16) | (mesh.vertices[8 * i + 1] << 8) | mesh.vertices[8 * i + 2];
                if (!newIndices.has(vertex))
                {
                    vertices[i] = count;
                    newVertices.push(i);
                    newIndices.set(vertex, count++);
                }
                else
                {
                    vertices[i] = newIndices.get(vertex);
                }
            }
            for (var i = 0; i < count; i++)
            {
                var position = makeVector();
                position.x = mesh.vertices[8 * newVertices[i]];
                position.y = mesh.vertices[8 * newVertices[i] + 1];
                position.z = mesh.vertices[8 * newVertices[i] + 2];
                if (parentTransform === undefined)
                {
                    var transformed = transformPosition(meta.size, position);
                }
                else
                {
                    var transformed = transformToParent(data.matrixGlobeFromMesh, parentTransform, position);
                }
                fs.writeSync(objFile, 'v ' + transformed.x + ' ' + transformed.y + ' ' + transformed.z + '\n');
            }
            for (var i = 0; i < vCount; i++)
            {
                var u = ((mesh.vertices[8 * i + 4] & 255) + (mesh.vertices[8 * i + 5] << 8)) / (mesh.texture.width - 1);
                var v = ((mesh.vertices[8 * i + 6] & 255) + (mesh.vertices[8 * i + 7] << 8)) / (mesh.texture.height - 1);
                fs.writeSync(objFile, 'vt ' + u + ' ' + v + '\n');
            }
            if (mesh.indices.length > 2)
            {
                var index0 = vertices[mesh.indices[0]] + totalVertices;
                var index1 = vertices[mesh.indices[1]] + totalVertices;
                var flip = false;
                if (index0 != totalVertices && index1 != totalVertices && index0 != index1)
                {
                    fs.writeSync(objFile, 'f ' + totalVertices + '/' + totalTextureIndices + ' ' + index0 + '/' + (mesh.indices[0] + totalTextureIndices) + ' ' + 
                    index1 + '/' + (mesh.indices[1] + totalTextureIndices) + '\n');
                    flip = !flip;
                }
                for (var i = 0; i < (mesh.indices.length) - 2; i++)
                {
                    var tri = new Array(3);                         
                    tri[0] = vertices[mesh.indices[i]] + totalVertices;
                    tri[1] = vertices[mesh.indices[i + 1]] + totalVertices;
                    tri[2] = vertices[mesh.indices[i + 2]] + totalVertices;
                    if (tri[0] != tri[1] && tri[0] != tri[2] && tri[1] != tri[2])
                    {
                        if (flip)
                        {
                            fs.writeSync(objFile, 'f ' + tri[2] + '/' + (mesh.indices[i + 2] + totalTextureIndices) + ' '
                            + tri[1] + '/' + (mesh.indices[i + 1] + totalTextureIndices) + ' ' 
                            + tri[0] + '/' + (mesh.indices[i] + totalTextureIndices) + '\n');
                        }
                        else
                        {
                            fs.writeSync(objFile, 'f ' + tri[0] + '/' + (mesh.indices[i] + totalTextureIndices) + ' '
                            + tri[1] + '/' + (mesh.indices[i + 1] + totalTextureIndices) + ' ' 
                            + tri[2] + '/' + (mesh.indices[i + 2] + totalTextureIndices) + '\n');
                        }
                    }
                    flip = !flip;
                }
            }
            totalVertices += count;
            totalTextureIndices += vCount;
        }
        fs.closeSync(objFile);
    }

    function makeDDSHeader(height, width, format)
    {
        var result = new Int32Array(32);
        for (var i = 0; i < 32; i++)
        {
            result[i] = 0;
        }
        result[0] = 0x20534444;
        result[1] = 124;
        result[2] = 0x1 | 0x2 | 0x4 | 0x1000;
        result[3] = height;
        result[4] = width;
        result[19] = 32;
        if (format == 1)
        {
            result[20] = 0x40;
            result[22] = 32;
            result[23] = 0x00ff0000;
            result[24] = 0x0000ff00;
            result[25] = 0x000000ff;
            result[26] = 0xff000000;
        }
        else
        {
            result[20] = 0x4;
            result[21] = 0x31545844;
        }
        result[27] = 0x1000;
        return result.buffer;
    }

    function writeDds(path, texture)
    {
        var file = fs.openSync(path, 'w');
        fs.writeSync(file, Buffer.from(makeDDSHeader(texture.height, texture.width, texture.format)));
        fs.writeSync(file, Buffer.from(texture.bytes.buffer));
        fs.closeSync(file);
        console.log("Saved file: " + path);
    }

    var lodMap = new Map();
    var minLodIsInRange = [];

    async function downloadData(data)
    {
        for (const [key, value] of Object.entries(data.m))
        {
            if (data.m.hasOwnProperty(key))
            {
                let dataBox = makeBoxFromData(data.c, value);
                let currentLod = data.c.headNodePath.length + key.length;
                let dataId = data.c.headNodePath + key;
                let parentIsInRange = false

                if(currentLod > minLod) {
                    let minLodDataId = dataId.slice(0, minLod)
                    parentIsInRange = minLodIsInRange.includes(minLodDataId)
                }

                if (getCollision(box, dataBox) || parentIsInRange)
                {
                    if (!(data.c.flags[value] & 8) && currentLod <= maxLod && currentLod >= minLod)
                    {
                        let dataUrl = getDataUrl(data.c, value, key);

                        if( currentLod == minLod)
                        {
                            minLodIsInRange.push(dataId)
                        }

                        console.log("Data url: " + dataUrl);
                        await loadData(dataUrl).then(data => writeObj(outputFolder, dataId, data));
                    }
                    if (key.length == 4 && !(data.c.flags[value] & 8) && currentLod <= minLod)
                    {
                        let url = getMetaUrl(data.c.headNodePath, key, data.c.bulkMetadataEpoch[value]);
                        console.log("url: " + url);
                        await loadMeta(url).then(downloadData)
                    }
                }
            }
        }
    }

    const deleteFolderRecursive = function(path) {
        if (fs.existsSync(path)) {
            fs.readdirSync(path).forEach((file, index) => {
                const curPath = Path.join(path, file);
                if (fs.lstatSync(curPath).isDirectory()) {
                    deleteFolderRecursive(curPath);
                } else {
                    fs.unlinkSync(curPath);
                }
            });
            fs.rmdirSync(path);
        }
    };

	// Earth is represented as octree, i.e. at each level of detail it's divided into boxes, each of which is divided into eight
    // equal parts of the next level of detail. Thus size of box at n-th level of detail is (Earth diameter) / (2 ^ (n - 1)).
    // Levels of detail:
    // 22 - ~0.05 meter per texel
    // 21 - ~0.1 meter per texel
    // 20 - ~0.19 meter per texel
    // 19 - ~0.38 meter per texel
    // 18 - ~0.75 meter per texel
    // 17 - ~1.5 meter per texel
    // 16 - ~3 meter per texel
    // and so on down to ze

    // Minimum lod for which data is downloaded.
    var maxLod = 19;
    // Maximum lod for which data is downloaded.
    var minLod = 17;
	var lat = 51.218704;
	var lon = 4.402457;
	var l = 400.0;
	var w = 400.0;


    // Output folder
	var decoderFolder = 'C:\\Non_Sauvegardé\\perso\\python\\decoder';
	var projectFolder = 'C:\\Non_Sauvegardé\\perso\\python\\decoder\\Anvers';
    var outputFolder = projectFolder + '\\decoder_export';

    deleteFolderRecursive(outputFolder);
    fs.mkdirSync(outputFolder);
    loadMeta(rootMeta).then(downloadData);
    // Box limiting dowloaded part of Earth surface. Arguments: latitude (degrees), longitude (degrees), half-width (meters), half-height (meters).
    var box = makeSurfaceBox(lat, lon, l, w);

	var settings = [projectFolder, maxLod, minLod, lat, lon, l, w];
	fs.writeFileSync(`${decoderFolder}\\decoder.cfg`, JSON.stringify(settings));
	