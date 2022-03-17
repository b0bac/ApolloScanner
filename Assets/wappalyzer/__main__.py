import argparse
import json
from .Wappalyzer import analyze

def get_parser() -> argparse.ArgumentParser:
    """Get the CLI `argparse.ArgumentParser`"""
    parser = argparse.ArgumentParser(description="python-Wappalyzer CLI", prog="python -m Wappalyzer")
    parser.add_argument('url', help='URL to analyze')
    parser.add_argument('--update', action='store_true', help='Use the latest technologies file downloaded from the internet')
    parser.add_argument('--user-agent', help='Request user agent', dest='useragent')
    parser.add_argument('--timeout', help='Request timeout', type=int, default=10)
    parser.add_argument('--no-verify', action='store_true', help='Skip SSL cert verify', dest='noverify')
    return parser

def main(args) -> None:
    """Entrypoint
    :param args: `Namespace` returned by `argparse.ArgumentParser.parse_args`. 
    """
    result = analyze(args.url, update=args.update, useragent=args.useragent, timeout=args.timeout, verify=not args.noverify)
    print(json.dumps(result))

if __name__ == '__main__':
    main(get_parser().parse_args())
