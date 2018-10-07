from unittest import TestCase
import xyz2shp
import nose

class Reducer_Test(TestCase):
    def reducer_Test(self):
        reducer = xyz2shp.Reducer()
        reducer.register("min_max", xyz2shp.min_max_reducer_default_seed(), xyz2shp.min_max_reducer)
        for i in [1,2,3,4,5,6,7,101,9,10,11]:
            reducer.feed("min_max", i)
        min_max = reducer.get("min_max")
        self.assertEquals(min_max, {"min": 1, "max":101})

    def reducer_register_called_multiple_times_Test(self):
        reducer = xyz2shp.Reducer()
        for i in [1,2,3,4,5,6,7,101,9,10,11]:
            reducer.register("min_max",xyz2shp.min_max_reducer_default_seed(), reducing_logic=xyz2shp.min_max_reducer)
            reducer.feed("min_max", i)
        minmax = reducer.get("min_max")
        self.assertEquals(minmax, {"min": 1, "max": 101})
    
    def simple_count_Test(self):
        reducer = xyz2shp.Reducer()
        reducer.register("counts", 0, lambda x, y:  x+1)
        test_list = [1,2,3,4,5,6,7,101,9,10,11] 
        for i in test_list:
            reducer.feed("counts", i)
        self.assertEquals(reducer.get("counts"), len(test_list))

    def feature_parser_Test(self):
        feature = ["name=Jakarta", "pop=12000000", "country=Indonesia", " 106.5,-6.8", "106.4,-6.86"]
        parsed_feature = xyz2shp.feature_parser(feature)
        self.assertEquals(parsed_feature, {
            "attributes": {
                "name": "Jakarta",
                "pop": "12000000",
                "country": "Indonesia"
            },
            "geometry": [
                [106.5, -6.8],
                [106.4, -6.86]
            ]
        })

class With_Sample_Data_Test(TestCase):
    def sample_data_one_test(self):
        input_xyz = "test_data\\Pitsit_CRST.xyz"
        output_shp = "test_data\\Pitsit_CRST.shp"
        
        feature_statistics = xyz2shp.get_xyz_feature_statistics(input_xyz)
        self.assertEquals(feature_statistics, {
            'vertex_length': {'min': 1, 'max': 3021},
            'counts': 3889,
            'field_set': {'DESCRIPTION', 'DATE', 'ELEVATION', 'LINE', 'LAYER'},
            'DESCRIPTION_length': {'min': 6, 'max': 6},
            'LINE_length': {'min': 1, 'max': 4},
            'LAYER_length': {'min': 4, 'max': 4},
            'ELEVATION_length': {'min': 1, 'max': 4},
            'DATE_length': {'min': 3, 'max': 14},
            'ring_like': False})

    #def get_xyz_features_test(self):
    #    self.assertTrue(False)
    
    #def infer_schema_test(self):
    #    self.assertTrue(False)
    
nose.main()