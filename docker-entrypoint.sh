#!/bin/sh
set -eu

python manage.py migrate --noinput
python manage.py collectstatic --noinput --clear

if [ -n "${ADMIN_PASSWORD:-}" ]; then
    if [ "${INIT_ADMIN_FORCE:-}" = "true" ]; then
        python manage.py init_admin \
            --username "${ADMIN_USERNAME:-admin}" \
            --nickname "${ADMIN_NICKNAME:-站长}" \
            --password "${ADMIN_PASSWORD}" \
            --force
    else
        python manage.py init_admin \
            --username "${ADMIN_USERNAME:-admin}" \
            --nickname "${ADMIN_NICKNAME:-站长}" \
            --password "${ADMIN_PASSWORD}"
    fi
fi

exec "$@"
