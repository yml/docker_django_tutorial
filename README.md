# Docker Django Tutorial

This is a step by step tutorial on how to setup docker based local environment that is well suited for day to day development.
Most of the time a local environment setup requires to work with multiple docker containers. Each of these container needs to share some information and start in a well-defined order and predictable order. In order to do this, I like to rely on [docker-compose](https://docs.docker.com/compose/) and a common `dotenv` file.


## docker-compose.yml

For this tutorial we are going to only work with 2 containers:
* one for the python code
* one for Postgres

The database config is passed to the Django application via environment variable.

## Performance optimization

This is an extremely vast area and it is important to understand that you can improve performances on multiple angles.

### Build time 

You can have an impact on this factor by reducing the size of your images and being more efficient in the construction of your Dockerfile. An effective use of docker caching layer will make a huge difference.

### Mounted volume

At Lincoln Loop, as we started to use docker more and more we realized that not all operating systems are equals with regards to performances. 

On Linux systems, Docker directly leverages the kernel of the host system, and file system mounts are native. On Windows and Mac, it’s slightly different. These operating systems do not provide a Linux Kernel, so Docker starts a virtual machine with a small Linux installed and runs Docker containers in there.  File system mounts are also not possible natively and need a “helper-system” in between. This “helper-system” has a significant measurable overhead.

In the recent version, starting with Docker 17.06 CE Stable, you can configure container-and-host consistency requirements for bind-mounted directories in Compose files to allow for better performance on read/write of volume mounts. These options address issues specific to OSXFS file sharing, and therefore are only applicable on Docker Desktop for Mac.
You can still use the same docker-compose.yml file on Linux but they do not affect. 

The flags are:

* **consistent:** Full consistency. The container runtime and the host maintain an identical view of the mount at all times. This is the default.
* **cached:** The host’s view of the mount is authoritative. There may be delays before updates made on the host are visible within a container.
* **delegated:** The container runtime’s view of the mount is authoritative. There may be delays before updates made in a container are visible on the host.

Slow “hot reloading” after a code change and database performance have been tasks that have significantly been improved by tunning the parameter above. 

Here it is an example of how you would apply it in your docker-compose.yml

```

version: "3"
services:
  db:
    image: postgres:11.5-alpine
    volumes:
      - db:/var/lib/postgresql/data**:cached**
      - $PWD/data/db_dumps:/db_dumps
[...]
  app:
   [...]
    volumes:
      - ./python-django-tutorial:/app**:delegated**
      - /app/python_django_tutorial/python_django_tutorial.egg-info
      - $PWD/data/web_project_media:/venv/var/web_project/media:cached
      - $PWD/data/bash_history:/root/.bash_history**:cached**
```

## Building the images

Pulling and building the images is as simple as running:

`docker-compose build`

## Starting the django app

Bootstrapping the environment is down with the following command:

`docker-compose up`


## Running a Django management command

You can easily get access to a shell inside you docker container via the following command:

`docker-compose run app bash`

From there you can for example run the migrations:

```
yml@kodi-T470s$ docker-compose run app bash
Starting dockerdjangotutorial_db_1 ... done
root@8666df39586d:/app# django-admin migrate
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, hello, sessions
Running migrations:
  No migrations to apply.
```

You can also directly access your Postgres database :

```
yml@kodi-T470s$ docker-compose run app bash
Starting dockerdjangotutorial_db_1 ... done
root@8666df39586d:/app# django-admin migrate
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, hello, sessions
Running migrations:
  No migrations to apply.
```

## Vscode integration

All the above is probably enough if you like to develop with a lightweight editor but in the following section, I would like to showcase how you could work with the setup above from within vscode.


As you would have guessed in vscode you enable support for docker and docker-compose by installing 2 extensions:

* [docker](https://code.visualstudio.com/docs/azure/docker]
* [remote containers](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers]

With this setup in place the code provided in this repo you should be able to “Reopen folder in container”.

 


This will automatically do the following steps for you :

* docker-compose build
* docker-compose up
* install vscode remote package to run in the container
* install vscode extension: python

All the magic above is defined in the .devcontainer.json

```
{
    "dockerComposeFile": "docker-compose.yml",
    "service": "app",
    "workspaceFolder": "/app/",
    "extensions": ["ms-python.python"],
    "settings": {
        "python.pythonPath": "/venv/bin/python"
    }
}
```

Unlike the experience you would get when you develop remotely in a lightweight editor from now on you will be able to take advantage of the following features: IntelliSense support, go to definition and much more.

### Tips and tricks

From now on there is an infinity of things that you can customize to increase your productivity. I am going to share with you 3 tips.

#### Test suite

In vscode you can define custom tasks, I like to override the default build task to run the Django test suite. You can do this by adding the following snippet to your `tasks.json`



```

       {
           "label": "django test",
           "type": "shell",
           "command": "django-admin test",
           "group": {
               "kind": "build",
               "isDefault": true
           },
           "presentation": {
               "echo": true,
               "reveal": "always",
               "focus": false,
               "panel": "shared",
               "showReuseMessage": true,
               "clear": false
           }
       }

```

Ctrl+shif +b will run your test suite.



#### Debugger

There are 2 activity where it is really handy to observe the code behavior under a debugger. Obviously, you can still use `import pdb; pdb.set_trace()` but if you are more a GUI person you might be interested in the following customization that will let you take advantage of the vscode built in debugger UI. This time you will need to modify the `launch.json`


```
        {
            "name": "Django runserver",
            "type": "python",
            "request": "launch",
            "program": "/venv/bin/django-admin",
            "console": "integratedTerminal",
            "args": [
                "runserver",
                "--noreload",
                "--nothreading",
                "0.0.0.0:8001"
            ],
            "django": true
        },
        {
            "name": "Django test",
            "type": "python",
            "request": "launch",
            "program": "/venv/bin/django-admin",
            "console": "integratedTerminal",
            "args": [
                "test"
            ],
            "django": true
        }
```

ctrl+shift+D and then selecting `Django test` will start the test suite under the control of the debugger. 


In a similar way ctrl+shit+D and then selecting Django runserver will start your application on the port 8001. You can access it via your browser http://localhost:8001 and while you navigate your code will run under the control of the debugger.

Obviously in the setup above I have committed few files that are in the `.gitignore` list on my usual project:

* bash_history
* the files in the `.vscode` and the `.devcontainer.json`. If most of your team use vscode it might be useful to share them between the team members.

Please do not hesitate to let me know what your preferred trick is.
