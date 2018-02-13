
# coding: utf-8

# In[ ]:

from xml.dom.minidom import parse
import scipy.ndimage as ndi
from mpl_toolkits.basemap import Basemap
import numpy
from pylab import*
#get_ipython().magic('pylab inline')

# parse an XML file
dom=parse('TDX1_SAR_SSC_BRX2_SM_D_SRA_20150321T165909_20150321T165917.xml')

#Find the Corner Coordinates
sceneCornerCoordList=dom.getElementsByTagName('sceneCornerCoord')
CornercoordsList=[]
#Sort out the corners
for sceneCornerCoord in sceneCornerCoordList:
    lat=float(sceneCornerCoord.getElementsByTagName('lat')[0].childNodes[0].wholeText)
    lon=float(sceneCornerCoord.getElementsByTagName('lon')[0].childNodes[0].wholeText)
    CornercoordsList.append ({'lat':lat,'lon':lon})


#Empty massives
x=[]
y=[]

#Add the corner coordinates of the image
for i in range(4):
    x.append(CornercoordsList[i]['lon'])
    y.append(CornercoordsList[i]['lat'])
    
mpl.rcParams['axes.unicode_minus']=False
#Create figure and axes instances.
fig=plt.figure(figsize=(10,10))
ax=fig.add_axes([0.1,0.1,0.8,0.8])
#Create polar stereographic Basemap instance.
m=Basemap(projection='stere',resolution='l',llcrnrlon=-157.7,llcrnrlat=70.8,urcrnrlon=-155.9,urcrnrlat=71.6,lon_0=-156.8,lat_0=71.2,rsphere=(6378273.,6356889.))

#Change the projection
lon=(x[0],x[1],x[3],x[2],x[0])
lat=(y[0],y[1],y[3],y[2],y[0])
x,y=m(lon,lat)

#New "stere" coorner coordinates
X=array([[x[0],x[1]],[x[3],x[2]]],dtype=float)
Y=array([[y[0],y[1]],[y[3],y[2]]],dtype=float)

rows=15996
cols=2528

#coordinates interpolation
X1=ndi.zoom(X,(rows/2,cols/2),order=1)
Y1=ndi.zoom(Y,(rows/2,cols/2),order=1)

#Draw coastlines, state and country boundaries, edge of map.
m.drawcoastlines()
m.drawstates()
m.drawcountries()
m.drawmapboundary(fill_color='dodgerblue')
m.drawrivers()
m.fillcontinents(color='snow',lake_color='aqua',zorder=0)
m.drawparallels(np.arange(70.9,71.6,0.1), labels=[1,0,0,1],fontsize=10)
m.drawmeridians(np.arange(-157.4,-156.0,0.3), labels=[1,0,0,1], labelstyle='+/-',fontsize=10)
m.plot(x,y,linewidth=3,color='r')
#m.scatter(X1,Y1,color='black')
plt.title('Barrow, Alaska')

#Find our file

img2 = plt.imread('2.jpg')

c=9.14/(2*pi)*25
B=-22.6
img_v=img2*c/B


#Plot this image on the map
#plt.pcolormesh(X1[::35,::4], Y1[::35,::4], img_v[0:-7,0:-68,0],cmap=cm.bwr)
plt.pcolormesh(X1[::70,::8], Y1[::70,::8], img_v[0:-7:2,0:-68:2,1],cmap=cm.bwr)
plt.colorbar(label='velocity')
plt.show()

