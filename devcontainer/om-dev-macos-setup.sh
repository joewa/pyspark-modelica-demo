#!/bin/bash

echo "🚀 Starting Modelica Dev Environment Setup..."

# 1. Generate SSH Key if it doesn't exist
if [ ! -f ~/.ssh/id_om_container ]; then
    echo "🔑 Generating SSH keys..."
    ssh-keygen -t ed25519 -f ~/.ssh/id_om_container -N ""
else
    echo "SSH key already exists."
fi

# 2. Copy the public key to the current directory for Docker to "see" it
cp ~/.ssh/id_om_container.pub ./id_om_container.pub

# 3. Setup ~/.ssh/config if not already configured
if ! grep -q "Host om-dev" ~/.ssh/config 2>/dev/null; then
    echo "Adding om-dev to ~/.ssh/config..."
    mkdir -p ~/.ssh && chmod 700 ~/.ssh
    cat <<EOF >> ~/.ssh/config

Host om-dev
    HostName omlinuxenv.test
    User root
    IdentityFile ~/.ssh/id_om_container
    StrictHostKeyChecking no
    UserKnownHostsFile /dev/null
EOF
    chmod 600 ~/.ssh/config
else
    echo "Don't setting up ssh. ~/.ssh/config already contains om-dev."
fi

# 4. Setup Container DNS Service
# Check if 'test' zone already exists in container system
if ! container system dns list | grep -q "test"; then
    echo "Creating container DNS zone 'test'..."
    sudo container system dns create test
    container system property set dns.domain test
else
    echo "Container DNS zone 'test' is already configured."
fi

# 5. Build the Container
echo "Building the container (this may take a few minutes)..."
container build --arch amd64 --tag om-linux-env .

echo "🎉 Setup complete!"
echo "You can now run:"
echo "# container run -it --rm --arch amd64 --name omlinuxenv --volume \"\$(pwd):/workspace\" om-linux-env"
echo "# container run -it --rm --arch amd64 --name omlinuxenv \\"
echo "  --cpus 4 \\"
echo "  --memory 4096MB \\"
echo "  --volume \"$(pwd):/workspace\" \""
echo "  om-linux-env"
echo "Then connect via VS Code or 'ssh om-dev' without a password."
echo "Happy Modeling!"
