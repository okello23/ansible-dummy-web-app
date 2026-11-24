
#!/usr/bin/env bash
# ==============================================================================
# Helper script to execute the Ansible deployment
# Accepts standard ansible-playbook arguments
# Handles both sudo and Ansible Vault authentication
# ==============================================================================

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

cd "$PROJECT_ROOT"

# Use virtual environment Ansible if available
if [ -f "$PROJECT_ROOT/.venv/bin/ansible-playbook" ]; then
    ANSIBLE_BIN="$PROJECT_ROOT/.venv/bin/ansible-playbook"
else
    ANSIBLE_BIN="ansible-playbook"
fi

export ANSIBLE_CONFIG="$PROJECT_ROOT/ansible.cfg"

echo "Executing Ansible deployment..."

"$ANSIBLE_BIN" \
    -i "$SCRIPT_DIR/inventory.ini" \
    "$SCRIPT_DIR/playbook.yml" \
    --ask-become-pass \
    --ask-vault-pass \
    "$@"
