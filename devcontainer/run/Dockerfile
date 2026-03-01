# We explicitly ask for the Linux x86_64 version of Miniforge
FROM --platform=linux/amd64 condaforge/miniforge3:latest

WORKDIR /workspace

# Copy the environment definition
COPY environment.yaml .

# Update the default environment with our tools
#RUN mamba env update --file environment.yaml --prune && \
#    mamba clean --all -f -y

# Limit threads to reduce memory footprint during emulation
# RUN MAMBA_NUM_THREADS=1 mamba env update --file environment.yaml --prune && \
#     mamba clean --all -f -y
RUN MAMBA_NUM_THREADS=1 mamba env update --file environment.yaml && \
    mamba clean --all -f -y

# Switch to root for system-level configuration
USER root

# 2. Create the entire directory path for SSH and the separation user
# This prevents the "Directory nonexistent" error
RUN mkdir -p /etc/ssh /var/run/sshd /root/.ssh /var/empty && \
    chmod 700 /root/.ssh && \
    chmod 755 /var/empty && \
    groupadd -f sshd && \
    useradd -g sshd -c "Privilege-separated SSH" -s /sbin/nologin -d /var/run/sshd sshd

# 3. Write a fresh sshd_config from scratch
RUN echo "Port 22" > /etc/ssh/sshd_config && \
    echo "PermitRootLogin yes" >> /etc/ssh/sshd_config && \
    echo "PasswordAuthentication yes" >> /etc/ssh/sshd_config && \
    echo "Subsystem sftp internal-sftp" >> /etc/ssh/sshd_config

# Set root password
RUN echo 'root:root' | chpasswd

EXPOSE 22

# 6. Start-up: Generate host keys and run SSH in the foreground
# CMD ["/bin/bash", "-c", "ssh-keygen -A && sshd -D &"]
CMD ["/bin/bash", "-c", "ssh-keygen -A && sshd -f /etc/ssh/sshd_config && exec /bin/bash"]
# CMD ["/bin/bash"]