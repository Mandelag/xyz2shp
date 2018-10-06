from unittest import TestCase
import xyz2shp
import nose

class Reducer_Test(TestCase):
    def reducer_test(self):
        reducer = xyz2shp.Reducer()
        reducer.register("min_max", xyz2shp.min_max_reducer_default_seed, xyz2shp.min_max_reducer)
        for i in [1,2,3,4,5,6,7,101,9,10,11]:
            reducer.feed("min_max", i)
        min_max = reducer.get("min_max")
        self.assertEquals(min_max, {"min": 1, "max":101})

    def reducer_register_called_multiple_times(self):
        reducer = xyz2shp.Reducer()
        for i in [1,2,3,4,5,6,7,101,9,10,11]:
            reducer.register("minmax", {"min": 20000000, "max": 0}, reducing_logic=xyz2shp.min_max_reducer)
            reducer.feed("min_max", i)
        minmax = reducer.get("minmax")
        self.assertEquals(minmax, {"min": 1, "max": 101})
    
    def simple_count(self):
        reducer = xyz2shp.Reducer()
        reducer.register("counts", 0, lambda x, y:  x+1)
        test_list = [1,2,3,4,5,6,7,101,9,10,11] 
        for i in test_list:
            reducer.feed("counts", i)
        self.assertEquals(len(i), len(test_list))

class Xyz2Shp_Test(TestCase):
    def get_xyz_feature_statistics_test(self):
        statistics = xyz2shp.get_xyz_feature_statistics("./test_data/Pitsit_CRST.xyz")
        self.assertEquals(statistics["counts"], 3889)
        self.assertEquals(statistics["vertex_length"], {"min": 1, "max": 3021})
        self.assertEquals(statistics["ring_like"], False)
        
    
    #def get_xyz_features_test(self):
    #    self.assertTrue(False)
    
    #def infer_schema_test(self):
    #    self.assertTrue(False)
    
nose.main()