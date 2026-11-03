"""Offline integrity checks: checksums are NOT signatures or attestations."""
import hashlib
import json
from pathlib import Path


def sha256_file(path:Path) -> str:
    h=hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda:f.read(1024*1024),b''): h.update(chunk)
    return h.hexdigest()

def write_manifest(base:Path, files:list[Path], output:Path) -> dict:
    base=base.resolve(); output=output.resolve()
    artifacts={}
    for file in files:
        path=file.resolve()
        if not path.is_relative_to(base): raise ValueError('Artifact outside approved base directory')
        if path==output: raise ValueError('Manifest cannot hash itself')
        if not path.is_file(): raise FileNotFoundError(path)
        artifacts[path.relative_to(base).as_posix()]=sha256_file(path)
    data={'schema':'portfolio-sha256-v1','artifacts':dict(sorted(artifacts.items()))}
    output.parent.mkdir(parents=True,exist_ok=True)
    output.write_text(json.dumps(data,indent=2)+'\n')
    return data

def verify_manifest(base:Path, manifest_path:Path)->list[str]:
    base=base.resolve()
    data=json.loads(manifest_path.read_text())
    if data.get('schema')!='portfolio-sha256-v1': return ['Unknown manifest schema']
    if not isinstance(data.get('artifacts'),dict) or not data['artifacts']: return ['Empty manifest']
    errors=[]
    for name,digest in data['artifacts'].items():
        path=(base/name).resolve()
        if not path.is_relative_to(base): errors.append(f'Unsafe path: {name}');continue
        if not path.is_file(): errors.append(f'Missing file: {name}');continue
        if sha256_file(path)!=digest: errors.append(f'Checksum mismatch: {name}')
    return errors

def validate_sbom(data:dict)->list[str]:
    if data.get('bomFormat')=='CycloneDX':
        missing=[k for k in ('specVersion','components') if k not in data]
        if not isinstance(data.get('components'),list): missing.append('valid components list')
        return [f'Missing CycloneDX field: {x}' for x in missing]
    if data.get('spdxVersion','').startswith('SPDX-'):
        missing=[k for k in ('SPDXID','creationInfo','packages') if k not in data]
        return [f'Missing SPDX field: {x}' for x in missing]
    return ['Unrecognized SBOM format']
