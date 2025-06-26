# backend/app.py

from flask import Flask, send_file
import matplotlib.pyplot as plt
import numpy as np
import io

app = Flask(__name__)

@app.route("/")
def plot():
    # --- Load your theory and binned data here (you already have this logic) ---
    theory_data = np.loadtxt("COM_PowerSpect_CMB-base-plikHM-TTTEEE-lowl-lowE-lensing-minimum-theory_R3.01.txt")
    binned_data = np.loadtxt("COM_PowerSpect_CMB-TT-binned_R3.01.txt")

    ell_theory, D_ell_theory = theory_data[:, 0], theory_data[:, 1]
    ell_data, D_ell_data, err_down, err_up = binned_data[:, 0], binned_data[:, 1], binned_data[:, 2], binned_data[:, 3]

    # --- Plot ---
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(ell_theory, D_ell_theory, 'k--', label='ΛCDM best-fit theory')
    ax.errorbar(ell_data, D_ell_data, yerr=[err_down, err_up], fmt='s', color='darkorange', label=r"Planck binned TT spectrum ($\ell \geq 30$)", markersize=4)
    ax.set_xlim(30, 2500)
    ax.set_ylim(0, 6000)
    ax.set_xlabel(r'Multipole $\ell$')
    ax.set_ylabel(r'$D_\ell = \ell(\ell + 1)C_\ell/2\pi\ [\mu K^2]$')
    ax.set_title('Planck 2018 Temperature Power Spectrum (Plik binned vs Theory)')
    ax.legend()

    # --- Save to buffer and return as PNG ---
    buf = io.BytesIO()
    plt.tight_layout()
    plt.savefig(buf, format="png")
    buf.seek(0)
    return send_file(buf, mimetype='image/png')
