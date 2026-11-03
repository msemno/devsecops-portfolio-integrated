"""Transparent lightweight baseline checks, complementary to OPA/Trivy."""
import json
import re
from pathlib import Path

import yaml


def inspect_deployment(doc: dict) -> list[str]:
    if doc.get('kind') != 'Deployment':
        return []
    pod = doc.get('spec', {}).get('template', {}).get('spec', {})
    sc = pod.get('securityContext') or {}
    issues=[]
    if pod.get('hostNetwork',False): issues.append('K8S001 hostNetwork prohibited')
    if pod.get('automountServiceAccountToken') is not False: issues.append('K8S002 disable automountServiceAccountToken')
    if sc.get('runAsNonRoot') is not True: issues.append('K8S003 runAsNonRoot required')
    if (sc.get('seccompProfile') or {}).get('type') != 'RuntimeDefault': issues.append('K8S004 RuntimeDefault seccomp required')
    for c in pod.get('containers', []):
        name=c.get('name','unnamed')
        cs=c.get('securityContext') or {}
        if re.fullmatch(r'.+@sha256:[a-f0-9]{64}', c.get('image','')) is None: issues.append(f'K8S005 {name} immutable image digest required')
        if cs.get('privileged') is True: issues.append(f'K8S010 {name} privileged containers prohibited')
        if cs.get('allowPrivilegeEscalation') is not False: issues.append(f'K8S006 {name} privilege escalation blocked')
        if cs.get('readOnlyRootFilesystem') is not True: issues.append(f'K8S007 {name} read-only filesystem required')
        if 'ALL' not in (cs.get('capabilities') or {}).get('drop',[]): issues.append(f'K8S008 {name} drop ALL capabilities')
        resources=c.get('resources') or {}
        for typ in ('requests','limits'):
            for x in ('cpu','memory'):
                if not (resources.get(typ) or {}).get(x): issues.append(f'K8S009 {name} missing {typ}.{x}')
    return issues

def inspect_terraform_plan(plan: dict) -> list[str]:
    issues=[]
    for change in plan.get('resource_changes', []):
        metadata=change.get('change') or {}
        if 'delete' in metadata.get('actions', []):
            continue
        resource_type=change.get('type')
        after=metadata.get('after') or {}
        if resource_type=='aws_security_group_rule':
            rules=[after] if after.get('type')=='ingress' else []
        elif resource_type=='aws_security_group':
            rules=after.get('ingress') or []
        else:
            continue
        for rule in rules:
            world=('0.0.0.0/0' in (rule.get('cidr_blocks') or []) or
                   '::/0' in (rule.get('ipv6_cidr_blocks') or []))
            if not world:
                continue
            lo,hi=rule.get('from_port'),rule.get('to_port')
            if not isinstance(lo,int) or not isinstance(hi,int):
                issues.append(f"TF002 {change.get('address','unknown')} unresolved public ingress port; review required")
                continue
            ports= [(22,'SSH'),(3389,'RDP')]
            for port, label in ports:
                if str(rule.get('protocol'))=='-1' or (lo<=port<=hi):
                    issues.append(f"TF001 {change.get('address','unknown')} world-accessible {label}")
    return issues

def scan_yaml_file(path: Path) -> list[str]:
    result=[]
    for i,doc in enumerate(yaml.safe_load_all(path.read_text()),start=1):
        if isinstance(doc,dict):
            result += [f'{path}:{i}: {msg}' for msg in inspect_deployment(doc)]
    return result

def scan_json_file(path:Path) -> list[str]:
    return [f'{path}: {x}' for x in inspect_terraform_plan(json.loads(path.read_text()))]
