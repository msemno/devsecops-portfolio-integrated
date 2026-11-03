import json

import pytest

from labsec.supply_chain import validate_sbom, verify_manifest, write_manifest


def test_write_verify_checksums(tmp_path):
    x=tmp_path/'artifact.bin';x.write_bytes(b'approved bytes')
    write_manifest(tmp_path,[x],tmp_path/'checksums.json')
    assert verify_manifest(tmp_path,tmp_path/'checksums.json')==[]

def test_modification_detected(tmp_path):
    x=tmp_path/'artifact.bin';x.write_bytes(b'original')
    write_manifest(tmp_path,[x],tmp_path/'checksums.json');x.write_bytes(b'changed')
    assert 'Checksum mismatch' in verify_manifest(tmp_path,tmp_path/'checksums.json')[0]

def test_manifest_path_traversal_denied(tmp_path):
    x=tmp_path/'outside.txt';x.write_text('x')
    path=tmp_path/'checksums.json';path.write_text(json.dumps({'schema':'portfolio-sha256-v1','artifacts':{'../outside.txt':'f'*64}}))
    assert 'Unsafe path' in verify_manifest(tmp_path,path)[0]

def test_refuse_out_of_scope_writes(tmp_path):
    outside=tmp_path.parent/'outside-artifact.txt';outside.write_text('x')
    with pytest.raises(ValueError): write_manifest(tmp_path,[outside],tmp_path/'hash.json')
    outside.unlink()

def test_refuse_self_hash(tmp_path):
    m=tmp_path/'manifest.json';m.write_text('x')
    with pytest.raises(ValueError): write_manifest(tmp_path,[m],m)

def test_spdx_format_good():
    assert validate_sbom({'spdxVersion':'SPDX-2.3','SPDXID':'SPDXRef-DOCUMENT','creationInfo':{},'packages':[]})==[]

def test_cyclonedx_format_good():
    assert validate_sbom({'bomFormat':'CycloneDX','specVersion':'1.6','components':[]})==[]

def test_missing_sbom_fields_rejected():
    assert validate_sbom({'bomFormat':'CycloneDX'})
    assert validate_sbom({'untrusted':True})
