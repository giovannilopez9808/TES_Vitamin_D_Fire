from Class_list import *
inputs = {
    "path data": "../Data/",
    "file Davis": "data_Davis.csv",
    "file OMI": "data_OMI_OMT03",
    "day initial": "2020-05-11",
    "day final": "2020-09-30",
}
Davis = Davis_data(inputs["path data"],
                   inputs["file Davis"],
                   inputs["day initial"],
                   inputs["day final"])
OMI = OMI_data(inputs["path data"],
               inputs["file OMI"],
               inputs["day initial"],
               inputs["day final"])
print(Davis.data)
print(OMI.data)
