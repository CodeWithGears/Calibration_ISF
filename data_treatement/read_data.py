import pandas as pd
import numpy as np

def read_displacement_data(config_number):
    """
    Reads the displacement data from a CSV file for a given configuration number.
    Args:
        config_number (int): The configuration number to read the data for.
        Automatically sets the zero.
        Returns:
        tuple: The displacement data as a tuple of two NumPy arrays (index, displacement).
    """
    data = pd.read_csv(rf"C:\Users\Client\Documents\Calibration_ISF\Data\ForceDisplacement\Config{config_number}\displacement.csv",
                    header=None,
                    names=["index", "mesure_cadran"])
    return (np.array(data["index"]), -np.array(data["mesure_cadran"]) + np.array(data["mesure_cadran"])[0] )


def read_load_cell_data(config_number):
    """
    Reads the load cell data from a CSV file for a given configuration number.
    Args:
        config_number (int): The configuration number to read the data for.
        Returns:
        pd.DataFrame: The load cell data.
    """
    measurements = pd.read_csv(rf"C:\Users\Client\Documents\Calibration_ISF\Data\ForceDisplacement\Config{config_number}\controller_data_config{config_number}.csv",
                           sep = ";",
                           header = 0)
    
    # Convert all columns to numeric, coercing errors to NaN
    for col in measurements.columns:
        measurements[col] = pd.to_numeric(measurements[col], errors='coerce')
    
    # Remove rows with any NaN values (includes -1.#SNAN0 and invalid data)
    measurements = measurements.dropna()

    return measurements