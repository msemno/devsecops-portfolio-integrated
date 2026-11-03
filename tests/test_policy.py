import json
from pathlib import Path

import yaml

from labsec.policy import inspect_deployment, inspect_terraform_plan, scan_yaml_file

ROOT=Path(__file__).resolve().parents[1]

def test_good_deployment_passes():
    doc=yaml.safe_load((ROOT/'k8s/base/deployment.yaml').read_text())
    assert inspect_deployment(doc)==[]

def test_bad_deployment_fails_multiple_independent_checks():
    doc=yaml.safe_load((ROOT/'k8s/fixtures/bad-deployment.yaml').read_text())
    findings=inspect_deployment(doc)
    assert len(findings)>=7
    assert any('immutable image' in x for x in findings)
    assert any('privilege escalation' in x for x in findings)

def test_non_deployment_does_not_false_positive():
    assert inspect_deployment(yaml.safe_load((ROOT/'k8s/base/service.yaml').read_text()))==[]

def test_secure_terraform_passes():
    assert inspect_terraform_plan(json.loads((ROOT/'fixtures/terraform/secure-plan.json').read_text()))==[]

def test_world_ssh_fails():
    items=inspect_terraform_plan(json.loads((ROOT/'fixtures/terraform/insecure-plan.json').read_text()))
    assert len(items)==1 and 'SSH' in items[0]

def test_world_rdp_fails():
    doc={'resource_changes':[{'type':'aws_security_group_rule','address':'x','change':{'actions':['create'], 'after':{'type':'ingress','cidr_blocks':['0.0.0.0/0'],'from_port':3000,'to_port':4000}}}]}
    assert any('RDP' in x for x in inspect_terraform_plan(doc))

def test_terraform_deletion_is_not_reported():
    doc={'resource_changes':[{'type':'aws_security_group_rule','address':'x','change':{'actions':['delete'],'after':{'type':'ingress','cidr_blocks':['0.0.0.0/0'],'from_port':22,'to_port':22}}}]}
    assert inspect_terraform_plan(doc)==[]

def test_fail_closed_unresolved_port():
    doc={'resource_changes':[{'type':'aws_security_group_rule','address':'x','change':{'actions':['create'],'after':{'type':'ingress','cidr_blocks':['0.0.0.0/0'],'from_port':None,'to_port':None}}}]}
    assert 'review required' in inspect_terraform_plan(doc)[0]

def test_multi_document_scanner(tmp_path):
    p=tmp_path/'mixed.yaml'
    p.write_text((ROOT/'k8s/base/service.yaml').read_text()+'\n---\n'+(ROOT/'k8s/fixtures/bad-deployment.yaml').read_text())
    assert scan_yaml_file(p)

def test_inline_security_group_world_ssh_is_blocked():
    doc={'resource_changes':[{'type':'aws_security_group','address':'aws_security_group.example',
       'change':{'actions':['create'], 'after':{'ingress':[{'from_port':22,'to_port':22,
       'cidr_blocks':['0.0.0.0/0']}]}}}]}
    assert 'SSH' in inspect_terraform_plan(doc)[0]

def test_ipv6_public_rdp_is_blocked():
    doc={'resource_changes':[{'type':'aws_security_group_rule','address':'rule',
      'change':{'actions':['create'],'after':{'type':'ingress', 'protocol':'tcp',
      'from_port':3389,'to_port':3389,'ipv6_cidr_blocks':['::/0']}}}]}
    assert 'RDP' in inspect_terraform_plan(doc)[0]

def test_all_protocol_public_inbound_is_blocked():
    doc={'resource_changes':[{'type':'aws_security_group_rule','address':'rule',
      'change':{'actions':['create'],'after':{'type':'ingress','protocol':'-1',
      'from_port':0,'to_port':0,'cidr_blocks':['0.0.0.0/0']}}}]}
    findings=inspect_terraform_plan(doc)
    assert len(findings)==2
