import sys
import math

def S2P_SParameters(S2P_File, dB = True, Radians = True):
    '''Takes a S2P file as an argument and returns a dictionary with the frequencies and S-Parameters in terms of magnitude and phase'''

    # To hold the outputs
    Plots = dict()

    # Open and read the contents of the S2P file
    with open(S2P_File) as f:
        content = f.readlines()

    # Remove comment lines (starting with "!")
    content_processed = []
    for line in content:
        if not line.lstrip().startswith("!"):
            content_processed.append(line)
        
    # Variables to mark beginning and end of the S-parameters
    beginIndex = -1
    endIndex = len(content_processed) - 1 # Assume end of file as end of S-parameters
    
    # Find the beginning of the S-parameters section
    for i in range(0, len(content_processed)):
        if(content_processed[i].find("#") != -1):
            beginIndex = i
            break # first option line
        
    # If could not find beginning and end locations
    if(beginIndex == -1 or endIndex == -1 or beginIndex >= endIndex):
        raise Exception("Error reading the file! Make sure the PUF file has a \s{parameters} section.")
    else:
        try:
            Plot_Names = ["Frequencies", "S11_M", "S11_P", "S21_M", "S21_P", "S12_M", "S12_P", "S22_M", "S22_P"]

            # Create a list for each S-parameter
            for plot_name in Plot_Names:
                Plots[plot_name] = []

            content_processed = [x.split() for x in content_processed][beginIndex + 1: endIndex]
            
            for line in content_processed:
                Frequency = float(line[0])
                S11RE = float(line[1])
                S11IM = float(line[2])
                S21RE = float(line[3])
                S21IM = float(line[4])
                S12RE = float(line[5])
                S12IM = float(line[6])
                S22RE = float(line[7])
                S22IM = float(line[8]) 

                S11Magnitude = math.sqrt((S11RE ** 2) + (S11IM ** 2))
                S11Phase = math.atan2(S11IM, S11RE)

                S21Magnitude = math.sqrt((S21RE ** 2) + (S21IM ** 2))
                S21Phase = math.atan2(S21IM, S11RE)

                S12Magnitude = math.sqrt((S12RE ** 2) + (S12IM ** 2))
                S12Phase = math.atan2(S12IM, S12RE)

                S22Magnitude = math.sqrt((S22RE ** 2) + (S22IM ** 2))
                S22Phase = math.atan2(S22IM, S22RE)

                Plots["Frequencies"].append(Frequency)

                if(dB):       
                    Plots["S11_M"].append(20 * math.log10(S11Magnitude + (not bool(S11Magnitude) * sys.float_info.epsilon)))
                    Plots["S21_M"].append(20 * math.log10(S21Magnitude + (not bool(S21Magnitude) * sys.float_info.epsilon)))
                    Plots["S12_M"].append(20 * math.log10(S12Magnitude + (not bool(S12Magnitude) * sys.float_info.epsilon)))
                    Plots["S22_M"].append(20 * math.log10(S22Magnitude + (not bool(S22Magnitude) * sys.float_info.epsilon)))       
                else:
                    Plots["S11_M"].append(S11Magnitude)
                    Plots["S21_M"].append(S21Magnitude)
                    Plots["S12_M"].append(S12Magnitude)
                    Plots["S22_M"].append(S22Magnitude)
                if(Radians):
                    Plots["S11_P"].append(S11Phase)
                    Plots["S21_P"].append(S21Phase)
                    Plots["S12_P"].append(S12Phase)
                    Plots["S22_P"].append(S22Phase)
                else:
                    Plots["S11_P"].append((S11Phase * 180.0) / math.pi)
                    Plots["S21_P"].append((S21Phase * 180.0) / math.pi)
                    Plots["S12_P"].append((S12Phase * 180.0) / math.pi)
                    Plots["S22_P"].append((S22Phase * 180.0) / math.pi)

            print("Returning a dictionary with Keys: ", [key for key in Plots])
            return Plots
        
        except Exception as e:
            print("Error reading the file. Make sure it is not corrupted. Exception:\n", e)