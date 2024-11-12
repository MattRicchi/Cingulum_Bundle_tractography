#!/usr/bin/env python3

import subprocess

def synb0_correct(stripped = False):
    print('Starting distorsion correction with synb0 docker...')
    
    # Run the Docker command for distorsions correction
    if stripped == True:
        docker_command = "docker run --rm -v $(pwd)/INPUTS/:/INPUTS/ -v $(pwd)/OUTPUTS:/OUTPUTS/ -v $(pwd)/license.txt:/extra/freesurfer/license.txt --user $(id -u):$(id -g) leonyichencai/synb0-disco:v3.0 --stripped"
    else:
        docker_command = "docker run --rm -v $(pwd)/INPUTS/:/INPUTS/ -v $(pwd)/OUTPUTS:/OUTPUTS/ -v $(pwd)/license.txt:/extra/freesurfer/license.txt --user $(id -u):$(id -g) leonyichencai/synb0-disco:v3.0"

    # Use subprocess.Popen to run the Docker command
    process = subprocess.Popen(docker_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

    # Print the output in real-time
    for line in process.stdout:
        print(line, end='')

    # Wait for the process to finish
    process.wait()

    # Check the exit code
    if process.returncode == 0:
        print('Synb0 distorsion correction completed successfully!')
        return
    else:
        print("ERROR: Docker command failed with exit code", process.returncode)
        exit()
    
