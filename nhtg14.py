import Image, numpy, ephem, datetime

def datetime2azalt(datetime):
  # At datetime, what is the angular location
  # of the sun over the map in radians?
  # azimuthal angle is measured clockwise from north
  # altitude angle is the elevation from the horizon
  # Returns radians
  o = ephem.Observer()
  o.lat, o.long, o.date = '51:45', '-1:15', datetime
  sun = ephem.Sun(o)
  return float(sun.az), float(sun.alt)

def array2image(array):
  # Converts a numpy array to an image
  normArray = (255.0 / array.max() * (array - array.min())).astype(numpy.uint8)
  im = Image.fromarray(normArray)
  return im

def bitmaskArray(array, thresh):
  # produces a bitmask of the data
  lowValueIndicies = array < thresh
  threshArray = numpy.zeros((1000,1000))
  threshArray[lowValueIndicies] = 1
  return threshArray

def GIS2array():
  # Extract what we want from the GIS file
  filename = 'SP5106_DSM_1M.asc'
  data = open(filename, 'r')
  #parameters = dict()
  heightmap = []
  for line in data:
    if not line[0].isdigit():
      # parse the parameters; ncols, nrows etc.
      # parameters[line.split(' ')[0]] = line[14:]
      continue
    # For the space-delimited numeric data
    heightmap.append(line.split(' ')[:-1])
  buildingMap = numpy.array(heightmap).astype(float)
  return buildingMap

def zeroedBuildingMap(buildingMap):
  # We want heights to be measured from an average "ground"
  # clip any negative values to zero?
  return buildingMap - buildingMap.min() - 30.

def generateShadowMap(buildingMap, datetime):
  # A shadow map represents a surface defined for each point in the plane
  # that defines how far up an object standing in a certain point
  # will be shaded by the occulting structure(s)
  # Initalize a shadow map, same size as the building map
  # This will be built up through a monte carlo style random sampling
  # Is an iterative approach necessarily necessary, because shadows overlap?
  shadowMap = numpy.zeros((1000,1000))
  az, alt = datetime2azalt(datetime)
  azDispl = numpy.array([numpy.sin(az),-numpy.cos(az)])
  for iteration in range(0,99):
    # Make a temporary array for this round of random numbers
    tempShadowMap = numpy.zeros((1000,1000))
    # generate random numbers on a subset of the image,
    # attempting to avoid problems with out of range indicies
    # low and high define the internal bounding box
    # size is (number of desired samples, 2)
    randomSample = numpy.random.random_integers(100, 900, (1000,2))
    for sample in range(0,1000):
      arrayPoint = randomSample[sample]
      tuplePoint = arrayPoint[0],arrayPoint[1]
      # Find the height at randomCoord
      height = buildingMap[tuplePoint]
      # Project randomCoord by az and alt, basic trigonometry
      shadowL = height / numpy.tan(alt)
      projectedPoint = arrayPoint + shadowL*azDispl
      # Interpolate the points between, making unit steps along x
      difference = projectedPoint - arrayPoint
      xSteps = difference[0]
      xUnitDispl = difference / xSteps
      for i in range(0,abs(int(xSteps))):
        inter = arrayPoint + i*xUnitDispl
        shadowHeight = height*(1-(numpy.linalg.norm(i*xUnitDispl)/shadowL))
        tempShadowMap[inter[0],inter[1]] = shadowHeight
    # After generating a new tempShadowMap each iteration,
    # we want to update the existing map,
    # but only rewriting an entry if it is larger than the one already there
    shadowMapIndicies = shadowMap > tempShadowMap
    tempShadowMap[shadowMapIndicies] = 0
    shadowMap = shadowMap + tempShadowMap
  return shadowMap

def compareShadow2Building(buildingMap, datetime):
  bitmask = numpy.zeros((1000,1000))
  shadowMap = generateShadowMap(buildingMap, datetime)
  lowValues = shadowMap > buildingMap
  bitmask[lowValues] = 1
  return bitmask

# Sample date time
# to achieve 7 points in the day, sampled at the first of each month
# To form the averaged images, we will iterate over
# months = range(1,13)
# hours = range(6,20,2)
# to achieve 7 points in the day, sampled at the first of each month
# datetime.datetime(2014,month,1,hour,0)

sample_datetime = datetime.datetime(2014,3,8,14,0)
buildingMap = zeroedBuildingMap(GIS2array())
bitmask = compareShadow2Building(buildingMap,sample_datetime)
bitmaskImage = array2image(bitmask)
bitmaskImage.save('some1.png')

#buildings = array2image(displArray)
#buildings.save('some1.png')

#threshtest = array2image(thresholdArray(GIS2array(), 70))
#threshtest.save('some1.png')
