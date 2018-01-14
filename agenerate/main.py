from template.generator import Generator
import argparse


def entry():
    """
    Generate a valid cloudformation template. Allows printing to console,
    writing to file in either YAML or JSON. Please see --help for specific usage ooptions
    """
    parser = parse_args()
    args = vars(parser.parse_args())

    if args.get('help'):
        return

    """Set defaults"""
    filename = "sample.cfn.template"
    output_type = "json"
    if args["filename"]:
        filename = args["filename"][0]

    if args["output"]:
        output_type = args["output"][0]

    g = Generator()
    template_content = ''
    if output_type == 'json':
        template_content = g.to_json()
    elif output_type == 'yaml':
        template_content = g.to_yaml()

    if args["console"]:
        print(template_content)
    else:
        write_to_file(filename, template_content)


def parse_args():
    """Parse the arguments with argparse"""
    parser = argparse.ArgumentParser(
        prog='agenerate',
        usage='%(prog)s [options]',
        description="Generate a sample cloudformation template"
    )
    parser.add_argument(
        '--filename',
        type=str,
        nargs=1,
        metavar="<FILE_NAME>",
        help="Set the filename of the generated template."
    )
    parser.add_argument(
        '--output',
        type=str,
        nargs=1,
        metavar="<OUTPUT_TYPE>",
        help="Set the output type of the generated template.",
        choices=['json', 'yaml']
    )
    parser.add_argument(
        '--console',
        action='store_true',
        help="Print template to console."
    )
    return parser


def write_to_file(template_name, template_content):
    """ Write template content to file """
    with open(template_name, "a+") as f:
        f.write(template_content)


if __name__ == '__main__':
    entry()
