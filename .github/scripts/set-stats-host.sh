#!/usr/bin/env bash
# Переключает README на собственный инстанс github-readme-stats.
#
# Подготовка:
#   1. gh repo fork anuraghazra/github-readme-stats --clone=false
#      (нужен токен с правом создавать репозитории)
#   2. Импортировать форк в Vercel: https://vercel.com/new
#   3. В переменных окружения проекта задать PAT с правом "public_repo"
#      под именем PAT_1
#
# Запуск: bash .github/scripts/set-stats-host.sh my-stats.vercel.app
set -euo pipefail

host="${1:?укажите хост, например my-stats.vercel.app}"
sed -i "s|github-stats-extended\.vercel\.app|${host}|g" README.md README.ru.md
echo "готово: карточки статистики теперь берутся с ${host}"
grep -c "${host}" README.md README.ru.md
