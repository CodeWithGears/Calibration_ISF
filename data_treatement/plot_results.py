import matplotlib.pyplot as plt
import numpy as np

def plot_force_deplacement(deplacement, force_cellule_en_s):
    fig, axs = plt.subplots(2, 1, figsize=(8, 8))
    axs[0].plot(deplacement, force_cellule_en_s)

    coeffs = np.polyfit(deplacement, force_cellule_en_s, deg=1)
    coeffs_deplacements = np.polyfit(force_cellule_en_s, deplacement, deg=1)

    # Refaire l'escalier
    regression = np.polyval(coeffs, deplacement)

    r_2 = np.corrcoef(deplacement, force_cellule_en_s)[0, 1] ** 2

    diff = force_cellule_en_s - regression
    max_diff = np.abs(diff).max()
    arg_max_diff = np.abs(diff).argmax()

    print(f"Max error: {max_diff:.4f}")
    print(f"Max error @ index: {deplacement[arg_max_diff]}")
    print(f"Mean error: {np.mean(np.abs(diff)):.4f}")

    # Déterminer l'écart en terme de déplacement
    diff_deplacement = deplacement - np.polyval(coeffs_deplacements, force_cellule_en_s)
    max_diff_deplacement = np.abs(diff_deplacement).max()
    index_max_diff_deplacement = np.abs(diff_deplacement).argmax()
    print(f"Max error in displacement: {max_diff_deplacement:.4f} @ index: {deplacement[index_max_diff_deplacement]}")

    x_line = [deplacement[index_max_diff_deplacement], deplacement[index_max_diff_deplacement] - max_diff_deplacement]
    y_line = [force_cellule_en_s[index_max_diff_deplacement], force_cellule_en_s[index_max_diff_deplacement]]

    axs[0].plot(x_line, y_line, color = "red", label = f"Max error: {max_diff_deplacement:.4f} mm @ {deplacement[index_max_diff_deplacement]:.2f} mm")
    axs[0].plot(deplacement, regression, color="orange", label=f"F[N] = {coeffs[0]:.4f}x [mm] + {coeffs[1]:.4f}, R² = {r_2:.4f}")

    axs[1].plot(deplacement, diff, color="red", label="Error (N)", alpha=0.5)
    axs[1].set_ylabel("Error (N)", color="red")
    axs[1].legend(loc="upper left")

    axs[0].set_xlabel("Displacement (mm)")
    axs[0].set_ylabel("Force (N)")
    axs[0].legend(loc="upper left")

    axs[0].set_title("Lecture de force de la cellule \n en S comparée au déplacement")

    return fig, axs

def plot_load_cell_regression(sliced_data, channels):
    fig, axs = plt.subplots(1, 1, figsize=(8, 4))

    for col, name, color in channels:
        #Scatter
        axs.scatter(sliced_data["V008"], sliced_data[col], label = name, color=color)
        
        # Linear fit
        coeff = np.polyfit(sliced_data["V008"], sliced_data[col], deg=1)
        
        # Plot the linear fit and calculate R²
        axs.plot(sliced_data["V008"], coeff[0] * sliced_data["V008"] + coeff[1], color=color, linestyle='--', label=f"S = {coeff[0]:.2e}x + {coeff[1]:.4f}")
        r_2 = np.corrcoef(sliced_data[col], coeff[0] * sliced_data["V008"] + coeff[1])[0, 1] ** 2
        print(f"R² for {col}: {r_2:.4f}")

        # Plot the linear fit line for each measurement
        axs.plot(sliced_data["V008"], coeff[0] * sliced_data["V008"] + coeff[1], color=color, linestyle='--')

    axs.set_xlabel("Force cellule en S")
    axs.set_ylabel("Mesure de la cellule de charge")
    axs.legend()

    return fig, axs