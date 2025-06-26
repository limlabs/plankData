from flask import Flask, send_file, request
import matplotlib.pyplot as plt
import numpy as np
import io

app = Flask(__name__)

def load_planck_data():
    theory = np.loadtxt("COM_PowerSpect_CMB-base-plikHM-TTTEEE-lowl-lowE-lensing-minimum-theory_R3.01.txt")
    binned = np.loadtxt("COM_PowerSpect_CMB-TT-binned_R3.01.txt")
    return theory, binned

def plot_spectrum(extra=None, label="Model"):
    theory, binned = load_planck_data()
    ell_t, D_t = theory[:, 0], theory[:, 1]
    ell_d, D_d = binned[:, 0], binned[:, 1]
    err_lo, err_hi = binned[:, 2], binned[:, 3]

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(ell_t, D_t, 'k--', label='ΛCDM best-fit')
    ax.errorbar(ell_d, D_d, yerr=[err_lo, err_hi], fmt='s',
                color='darkorange', label="Planck binned TT", markersize=4)
    if extra:
        ax.plot(extra[0], extra[1], 'b-', label=label)
    ax.set_xlim(30, 2500)
    ax.set_ylim(0, 6000)
    ax.set_xlabel(r'Multipole $\ell$')
    ax.set_ylabel(r'$D_\ell = \ell(\ell + 1)C_\ell / (2\pi)$')
    ax.set_title("Planck 2018 TT Spectrum")
    ax.legend()
    buf = io.BytesIO()
    plt.tight_layout()
    plt.savefig(buf, format="png")
    buf.seek(0)
    return buf

@app.route("/")
def base():
    return send_file(plot_spectrum(), mimetype='image/png')

@app.route("/starobinsky")
def starobinsky():
    ell = np.linspace(30, 2500, 800)
    amp = float(request.args.get("amp", 5700))
    decay = float(request.args.get("decay", 3000))
    phase = float(request.args.get("phase", 4.0))
    freq = float(request.args.get("freq", 0.0132))
    supp = float(request.args.get("supp", 0.07))

    envelope = amp * (ell / 210) ** (-0.27) * np.exp(-ell / decay)
    osc1 = np.cos(freq * ell + phase)
    osc2 = 0.17 * np.cos(2 * freq * ell + 2.0)
    oscill = 0.43 * (1 + osc1 + osc2)
    suppression = 1 - supp * np.exp(-((ell - 90) / 90) ** 2)

    D_ell = envelope * oscill * suppression
    buf = plot_spectrum((ell, D_ell), label="Starobinsky-like (Planck-tuned)")
    return send_file(buf, mimetype='image/png')

@app.route("/hilltop")
def hilltop():
    ell = np.linspace(30, 2500, 800)
    amp = float(request.args.get("amp", 5000))
    decay = float(request.args.get("decay", 1800))
    phase = float(request.args.get("phase", 2.0))
    freq = float(request.args.get("freq", 0.012))
    alpha = float(request.args.get("alpha", 0.25))
    beta = float(request.args.get("beta", 0.4))

    envelope = amp * np.exp(-ell / decay)
    oscillations = (1 + alpha * np.cos(freq * ell + phase)) * (1 - beta * np.exp(-((ell - 200) / 100) ** 2))
    D_ell = envelope * oscillations

    buf = plot_spectrum((ell, D_ell), label="Hilltop-like model")
    return send_file(buf, mimetype='image/png')
