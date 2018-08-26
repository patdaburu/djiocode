from pathlib import Path
from djiocode.osgeo.ogr import opends, apply
import multiprocessing as mp
from osgeo.ogr import Feature

path = Path('/home/pblair/Data/gcgc/tl_2017_27145_roads/tl_2017_27145_roads.shp')


# def iterate_all_features(ds_path: str):
#     print('STARTING')
#     layer_names = []
#     # driver = OgrDrivers.guess(Path(ds_path))
#     # ds = driver.Open(str(ds_path), 0)
#     ds = opends(ds_path)
#     for layer in ds:
#         print(layer.GetName())
#         layer_names.append(layer.GetName())
#         for _ in layer:
#             continue
#     return layer_names
#
#
# pool = mp.Pool(processes=mp.cpu_count())
# results = [pool.apply_async(iterate_all_features, args=(str(path),)) for x in range(1,7)]
# outputs = [p.get() for p in results]
#
# for output in outputs:
#     print(output)
#
#
# #https://gist.github.com/filipkral/00d38ba761f72289b0df
#
#
# import usaddress
# addr='123 Main St. Suite 100 Chicago, IL'
#
# # The parse method will split your address string into components, and label each component.
# # expected output: [(u'123', 'AddressNumber'), (u'Main', 'StreetName'), (u'St.', 'StreetNamePostType'), (u'Suite', 'OccupancyType'), (u'100', 'OccupancyIdentifier'), (u'Chicago,', 'PlaceName'), (u'IL', 'StateName')]
# print(usaddress.parse(addr))
#
# # The tag method will try to be a little smarter
# # it will merge consecutive components, strip commas, & return an address type
# # expected output: (OrderedDict([('AddressNumber', u'123'), ('StreetName', u'Main'), ('StreetNamePostType', u'St.'), ('OccupancyType', u'Suite'), ('OccupancyIdentifier', u'100'), ('PlaceName', u'Chicago'), ('StateName', u'IL')]), 'Street Address')
# print(usaddress.tag(addr))
#
#
#
# print(usaddress.tag('Robie House, 5757 South Woodlawn Avenue, Chicago, IL 60637'))
# # (OrderedDict([
# #    ('BuildingName', 'Robie House'),
# #    ('AddressNumber', '5757'),
# #    ('StreetNamePreDirectional', 'South'),
# #    ('StreetName', 'Woodlawn'),
# #    ('StreetNamePostType', 'Avenue'),
# #    ('PlaceName', 'Chicago'),
# #    ('StateName', 'IL'),
# #    ('ZipCode', '60637')]),
# # 'Street Address')
# print(usaddress.tag('State & Lake, Chicago'))
# # (OrderedDict([
# #    ('StreetName', 'State'),
# #    ('IntersectionSeparator', '&'),
# #    ('SecondStreetName', 'Lake'),
# #    ('PlaceName', 'Chicago')]),
# # 'Intersection')
# print(usaddress.tag('P.O. Box 123, Chicago, IL'))
# # (OrderedDict([
# #    ('USPSBoxType', 'P.O. Box'),
# #    ('USPSBoxID', '123'),
# #    ('PlaceName', 'Chicago'),
# #    ('StateName', 'IL')]),
# # 'PO Box')
#
# print(usaddress.tag('First Street & East Main Avenue Southwest'))


def getfiddo(feature: Feature) -> int:
    return feature.GetFID()


for i in range(1, 100):
    results = set(apply(path=path, func=getfiddo))
    for result in results:
        print(result)

    ds = opends(path)
    for layer in ds:
        print(f'{layer.GetName()}: {layer.GetFeatureCount()}')

    print(f'How many results? {len(results)}')