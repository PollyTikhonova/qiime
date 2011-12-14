#!/usr/bin/env python
# File created on 15 Feb 2011
from __future__ import division

__author__ = "Greg Caporaso"
__copyright__ = "Copyright 2011, The QIIME Project"
__credits__ = ["Greg Caporaso"]
__license__ = "GPL"
__version__ = "1.4.0-dev"
__maintainer__ = "Greg Caporaso"
__email__ = "gregcaporaso@gmail.com"
__status__ = "Development"
 

from qiime.util import make_option
from qiime.parse import parse_mapping_file, parse_otu_table
from qiime.format import format_otu_table
from qiime.util import parse_command_line_parameters, get_options_lookup
from qiime.sort import sort_otu_table, sort_otu_table_by_mapping_field

options_lookup = get_options_lookup()

script_info = {}
script_info['brief_description'] = "Script for sorting the sample IDs in an OTU table based on a specified value in a mapping file."
script_info['script_description'] = ""
script_info['script_usage'] = [("",
                                "sort samples by the age field in the mapping file",
                                "sort_otu_table.py -i otu_table.txt -o age_sorted_otu_table.txt -m map.txt -s Age"),
                                ("",
                                 "sort samples based on order in a file where each line starts with a sample id",
                                 "sort_otu_table.py -i otu_table.txt -o age_sorted_otu_table.txt -l sorted_sample_id_list.txt")]
script_info['output_description']= ""
script_info['required_options'] = [
    make_option('-i','--input_otu_table',
        help='Input OTU table filepath.',
        type='existing_filepath'),
    make_option('-o','--output_fp',
        help='Output OTU table filepath.',
        type='new_filepath'),
]
script_info['optional_options'] = [
    make_option('-m','--mapping_fp',
        help='Input metadata mapping filepath. [default: %default]',
        type='existing_filepath'),
    make_option('-s','--sort_field',
        help='Category to sort OTU table by. [default: %default]'),
    make_option('-l','--sorted_sample_ids_fp',
        help='Sorted sample id filepath [default: %default]',
        type='existing_filepath')
]
script_info['option_label']={'input_otu_table':'OTU table filepath',
                             'output_fp': 'Output filepath',
                             'mapping_fp':'QIIME-formatted mapping filepath',
                             'sort_field':'Category to sort by',
                             'sorted_sample_ids_fp': 'Sorted sample id filepath'}
script_info['version'] = __version__

def sample_ids_from_f(lines):
    result = []
    for line in lines:
        line = line.strip()
        if line and not line.startswith('#'):
            result.append(line.split()[0])
    return result

def main():
    option_parser, opts, args =\
      parse_command_line_parameters(**script_info)

    otu_table_data = parse_otu_table(open(opts.input_otu_table,'U'))
    sort_field = opts.sort_field
    mapping_fp = opts.mapping_fp
    sorted_sample_ids_fp = opts.sorted_sample_ids_fp
    
    if sort_field and mapping_fp:
        mapping_data = parse_mapping_file(open(mapping_fp,'U'))
        result = sort_otu_table_by_mapping_field(otu_table_data,
                                                 mapping_data,
                                                 sort_field)
    elif sorted_sample_ids_fp:
        sorted_sample_ids = sample_ids_from_f(open(sorted_sample_ids_fp,'U'))
        result = sort_otu_table(otu_table_data,
                                sorted_sample_ids)
    else:
        parser.error("must provide either --sort_field and --mapping_fp OR --sorted_sample_ids_fp")

    # format and write the otu table
    result_str = format_otu_table(result[0],result[1],result[2],result[3])
    of = open(opts.output_fp,'w')
    of.write(result_str)
    of.close()

if __name__ == "__main__":
    main()