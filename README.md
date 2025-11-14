# pysmbserver

A simple, lightweight, and customizable SMB (Server Message Block) server implementation in Python. Perfect for sharing files across networks, testing SMB client applications, or building custom file-sharing solutions.

This implementation is based on Impacket 0.13.0, but has been refactored to remove all offensive or attack-oriented capabilities originally provided by the library. The goal is to provide a clean SMB server suitable for legitimate development and testing purposes.

All file headers have been removed, and several minor adjustments were made in smbserver.py, including improvements to logging information and updates to the addCredential method to simplify password handling.

## Features

- **Easy-to-use CLI** - Quick setup with command-line interface
- **Programmatic API** - Full control through Python classes
- **Authentication Support** - Optional username/password and NTLM hash authentication
- **IPv6 Support** - Listen on both IPv4 and IPv6
- **SMB2 Support** - Experimental SMB2 protocol support
- **Custom Shares** - Add multiple shares with custom comments and permissions
- **Flexible Logging** - Output logging to file or console
- **No Root Required** - Bind to custom ports without elevated privileges

## Requirements

- Python 3.7+

## Installation

Install from PyPI:

```bash
pip install pysmbserver
```

Or install from source:

```bash
pipx install git+https://github.com/yourusername/pysmbserver.git
```

## Quick Start

### Using the CLI

The simplest way to get started is using the command-line interface:

```bash
# Basic usage - share /tmp directory as 'TMP'
sudo pysmbserver TMP /tmp

# With a custom comment (no root required for ports > 1024)
pysmbserver SHARED /home/user/shared -comment "My Shared Folder"

# With authentication
pysmbserver -username admin -password mypassword TMP /tmp

# With NTLM hash authentication
pysmbserver -username admin -hashes "AAD3B435B51404EEAAD3B435B51404EE:8846F7EAEE8FB117AD06BDD830B7586C" TMP /tmp

# With custom port and IPv6
pysmbserver -port 1445 -6 SHARED /home/user/shared

# With SMB2 support and debug output
pysmbserver -smb2support -debug -timestamp TMP /tmp

# Output to log file
pysmbserver -outputfile server.log TMP /tmp
```

### Using the API

For advanced use cases, import and use the `SimpleSMBServer` class directly:

```python
from pysmbserver.smbserver import SimpleSMBServer
from pysmbserver import logger

# Enable Debug
logger.init(ts=True, debug=True)

# Create a basic SMB server
server = SimpleSMBServer(listenAddress='0.0.0.0', listenPort=445)

# Add a share
server.addShare('TMP', '/tmp', 'Temporary files')

# Add another share (read-only)
server.addShare('BACKUP', '/home/user/backup', 'Read-only backup', readOnly='yes')

# Add authentication
server.addCredential('admin', password='mypassword')
server.addCredential('user', password='userpass')

# Configure SMB2 support
server.setSMB2Support(True)

# Set log file
server.setLogFile('server.log')

# Start the server
server.start()
```

#### Advanced Examples

**Listen on IPv6:**

```python
server = SimpleSMBServer(
    listenAddress='::',
    listenPort=445,
    ipv6=True
)
server.addShare('DATA', '/var/data')
server.start()
```

**Use NTLM hashes for authentication:**

```python
server = SimpleSMBServer()
server.addShare('SECURE', '/secure/data')

# Add credential with NTLM hash
server.addCredential(
    'admin',
    hashes='AAD3B435B51404EEAAD3B435B51404EE:8846F7EAEE8FB117AD06BDD830B7586C'
)

server.start()
```

**Custom authentication callback:**

```python
def custom_auth(username, password):
    # Implement custom authentication logic
    return username in ['admin', 'user']

server = SimpleSMBServer()
server.setAuthCallback(custom_auth)
server.addShare('PUBLIC', '/public')
server.start()
```

**Multiple shares with different permissions:**

```python
server = SimpleSMBServer(listenPort=1445)

# Writable share
server.addShare('UPLOAD', '/home/user/uploads', 'Upload folder', readOnly='no')

# Read-only share
server.addShare('DATA', '/home/user/data', 'Read-only data', readOnly='yes')

# Share with IPC
server.addShare('IPC$', '', 'Inter-process communication', shareType='3')

server.addCredential('uploader', password='uploadpass')
server.addCredential('reader', password='readpass')

server.start()
```

**Handle multiple named pipes:**

```python
server = SimpleSMBServer()
server.addShare('FILES', '/data')

# Register custom named pipes
server.registerNamedPipe('custom_pipe', ('127.0.0.1', 5000))

# List all registered pipes
pipes = server.getRegisteredNamedPipes()
print(f"Registered pipes: {pipes}")

server.start()
```

## Configuration

### SimpleSMBServer Class

#### Constructor

```python
SimpleSMBServer(
    listenAddress='0.0.0.0',
    listenPort=445,
    configFile='',
    ipv6=False
)
```

**Parameters:**
- `listenAddress` (str): Address to listen on (default: '0.0.0.0')
- `listenPort` (int): Port to listen on (default: 445)
- `configFile` (str): Optional configuration file path
- `ipv6` (bool): Enable IPv6 mode (default: False)

#### Methods

**Share Management:**
- `addShare(shareName, sharePath, shareComment='', shareType='0', readOnly='no')` - Add a share
- `removeShare(shareName)` - Remove a share

**Authentication & Credentials:**
- `addCredential(name, uid=0, password=None, hashes=None, prompt_if_missing=True)` - Add user credentials
- `setCredentialsFile(credFile)` - Set credentials file path
- `setAuthCallback(callback)` - Set custom authentication callback
- `getAuthCallback()` - Get the current authentication callback

**Security & Protocol Configuration:**
- `setSMB2Support(value)` - Enable/disable SMB2 support
- `setDropSSP(value)` - Enable/disable SSP/ESS negotiation
- `setSMBChallenge(challenge='')` - Set custom SMB challenge string

**Logging :**
- `setLogFile(logFile)` - Set log file path

**Named Pipes:**
- `registerNamedPipe(pipeName, address)` - Register a named pipe
- `unregisterNamedPipe(pipeName)` - Unregister a named pipe
- `getRegisteredNamedPipes()` - Get list of registered pipes

**Server Management:**
- `getServer()` - Get the underlying SMBSERVER instance for advanced operations
- `start()` - Start the server (blocking call)
- `stop()` - Stop the server

### Network Testing

Test network connectivity and SMB protocol compatibility:

```bash
pysmbserver -smb2support -debug -port 1445 -u user -password secret TMP /tmp
```

Then connect from another machine:
```bash
smbclient \\\\server_ip\\TMP -U user secret -p 1445 
```