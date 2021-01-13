import mooda as md
import pprint

emso = md.util.EMSO(user='bardaji', password='1234test')

# plot_list = emso.get_info_fig()
# for plot_type in plot_list:
#     print(plot_type)
#     arguments = emso.get_info_fig_plot(plot_type)
#     for argument in arguments:
#         argument_info = emso.get_info_fig_plot_argument(plot_type, argument)
#         print('  -', argument, '->', argument_info[0])
#         for option in argument_info[1]:
#             print('    -', option)

# metadata_ids = emso.get_info_metadata_id()
# print(*metadata_ids, sep='\n')

# parameters = emso.get_info_parameter()
# print(*parameters, sep='\n')

# platform_codes = emso.get_info_platform_code()
# print(*platform_codes, sep='\n')

# sites = emso.get_info_site()
# print(*sites, sep='\n')

# metadatas = emso.get_metadata()
# for metadata in metadatas:      
#     pprint.pprint(metadata)

data_list = emso.get_data()
for data in data_list:      
    pprint.pprint(data)
