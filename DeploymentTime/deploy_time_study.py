"""
Deployment-time study: how slow must deployment be before the inertial terms
in the equation of motion (Derivation/main.tex) can be dropped?

Full EOM (1-DOF, generalized coordinate theta):
    I_eff(theta)*ddtheta + M_j*S1*L^2*sin*cos*dtheta^2 + N_s*k*theta
        + 2*N_k*M_k = N_s*tau_f
The quasi-static equation keeps only the last three terms. Both dropped terms
scale as 1/T^2 (acceleration ~ dth/T^2, rate^2 ~ (dth/T)^2), so the phase
duration T needed to keep them below a fraction eps of the friction torque is
    T_min = sqrt(c / eps),   c = peak inertial torque * T^2 / (N_s * tau_f).

Both parameter sets are evaluated regardless of params.USE_TESTING_PARAMS: the
params.py source is exec'd twice with that flag forced, so params.py itself is
not modified.

Outputs (in this folder): results.tex (numbers for the report), results.csv,
fig_ratio_vs_time.png.
"""

import csv
import os
import sys

import numpy as np
from scipy.integrate import solve_ivp

HERE = os.path.dirname(os.path.abspath(__file__))
CODE = os.path.dirname(HERE)
sys.path.insert(0, CODE)

# Min-jerk profile theta(t) = th0 + dth*(10s^3 - 15s^4 + 6s^5), s = t/T:
# peak |accel| = 5.7735*dth/T^2, peak |rate| = 1.875*dth/T.
A_PK, W_PK = 5.7735, 1.875
EPS_LIST = (0.01, 0.05, 0.10)
EPS_DESIGN = 0.05
EPS_TAG = {0.01: "One", 0.05: "Five", 0.10: "Ten"}
# Recommended (Phase 1, Phase 2) durations in s: production 2 h / 4.5 h, bench 30 s / 65 s.
REC = {"P": (7200.0, 16200.0), "B": (30.0, 65.0)}


def load(testing):
    src = open(os.path.join(CODE, "params.py")).read()
    src = src.replace("USE_TESTING_PARAMS = True", f"USE_TESTING_PARAMS = {testing}")
    ns = {"__name__": "params_exec"}
    exec(compile(src, "params.py", "exec"), ns)
    return ns


def study(ns, label):
    n, L, Mj = ns["n_links"], ns["link_length"], ns["M_j"]
    S1, Ij = ns["S1_link_index"], ns["I_j"]
    Ns, Nk = ns["N_springs"], ns["N_kinks"]
    tau_fd = ns["tau_friction_design"]
    th0, thmin = ns["theta_0"], ns["theta_min"]
    th1 = (np.pi - np.arcsin(ns["handoff_margin"])) / 2.0
    marg = ns["spring_margin_over_kmin"]

    def I_eff(t):
        return Mj * S1 * L**2 * np.sin(t) ** 2 + n * Ij + 0.5 * n * Mj * L**2

    # Quasi-static sizing (Derivation, Sec. PHASE 1 / PHASE 2)
    k = marg * tau_fd / th1
    Mk0 = marg * Ns * (tau_fd - k * thmin) / (2 * Nk)
    Q_fric = Ns * tau_fd

    def phase(lo, hi):
        ths = np.linspace(lo, hi, 400)
        dth = hi - lo
        I_max = I_eff(ths).max()
        sc_max = (np.sin(ths) * np.cos(ths)).max()
        # peak torque = c_acc*dth/T^2 + c_rate*(dth/T)^2; both peaks summed
        # (conservative). Return c/Q_fric so ratio(T) = c/T^2.
        c = I_max * A_PK * dth + Mj * S1 * L**2 * sc_max * (W_PK * dth) ** 2
        return dth, I_max, c / Q_fric

    out = dict(label=label, n=n, L=L, Mj=Mj, k=k, Mk0=Mk0, Q_fric=Q_fric,
               th1=th1, th0=th0, thmin=thmin, Ns=Ns, Nk=Nk, tau_fd=tau_fd)
    for name, (lo, hi) in (("p1", (th1, th0)), ("p2", (thmin, th1))):
        dth, I_max, c = phase(lo, hi)
        out[name] = dict(dth=dth, I_max=I_max, c=c,
                         Tmin={e: np.sqrt(c / e) for e in EPS_LIST})

    # Natural period of the spring-inertia mode (largest inertia in the sweep,
    # spring stiffness N*k).
    I_all = I_eff(np.linspace(thmin, th0, 400)).max()
    out["Tn"] = 2 * np.pi * np.sqrt(I_all / (Ns * k))

    # Free-running (no rate limiter) deployment from rest at stow.
    def rhs(t, y):
        th, w = y
        cent = Mj * S1 * L**2 * np.sin(th) * np.cos(th) * w**2
        kink = 2 * Nk * Mk0 if th < th1 else 0.0
        torque = -Ns * k * th - kink + Ns * tau_fd   # negative = drives theta down
        return [w, (torque - cent) / I_eff(th)]

    def ev(t, y):
        return y[0] - thmin
    ev.terminal, ev.direction = True, -1
    sol = solve_ivp(rhs, [0, 3600], [th0, 0.0], events=ev, rtol=1e-9, atol=1e-12,
                    max_step=0.05)
    if sol.t_events[0].size:
        out["t_free"] = sol.t_events[0][0]
        w_end = sol.y_events[0][0][1]
        out["w_free_end"] = abs(w_end)
        out["KE_free_end"] = 0.5 * I_eff(thmin) * w_end**2
    else:
        out["t_free"] = np.inf
        out["w_free_end"] = 0.0
        out["KE_free_end"] = 0.0
    out["E_spring"] = 0.5 * Ns * k * th0**2
    out["W_fric"] = Ns * tau_fd * (th0 - thmin)
    return out


def main():
    res = [study(load(False), "Production (orbit)"), study(load(True), "Bench test")]
    for r in res:
        p1, p2 = r["p1"], r["p2"]
        print(f"\n== {r['label']} ==  n={r['n']}  L={r['L']:.4f} m  M_j={r['Mj']:.4g} kg")
        print(f"  k={r['k']:.4g} N*m/rad  Mk0={r['Mk0']:.4g} N*m  Q_fric={r['Q_fric']:.4g} N*m  Tn={r['Tn']:.3g} s")
        for nm, p in (("Phase 1", p1), ("Phase 2", p2)):
            print(f"  {nm}: dth={np.degrees(p['dth']):.1f} deg  Imax={p['I_max']:.4g}  "
                  + "  ".join(f"Tmin({e:.0%})={p['Tmin'][e]:.3g}s" for e in EPS_LIST))
        print(f"  free-run: t={r['t_free']:.4g} s  w_end={r['w_free_end']:.4g} rad/s  "
              f"KE_end={r['KE_free_end']:.4g} J  E_spring={r['E_spring']:.4g} J  W_fric={r['W_fric']:.4g} J")

    # ---------------- figure ----------------
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    T = np.logspace(-1, np.log10(12 * 3600), 400)
    fig, axs = plt.subplots(1, 2, figsize=(9.5, 3.8), sharey=True)
    for ax, r in zip(axs, res):
        for nm, p, ls in (("Phase 1", r["p1"], "-"), ("Phase 2", r["p2"], "--")):
            ax.loglog(T, p["c"] / T**2, ls,
                      label=f"{nm} ({np.degrees(p['dth']):.0f}$^\\circ$ sweep)")
        for e in EPS_LIST:
            ax.axhline(e, color="gray", lw=0.7, ls=":")
        ax.text(T[0] * 1.1, EPS_DESIGN * 1.3, r"$\varepsilon=5\%$ (design)", fontsize=7, color="gray")
        ax.axvline(3600, color="k", lw=0.7, alpha=0.4)
        ax.text(3600 * 0.8, 1e-11, "1 h", rotation=90, fontsize=7, ha="right")
        ax.set_title(r["label"], fontsize=10)
        ax.set_xlabel("phase duration $T$ (s)")
        ax.set_ylim(1e-13, 1e3)
        ax.grid(True, which="both", alpha=0.2)
    axs[0].set_ylabel(r"peak inertial torque / friction torque $N_s\tau_f$")
    axs[0].legend(fontsize=8, loc="upper right")
    fig.tight_layout()
    fig.savefig(os.path.join(HERE, "fig_ratio_vs_time.png"), dpi=200)
    plt.close(fig)

    # ---------------- csv + tex macros ----------------
    with open(os.path.join(HERE, "results.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["set", "phase", "eps", "Tmin_s"])
        for r in res:
            for nm in ("p1", "p2"):
                for e in EPS_LIST:
                    w.writerow([r["label"], nm, e, r[nm]["Tmin"][e]])

    def g(x, d=3):
        return f"{x:.{d}g}"

    def tm(x):
        return f"{x:.1f}" if x < 100 else f"{x:.0f}"

    with open(os.path.join(HERE, "results.tex"), "w") as f:
        for tag, r in zip(("P", "B"), res):
            def m(name, val):
                f.write(f"\\newcommand{{\\{name}{tag}}}{{{val}}}\n")
            m("nlinks", r["n"]); m("Llink", g(r["L"], 4)); m("Mj", g(r["Mj"], 4))
            m("kk", g(r["k"], 3)); m("Mkzero", g(r["Mk0"], 3)); m("Qfric", g(r["Q_fric"], 3))
            m("Imaxa", g(r["p1"]["I_max"], 3)); m("Imaxb", g(r["p2"]["I_max"], 3))
            for e in EPS_LIST:
                t = EPS_TAG[e]
                m(f"Ta{t}", tm(r["p1"]["Tmin"][e]))
                m(f"Tb{t}", tm(r["p2"]["Tmin"][e]))
                m(f"Ttot{t}", tm(r["p1"]["Tmin"][e] + r["p2"]["Tmin"][e]))
            m("Tn", g(r["Tn"], 3))
            m("tfree", g(r["t_free"], 3))
            m("wfree", g(r["w_free_end"], 3))
            m("KEfree", g(r["KE_free_end"], 3))
            m("Espring", g(r["E_spring"], 3))
            m("Wfric", g(r["W_fric"], 3))
            m("marginA", g(3600 / r["p1"]["Tmin"][EPS_DESIGN], 3))
            m("marginB", g(11 * 3600 / r["p2"]["Tmin"][EPS_DESIGN], 3))
            m("ratioA", f"{r['p1']['c'] / 3600**2:.1e}")
            m("ratioB", f"{r['p2']['c'] / (11 * 3600) ** 2:.1e}")
            m("Tnratio", g(3600 / r["Tn"], 3))
            # recommended phase durations (about 1% neglect, equal in both phases)
            t1, t2 = REC[tag]
            m("recTa", tm(t1)); m("recTb", tm(t2)); m("recTtot", tm(t1 + t2))
            m("recRa", f"{100 * r['p1']['c'] / t1**2:.2f}")
            m("recRb", f"{100 * r['p2']['c'] / t2**2:.2f}")
            m("recRaHuman", f"{t1 / 3600:.2g}"); m("recRbHuman", f"{t2 / 3600:.2g}")
            m("recTotHuman", f"{(t1 + t2) / 3600:.3g}")
            # split currently in params.py (Phase 1 = 1 h, Phase 2 = 11 h) for comparison
            m("curRa", f"{100 * r['p1']['c'] / 3600**2:.2f}")
            m("curRb", f"{100 * r['p2']['c'] / (11 * 3600) ** 2:.3f}")


if __name__ == "__main__":
    main()
