FROM grafana/grafana:6.7.3
# Temporarily switch to root to run OS-level package managers
USER root
# Upgrade apk-tools to patch CVE-2021-36159
# We explicitly point to a newer Alpine repository because 6.7.3 uses an EOL Alpine base
RUN apk add --upgrade --no-cache apk-tools --repository=http://dl-cdn.alpinelinux.org/alpine/v3.14/main
# Drop privileges back to the standard Grafana user for security
USER grafana

FROM grafana/grafana:9.4.13
# Temporarily switch to root to run OS-level package managers
USER root
# Upgrade apk-tools and system packages to ensure OS-level CVEs remain patched
RUN apk upgrade --no-cache apk-tools
# Drop privileges back to the standard Grafana user for security
USER grafana

# Bump the image to pull the recompiled Go binaries
FROM grafana/grafana:latest
# Temporarily switch to root for OS-level patching
USER root
# Upgrade system packages to catch any lingering OS vulnerabilities
RUN apk upgrade --no-cache
# Drop privileges back to the standard Grafana user
USER grafana
