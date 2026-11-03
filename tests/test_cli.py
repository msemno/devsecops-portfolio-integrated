from pathlib import Path

from labsec.cli import main

ROOT=Path(__file__).resolve().parents[1]

def test_policy_cli_pass(capsys):
    assert main(['policy','--k8s',str(ROOT/'k8s/base/deployment.yaml'),'--tf-plan',str(ROOT/'fixtures/terraform/secure-plan.json')])==0
    assert '"status": "pass"' in capsys.readouterr().out

def test_policy_cli_fail(capsys):
    assert main(['policy','--k8s',str(ROOT/'k8s/fixtures/bad-deployment.yaml')])==1
    assert '"status": "fail"' in capsys.readouterr().out

def test_manifest_cli(tmp_path):
    f=tmp_path/'x.txt';f.write_text('a')
    assert main(['checksums','--base',str(tmp_path),'--output',str(tmp_path/'manifest.json'),'x.txt'])==0
    assert main(['verify-checksums','--base',str(tmp_path),'--manifest',str(tmp_path/'manifest.json')])==0
    f.write_text('b')
    assert main(['verify-checksums','--base',str(tmp_path),'--manifest',str(tmp_path/'manifest.json')])==1
