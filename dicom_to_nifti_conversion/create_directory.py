#!/usr/bin/env python3
import os 
import dicom2nifti

def create_new_directory(directory_name):
    ok = 0
    num = 1

    while ok == 0:
        try:
            NewName = directory_name + '_' + str(num)
            os.mkdir(NewName)
            ok = 1
        except:
            num += 1
        pass

    return NewName


def DCM2Nii_Directory(FileLoc, SaveLoc):

  dicom2nifti.convert_directory(FileLoc, SaveLoc, compression=True, reorient=True)

  return