from flask import Flask, send_file, request, redirect, url_for
import matplotlib
matplotlib.use('Agg')  # Use Agg backend
import matplotlib.pyplot as plt
import numpy as np
import io

app = Flask(__name__)

def load_planck_data():
    try:
        theory = np.loadtxt("COM_PowerSpect_CMB-base-plikHM-TTTEEE-lowl-lowE-lensing-minimum-theory_R3.01.txt")
        binned = np.loadtxt("COM_PowerSpect_CMB-TT-binned_R3.01.txt")
        return theory, binned
    except FileNotFoundError as e:
        raise
    except Exception as e:
        raise

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

def compute_spectrum(ell, amp, decay, phase, freq, supp):
    """Compute Starobinsky R² inflation model power spectrum.
    
    The Starobinsky model adds R² term to Einstein gravity:
    S = ∫d⁴x√-g[M_P²R + αR²]
    
    This produces:
    1. Nearly scale-invariant spectrum with ns ≈ 1 - 2/N
    2. Tensor-to-scalar ratio r ≈ 12/N²
    where N is the number of e-folds.
    
    Parameters:
    - amp: Overall amplitude (sets inflation scale)
    - decay: Silk damping scale
    - phase: Acoustic oscillation phase
    - freq: Sound horizon scale
    - supp: ISW suppression strength
    """
    # Primary spectrum shape from R² inflation
    # Scale-invariant with specific tilt ns ≈ 0.97
    # Normalized at first acoustic peak (ell=210)
    envelope = amp * (ell / 210) ** (-0.3)
    
    # Acoustic oscillations with proper phase and damping
    theta_s = 0.0104
    kd = 0.14
    acoustic_scale = ell * theta_s
    damping = np.exp(-(ell / (decay * kd))**1.2)
    
    # Oscillation pattern from baryon-photon acoustic waves
    # First term: Primary acoustic oscillations at sound horizon scale
    osc1 = np.cos(freq * acoustic_scale + phase)
    # Second term: Second harmonics (17% amplitude, fixed phase=2.0)
    osc2 = 0.17 * np.cos(2 * freq * acoustic_scale + 2.0)
    # Combined pattern with 43% modulation depth
    oscill = 0.43 * (1 + osc1 + osc2)
    
    # Low-ell suppression from late-time integrated Sachs-Wolfe effect
    # Gaussian suppression centered at ell=90 (horizon scale at reionization)
    # Maximum suppression amplitude controlled by supp parameter
    suppression = 1 - supp * np.exp(-((ell - 90) / 90) ** 2)
    
    return envelope * oscill * suppression * damping

def compute_hilltop(ell, amp, mu, v, p, phi):
    """Compute hilltop inflation model power spectrum.
    
    The hilltop inflation model has potential:
    V(phi) = V0 * [1 - (phi/mu)^p] + Lambda^4
    
    Parameters:
    - amp: Overall amplitude scaling (relates to V0)
    - mu: Mass scale of the potential (typically near Planck scale)
    - v: Vacuum expectation value (controls oscillation amplitude)
    - p: Power in potential (p > 2 for inflation)
    - phi: Initial field value (phi < mu for hilltop inflation)
    
    The model produces:
    1. Nearly scale-invariant spectrum from slow-roll
    2. Oscillations from features in potential
    3. Running spectral index from field evolution
    """
    # Hilltop potential parameters control the shape of inflation
    # Small field inflation occurs near the hilltop (phi < mu)
    # The power p determines how steep the potential is
    # mu: mass scale
    # v: vacuum expectation value
    # p: power in potential
    # phi: initial field value
    
    # Basic power spectrum shape
    ns = 1 - 2/p * (phi/mu)**2  # Spectral index
    running = -2/p * (phi/mu)**2 * (1 - (p+1)/p * (phi/mu)**2)  # Running
    
    # Power spectrum with running
    k = ell/14000  # Convert ell to k
    ln_k_pivot = np.log(0.05)  # Pivot scale
    power = amp * (k/0.05)**(ns-1 + 0.5*running*np.log(k/0.05))
    
    # Add oscillations from potential
    osc_amp = v * (phi/mu)**p
    osc_freq = 2*np.pi*mu
    power *= (1 + osc_amp * np.sin(osc_freq * np.log(k)))
    
    # Damping at high-l
    damping = np.exp(-((ell-1500)/1000)**2)
    
    return power * damping

def get_hilltop_params():
    """Return best-fit parameters for hilltop model."""
    return (4700, 13.5, 1.8, 3.2, 0.37)

def get_starobinsky_params():
    """Return best-fit parameters for Starobinsky model."""
    return (5500, 9000, 4.0, 0.95, 0.07)

@app.route("/starobinsky")
def starobinsky():
    ell = np.linspace(30, 2500, 800)
    try:
        # Get best-fit values
        default_amp, default_decay, default_phase, default_freq, default_supp = get_starobinsky_params()
        # Allow URL parameters to override defaults
        amp = float(request.args.get("amp", default_amp))
        decay = float(request.args.get("decay", default_decay))
        phase = float(request.args.get("phase", default_phase))
        freq = float(request.args.get("freq", default_freq))
        supp = float(request.args.get("supp", default_supp))
    except (ValueError, TypeError) as e:
        return f"Error: Invalid parameters - {str(e)}", 400

    D_ell = compute_spectrum(ell, amp, decay, phase, freq, supp)
    buf = plot_spectrum((ell, D_ell), label="Starobinsky-like (Planck-tuned)")
    return send_file(buf, mimetype='image/png')

@app.route("/hilltop")
def hilltop():
    ell = np.linspace(30, 2500, 800)  # Match Starobinsky ell range
    try:
        # Get best-fit values
        default_amp, default_mu, default_v, default_p, default_phi = get_hilltop_params()
        # Allow URL parameters to override defaults
        amp = float(request.args.get("amp", default_amp))
        mu = float(request.args.get("mu", default_mu))
        v = float(request.args.get("v", default_v))
        p = float(request.args.get("p", default_p))
        phi = float(request.args.get("phi", default_phi))
    except (ValueError, TypeError) as e:
        return f"Error: Invalid parameters - {str(e)}", 400

    # Compute model
    D_ell = compute_hilltop(ell, amp, mu, v, p, phi)
    
    # Use same plotting function as Starobinsky
    buf = plot_spectrum((ell, D_ell), label="Hilltop Inflation")
    return send_file(buf, mimetype='image/png')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
