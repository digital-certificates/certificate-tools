#!/usr/bin/env python
'''
Generates the issuer file (.json) thar represents the issues which is needed for issuing and validating certificates.

Currently, just not check for inputs' validity (e.g. valid address, URLs, etc.)
'''
import os
import sys
import configargparse
import json
import datetime

import helpers

ISSUER_TYPE = 'Profile'

OPEN_BADGES_V2_CONTEXT_JSON = 'https://openbadgespec.org/v2/context.json'
BLOCKCERTS_V2_CONTEXT_JSON = 'https://www.blockcerts.org/blockcerts_v2_alpha/context_bc.json'


def generate_issuer_file(config):
    output_handle = open(config.output_file, 'w') if config.output_file else sys.stdout

    context = [BLOCKCERTS_V2_CONTEXT_JSON, OPEN_BADGES_V2_CONTEXT_JSON]

    issuer_json = {
        '@context': context,
        'id': config.issuer_id,
        'url': config.issuer_url,
        'name': config.issuer_name,
        'email': config.issuer_email,
        'image': helpers.encode_image(config.issuer_logo_file),
        'publicKeys': [{'publicKey': config.public_key}],
        'revocationList': config.revocation_list_uri,
        'type': ISSUER_TYPE
    }

    if config.intro_url:
        issuer_json['introductionUrl'] = config.intro_url

    output_handle.write(json.dumps(issuer_json, indent=2))

    if output_handle is not sys.stdout:
        output_handle.close()


def get_config():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
    p = configargparse.getArgumentParser(default_config_files=[os.path.join(base_dir, 'conf.ini')]) 
    p.add('-c', '--my-config', required=True, is_config_file=True, help='config file path')
    p.add_argument('-k', '--public_key', type=str, required=True, help='The key(s) an issuer uses to sign Assertions. See https://openbadgespec.org/#Profile for more details')
    p.add_argument('-r', '--revocation_list_uri', type=str, required=True, help='URI of the Revocation List used for marking revocation. See https://openbadgespec.org/#Profile for more details')
    p.add_argument('-d', '--issuer_id', type=str, required=True, help='the issuer\'s publicly accessible identification file; i.e. URL of the file generated by this tool')
    p.add_argument('-u', '--issuer_url', type=str, help='the issuer\'s main URL address')
    p.add_argument('-n', '--issuer_name', type=str, help='the issuer\'s name')
    p.add_argument('-e', '--issuer_email', type=str, help='the issuer\'s email')
    p.add_argument('-m', '--issuer_logo_file', type=str, help='the issuer\' logo image')
    p.add_argument('-i', '--intro_url', required=False, type=str, help='the issuer\'s introduction URL address')
    p.add_argument('-o', '--output_file', type=str, help='the output file to save the issuer\'s identification file')
    args, _ = p.parse_known_args()

    return args


def main():
    conf = get_config()
    generate_issuer_file(conf)


if __name__ == "__main__":
    main()

