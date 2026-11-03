"""Offline educational security checks; never claim live cloud or K8s validation."""
import argparse
import json
from pathlib import Path

from labsec.policy import scan_json_file, scan_yaml_file
from labsec.supply_chain import validate_sbom, verify_manifest, write_manifest


def main(argv=None):
    p=argparse.ArgumentParser(prog='labsec')
    sub=p.add_subparsers(dest='command',required=True)
    policy=sub.add_parser('policy', help='offline configuration policy checks')
    policy.add_argument('--k8s',nargs='*',default=[])
    policy.add_argument('--tf-plan',nargs='*',default=[])
    verify=sub.add_parser('verify-checksums')
    verify.add_argument('--base',required=True);verify.add_argument('--manifest',required=True)
    sums=sub.add_parser('checksums')
    sums.add_argument('--base',required=True);sums.add_argument('--output',required=True);sums.add_argument('files',nargs='+')
    sbom=sub.add_parser('validate-sbom');sbom.add_argument('file')
    args=p.parse_args(argv)
    if args.command=='policy':
        findings=[]
        for name in args.k8s: findings.extend(scan_yaml_file(Path(name)))
        for name in args.tf_plan: findings.extend(scan_json_file(Path(name)))
        print(json.dumps({'status':'fail' if findings else 'pass','findings':findings},indent=2))
        return 1 if findings else 0
    if args.command=='checksums':
        base=Path(args.base);files=[base / x for x in args.files]
        manifest=write_manifest(base,files,Path(args.output))
        print(json.dumps(manifest,indent=2));return 0
    if args.command=='verify-checksums':
        errors=verify_manifest(Path(args.base),Path(args.manifest))
        print(json.dumps({'status':'fail' if errors else 'pass','issues':errors},indent=2))
        return 1 if errors else 0
    if args.command=='validate-sbom':
        errors=validate_sbom(json.loads(Path(args.file).read_text()))
        print(json.dumps({'status':'fail' if errors else 'pass','issues':errors},indent=2))
        return 1 if errors else 0

if __name__=='__main__': raise SystemExit(main())
