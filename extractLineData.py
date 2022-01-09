# based on "An efficient and robust ray-box intersection algorithm." Journal of graphics tools 10, no. 1 (2005)
import vtk
import time
import numpy as np
import matplotlib.pyplot as plt
import logging
from vtk.util import numpy_support

# TODO: - implement Super Cursor search method when they are fixed -> probably more efficient than current method
#       - Speed improvements: for hor/ver lines
#       - use logging for errors

class extractLineData(object):
  """
  Tool to extract data along a segment defined by two points in a HyperTreeGrid structure.

  The HyperTreeGrid can be 3D or 2D. The method findIntersection() can be called mutltiple
  times to extract different areas of the HTG. Il will return the extracted data each time.

  Note: this class will only store one type of field, so as to hold homogeneous data.
  In order to extract data from a different field, a new extractLineData object should
  be created.

  Methods
  -------
  findIntersection()
  displaySegments()
  plotData()
  """

  constantAxis = np.array([])
  cursor = vtk.vtkHyperTreeGridNonOrientedGeometryCursor()
  dataNumber = 0
  initialized = False
  data = {}

  bounds = np.zeros(6)

  inv_log2 = 1/np.log(2)

  def __init__(self, htg, field=None, maxLevel=99, intersectionField=None):
    """
    Parameters
    ----------
    htg: vtk HyperTreeGrid object.
      the tree used to extract Data. This tree must have a dataset attached to it.
    field: string
      Gives the name of field on the HTG (htg).
    maxLevel: int, optional
      Sets a limit to the depth traversal of the HTG (htg)
    """
    self.htg = htg

    self.dimension = htg.GetDimension()
    self.maxLevel = maxLevel

    self.xGridCoords = numpy_support.vtk_to_numpy( htg.GetXCoordinates() )
    self.yGridCoords = numpy_support.vtk_to_numpy( htg.GetYCoordinates() )
    self.zGridCoords = numpy_support.vtk_to_numpy( htg.GetZCoordinates() )

    self.boxLen = abs( self.xGridCoords[1] - self.xGridCoords[0] )

    self.field = field

    assert self.field != None

    self.dataArray = self.htg.GetPointData().GetArray(self.field)

  def __initializeSegment(self):
    self.direction = self.endPoint - self.startPoint
    self.sign = np.where(self.direction < 0, [1]*len(self.endPoint), [0]*len(self.endPoint))

    # Avoid printing error when infinity encoutered
    with np.errstate(divide='ignore'):
      self.invDirection = np.divide(1.0, self.direction)

    # Signal along which axis the line is constant
    self.constantAxis = (self.direction == 0)

    self.length = np.linalg.norm(self.direction, ord=2)

  def __validatePoints(self):
    errorA = False
    errorB = False

    if( not(self.xGridCoords[0] <= self.startPoint[0] <= self.xGridCoords[1]) ):
      print("Invalid range for x coordinate of point A. Setting default range")
      errorA = True

    if( not(self.yGridCoords[0] <= self.startPoint[1] <= self.yGridCoords[1]) ):
      print("Invalid range for y coordinate of point A. Setting default range")
      errorA = True

    if( len(self.startPoint) > 2 ):
      if( not(self.zGridCoords[0] <= self.startPoint[2] <= self.zGridCoords[1]) ):
        print("Invalid range for z coordinate of point A. Setting default range")
        errorA = True

    if( not(self.xGridCoords[0] <= self.endPoint[0] <= self.xGridCoords[1]) ):
      print("Invalid range for x coordinate of point B. Setting default range")
      errorB = True

    if( not(self.yGridCoords[0] <= self.endPoint[1] <= self.yGridCoords[1]) ):
      print("Invalid range for y coordinate of point B. Setting default range")
      errorB = True

    if( len(self.startPoint) > 2 ):
      if( not(self.yGridCoords[0] <= self.endPoint[2] <= self.yGridCoords[1]) ):
        print("Invalid range for z coordinate of point B. Setting default range")
        errorB = True

    if( np.array_equal(self.startPoint, self.endPoint) ):
      print("The points are the same!")
      errorA = True
      errorB = True

    if( errorA ):
      self.startPoint = [self.xGridCoords[0], self.yGridCoords[0]] if (self.dimension == 2) else [self.xGridCoords[0], self.yGridCoords[0], self.zGridCoords[0]]
    if( errorB ):
      self.endPoint = [self.xGridCoords[1], self.yGridCoords[1]] if (self.dimension == 2) else [self.xGridCoords[1], self.yGridCoords[1], self.zGridCoords[1]]

  def __initMask(self):
        # Stop conditions
    if( self.cursor.GetLevel() >= self.maxLevel ):
      return

    if self.cursor.IsLeaf() or self.cursor.GetLevel() == self.maxLevel:
      self.cursor.SetMask(True)
      return
    else:
      for ison in range( self.cursor.GetNumberOfChildren() ):
        self.cursor.ToChild(ison)
        self.__initMask()
        self.cursor.ToParent()

  def __intersects(self, cellBounds):
    # Bounds is of form (xmin, xmax, ymin, ymax, zmin, zmax)
    # must be reshaped to ( [xmin; ymin; zmin], [xmax; ymax; zmax] )
    l = len(cellBounds)
    min = np.reshape(cellBounds[range(0, l, 2)], (3, 1))
    max = np.reshape(cellBounds[range(1, l+1, 2)], (3, 1))
    bounds = np.concatenate((min, max), axis=1)

    for i in range(len(self.constantAxis)):
      if( self.constantAxis[i] ):
        if( not (cellBounds[2*i] <= self.startPoint[i] <= cellBounds[2*i+1]) ):
          return False

    if( self.constantAxis[0] ):
      tmin = -np.inf
      tmax = +np.inf
    else:
      tmin = (bounds[:, self.sign[0]][0] - self.startPoint[0]) * self.invDirection[0]
      tmax = (bounds[:, 1 - self.sign[0]][0] - self.startPoint[0]) * self.invDirection[0]

    if( self.constantAxis[1] ):
      tymin = -np.inf
      tymax = +np.inf
    else:
      tymin = (bounds[:, self.sign[1]][1] - self.startPoint[1]) * self.invDirection[1]
      tymax = (bounds[:, 1 - self.sign[1]][1] - self.startPoint[1]) * self.invDirection[1]

    if( (tmin >= tymax) or (tymin >= tmax) ):
      return False
    if( tymin > tmin ):
      tmin = tymin
    if( tymax < tmax ):
      tmax = tymax

    if( len(self.startPoint) > 2 ):
      if( self.constantAxis[2] ):
        tzmin = -np.inf
        tzmax = +np.inf
      else:
        tzmin = ( bounds[:, self.sign[2]][2] - self.startPoint[2] ) * self.invDirection[2]
        tzmax = ( bounds[:, 1 - self.sign[2]][2] - self.startPoint[2] ) * self.invDirection[2]

      if( (tmin >= tzmax) or (tzmin >= tmax) ):
        return False
      if( tzmin > tmin ):
        tmin = tzmin
      if( tzmax < tmax ):
        tmax = tzmax

    # Check that we are in the rectangular box defined by our segment
    return (0 <= tmin) and (tmax <= 1)

  def __findIntersectionRec(self):

    self.cursor.GetBounds(self.bounds)
    IsLeaf = self.cursor.IsLeaf()
    intersects = self.__intersects(self.bounds)

    # Check for line in leaf cells
    if( intersects or self.cursor.GetLevel() <= self.minLevel ):
      if( IsLeaf or self.cursor.GetLevel() == self.maxLevel ):
        self.cursor.SetMask(False)
        self.data[self.dataNumber] = np.append( self.data[self.dataNumber], self.dataArray.GetTuple1(self.cursor.GetGlobalNodeIndex()) )
      else:
        for ison in range( self.cursor.GetNumberOfChildren() ):
          self.cursor.ToChild(ison)
          self.__findIntersectionRec()
          self.cursor.ToParent()

    else:
      return

  def findIntersection(self, startPoint=None, endPoint=None, maxLevel=99):
    """Recursively finds the cells intersected by the line segment.

    Parameters
    ----------
    startPoint/endPoint: array_like
      array containing a point, should therefore be of size (1, 3) or (1, 2)

    Returns
    -------
    dict of numpy array(s)
      numpy arrays of found data.
    """
    self.startPoint = np.array(startPoint)
    self.endPoint = np.array(endPoint)

    self.htg.InitializeNonOrientedGeometryCursor(self.cursor, 0, True)

    if( not self.initialized ):
      self.__initMask()
      self.initialized = True

    self.__initializeSegment()
    self.__validatePoints()

    self.data[self.dataNumber] = np.array([])

    self.minLevel = int( self.inv_log2 * np.log(self.boxLen/self.length) )
    
    if( self.maxLevel <= self.minLevel ):
      self.maxLevel = self.minLevel
      print("Segment is too small for the desired maxLevel. Please lengthen the segment")
    else:
      self.maxLevel = maxLevel

    # print( "\t> Starting extraction of {} field along specified segment(s)...".format(self.field) )
    tic = time.perf_counter()

    self.__findIntersectionRec()

    tac = time.perf_counter()
    # print( "\t> Finished extraction of {0} field...  time spent : {1:10.6f} s \n".format(self.field, tac-tic) )
    print( tac-tic )

    self.dataNumber += 1

    return self.data

  def displaySegments(self):
    """Tool method to displays the found segments.

    No parameters, no returned values.
    """

    colors = vtk.vtkNamedColors()

    self.htg.GetPointData().SetActiveScalars(self.field)
    dataRange = self.htg.GetPointData().GetArray(self.field).GetRange()
    dataRange = np.array(dataRange)

    #Generate a polygonal representation of a hypertree grid
    geometry = vtk.vtkHyperTreeGridGeometry()
    geometry.SetInputData(self.htg)

    shrink = vtk.vtkShrinkFilter()
    shrink.SetInputConnection(geometry.GetOutputPort())
    shrink.SetShrinkFactor(1) # 1.0 no shrink

    font = vtk.vtkTextProperty()
    font.SetFontSize(3)
    font.SetFontFamilyToTimes()

    # Look up table
    lut = vtk.vtkLookupTable()
    lut.SetScaleToLinear()

    propT = vtk.vtkTextProperty()
    propL = vtk.vtkTextProperty()
    propT.SetFontFamilyToArial()
    propT.SetFontSize(25)
    propT.SetColor(0, 0, 0)
    propL.SetColor(0, 0, 0)

    scalarBar = vtk.vtkScalarBarActor()
    scalarBar.SetLookupTable(lut)
    scalarBar.SetMaximumWidthInPixels(80)
    scalarBar.SetLabelTextProperty(font)
    scalarBar.SetTitleTextProperty(font)
    scalarBar.SetTitleTextProperty(propT)
    scalarBar.SetLabelTextProperty(propL)
    # scalarBar.SetLabelFormat("%5.2f")
    scalarBar.UnconstrainedFontSizeOn()
    scalarBar.DrawTickLabelsOn()
    scalarBar.SetTextPad(5)

    scalarBar.SetTitle(self.field)

    mapper = vtk.vtkDataSetMapper()
    mapper.SetInputConnection(shrink.GetOutputPort())
    mapper.ScalarVisibilityOn()
    mapper.SetColorModeToMapScalars()
    mapper.SetScalarModeToUseCellFieldData()
    mapper.SelectColorArray(self.field)
    mapper.SetLookupTable(lut)
    mapper.SetScalarRange(dataRange)

    actor = vtk.vtkActor()
    actor.SetMapper(mapper)
    actor.GetProperty().SetDiffuseColor(colors.GetColor3d('Burlywood'))
    actor.GetProperty().SetEdgeVisibility(True)

    # Create the RenderWindow, Renderer and Interactor
    renderer = vtk.vtkRenderer()

    istyle = vtk.vtkInteractorStyleTrackballCamera()

    renderWindow = vtk.vtkRenderWindow()
    renderWindow.AddRenderer(renderer)
    interactor = vtk.vtkRenderWindowInteractor()
    interactor.SetRenderWindow(renderWindow)
    interactor.SetInteractorStyle(istyle)

    renderer.SetBackground(colors.GetColor3d('white'))
    renderer.AddActor(actor)

    bounds = np.concatenate((self.xGridCoords, self.yGridCoords, self.zGridCoords))

    cubeAxesActor = vtk.vtkCubeAxesActor()
    cubeAxesActor.SetBounds(bounds)
    cubeAxesActor.SetCamera(renderer.GetActiveCamera())
    cubeAxesActor.GetTitleTextProperty(0).SetColor(0, 0, 0)
    cubeAxesActor.GetLabelTextProperty(0).SetColor(0, 0, 0)

    cubeAxesActor.GetTitleTextProperty(1).SetColor(0, 0, 0)
    cubeAxesActor.GetLabelTextProperty(1).SetColor(0, 0, 0)

    cubeAxesActor.GetTitleTextProperty(2).SetColor(0, 0, 0)
    cubeAxesActor.GetLabelTextProperty(2).SetColor(0, 0, 0)

    cubeAxesActor.GetXAxesLinesProperty().SetColor(0, 0, 0)
    cubeAxesActor.GetYAxesLinesProperty().SetColor(0, 0, 0)
    cubeAxesActor.GetZAxesLinesProperty().SetColor(0, 0, 0)
    cubeAxesActor.GetXAxesGridlinesProperty().SetColor(0, 0, 0)
    cubeAxesActor.GetYAxesGridlinesProperty().SetColor(0, 0, 0)
    cubeAxesActor.GetZAxesGridlinesProperty().SetColor(0, 0, 0)

    cubeAxesActor.DrawXGridlinesOn()
    cubeAxesActor.DrawYGridlinesOn()
    cubeAxesActor.DrawZGridlinesOn()
    cubeAxesActor.SetGridLineLocation(cubeAxesActor.VTK_GRID_LINES_FURTHEST)
    cubeAxesActor.XAxisMinorTickVisibilityOff()
    cubeAxesActor.YAxisMinorTickVisibilityOff()
    cubeAxesActor.ZAxisMinorTickVisibilityOff()

    renderer.AddActor(cubeAxesActor)

    renderer.AddActor2D(scalarBar)
    renderer.ResetCamera()
    renderer.GetActiveCamera().Azimuth(150)
    renderer.GetActiveCamera().Elevation(30)
    renderer.ResetCameraClippingRange()

    renderWindow.SetSize(640, 480)
    renderWindow.Render()
    renderWindow.SetWindowName('HyperTreeGrid')

    interactor.Start()

  def plotData(self, logY = False, select = None):
    """Quick tool to plot the found data
    Uses matplotlib.
    Parameters
    ----------
    logY: bool
      If set to true, will plot data with log set on y axis
    select: array_like
      List of keys wished to be plotted
    """
    fig, ax = plt.subplots()

    if( select == None ):
      if( logY ):
        for key, data in self.data.items():
          xRange = np.linspace(0, 1, len(data))
          ax.semilogy(xRange, data, label=key)
      else:
        for key, data in self.data.items():
          xRange = np.linspace(0, 1, len(data))
          ax.plot(xRange, data, label=key)
    else:
      subData = {key: self.data[key] for key in select}
      if( logY ):
        for key, data in subData.items():
          xRange = np.linspace(0, 1, len(data))
          ax.semilogy(xRange, data, label=key)
      else:
        for key, data in subData.items():
          xRange = np.linspace(0, 1, len(data))
          ax.plot(xRange, data, label=key)

    ax.set(xlabel='% of length of AB', ylabel=self.field,
          title='Extracted data along line segment(s)')
    ax.grid()

    if( len(self.data.keys()) < 10 ):
      ax.legend()
    else:
      print("Not enough space for legend")

    plt.show()
