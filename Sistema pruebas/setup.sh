#!/bin/bash
# =============================================================================
#  setup.sh — Leaderboard (FastAPI + Vue.js)
#  NOTA: Este script NO es usado por el Vagrantfile actual.
#        El despliegue se realiza mediante Ansible (ansible/playbook.yml).
#        Se mantiene aquí como referencia / alternativa manual.
# =============================================================================

echo ">>> [setup.sh] AVISO: Este script es solo referencia."
echo ">>> El despliegue real se hace con: vagrant up (usa Ansible)"
echo ""
echo ">>> Para provisionar manualmente desde dentro de la VM:"
echo ">>>   ansible-playbook /vagrant/ansible/playbook.yml"