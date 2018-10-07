#!C:\\Python27\ArcGIS10.5\Python python
"""
    Converts special case of XYZ file into shapefiles.
    
    @author Keenan Mandela Gebze
    @ver 6 October 2018
"""

def get_xyz_feature_statistics(path_to_xyz, feature_delimiter="\n", field_delimiter="="):
    """
        Get xyz feature counts.
    """

    first_feature = True
    ring = True

    reducer = Reducer()
    reducer.register("vertex_length", min_max_reducer_default_seed(), min_max_reducer)
    reducer.register("counts", 0, lambda x, y: x+1)

    for feature in get_xyz_features(path_to_xyz):
        parsed_feature = feature_parser(feature)
        attributes = parsed_feature["attributes"]
        geometry = parsed_feature["geometry"]
        reducer.register("field_set", set(), set_reducer)
        for field_name, field_data in attributes.items():
            reducer.register(field_name+"_length", min_max_reducer_default_seed(), min_max_reducer)
            reducer.feed(field_name+"_length", len(field_data))
            reducer.feed("field_set", field_name)
        # check geometry's vertex number
        if first_feature:
            reducer.register("vertex_length", {"min":len(geometry), "max": 0}, min_max_reducer)
        reducer.feed("vertex_length", len(geometry))
        
        # check for ring like geometry
        if ring and len(geometry) >= 3:
            if (geometry[0] != geometry[-1]): ring = False

        # feature counts
        reducer.feed("counts", 1)

    result = reducer.getAll()
    result.update({"ring_like": ring})
    return result

def get_xyz_features(path_to_xyz):
    """
        Extract XYZ data in to python list as string (text).
    """
    with open(path_to_xyz) as file:
        line_buffer = []
        for line in file:
            if line == "\n":
                yield line_buffer
                line_buffer = []
            else:
                line_buffer.append(line.strip('\n'))

def feature_parser(feature, field_delimiter="="):
    result = {"attributes": {}, "geometry": []}
    infer_field = [i for i in filter(lambda f: len(f.split(field_delimiter)) >= 2 , feature)]
    infer_geom = [i for i in filter(lambda f: len(f.split(field_delimiter)) < 2 , feature)]
    for field in infer_field:
        token = field.split("=")
        field_name = token[0].strip(" \r\n\t").replace(" ", "_")
        field_data = token[1].strip(" \r\n\t")
        result["attributes"].update({field_name: field_data})
    for geom in infer_geom:
        point = map(lambda v: float(v), geom.split(","))
        result["geometry"].append(point)
    return result

def main():    
    import arcpy
    import os, sys
    arcpy.env.overwriteOutput = True

    input_xyz = sys.path[0]+os.sep+"test_data"+os.sep+"Pitsit_CRST.xyz"
    output_workspace = sys.path[0]+os.sep+"test_data"
    output_shp = "output.shp"
    output_path = output_workspace+os.sep+output_shp
    
    arcpy.CreateFeatureclass_management(output_workspace, output_shp, "POLYLINE", "#", "DISABLED", "ENABLED", arcpy.SpatialReference(32753))
    
    feature_statistics = get_xyz_feature_statistics(input_xyz)

    for field in feature_statistics["field_set"]:
        arcpy.AddField_management(output_path, field[:10], "TEXT", "#", "#", feature_statistics[field+"_length"]["max"])
        
    with arcpy.da.InsertCursor(output_shp, ["*"]) as cursor:
        for feature in get_xyz_features(input_xyz):
            parsed_feature = feature_parser(feature)
            
            cursor.insertRow()

class Reducer():
    
    def __init__(self):
        self.acc = {}
        self.reducing_logics = {}
    
    def register(self, variable_name, seed_value, reducing_logic):
        try:
            self.acc[variable_name]
            self.reducing_logics[variable_name]
        except KeyError:
            self.acc[variable_name] = seed_value
            self.reducing_logics[variable_name] = reducing_logic
    
    def feed(self, variable_name, value):
        reducing_logic = self.reducing_logics[variable_name]
        self.acc[variable_name] = reducing_logic(self.acc[variable_name], value)
    
    def get(self, variable_name):
        return self.acc[variable_name]

    def getAll(self):
        return dict(self.acc)

min_max_reducer_default_seed = lambda: dict({"min": 20000000, "max": 0})

def min_max_reducer(seed, value):
    if (value < seed["min"]): seed["min"] = value
    if (value > seed["max"]): seed["max"] = value
    return seed

def set_reducer(seed, value):
    seed.add(value)
    return seed

if __name__ == "__main__":
    main()
