#---------------------------------------INTRODUCTION-------------------------------------------------------------#
# Institute of Chinese Materia Medica, China Academy of Chinese Medical Sciences, Beijing, China.@ Copy right
# Date of development 2018/06/08
# Author
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
outPut = arcpy.GetParameterAsText(2)
#-------------------------------To extract environment variables-----------------------------------------------#
arcpy.SetProgressorLabel("The progress is extracting environment variables,please wait for several minutes...")
fileName="ecoFactor.xls"
arcpy.sa.ExtractMultiValuesToPoints(input,envList, "NONE")
arcpy.TableToExcel_conversion(input,outPut+"/"+fileName,"ALIAS","CODE")