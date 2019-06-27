import sys
import math

def PUFF_SParameters(Puff_File, dB = True, Radians = True):
    '''Takes a PUF file as an argument and returns a dictionary with the frequencies and S-Parameters in terms of magnitude and phase'''

    # To hold the outputs
    Plots = dict()

    # Open and read the contents of the PUF file
    with open(Puff_File) as f:
        content = f.readlines()
    
    # Variables to mark beginning and end of the S-parameters
    beginIndex = -1
    endIndex =  -1
    
    # Find the beginning of the S-parameters section
    for i in range(0, len(content)):
        if(content[i].find("\s{parameters}") != -1):
            beginIndex = i
            
    # Assuming the S-parameters section ends with "\"
    if(beginIndex != -1):
        for i in range(0, len(content)):
            if(content[beginIndex + 1:][i].find("\\") != -1):
                endIndex = beginIndex + 1 + i
                break
    
    # If could not find beginning and end locations
    if(beginIndex == -1 or endIndex == -1 or beginIndex >= endIndex):
        raise Exception("Error reading the file! Make sure the PUF file has a \s{parameters} section.")
    else:
        try:
            Plot_Names = content[beginIndex + 1].split()

            # Create a list for each S-parameter
            for i, plot_name in enumerate(Plot_Names):
                if(i == 0):
                    Plots["Frequencies"] = []
                else:
                    Plots[Plot_Names[i] + "_M"] = []
                    Plots[Plot_Names[i] + "_P"] = []
                    
            content = [x.split() for x in content][beginIndex + 2 : endIndex]
            
            for line in content:
                for i, plot in enumerate(Plots):
                    if(i == 0):
                        Plots[plot].append(float(line[0]))
                    elif(i % 2 == 0):
                        phase = float(line[i])
                        if(Radians):
                            Plots[plot].append((phase * math.pi) / 180.0)
                        else:
                            Plots[plot].append(phase)
                    else:
                        magnitude = float(line[i])
                        if(dB):
                            # Magnitude 0 is -infinity in dB. We can settle for a large negative number for graphing purposes
                            Plots[plot].append(20 * math.log10(float(line[i]) + (not bool(float(line[i])) * sys.float_info.epsilon)))
                        else:
                            Plots[plot].append(float(line[i]))
                        
            print("Returning a dictionary with Keys: ", [key for key in Plots])
            return Plots

        except Exception as e:
            print("Error reading the file. Make sure it is not corrupted. Exception:\n", e)