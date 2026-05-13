# Tor Proxy with Controlled IP Rotation on Ubuntu 24.04

## Scope

This guide configures a Tor SOCKS proxy and uses the Tor ControlPort to request new circuits.

> [!WARNING]
> Use Tor only for lawful privacy, testing, and research purposes.
> Do not use this setup to bypass access controls, evade bans, scrape services against their terms, or hide abusive activity.

## Security Baseline

The safe default is:

```text
SocksPort 127.0.0.1:9050
ControlPort 127.0.0.1:9051
CookieAuthentication 1
```

Do not expose the ControlPort to the LAN or internet unless you have a strict firewall policy and strong authentication.

## Prerequisites

```bash
sudo apt update
sudo apt install -y tor python3 python3-pip
```

Validate:

```bash
tor --version
```

## 1. Configure Tor Locally

Edit:

```bash
sudo nano /etc/tor/torrc
```

Minimal safe configuration:

```text
SocksPort 127.0.0.1:9050
ControlPort 127.0.0.1:9051
CookieAuthentication 1
```

Restart:

```bash
sudo systemctl restart tor
sudo systemctl status tor --no-pager
```

Validate listening ports:

```bash
ss -tuln | grep -E '9050|9051'
```

## 2. Optional LAN Access

Only if the proxy is intentionally used by trusted internal clients:

```text
SocksPort 192.168.1.121:9050
ControlPort 192.168.1.121:9051
CookieAuthentication 0
HashedControlPassword 16:...
```

Generate the password hash:

```bash
tor --hash-password "CHANGE_THIS_STRONG_PASSWORD"
```

Firewall example:

```bash
sudo ufw allow from 192.168.1.0/24 to any port 9050 proto tcp
sudo ufw allow from 192.168.1.0/24 to any port 9051 proto tcp
sudo ufw status
```

> [!WARNING]
> Never expose `ControlPort 0.0.0.0:9051` without a firewall and authentication.
> The ControlPort can control Tor behavior and must be treated as administrative access.

## 3. Install Python Dependencies

```bash
python3 -m pip install --user "requests[socks]" stem
```

## 4. Rotation Test Script

Use:

```text
scripts/tor/rotate_ip.py
```

Example with local Tor and cookie authentication:

```bash
python3 scripts/tor/rotate_ip.py \
  --server 127.0.0.1 \
  --socks-port 9050 \
  --control-port 9051 \
  --requests 5 \
  --wait-seconds 15
```

Example with password authentication:

```bash
export TOR_CONTROL_PASSWORD='CHANGE_THIS_STRONG_PASSWORD'

python3 scripts/tor/rotate_ip.py \
  --server 192.168.1.121 \
  --socks-port 9050 \
  --control-port 9051 \
  --password-env TOR_CONTROL_PASSWORD \
  --requests 5 \
  --wait-seconds 15
```

## 5. Manual ControlPort Test

```bash
telnet 127.0.0.1 9051
```

Password mode:

```text
AUTHENTICATE "CHANGE_THIS_STRONG_PASSWORD"
SIGNAL NEWNYM
QUIT
```

Expected responses:

```text
250 OK
250 OK
250 closing connection
```

## Troubleshooting

### ControlPort Connection Refused

```bash
sudo ss -tuln | grep 9051
sudo journalctl -u tor -n 200 --no-pager
```

### Authentication Failed

Check:

- `CookieAuthentication`
- `HashedControlPassword`
- Password environment variable
- ControlPort host and port

### IP Does Not Change Every Time

Tor may rate-limit circuit changes. Increase wait time:

```bash
--wait-seconds 20
```

## Rollback

```bash
sudo systemctl stop tor
sudo apt purge -y tor
sudo apt autoremove -y
```
