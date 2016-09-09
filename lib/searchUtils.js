/**
 * Created by taozhengkai on 9/8/16.
 */


define("common:widget/ui/searchUtils/searchUtils", function (e, r, n) {
    var t = e("common:widget/ui/base/base"), a = n.exports = {};
    a.escapeXSS = function (e) {
        return e.replace(/[<>]/g, function (e) {
            return encodeURIComponent(e)
        }).replace(/"/g, "%22").replace(/'/g, "%27")
    }, a.escapeHTML = function (e) {
        return e.replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;").replace(/'/g, "&#39;")
    };
    var f = new Date;
    a.fmqDetailValueSet = function () {
        var e = a.getSearchConf(), r = f.getTime();
        if (void 0 == e.fmq || "" == e.fmq)e.fmq = r + "_D"; else if (e.fmq.indexOf("m") > -1 && -1 == e.fmq.indexOf("_m") && -1 == e.fmq.indexOf("_D")) {
            var n = e.fmq;
            e.fmq = r + "_" + n + "_D"
        } else if (-1 == e.fmq.indexOf("_D")) {
            var n = e.fmq;
            e.fmq = n + "_D"
        }
        return e.fmq
    }, a.query2Json = function (e) {
        if (null == e || "string" != typeof e)return e;
        for (var r = {}, n = e.split("&"), t = 0, a = n.length; a > t; t++) {
            var f = n[t].split("=");
            r[f[0]] = f[1]
        }
        return r
    };
    var i;
    a.getSearchConf = function () {
        return i ? i : i = a.query2Json(a.escapeXSS(window.location.search.substring(1)))
    }, a.getHashConf = function () {
        var e = t.trim(location.href.split("#")[1] || "");
        e = e ? e.split("&") : [];
        for (var r = 0, n = e.length; n > r; r++)e[r] = a.escapeHTML(o(e[r]));
        return e
    }, a.getHashConfObj = function (e) {
        var r = {
            pn: "int",
            id: "string",
            objURL: "string",
            fromURL: "string",
            W: "int",
            H: "int",
            TP: "string",
            di: "string"
        };
        if ("object" == typeof e)for (var n in e)r[n] = e[n];
        var t, f = {};
        for (n in r)t = a.getHashConfValue(n, r[n]), f[n] = t;
        return f
    }, a.getHashConfValue = function (e, r) {
        e = e || 0;
        var n = a.getHashConf();
        if ("number" == typeof e && !isNaN(e))return a.toVarType(n[e], r);
        for (var t = "", f = 0, i = n.length; i > f; f++)if (n[f] && 0 === n[f].indexOf(e)) {
            t = n[f].replace(new RegExp("^" + e), "");
            break
        }
        return a.toVarType(t, r)
    };
    var o = function (e) {
        try {
            return decodeURIComponent(e)
        } catch (r) {
            return e
        }
    };
    a.decodeURIComponent = o, a.toVarType = function (e, r) {
        switch (r = r || "string") {
            case"int":
                return parseInt(e, 10);
            case"float":
                return parseFloat(e);
            case"number":
                return tmp = parseFloat(e), isNaN(tmp) && (tmp = 0), tmp;
            case"boolean":
                return !!e;
            case"array":
                return t.makeArray(e);
            default:
                return String(e)
        }
    };
    var u = function (e) {
        var r = a.getSearchConf(), n = new Date, t = n.getTime();
        if (void 0 == r.fmq)e.fmq.value = t + "_R"; else if (r.fmq.indexOf("m") > -1 && -1 == r.fmq.indexOf("_m") && -1 == r.fmq.indexOf("_R")) {
            var f = r.fmq;
            e.fmq.value = t + "_" + f + "_R"
        } else e.fmq.value = t + "_R";
        return e.fm.value = void 0 == r.fr || "" == r.fr ? "detail" : r.fr, !0
    }, c = {
        w: "a",
        k: "b",
        v: "c",
        1: "d",
        j: "e",
        u: "f",
        2: "g",
        i: "h",
        t: "i",
        3: "j",
        h: "k",
        s: "l",
        4: "m",
        g: "n",
        5: "o",
        r: "p",
        q: "q",
        6: "r",
        f: "s",
        p: "t",
        7: "u",
        e: "v",
        o: "w",
        8: "1",
        d: "2",
        n: "3",
        9: "4",
        c: "5",
        m: "6",
        0: "7",
        b: "8",
        l: "9",
        a: "0",
        _z2C$q: ":",
        "_z&e3B": ".",
        AzdH3F: "/"
    }, s = /([a-w\d])/g, m = /(_z2C\$q|_z&e3B|AzdH3F)/g;
    a.uncompile = function (e) {
        var r = e.replace(m, function (e, r) {
            return c[r]
        });
        return r.replace(s, function (e, r) {
            return c[r]
        })
    }, a.uncompileURL = function (e) {
        return /^(http|https)/.test(e) ? e : a.uncompile(e)
    }, a.f_submit = u, window.f_submit = u
});