#!/bin/bash
# LurkerX auto-setup script or installtion file
clear
echo "Installation of LurkerX has started..."
echo .............................
echo 
# Create $HOME/bin directory if it doesn't exist
mkdir -p $HOME/bin

echo "Extracting files into $HOME/bin/LurkerX..."
echo .............................
echo

rm -rf $HOME/bin/LurkerX
sudo cp bin/workdir/android/apktool_2.9.3 /usr/local/bin/apktool
sudo cp bin/workdir/android/apktool_2.9.3.jar /usr/local/bin/apktool.jar
cp -r bin $HOME/bin/LurkerX

# Make the lurkerx binary executable
echo "Making LurkerX executable..."
echo .............................
echo
chmod +x $HOME/bin/LurkerX/*
echo "Finishing installation..."

sed -i '/export PATH="$HOME\/bin\/LurkerX:\$PATH"/d' ~/.bashrc
sed -i '/export PATH="$HOME\/bin\/LurkerX:\$PATH"/d' ~/.zshrc

# Check for .zshrc file and update PATH if present
if [ -f ~/.zshrc ]; then
  echo 'export PATH="$HOME/bin/LurkerX:$PATH"' >> ~/.zshrc
fi

# Add $HOME/bin to the PATH environment variable in .bashrc
echo 'export PATH="$HOME/bin/LurkerX:$PATH"' >> ~/.bashrc

# Try to source bashrc, if it fails then try to source zshrc
source ~/.bashrc||source ~/.zshrc

# Inform the user about the successful installation
echo "LurkerX has been installed successfully."
echo "You can now run LurkerX by typing 'lurkerx' in the terminal."
echo "To update LurkerX, download the latest archive from GitHub and extract it into the $HOME/bin directory."