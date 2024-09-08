## LurkerX Installation Guide

This guide provides step-by-step instructions on installing LurkerX on both Termux and Linux systems.

### Termux Users

**1. Update and Install Dependencies:**

```bash
termux-setup-storage && cd $HOME && apt update && apt upgrade && apt install openjdk-17 && pkg install git apktool python3 python3-pip -y
```

This command updates your system, installs the necessary Java Development Kit (JDK), Git, Apktool, Python 3, and Pip.

**2. Clone the Repository:**

```bash
git clone https://github.com/nemesis-guy/LurkerX.git && git clone https://github.com/Lexiie/Termux-Apktool && cd Termux-Apktool && dpkg -i apktool_2.3.4_all.deb && cd $HOME && cd LurkerX
```

This command clones the LurkerX repository from GitHub into your home directory and navigates to the newly created `LurkerX` directory.

**3. Install LurkerX:**

```bash
ls && bash install.sh
```

This command lists the contents of the `LurkerX` directory and executes the `install.sh` script, which installs the required Python dependencies and configures the application.

**4. Refresh or restart termux**
```bash
source ~/.bashrc
```

This command will refresh the command list in termux to ensure that LurkerX is functioning. If there is failure, retart Termux.

**5. Start LurkerX:**

```bash
lurkerx
```

This command starts the LurkerX application.

### Linux Users

**1. Update and Install Dependencies:**

```bash
cd $HOME && sudo apt update && sudo apt upgrade && sudo apt install default-jdk git python3 python3-pip -y
```

This command updates your system, installs the necessary JDK, Git, and Python 3 with Pip.

**2. Clone the Repository:**

```bash
git clone https://github.com/nemesis-guy/LurkerX.git && cd LurkerX
```

This command clones the LurkerX repository from GitHub into your home directory and navigates to the newly created `LurkerX` directory.

**3. Install LurkerX:**

```bash
ls && ./install.sh
```

This command lists the contents of the `LurkerX` directory and executes the `install.sh` script, which installs the required Python dependencies and configures the application.

**4. Refresh or restart Terminal**
```bash
source ~/.zshrc || source ~/.bashrc 
```

This command will refresh the command list in the terminalto ensure that LurkerX is functioning. If there is failure, retart your terminal.

**5. Run LurkerX:**

```bash
lurkerx
```

This command starts the LurkerX application.

## Additional Notes

- Ensure you have a stable internet connection during the installation process.
- If you encounter any errors, please refer to the LurkerX documentation or seek assistance from the community.
- This guide assumes you have basic knowledge of using the command line.
