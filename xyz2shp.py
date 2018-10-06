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
    reducer.register("max_vertex_length", 0, max_reducer)
    reducer.register("counts", 0, lambda x, y: x+1)

    for feature in get_xyz_features(path_to_xyz):
        # checks field
        infer_field = [i for i in filter(lambda f: len(f.split(field_delimiter)) >= 2 , feature)]
        infer_geom = [i for i in filter(lambda f: len(f.split(field_delimiter)) < 2 , feature)]
        reducer.register("field_set", set(), set_reducer)

        for field in infer_field:
            token = field.split(field_delimiter)
            field_name = token[0].strip(" \r\n\t").replace(" ", "_")
            field_data = token[1].strip(" \r\n\t")
            reducer.register(field_name+"_min_length", 0, min_reducer)
            reducer.register(field_name+"_max_length", 0, max_reducer)
            reducer.feed(field_name+"_max_length", len(field_data))
            reducer.feed(field_name+"_max_length", len(field_data))
        # check geometry's vertex number
        if first_feature:
            reducer.register("min_vertex_length", len(infer_geom), min_reducer)
        reducer.feed("max_vertex_length", len(infer_geom))
        reducer.feed("min_vertex_length", len(infer_geom))
        
        # check for ring like geometry
        if ring and len(infer_geom) >= 3:
            if (infer_geom[0] != infer_geom[-1]): ring = False

        # feature counts
        reducer.feed("counts", 1)

    result = reducer.getAll()
    result.update({"ring_like": ring})
    print(result)
    return result

def get_xyz_features(path_to_xyz):
    """
        Extract XYZ data in to python list as string (text).
    """
    xyz_features = []
    with open(path_to_xyz) as file:
        line_buffer = []
        for line in file:
            if line == "\n":
                yield line_buffer
                line_buffer = []
            else:
                line_buffer.append(line.strip('\n'))

def main():
    input_xyz = "Pitsit_CRST.xyz"
    output_shp = "Pitsit_CRST.shp"
    
    feature_count = get_xyz_feature_counts(input_xyz)
    print(feature_count)
    
    import arcpy
    arcpy.CreateFeatureclass_management(".", output_shp, "POLYLINE", "#", "DISABLED", "ENABLED", arcpy.SpatialReference(32753))
    
    #for feature in get_xyz_features(input_xyz):
    #    print(feature)
    
    #import arcpy
    
    #with arcpy.da.InserCursor(output_shp) as cursor:
        # baca xyz_feature, buat geometri, buat fitur, save

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
        print(self.acc)
        return self.acc[variable_name]

    def getAll(self):
        return dict(self.acc)

    # sample reducing logic 
def max_reducer(seed, value):
    if (value > seed): seed = value
    return seed
    
def min_reducer(seed, value):
    if (value < seed): seed = value
    return seed

def set_reducer(seed, value):
    seed.add(value)
    return seed

if __name__ == "__main__":
    main()
