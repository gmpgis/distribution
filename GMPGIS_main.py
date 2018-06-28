#---------------------------------------INTRODUCTION-------------------------------------------------------------#
# Institute of Chinese Materia Medica, China Academy of Chinese Medical Sciences, Beijing, China.@ Copy right
# Date of development 2018/06/08
# Author J.W.
#----------------------------------Import system module----------------------------------------------------------#
import arcpy
import os
import arcpy.mapping as mapping
from arcpy.sa import *
from arcpy import env
isOK= arcpy.CheckOutExtension("Spatial")
print isOK
input = arcpy.GetParameterAsText(0)
envList = arcpy.GetParameter(1)
input1 = arcpy.GetParameterAsText(2)
input2 = arcpy.GetParameterAsText(3)
outPut = arcpy.GetParameterAsText(4)
outPutEnv = arcpy.Describe(input)
shapeBaseName=outPutEnv.BaseName
envListField=arcpy.ListFields(input)
envFieldName=[]
#-------------------------------To extract environment variables-----------------------------------------------#
for temp in envListField:
	envFieldName.append(temp.name)
if "PC1" not in envFieldName:
	arcpy.sa.ExtractMultiValuesToPoints(input,envList, "NONE")
	arcpy.sa.ExtractMultiValuesToPoints(input,"hwsd", "NONE")
#-------------------------------Remove the point in the (.shp ) file where the data is 0---------------------------#
envStr=["PC1","PC2","PC3","PC4","PC5","PC6"]
for st in envStr:
	with arcpy.da.UpdateCursor(input,st) as cursor:
		for row in cursor:
			if row[0]==0:
				cursor.deleteRow()
del row
del cursor
calcName=[]
for list in envList:	
	max=0;
	min=1000;
	listD = arcpy.Describe(list)
	listName=listD.BaseName
	arcpy.SetProgressorLabel("The progress is runing a "+listName+" Raster,please wait for several minutes...")
	calcName.append(outPut+"/"+listName)
	with arcpy.da.SearchCursor(input,listName) as cursor:
		for row in cursor:
			if max < row[0]:
				max = row[0]
			if min > row[0]:
				min = row[0]
	envRaster = arcpy.Raster(listD.path+"/"+listName)
	raster=Con((envRaster>=min) & (envRaster <=max) ,0,Con(envRaster >=(max+min)//2,max-envRaster,envRaster-min))
	arcpy.SetProgressorLabel("The progress is saving a "+listName+" Raster,please wait for several minutes...")
	raster.save(outPut+"/"+listName)
# To calculate Euclidean distance
PC1 = Raster(outPut+"/PC1")
PC2 = Raster(outPut+"/PC2")
PC3 = Raster(outPut+"/PC3")
PC4 = Raster(outPut+"/PC4")
PC5 = Raster(outPut+"/PC5")
PC6 = Raster(outPut+"/PC6")
arcpy.SetProgressorLabel("The progress is runing  dis,please wait for several minutes...")
dis =(PC1 * PC1 * 0.166 + PC2 * PC2 * 0.166 + PC3 * PC3 * 0.166 + PC4 * PC4 * 0.166 + PC5 * PC5 * 0.166 + PC6 * PC6 * 0.166 )**0.5
dis.save(outPut+"/dis")
myremap = RemapRange([[0,0.1,1],[0.1,100,2]])
arcpy.SetProgressorLabel("The progress is recalssifation, please wait for several minutes...")
redis = Reclassify(dis,"Value",myremap)
arcpy.SetProgressorLabel("The progress is saving redis, please wait for several minutes...")
redis.save(outPut+"/redis")
#------------------------------To calculate suitable soil regions--------------------------------------------#
table = outPut+"/table"
print table
arcpy.CopyRows_management(input,table)
arcpy.CopyRows_management("HWSD_SMU",outPut+"/HWSD_SMU")
arcpy.CopyRows_management("HWSD_DATA",outPut+"/HWSD_DATA")

table_listfield=arcpy.ListFields(table)
fieldName=[]
for tt in table_listfield:
	fieldName.append(tt.name)
if 'SU_CODE' not in fieldName:
	arcpy.JoinField_management (table, "hwsd", outPut+"/HWSD_SMU", "MU_GLOBAL", "SU_CODE;MU_GLOBAL")
	arcpy.JoinField_management (table, "MU_GLOBAL", outPut+"/HWSD_DATA","MU_GLOBAL","T_GRAVEL;T_SAND;T_SILT;T_CLAY;T_USDA_TEX_CLASS;T_REF_BULK_DENSI;T_BULK_DENSITY;T_OC;T_PH_H2O;T_CEC_CLAY;T_CEC_SOIL;T_BS;T_TEB;T_CACO3;T_CASO4;T_ESP;T_ECE")

arcpy.AddJoin_management("hwsd","VALUE","HWSD_SMU","MU_GLOBAL")
arcpy.AddJoin_management("hwsd","HWSD_SMU.MU_GLOBAL", "HWSD_DATA", "MU_GLOBAL", "KEEP_ALL")

cursor=arcpy.da.UpdateCursor(table,["SU_CODE"])
for row in cursor:
	if row[0]>=29:
		cursor.deleteRow()
del row
del cursor
T_USDA_TEX_CLASS=[]
T_SAND=[]
T_GRAVEL=[]
T_SILT=[]
T_CLAY=[]
T_USDA_TEX=[]
T_REF_BULK_DENSI=[]
T_BULK_DENSITY=[]
T_OC=[]
T_PH_H2O=[]
T_CEC_CLAY=[]
T_CEC_SOIL=[]
T_BS=[]
T_TEB=[]
T_CACO3=[]
T_CASO4=[]
T_ESP=[]
T_ECE=[]
array = arcpy.da.TableToNumPyArray(table,"T_GRAVEL", skip_nulls=True)
for row in array:
	T_GRAVEL.append(row[0])
	T_GRAVEL.sort()
array = arcpy.da.TableToNumPyArray(table,"T_SAND", skip_nulls=True)
for row in array:
	T_SAND.append(row[0])
	T_SAND.sort()
array = arcpy.da.TableToNumPyArray(table,"T_SILT", skip_nulls=True)
for row in array:
	T_SILT.append(row[0])
	T_SILT.sort()
array = arcpy.da.TableToNumPyArray(table,"T_CLAY", skip_nulls=True)
for row in array:
	T_CLAY.append(row[0])
	T_CLAY.sort()
array = arcpy.da.TableToNumPyArray(table,"T_USDA_TEX_CLASS", skip_nulls=True)
for row in array:
	T_USDA_TEX_CLASS.append(row[0])
	T_USDA_TEX_CLASS.sort()
array = arcpy.da.TableToNumPyArray(table,"T_REF_BULK_DENSI", skip_nulls=True)
for row in array:
	T_REF_BULK_DENSI.append(row[0])
	T_REF_BULK_DENSI.sort()
array = arcpy.da.TableToNumPyArray(table,"T_BULK_DENSITY", skip_nulls=True)
for row in array:
	T_BULK_DENSITY.append(row[0])
	T_BULK_DENSITY.sort()
array = arcpy.da.TableToNumPyArray(table,"T_OC", skip_nulls=True)
for row in array:
	T_OC.append(row[0])
array = arcpy.da.TableToNumPyArray(table,"T_PH_H2O", skip_nulls=True)
for row in array:
	T_PH_H2O.append(row[0])
	T_PH_H2O.sort()
array = arcpy.da.TableToNumPyArray(table,"T_CEC_CLAY", skip_nulls=True)
for row in array:
	T_CEC_CLAY.append(row[0])
	T_CEC_CLAY.sort()
array = arcpy.da.TableToNumPyArray(table,"T_CEC_SOIL", skip_nulls=True)
for row in array:
	T_CEC_SOIL.append(row[0])
	T_CEC_SOIL.sort()
array = arcpy.da.TableToNumPyArray(table,"T_BS", skip_nulls=True)
for row in array:
	T_BS.append(row[0])
	T_BS.sort()
array = arcpy.da.TableToNumPyArray(table,"T_TEB", skip_nulls=True)
for row in array:
	T_TEB.append(row[0])
	T_TEB.sort()
array = arcpy.da.TableToNumPyArray(table,"T_CACO3", skip_nulls=True)
for row in array:
	T_CACO3.append(row[0])
	T_CACO3.sort()
array = arcpy.da.TableToNumPyArray(table,"T_CASO4", skip_nulls=True)
for row in array:
	T_CASO4.append(row[0])
	T_CASO4.sort()
array = arcpy.da.TableToNumPyArray(table,"T_ESP", skip_nulls=True)
for row in array:
	T_ESP.append(row[0])
	T_ESP.sort()
array = arcpy.da.TableToNumPyArray(table,"T_ECE", skip_nulls=True)
for row in array:
	T_ECE.append(row[0])
	T_ECE.sort()

T_GRAVEL_MAX = T_GRAVEL[-1]
T_GRAVEL_MIN = T_GRAVEL[0]
T_SAND_MAX = T_SAND[-1]
T_SAND_MIN = T_SAND[0]
T_SILT_MAX = T_SILT[-1]
T_SILT_MIN = T_SILT[0]
T_CLAY_MAX = T_CLAY[-1]
T_CLAY_MIN = T_CLAY[0]
T_USDA_TEX_MAX = T_USDA_TEX_CLASS[-1]
T_USDA_TEX_MIN = T_USDA_TEX_CLASS[0]
T_REF_BULK_MAX=T_REF_BULK_DENSI[-1]
T_REF_BULK_MIN=T_REF_BULK_DENSI[0]
T_BULK_DEN_MAX = T_BULK_DENSITY[-1]
T_BULK_DEN_MIN = T_BULK_DENSITY[0]
T_OC_MAX = T_OC[-1]
T_OC_MIN = T_OC[0]
T_PH_H2O_MAX = T_PH_H2O[-1]
T_PH_H2O_MIN = T_PH_H2O[0]
T_CEC_CLAY_MAX = T_CEC_CLAY[-1]
T_CEC_CLAY_MIN = T_CEC_CLAY[0]
T_CEC_SOIL_MAX = T_CEC_SOIL[-1]
T_CEC_SOIL_MIN = T_CEC_SOIL[0]
T_BS_MAX = T_BS[-1]
T_BS_MIN = T_BS[0]
T_TEB_MAX = T_TEB[-1]
T_TEB_MIN = T_TEB[0]
T_CACO3_MAX = T_CACO3[-1]
T_CACO3_MIN = T_CACO3[0]
T_CASO4_MAX = T_CASO4[-1]
T_CASO4_MIN = T_CASO4[0]
T_ESP_MAX = T_ESP[-1]
T_ESP_MIN = T_ESP[0]
T_ECE_MAX = T_ECE[-1]
T_ECE_MIN = T_ECE[0]
sql=""
inlist=[]
for num in T_USDA_TEX_CLASS:
	if num not in inlist:
		inlist.append(num)
inlist.sort()
max=inlist[-1]
for num in inlist:
	if num>=max:
		sql=sql+"HWSD_DATA.T_USDA_TEX_CLASS={0}".format(num)
		break;
	else:
		sql=sql+"HWSD_DATA.T_USDA_TEX_CLASS={0} OR ".format(num)
sql=sql+"AND HWSD_DATA.T_GRAVEL >= {0} AND T_GRAVEL <= {1}".format(T_GRAVEL_MIN,T_GRAVEL_MAX)		
sql=sql+"AND HWSD_DATA.T_SILT >= {0} AND HWSD_DATA.T_SILT <= {1}".format(T_SILT_MIN,T_SILT_MAX)
sql=sql+"AND HWSD_DATA.T_CLAY >={0} AND HWSD_DATA.T_CLAY <={1}".format(T_CLAY_MIN,T_CLAY_MAX)
sql=sql+"AND HWSD_DATA.T_REF_BULK_DENSITY >={0} AND HWSD_DATA.T_REF_BULK_DENSITY <={1}".format(T_REF_BULK_MIN,T_REF_BULK_MAX)
sql=sql+"AND HWSD_DATA.T_BULK_DENSITY >={0} AND HWSD_DATA.T_BULK_DENSITY <={1}".format(T_BULK_DEN_MIN,T_BULK_DEN_MAX)
sql=sql+"AND HWSD_DATA.T_OC >={0} AND HWSD_DATA.T_OC <={1}".format(T_OC_MIN,T_OC_MAX)
sql=sql+"AND HWSD_DATA.T_PH_H2O >={0} AND HWSD_DATA.T_PH_H2O <={1}".format(T_PH_H2O_MIN,T_PH_H2O_MAX)
sql=sql+"AND HWSD_DATA.T_CEC_CLAY >={0} AND HWSD_DATA.T_CEC_CLAY <={1}".format(T_CACO3_MIN,T_CACO3_MAX)
sql=sql+"AND HWSD_DATA.T_CEC_SOIL >={0} AND HWSD_DATA.T_CEC_SOIL <={1}".format(T_CEC_SOIL_MIN,T_CEC_SOIL_MAX)
sql=sql+"AND HWSD_DATA.T_BS >={0} AND HWSD_DATA.T_BS <={1}".format(T_BS_MIN,T_BS_MAX)
sql=sql+"AND HWSD_DATA.T_TEB >={0} AND HWSD_DATA.T_TEB <={1}".format(T_TEB_MIN,T_TEB_MAX)
sql=sql+"AND HWSD_DATA.T_CACO3 >={0} AND HWSD_DATA.T_CACO3 <={1}".format(T_CACO3_MIN,T_CACO3_MAX)
sql=sql+"AND HWSD_DATA.T_CASO4 >={0} AND HWSD_DATA.T_CASO4 <={1}".format(T_CASO4_MIN,T_CASO4_MAX)
sql=sql+"AND HWSD_DATA.T_ESP >={0} AND HWSD_DATA.T_ESP <={1}".format(T_ESP_MIN,T_ESP_MAX)
sql=sql+"AND HWSD_DATA.T_ECE >={0} AND HWSD_DATA.T_ECE <={1}".format(T_ECE_MIN,T_ECE_MAX)
arcpy.SetProgressorLabel("The progress is calculating soil, please wait for several minutes...")
soilRaster=Con("hwsd",10,0,sql)
arcpy.SetProgressorLabel("The progress is saving soil, Raster please wait for several minutes...")
soilRaster.save(outPut+"/soil")
arcpy.SetProgressorLabel("The progress is plus soil Raster and redis Raster, please wait for several minutes...")
#----------------------------------------Final processing-----------------------------------------------------------#
disfinal=soilRaster+redis
disfinal.save(outPut+"/disfin")
dismap = RemapValue([[1,1],[2,1],[11,0],[12,1]])
arcpy.SetProgressorLabel("The progress is recalssify disfinal Raster, please wait for several minutes...")
final = Reclassify(disfinal,"Value",dismap)
arcpy.SetProgressorLabel("The progress is saving final Raster, please wait for several minutes...")
final.save(outPut+"/fin")
#---------------------------------------Pretreatment to Extrate regions' anea----------------------------------------------#
env.workspace = outPut
mxd = mapping.MapDocument("CURRENT")
df = mapping.ListDataFrames(mxd,"Layers")[0]
refLayer = mapping.ListLayers(mxd,"HWSD*",df)[0]
fin= mapping.Layer(r"fin")
mapping.InsertLayer(df,refLayer,fin,"BEFORE")
#--------------------------------------To extrate suitalbe reginons' area in China----------------------------------------#
# Execute SelectLayerByAttribute
arcpy.SelectLayerByAttribute_management("fin", "NEW_SELECTION", "\"VALUE\" =0")
# Execute RasterToPolygon
arcpy.RasterToPolygon_conversion("fin", "zones.shp", "NO_SIMPLIFY", "value")
# Execute IntersectAnalysis
arcpy.Intersect_analysis(["zones.shp",input1],"Intersect","ALL","","")
# Execute ConversationReference
arcpy.DefineProjection_management("Intersect.shp", "PROJCS['Sphere_Aitoff',GEOGCS['GCS_Sphere',DATUM['D_Sphere',SPHEROID['Sphere',6371000.0,0.0]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Aitoff'],PARAMETER['False_Easting',0.0],PARAMETER['False_Northing',0.0],PARAMETER['Central_Meridian',0.0],UNIT['Meter',1.0]]")
# Execute AddFileld
arcpy.CalculateAreas_stats("Intersect.shp", "IntersectAreaField.shp")
# Execute CountAreas
arcpy.Statistics_analysis("IntersectAreaField.shp", "CountAreas1", [["F_AREA", "SUM"]], "PYNAME")
#-------------------------------------To extrate suitalbe reginons' area across the globle--------------------------------#
# Execute IntersectAnalysis
arcpy.Intersect_analysis(["zones.shp",input2],"Intersect1","ALL","","")
# Execute ConversationReference
arcpy.DefineProjection_management("Intersect1.shp", "PROJCS['Sphere_Aitoff',GEOGCS['GCS_Sphere',DATUM['D_Sphere',SPHEROID['Sphere',6371000.0,0.0]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Aitoff'],PARAMETER['False_Easting',0.0],PARAMETER['False_Northing',0.0],PARAMETER['Central_Meridian',0.0],UNIT['Meter',1.0]]")
# Execute AddFileld
arcpy.CalculateAreas_stats("Intersect1.shp", "IntersectAreaField1.shp")
# Execute CountAreas
arcpy.Statistics_analysis("IntersectAreaField1.shp", "CountAreas2", [["F_AREA", "SUM"]], "ENGLISH")

