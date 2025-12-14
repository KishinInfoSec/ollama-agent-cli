# Example Cybersecurity Queries

## Threat Analysis Mode

```bash
ollama-agent query "Analyze the threat profile of APT groups targeting financial institutions" --mode threat_analysis
```

```bash
ollama-agent query "What are the attack vectors for a supply chain compromise?" --mode threat_analysis
```

## Incident Response Mode

```bash
ollama-agent query "We detected a ransomware infection on our file server. What are the immediate steps to contain it?" --mode incident_response
```

```bash
ollama-agent query "Walk me through the incident response procedures for a data breach" --mode incident_response
```

## Vulnerability Assessment Mode

```bash
ollama-agent query "How critical is CVE-2024-1234 and what's the remediation path?" --mode vulnerability
```

```bash
ollama-agent query "Identify common vulnerabilities in microservices architectures" --mode vulnerability
```

## Compliance Mode

```bash
ollama-agent query "What are the key security requirements for HIPAA compliance?" --mode compliance
```

```bash
ollama-agent query "How do I prepare for a SOC 2 Type II audit?" --mode compliance
```

## Secure Coding Mode

```bash
ollama-agent query "Review this code for OWASP vulnerabilities: [paste code]" --mode secure_coding
```

```bash
ollama-agent query "What are the best practices for secure API development?" --mode secure_coding
```

## Network Security Mode

```bash
ollama-agent query "Design a secure network architecture for a cloud-native application" --mode network
```

```bash
ollama-agent query "How should I segment my network for defense in depth?" --mode network
```

## Malware Analysis Mode

```bash
ollama-agent query "What behavioral indicators should I look for when analyzing potential malware?" --mode malware
```

```bash
ollama-agent query "How would you analyze a suspicious executable?" --mode malware
```

## General Cybersecurity (Default Mode)

```bash
ollama-agent query "What's the difference between symmetric and asymmetric encryption?"
```

```bash
ollama-agent query "Explain zero-trust architecture and its benefits"
```

## Interactive Session Example

```bash
# Start interactive mode
ollama-agent interactive --mode threat_analysis --temperature 0.6

# Then type in the chat:
You: What are the latest attack trends?
You: How can we detect these attacks?
You: What tools would you recommend?
You: /mode incident_response
You: How would you respond to such an attack?
```

## Batch Analysis Script

```bash
#!/bin/bash

# Security Assessment Report Generator

echo "=== Comprehensive Security Assessment ==="
echo ""

echo "### 1. Threat Landscape Analysis"
ollama-agent query "What are the top cyber threats facing organizations in 2024?" --mode threat_analysis
echo ""

echo "### 2. Vulnerability Management"
ollama-agent query "What's a systematic approach to vulnerability management?" --mode vulnerability
echo ""

echo "### 3. Incident Response Readiness"
ollama-agent query "How should organizations prepare for security incidents?" --mode incident_response
echo ""

echo "### 4. Compliance Roadmap"
ollama-agent query "What's a prioritized approach to achieving multiple compliance standards?" --mode compliance
echo ""

echo "=== End of Report ==="
```

Save this as `security_audit.sh`, then run:
```bash
chmod +x security_audit.sh
./security_audit.sh
```
