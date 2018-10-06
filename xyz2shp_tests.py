from unittest import TestCase
import xyz2shp
import nose

class Reducer_Test(TestCase):
    def reducer_test(self):
        reducer = xyz2shp.Reducer()
        reducer.register("max", 0, xyz2shp.max_reducer)
        reducer.register("min", 200000000, xyz2shp.min_reducer)
        for i in [1,2,3,4,5,6,7,101,9,10,11]:
            reducer.feed("max", i)
            reducer.feed("min", i)
        max = reducer.get("max")
        min = reducer.get("min")
        self.assertEquals(max, 101)
        self.assertEquals(min, 1)

    def reducer_register_called_multiple_times(self):
        reducer = xyz2shp.Reducer()
        for i in [1,2,3,4,5,6,7,101,9,10,11]:
            reducer.register("max", 0, xyz2shp.max_reducer)
            reducer.register("min", 200000000, xyz2shp.min_reducer)
            reducer.feed("max", i)
            reducer.feed("min", i)
        max = reducer.get("max")
        min = reducer.get("min")
        self.assertEquals(max, 101)
        self.assertEquals(min, 1)
    
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
        self.assertEquals(statistics["min_vertex"], 1)
        self.assertEquals(statistics["max_vertex"], 3021)
        self.assertEquals(statistics["ring_like"], False)
        
    
    #def get_xyz_features_test(self):
    #    self.assertTrue(False)
    
    #def infer_schema_test(self):
    #    self.assertTrue(False)
    
nose.main()