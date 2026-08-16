#!/usr/bin/env bash
# Проставляет темы (topics) репозиториям профиля.
#
# Требует токен gh с правом "Administration: Read and write"
# (для fine-grained PAT) или классический токен со scope "repo":
#   gh auth refresh -h github.com -s repo
#
# Запуск: bash .github/scripts/set-topics.sh
set -euo pipefail

topics() {
    local repo="$1"
    shift
    local args=()
    for topic in "$@"; do
        args+=(--add-topic "$topic")
    done
    if gh repo edit "Fgeeha/$repo" "${args[@]}" >/dev/null; then
        echo "ok   $repo"
    else
        echo "fail $repo"
    fi
}

topics ROoP rag ollama llm self-hosted django chromadb docker python
topics Green-Sentry fastapi computer-vision resnet50 plant-disease react postgresql celery redis
topics plant_disease_resnet50 pytorch resnet50 deep-learning cuda image-classification tensorboard docker
topics stress-tester golang fyne stress-testing cpu ram cross-platform desktop-app
topics rocm-smi-exporter prometheus prometheus-exporter rocm amd-gpu grafana monitoring python
topics max-ollama max-messenger maxapi ollama llm chatbot self-hosted streaming python
topics template-max-bot-github-gitea max-messenger maxapi bot-template gitea-actions github-actions docker uv python
topics ID-Helper-Bot-max max-messenger maxapi chatbot docker uv python
topics base-max-bot max-messenger maxapi faq-bot postgresql sqlalchemy alembic python
topics max-action github-actions max-messenger notifications golang ci-cd
topics Tg-ollama telegram-bot ollama llm aiogram self-hosted python
topics arxiv2word arxiv pandoc docx python docker
topics ga_detector browser-extension chrome-extension firefox-addon google-analytics javascript
topics Fast-Chat-Auth fastapi jwt authentication chat python
topics PHPNewsHub php postgresql cms news
topics app-panel flask dashboard homelab python
topics vuln-scanner security trivy vulnerability-scanner bash
topics scan-image-trivy trivy docker security ci-cd
