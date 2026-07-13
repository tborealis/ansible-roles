ARG RELEASE=bookworm
FROM debian:${RELEASE}

ARG RELEASE
LABEL org.opencontainers.image.source=https://github.com/tborealis/ansible-roles
LABEL org.opencontainers.image.description="Molecule test image (Debian ${RELEASE} + systemd)"

ENV container=docker \
    DEBIAN_FRONTEND=noninteractive

# Baseline a real Debian server would have. Deliberately excludes packages the
# roles install themselves (e.g. python3-debian) so converge keeps testing them.
# Apt lists are kept: roles assume a populated cache (base updates it on real
# hosts) and tasks guarded by cache_valid_time skip the refresh otherwise.
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        systemd systemd-sysv dbus sudo \
        python3 python3-apt \
        ca-certificates iproute2 procps curl \
    && apt-get clean \
    && rm -rf /tmp/* /var/tmp/*

# Trim units that hang, spam, or serve no purpose in a container.
RUN find /etc/systemd/system /lib/systemd/system \
        \( -path '*.wants/*getty*' \
        -o -path '*.wants/*apt-daily*' \
        -o -path '*.wants/*systemd-udev*' \
        -o -path '*.wants/*systemd-timesyncd*' \) -delete \
    && systemctl mask getty.target console-getty.service \
        systemd-udevd.service systemd-udevd-kernel.socket systemd-udevd-control.socket

STOPSIGNAL SIGRTMIN+3
CMD ["/lib/systemd/systemd"]
