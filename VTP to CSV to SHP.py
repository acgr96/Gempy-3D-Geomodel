import vtk
import csv
import shapefile
import os

#Get the number of surface files generated in the directory by the model (Note: Subtract the number of additional folders in the directory)
iter = len(os.listdir('C:/Users/acgr9/Desktop/CBay_Crand/Geomodel/VTK_Export'))-3

for i in range(0, iter):

    # Make Numeric Assignment of Surface Input/Output Files Variable for Easy Iteration Through Them
    surface = i

    # Define Input VTP File and Output CSV File Names/Locations
    Input  = 'C:/Users/acgr9/Desktop/CBay_Crand/Geomodel/VTK_Export/CBayCRand_surfaces_{}.vtp'.format(surface)
    Output  = 'C:/Users/acgr9/Desktop/CBay_Crand/Geomodel/VTK_Export/CSV_Files/CBayCRand_Lith_{}.csv'.format(surface)

    # Read VTP File Into Data
    vtkreader = vtk.vtkXMLPolyDataReader()
    vtkreader.SetFileName(Input)
    vtkreader.Update()

    # Convert VTP File Data to Points
    points = vtkreader.GetOutput()
    point_cloud = points.GetPoints()

    # Create Table of Point Data
    table = vtk.vtkDataObjectToTable()
    table.SetInputData(points)
    table.Update()
    table.GetOutput().AddColumn(point_cloud.GetData())
    table.Update()

    #Write Point Data Table to CSV File
    vtkwriter = vtk.vtkDelimitedTextWriter()
    vtkwriter.SetInputConnection(table.GetOutputPort())
    vtkwriter.SetFileName(Output)
    vtkwriter.Update()
    vtkwriter.Write()

    # Read New CSV File into Data
    csvreader = csv.reader(open(Output, 'r+'), delimiter = ",")
    headers = list(csvreader)

    # Modify Entries in First Line (Headers) of CSV File
    headers[0][0] = 'X'
    headers[0][1] = 'Y'
    headers[0][2] = 'Z'

    # Write Modified Entries Back to File
    # NOTE: newline = '' argument required to avoid generation of empty space is csv file
    csvwriter = csv.writer(open(Output, 'w', newline = ''), delimiter = ",")
    csvwriter.writerows(headers)

    # Create Shapefile Writer and specify Point geometry type, NOTE: shapeType is the type of geometry, where 11 = POINTZ
    shpwriter = shapefile.Writer('C:/Users/acgr9/Desktop/CBay_Crand/Geomodel/VTK_Export/Shapefiles/CBayCRand_Surface_{}'.format(surface), shapeType = 11)

    # Ensure that for every record there is a corresponding geometry
    shpwriter.autoBalance = 1

    # Define Fields in New Shapefile
    shpwriter.field('X', 'N', decimal = 5)
    shpwriter.field('Y', 'N', decimal = 5)
    shpwriter.field('Z', 'N', decimal = 5)

    # Read Modified CSV File Again
    csvreader = csv.reader(open(Output, 'r'))

    # Skip the Header in the CSV File
    next(csvreader, None)

    # Convert Imported CSV Data to List
    Data = list(csvreader)

    # Loop through each row and assign their values to variables
    for row in Data:
        X = row[0]
        Y = row[1]
        Z = row[2]

    # Build the Point Geometry. NOTE: Be mindful, indent is needed here to keep it in the loop
        shpwriter.pointz(float(X),float(Y),float(Z))

    # Add attribute data. NOTE: Be mindful, indent is needed here to keep it in the loop
        shpwriter.record(X, Y, Z)

    i = i+1
